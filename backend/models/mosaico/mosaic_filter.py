import os
import cv2  
import numpy as np
from PIL import Image, UnidentifiedImageError
from models.base_filter import BaseFilter
import time
import pandas as pd
from multiprocessing import Pool, cpu_count
import contextlib
import sys
from scipy.spatial import cKDTree  # Importar cKDTree para KD-Tree eficiente
from typing import Optional, Dict, Tuple, List
from functools import lru_cache
import gc

from status import preprocessing_status


# Variables globales para el KD-Tree y las rutas de imágenes
global_kdtree: Optional[cKDTree] = None
global_image_paths: List[str] = []


def init_worker(kdtree: cKDTree, image_paths: List[str]) -> None:
    """
    Inicializador para cada proceso del Pool de multiprocessing.
    Establece el KD-Tree y las rutas de imágenes como variables globales en cada proceso.
    
    :param kdtree: Objeto cKDTree construido a partir de library_colors.
    :param image_paths: Lista de rutas de imágenes de la biblioteca.
    """
    global global_kdtree
    global global_image_paths
    global_kdtree = kdtree
    global_image_paths = image_paths


def calculate_average_color(image_path: str) -> Optional[Dict[str, int]]:
    """
    Calcula el color promedio de una imagen después de verificar su integridad con PIL.
    
    :param image_path: Ruta completa a la imagen.
    :return: Diccionario con la ruta de la imagen y sus valores promedio de B, G, R.
             Retorna None si hay un error al procesar la imagen.
    """
    try:
        # Verificar la integridad de la imagen con PIL
        with Image.open(image_path) as img_pil:
            img_pil.verify()  # Esto no carga la imagen pero verifica su integridad
        
        # Si la verificación pasó, cargar la imagen con OpenCV
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stderr(devnull):
                img = cv2.imread(image_path)

        if img is None:
            print(f"Error al cargar la imagen {image_path} con OpenCV.")
            return None

        # Calcular el color promedio en BGR
        avg_color = np.mean(img, axis=(0, 1)).astype(int)  # Promedio en 3 canales (B, G, R)

        return {
            'image_path': image_path,
            'B': int(avg_color[0]),  # OpenCV usa BGR
            'G': int(avg_color[1]),
            'R': int(avg_color[2])
        }
    except (UnidentifiedImageError, IOError) as e:
        return None
    except Exception as e:
        print(f"Error al procesar {image_path}: {e}")
        return None


@lru_cache(maxsize=10000)
def get_resized_tile(closest_image_path: str, expected_size: Tuple[int, int]) -> Optional[np.ndarray]:
    """
    Obtiene y redimensiona la imagen de la biblioteca al tamaño esperado.
    Utiliza caché para evitar redimensionamientos repetidos.
    
    :param closest_image_path: Ruta a la imagen más cercana.
    :param expected_size: Tupla (width, height) del tamaño esperado.
    :return: Imagen redimensionada o None si falla.
    """
    try:
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stderr(devnull):
                tile_img = cv2.imread(closest_image_path)
        if tile_img is None:
            print(f"Error al cargar la imagen de la biblioteca: {closest_image_path}")
            return None
        resized_tile = cv2.resize(tile_img, expected_size, interpolation=cv2.INTER_AREA)
        return resized_tile
    except Exception as e:
        print(f"Error al redimensionar la imagen {closest_image_path}: {e}")
        return None


def process_block(args: Tuple[Tuple[int, int, int, int], np.ndarray]) -> Tuple[int, int, Optional[np.ndarray]]:
    """
    Procesa un bloque de la imagen para aplicar el filtro mosaico.
    
    :param args: Tuple que contiene:
                 - block_coords: (x, y, block_width, block_height)
                 - resized_image: Arreglo NumPy de la imagen redimensionada.
    :return: Tuple que contiene:
             - x: Coordenada x del bloque.
             - y: Coordenada y del bloque.
             - resized_tile: Arreglo NumPy de la imagen de la biblioteca redimensionada.
    """
    block_coords, resized_image = args
    x, y, block_width, block_height = block_coords

    # Extraer el bloque de la imagen
    block = resized_image[y:y+block_height, x:x+block_width]
    if block.size == 0:
        return (x, y, None)  # Bloque vacío

    # Calcular el color promedio del bloque en BGR
    avg_color = tuple(block.mean(axis=(0, 1)).astype(int))  # Convertir a tupla para caché

    # Usar el KD-Tree global para encontrar la imagen más cercana
    if global_kdtree is not None:
        distance, min_index = global_kdtree.query(avg_color)
        closest_image_path = global_image_paths[min_index]
    else:
        # Si el KD-Tree no está disponible, retornar None
        print("KD-Tree no está disponible.")
        return (x, y, None)

    # Obtener el tile redimensionado desde el caché
    resized_tile = get_resized_tile(closest_image_path, (block_width, block_height))

    return (x, y, resized_tile)


