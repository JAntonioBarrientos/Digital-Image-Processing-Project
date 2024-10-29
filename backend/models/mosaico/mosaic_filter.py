import cv2  # Importar OpenCV
import os
import csv
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
    :return: Diccionario con la ruta de la imagen y sus valores promedio de R, G, B.
             Retorna None si hay un error al procesar la imagen.
    """
    try:
        # Cargar la imagen usando OpenCV
        img = cv2.imread(image_path)

        if img is None:
            print(f"Error al cargar la imagen {image_path}. Posiblemente está corrupta o el formato no es soportado.")
            return None
            
        avg_color_per_row = np.average(img, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0).astype(int)  # Promedio en 3 canales

        return {
            'image_path': image_path,
            'R': int(avg_color[2]),  # OpenCV usa BGR, así que R es el índice 2
            'G': int(avg_color[1]),
            'B': int(avg_color[0])
        }
    except Exception as e:
        print(f"Error al procesar {image_path}: {e}")
        return None


class MosaicFilter(BaseFilter):
    def __init__(self, image, library_dir='data/image_library/', csv_file='data/average_colors.csv'):
        """
        Inicializa el filtro mosaico con la imagen objetivo, la ruta de la biblioteca de imágenes
        y el archivo CSV donde se almacenarán los colores promedio.

        :param image: Imagen objetivo (PIL Image).
        :param library_dir: Ruta a la carpeta que contiene las imágenes de la biblioteca.
        :param csv_file: Nombre del archivo CSV para almacenar los colores promedio.
        """
        start_time = time.perf_counter()  

        super().__init__(image)

        # Obtener la ruta absoluta al directorio base (backend/)
        # __file__ está en /backend/models/mosaico/mosaic_filter.py
        # Necesitamos subir tres niveles para llegar a /backend/
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Construir rutas absolutas para la biblioteca de imágenes y el CSV
        self.library_dir = os.path.join(base_dir, library_dir)
        self.csv_file = os.path.join(base_dir, csv_file)


        self.image_paths = []
        self.library_colors = []
        
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
        df.to_csv(self.csv_file, index=False)

        end_timeData = time.perf_counter()  # Fin del tiempo de escritura
        elapsed_timeD = end_timeData - start_time
        print(f"Guardado en DataFrame y escritura en CSV completados en {elapsed_timeD:.4f} segundos.")

        print(f"Preprocesamiento completado. Datos guardados en {self.csv_file}")

        end_time = time.perf_counter()  # Fin del tiempo total
        elapsed_time = end_time - start_time
        print(f"Preprocesamiento de la biblioteca completado en {elapsed_time:.4f} segundos.")


    def load_library_data(self):
        """
        Carga los datos de colores promedio y rutas de imágenes desde el archivo CSV.
        """
        start_time = time.perf_counter()  # Inicio del tiempo

        colors = []
        image_paths = []
        with open(self.csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                colors.append([int(row['R']), int(row['G']), int(row['B'])])
                image_paths.append(row['image_path'])
        self.library_colors = np.array(colors)
        self.image_paths = image_paths
        print("Datos de la biblioteca cargados exitosamente.")

        end_time = time.perf_counter()  # Fin del tiempo
        elapsed_time = end_time - start_time
        print(f"Carga de datos de la biblioteca completada en {elapsed_time:.4f} segundos.")


    def find_closest_image(self, avg_color):
        """
        Encuentra la imagen en la biblioteca cuyo color promedio es el más cercano al color dado,
        iterando sobre todas las opciones y calculando la distancia euclidiana.

        :param avg_color: Color promedio del bloque (lista o arreglo de tres enteros).
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
        Aplica el filtro mosaico a la imagen objetivo.

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

        # Convertir la imagen a RGB si no lo está
        img = self.image.convert('RGB')

        # Ampliar la imagen según el upscale_factor
        original_width, original_height = img.size
        new_width = original_width * upscale_factor
        new_height = original_height * upscale_factor
        img = img.resize((new_width, new_height), Image.NEAREST)

        image_array = np.array(img)
        height, width, _ = image_array.shape

        # Crear una nueva imagen para el resultado
        processed_image = Image.new('RGB', (width, height))


        # Iniciar el tiempo de procesamiento de bloques
        blocks_start_time = time.perf_counter()


        # Iterar sobre los bloques
        for y in range(0, height, block_height):
            for x in range(0, width, block_width):
                # Definir el bloque
                block = image_array[y:y+block_height, x:x+block_width]
                if block.size == 0:
                    continue  # Si el bloque está vacío, continuar
                # Calcular el color promedio del bloque
                avg_color = block.mean(axis=(0, 1)).astype(int)
                # Encontrar la imagen más cercana en la biblioteca
                closest_image_path = self.find_closest_image(avg_color)
                if closest_image_path is None:
                    continue  # Si no se encuentra una imagen, omitir el bloque
                # Abrir la imagen seleccionada
                with Image.open(closest_image_path) as tile_img:
                    # Redimensionar la imagen al tamaño del bloque
                    tile_img = tile_img.resize((block.shape[1], block.shape[0]))
                    # Pegar la imagen en la posición correspondiente
                    processed_image.paste(tile_img, (x, y))
        
        # Fin del tiempo de procesamiento de bloques
        blocks_end_time = time.perf_counter()
        blocks_elapsed_time = blocks_end_time - blocks_start_time
        print(f"Procesamiento de bloques completado en {blocks_elapsed_time:.4f} segundos.")

        end_time = time.perf_counter()  # Fin del tiempo total del método
        elapsed_time = end_time - start_time
        print(f"apply_filter completado en {elapsed_time:.4f} segundos.")


        return processed_image