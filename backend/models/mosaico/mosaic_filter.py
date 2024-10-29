import os
import cv2  # Importar OpenCV
import numpy as np
from PIL import Image
from models.base_filter import BaseFilter
import time
import pandas as pd
from multiprocessing import Pool, cpu_count


def calculate_average_color(image_path):
    """
    Calcula el color promedio de una imagen.

    :param image_path: Ruta completa a la imagen.
    :return: Diccionario con la ruta de la imagen y sus valores promedio de B, G, R.
             Retorna None si hay un error al procesar la imagen.
    """
    try:
        # Cargar la imagen usando OpenCV
        img = cv2.imread(image_path)

        if img is None:
            print(f"Error al cargar la imagen {image_path}. Posiblemente está corrupta o el formato no es soportado.")
            return None

        # Calcular el color promedio en BGR
        avg_color_per_row = np.average(img, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0).astype(int)  # Promedio en 3 canales (B, G, R)

        return {
            'image_path': image_path,
            'B': int(avg_color[0]),  # OpenCV usa BGR
            'G': int(avg_color[1]),
            'R': int(avg_color[2])
        }
    except Exception as e:
        print(f"Error al procesar {image_path}: {e}")
        return None


def process_block(args):
    """
    Procesa un bloque de la imagen para aplicar el filtro mosaico.

    :param args: Tuple que contiene:
                 - block_coords: (x, y, block_width, block_height)
                 - resized_image: Arreglo NumPy de la imagen redimensionada.
                 - library_colors: Arreglo NumPy de colores promedio de la biblioteca.
                 - image_paths: Lista de rutas de imágenes de la biblioteca.
    :return: Tuple que contiene:
             - x: Coordenada x del bloque.
             - y: Coordenada y del bloque.
             - resized_tile: Arreglo NumPy de la imagen de la biblioteca redimensionada.
    """
    block_coords, resized_image, library_colors, image_paths = args
    x, y, block_width, block_height = block_coords

    # Extraer el bloque de la imagen
    block = resized_image[y:y+block_height, x:x+block_width]
    if block.size == 0:
        return (x, y, None)  # Bloque vacío

    # Calcular el color promedio del bloque en BGR
    avg_color = block.mean(axis=(0, 1)).astype(int)  # BGR

    # Encontrar la imagen más cercana en la biblioteca
    distances = np.linalg.norm(library_colors - avg_color, axis=1)
    min_index = np.argmin(distances)
    closest_image_path = image_paths[min_index]

    # Cargar la imagen de la biblioteca usando OpenCV
    tile_img = cv2.imread(closest_image_path)
    if tile_img is None:
        print(f"Error al cargar la imagen de la biblioteca: {closest_image_path}")
        return (x, y, None)

    # Redimensionar la imagen al tamaño del bloque
    resized_tile = cv2.resize(tile_img, (block.shape[1], block.shape[0]), interpolation=cv2.INTER_AREA)

    return (x, y, resized_tile)