class MosaicFilter(BaseFilter):
    def __init__(self, image: Image.Image, library_dir: str = 'data/image_library/', csv_file: str = 'data/average_colors.csv') -> None:
        """
        Inicializa el filtro mosaico con la imagen objetivo, la ruta de la biblioteca de imágenes
        y el archivo CSV donde se almacenarán los colores promedio.

        :param image: Imagen objetivo (PIL Image).
        :param library_dir: Ruta a la carpeta que contiene las imágenes de la biblioteca.
        :param csv_file: Nombre del archivo CSV para almacenar los colores promedio.
        """
        start_time = time.perf_counter()  # Inicio del tiempo total del método

        super().__init__(image)

        # Obtener la ruta absoluta al directorio base (backend/)
        # __file__ está en /backend/models/mosaico/mosaic_filter.py
        # Necesitamos subir tres niveles para llegar a /backend/
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Construir rutas absolutas para la biblioteca de imágenes y el CSV
        self.library_dir: str = os.path.join(base_dir, library_dir)
        self.csv_file: str = os.path.join(base_dir, csv_file)

        # Imprimir las rutas para verificar
        print(f"Library Directory: {self.library_dir}")
        print(f"CSV File Path: {self.csv_file}")

        self.image_paths: List[str] = []
        self.library_colors: np.ndarray = np.array([])
        self.corrupted_images: List[str] = []  # Lista para almacenar imágenes corruptas

        # Asegurar que el directorio para el CSV existe
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)

        # Verificar si el archivo CSV ya existe para evitar recalcular
        if not os.path.exists(self.csv_file):
            preprocessing_status.set_preprocessing(True)  # Indicar que comienza el preprocesamiento
            try:
                self.preprocess_image_library()
            finally:
                preprocessing_status.set_preprocessing(False)  # Indicar que finaliza el preprocesamiento


        self.load_library_data()

        end_time = time.perf_counter()  # Fin del tiempo
        elapsed_time: float = end_time - start_time
        print(f"Inicialización de MosaicFilter completada en {elapsed_time:.4f} segundos.")

    def preprocess_image_library(self) -> None:
        """
        Preprocesa las imágenes en la carpeta especificada, calcula el color promedio de cada imagen
        y guarda los resultados en un archivo CSV utilizando OpenCV y pandas de manera más eficiente.
        Esta versión utiliza multiprocessing para procesar imágenes en paralelo.
        También registra imágenes corruptas que no pudieron ser procesadas.
        """
        start_time = time.perf_counter()  # Inicio del tiempo

        # Extensiones de archivos de imagen soportadas
        valid_extensions: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')

        # Lista para almacenar las rutas de imágenes válidas
        image_paths: List[str] = []

        # Recorrer todos los archivos en la carpeta y subcarpetas
        for root, dirs, files in os.walk(self.library_dir):
            for file in files:
                if file.lower().endswith(valid_extensions):
                    image_path = os.path.join(root, file)
                    image_paths.append(image_path)

        print(f"Total de imágenes a procesar: {len(image_paths)}")

        # Utilizar Pool de multiprocessing para procesar imágenes en paralelo
        num_processes: int = cpu_count()
        print(f"Usando {num_processes} procesos para el preprocesamiento.")

        with Pool(processes=num_processes) as pool:
            # Mapear la función calculate_average_color a todas las rutas de imágenes
            results: List[Optional[Dict[str, int]]] = pool.map(calculate_average_color, image_paths)

        # Filtrar resultados exitosos (no None) y recopilar imágenes corruptas
        image_data: List[Dict[str, int]] = []
        corrupted_images: List[str] = []
        for img_path, res in zip(image_paths, results):
            if res is not None:
                image_data.append(res)
            else:
                corrupted_images.append(img_path)

        # Registrar imágenes corruptas
        if corrupted_images:
            print(f"Se encontraron {len(corrupted_images)} imágenes corruptas:")
            for img in corrupted_images:
                print(f" - {img}")

            # Guardar las imágenes corruptas en un archivo log (opcional)
            log_path: str = os.path.join(os.path.dirname(self.csv_file), 'corrupted_images.log')
            with open(log_path, 'w') as log_file:
                for img in corrupted_images:
                    log_file.write(f"{img}\n")
            print(f"Lista de imágenes corruptas guardadas en {log_path}")
        else:
            print("No se encontraron imágenes corruptas.")

        # Crear un DataFrame y guardar en CSV usando pandas
        df: pd.DataFrame = pd.DataFrame(image_data)
        df.to_csv(self.csv_file, index=False, columns=['image_path', 'B', 'G', 'R'])  # Asegurar orden y nombres de columnas

        end_time_data: float = time.perf_counter()  # Fin del tiempo de escritura
        elapsed_time_data: float = end_time_data - start_time
        print(f"Guardado en DataFrame y escritura en CSV completados en {elapsed_time_data:.4f} segundos.")

        print(f"Preprocesamiento completado. Datos guardados en {self.csv_file}")
        print(f"Tiempo total de preprocesamiento: {elapsed_time_data:.4f} segundos.")

        # Guardar las imágenes corruptas en una carpeta específica (opcional)
        if corrupted_images:
            corrupted_dir: str = os.path.join(os.path.dirname(self.csv_file), 'corrupted_images')
            os.makedirs(corrupted_dir, exist_ok=True)
            for img in corrupted_images:
                try:
                    basename: str = os.path.basename(img)
                    destination: str = os.path.join(corrupted_dir, basename)
                    os.rename(img, destination)
                    print(f"Moviendo {img} a {destination}")
                except Exception as e:
                    print(f"Error al mover {img} a {corrupted_dir}: {e}")

    def load_library_data(self) -> None:
        """
        Carga los datos de colores promedio y rutas de imágenes desde el archivo CSV utilizando pandas.
        Además, construye un KD-Tree para búsquedas rápidas.
        """
        start_time = time.perf_counter()  # Inicio del tiempo

        try:
            # Leer el CSV con pandas, especificando los tipos de datos para optimizar la lectura
            df: pd.DataFrame = pd.read_csv(
                self.csv_file,
                dtype={'image_path': str, 'B': np.float32, 'G': np.float32, 'R': np.float32}
            )

            # Verificar que las columnas necesarias existen
            required_columns = {'image_path', 'B', 'G', 'R'}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"El CSV debe contener las columnas: {required_columns}")

            # Asignar los datos a los atributos de la clase
            self.library_colors: np.ndarray = df[['B', 'G', 'R']].to_numpy(dtype=np.float32)
            self.image_paths: List[str] = df['image_path'].tolist()

            # Construir el KD-Tree usando cKDTree para mayor eficiencia
            self.kdtree: Optional[cKDTree] = cKDTree(self.library_colors)

            print("Datos de la biblioteca cargados exitosamente y KD-Tree construido.")
        except Exception as e:
            print(f"Error al cargar los datos de la biblioteca: {e}")
            self.library_colors = np.array([])
            self.image_paths = []
            self.kdtree = None

        end_time = time.perf_counter()  # Fin del tiempo
        elapsed_time: float = end_time - start_time
        print(f"Carga de datos de la biblioteca completada en {elapsed_time:.4f} segundos.")

    def find_closest_image(self, avg_color: np.ndarray) -> str:
        """
        Encuentra la imagen en la biblioteca cuyo color promedio es el más cercano al color dado,
        utilizando un KD-Tree para mejorar la eficiencia.

        :param avg_color: Color promedio del bloque (arreglo de tres enteros B, G, R).
        :return: Ruta a la imagen más cercana.
        """
        if self.kdtree is not None:
            distance, index = self.kdtree.query(avg_color)
            return self.image_paths[index]
        else:
            # Fallback a la implementación original si el KD-Tree no está disponible
            min_distance: float = float('inf')
            closest_image_path: Optional[str] = None

            # Convertir avg_color a un arreglo NumPy
            avg_color_np: np.ndarray = np.array(avg_color)

            # Iterar sobre todos los colores en la biblioteca
            for idx, lib_color in enumerate(self.library_colors):
                # Calcular la distancia euclidiana
                distance = np.linalg.norm(avg_color_np - lib_color)
                if distance < min_distance:
                    min_distance = distance
                    closest_image_path = self.image_paths[idx]

            return closest_image_path  # type: ignore

    def apply_filter(self, block_width: int, block_height: int, upscale_factor: int) -> Image.Image:
        """
        Aplica el filtro mosaico a la imagen objetivo utilizando OpenCV y multiprocessing.

        :param block_width: Ancho de cada bloque en píxeles.
        :param block_height: Alto de cada bloque en píxeles.
        :param upscale_factor: Factor de ampliación de la imagen final.
        :return: Imagen procesada (PIL Image).
        """
        start_time = time.perf_counter()  # Inicio del tiempo total del método

        # Validación de entradas
        if block_width <= 0 or block_height <= 0:
            raise ValueError("Las dimensiones del bloque deben ser enteros positivos.")
        if upscale_factor <= 0:
            raise ValueError("El factor de ampliación debe ser un entero positivo.")

        # Convertir la imagen a un arreglo NumPy utilizando OpenCV (BGR)
        img: Image.Image = self.image.convert('RGB')
        image_array: np.ndarray = np.array(img)
        image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)  # Convertir a BGR

        # Ampliar la imagen según el upscale_factor utilizando OpenCV
        new_width: int = image_array.shape[1] * upscale_factor
        new_height: int = image_array.shape[0] * upscale_factor
        resized_image: np.ndarray = cv2.resize(
            image_array,
            (new_width, new_height),
            interpolation=cv2.INTER_NEAREST
        )

        height, width, _ = resized_image.shape

        # Crear una lista de todas las coordenadas de los bloques
        blocks: List[Tuple[Tuple[int, int, int, int], np.ndarray]] = []
        for y in range(0, height, block_height):
            for x in range(0, width, block_width):
                current_block_width: int = min(block_width, width - x)
                current_block_height: int = min(block_height, height - y)
                blocks.append(((x, y, current_block_width, current_block_height), resized_image))

        print(f"Total de bloques a procesar: {len(blocks)}")

        # Crear el KD-Tree y las rutas de imágenes para los procesos
        kdtree = self.kdtree
        image_paths = self.image_paths

        if kdtree is None:
            print("KD-Tree no está disponible. No se puede aplicar el filtro.")
            return self.image

        # Inicializar el Pool de multiprocessing con el KD-Tree
        num_processes: int = cpu_count()
        print(f"Usando {num_processes} procesos para el procesamiento de bloques.")

        with Pool(processes=num_processes, initializer=init_worker, initargs=(kdtree, image_paths)) as pool:
            # Mapear la función process_block a todas las coordenadas de bloques
            results: List[Tuple[int, int, Optional[np.ndarray]]] = pool.map(process_block, blocks)

        # Crear una copia de la imagen redimensionada para colocar los tiles
        final_image: np.ndarray = resized_image.copy()

        # Iterar sobre los resultados y pegar los tiles en la posición correspondiente
        for result in results:
            x, y, resized_tile = result
            if resized_tile is not None:
                # Verificar que el tile tiene el tamaño correcto
                tile_height_resized, tile_width_resized = resized_tile.shape[:2]
                expected_height: int = min(block_height, height - y)
                expected_width: int = min(block_width, width - x)

                if tile_height_resized != expected_height or tile_width_resized != expected_width:
                    resized_tile = cv2.resize(
                        resized_tile,
                        (expected_width, expected_height),
                        interpolation=cv2.INTER_AREA
                    )

                # Pegar el tile en la imagen final
                final_image[y:y+expected_height, x:x+expected_width] = resized_tile

        # Liberar memoria innecesaria
        del resized_image
        gc.collect()

        # Convertir la imagen final de BGR a RGB para PIL
        final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
        processed_image: Image.Image = Image.fromarray(final_image)

        end_time = time.perf_counter()  # Fin del tiempo total del método
        elapsed_time: float = end_time - start_time
        print(f"apply_filter completado en {elapsed_time:.4f} segundos.")

        return processed_image