class MosaicFilter(BaseFilter):
    def __init__(self, image, library_dir='data/image_library/', csv_file='data/average_colors.csv'):
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
        self.library_dir = os.path.join(base_dir, library_dir)
        self.csv_file = os.path.join(base_dir, csv_file)

        # Debugging: Imprimir las rutas para verificar
        print(f"Library Directory: {self.library_dir}")
        print(f"CSV File Path: {self.csv_file}")

        self.image_paths = []
        self.library_colors = []

        # Asegurar que el directorio para el CSV existe
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)

        # Verificar si el archivo CSV ya existe para evitar recalcular
        if not os.path.exists(self.csv_file):
            self.preprocess_image_library()

        self.load_library_data()

        end_time = time.perf_counter()  # Fin del tiempo
        elapsed_time = end_time - start_time
        print(f"Inicialización de MosaicFilter completada en {elapsed_time:.4f} segundos.")

    def preprocess_image_library(self):
        """
        Preprocesa las imágenes en la carpeta especificada, calcula el color promedio de cada imagen
        y guarda los resultados en un archivo CSV utilizando OpenCV y pandas de manera más eficiente.
        Esta versión utiliza multiprocessing para procesar imágenes en paralelo.
        """
        start_time = time.perf_counter()  # Inicio del tiempo

        # Extensiones de archivos de imagen soportadas
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')

        # Lista para almacenar las rutas de imágenes válidas
        image_paths = []

        # Recorrer todos los archivos en la carpeta y subcarpetas
        for root, dirs, files in os.walk(self.library_dir):
            for file in files:
                if file.lower().endswith(valid_extensions):
                    image_path = os.path.join(root, file)
                    image_paths.append(image_path)

        print(f"Total de imágenes a procesar: {len(image_paths)}")

        # Utilizar Pool de multiprocessing para procesar imágenes en paralelo
        num_processes = cpu_count()
        print(f"Usando {num_processes} procesos para el preprocesamiento.")

        with Pool(processes=num_processes) as pool:
            # Mapear la función calculate_average_color a todas las rutas de imágenes
            results = pool.map(calculate_average_color, image_paths)

        # Filtrar resultados exitosos (no None)
        image_data = [res for res in results if res is not None]

        # Crear un DataFrame y guardar en CSV usando pandas
        df = pd.DataFrame(image_data)
        df.to_csv(self.csv_file, index=False, columns=['image_path', 'B', 'G', 'R'])  # Asegurar orden y nombres de columnas

        end_timeData = time.perf_counter()  # Fin del tiempo de escritura
        elapsed_timeD = end_timeData - start_time
        print(f"Guardado en DataFrame y escritura en CSV completados en {elapsed_timeD:.4f} segundos.")

        print(f"Preprocesamiento completado. Datos guardados en {self.csv_file}")

        end_time = time.perf_counter()  # Fin del tiempo total
        elapsed_time = end_time - start_time
        print(f"Preprocesamiento de la biblioteca completado en {elapsed_time:.4f} segundos.")

    def load_library_data(self):
        """
        Carga los datos de colores promedio y rutas de imágenes desde el archivo CSV utilizando pandas.
        """
        start_time = time.perf_counter()  # Inicio del tiempo

        try:
            # Leer el CSV con pandas, especificando los tipos de datos para optimizar la lectura
            df = pd.read_csv(self.csv_file, dtype={'image_path': str, 'B': np.int32, 'G': np.int32, 'R': np.int32})

            # Asignar los datos a los atributos de la clase
            self.library_colors = df[['B', 'G', 'R']].to_numpy()
            self.image_paths = df['image_path'].tolist()

            print("Datos de la biblioteca cargados exitosamente.")
        except Exception as e:
            print(f"Error al cargar los datos de la biblioteca: {e}")
            self.library_colors = np.array([])
            self.image_paths = []

        end_time = time.perf_counter()  # Fin del tiempo
        elapsed_time = end_time - start_time
        print(f"Carga de datos de la biblioteca completada en {elapsed_time:.4f} segundos.")

    def find_closest_image(self, avg_color):
        """
        Encuentra la imagen en la biblioteca cuyo color promedio es el más cercano al color dado,
        iterando sobre todas las opciones y calculando la distancia euclidiana.

        :param avg_color: Color promedio del bloque (arreglo de tres enteros B, G, R).
        :return: Ruta a la imagen más cercana.
        """
        min_distance = float('inf')
        closest_image_path = None

        # Convertir avg_color a un arreglo NumPy
        avg_color = np.array(avg_color)

        # Iterar sobre todos los colores en la biblioteca
        for idx, lib_color in enumerate(self.library_colors):
            # Calcular la distancia euclidiana
            distance = np.linalg.norm(avg_color - lib_color)
            if distance < min_distance:
                min_distance = distance
                closest_image_path = self.image_paths[idx]

        return closest_image_path

    def apply_filter(self, block_width, block_height, upscale_factor):
        """
        Aplica el filtro mosaico a la imagen objetivo utilizando OpenCV y multiprocessing.

        :param block_width: Ancho de cada bloque en píxeles.
        :param block_height: Alto de cada bloque en píxeles.
        :param upscale_factor: Factor de ampliación de la imagen final.
        :return: Imagen procesada (PIL Image).
        """
        start_time = time.perf_counter()  # Inicio del tiempo total del método

        if block_width <= 0 or block_height <= 0:
            raise ValueError("Las dimensiones del bloque deben ser enteros positivos.")

        if upscale_factor <= 0:
            raise ValueError("El factor de ampliación debe ser un entero positivo.")

        # Convertir la imagen a un arreglo NumPy utilizando OpenCV (BGR)
        img = self.image.convert('RGB')
        image_array = np.array(img)
        image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)  # Convertir a BGR

        # Ampliar la imagen según el upscale_factor utilizando OpenCV
        new_width = image_array.shape[1] * upscale_factor
        new_height = image_array.shape[0] * upscale_factor
        resized_image = cv2.resize(image_array, (new_width, new_height), interpolation=cv2.INTER_NEAREST)

        height, width, _ = resized_image.shape

        # Crear una lista de todas las coordenadas de los bloques
        blocks = []
        for y in range(0, height, block_height):
            for x in range(0, width, block_width):
                current_block_width = min(block_width, width - x)
                current_block_height = min(block_height, height - y)
                blocks.append(((x, y, current_block_width, current_block_height), resized_image, self.library_colors, self.image_paths))

        print(f"Total de bloques a procesar: {len(blocks)}")

        # Utilizar Pool de multiprocessing para procesar bloques en paralelo
        num_processes = cpu_count()
        print(f"Usando {num_processes} procesos para el procesamiento de bloques.")

        with Pool(processes=num_processes) as pool:
            # Mapear la función process_block a todas las coordenadas de bloques
            results = pool.map(process_block, blocks)

        # Crear una copia de la imagen redimensionada para colocar los tiles
        final_image = resized_image.copy()

        # Iterar sobre los resultados y pegar los tiles en la posición correspondiente
        for result in results:
            x, y, resized_tile = result
            if resized_tile is not None:
                # Verificar que el tile tiene el tamaño correcto
                tile_height_resized, tile_width_resized = resized_tile.shape[:2]
                expected_height = min(block_height, height - y)
                expected_width = min(block_width, width - x)

                if tile_height_resized != expected_height or tile_width_resized != expected_width:
                    resized_tile = cv2.resize(resized_tile, (expected_width, expected_height), interpolation=cv2.INTER_AREA)

                # Pegar el tile en la imagen final
                final_image[y:y+expected_height, x:x+expected_width] = resized_tile

        # Convertir la imagen final de BGR a RGB para PIL
        final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
        processed_image = Image.fromarray(final_image)

        end_time = time.perf_counter()  # Fin del tiempo total del método
        elapsed_time = end_time - start_time
        print(f"apply_filter completado en {elapsed_time:.4f} segundos.")

        return processed_image
