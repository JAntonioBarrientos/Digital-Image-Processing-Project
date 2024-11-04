from PIL import Image, ImageDraw
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter
import numpy as np
import math

class HalftoneFilter(BaseFilter):

    def __init__(self, image, num_variations):
        """
        Inicializa el filtro de imágenes recursivas con una imagen,
        calcula el tamaño de la cuadrícula en función del tamaño de la imagen y un factor de escala,
        y establece el número de variaciones en escala de grises.

        :param image: Objeto de imagen (PIL Image).
        :param num_variations: Número de versiones en escala de grises.
        """
        im_gray = GrayscaleFilter(image)
        super().__init__(im_gray.apply_filter())
        
        # Obtener dimensiones originales de la imagen
        width, height = self.image.size

        self.width = num_variations * width 
        self.height = num_variations * height

        self.grid_dim = num_variations

        # Validar el número de variantes esté en el rango correcto
        if not (2 <= num_variations <= 256):
            raise ValueError("El número de variaciones debe estar entre 2 y 256")

        # Definir el número de variaciones
        self.num_variations = num_variations

    def get_palette(self):
        """
        Genera n variantes de imágenes con círculos de diferentes tamaños.
        :return: Diccionario con las versiones de la imagen. 
                Las claves son los valores representativos de brillo y los valores son las imágenes con los círculos correspondientes.
        """
        # Diccionario para almacenar las versiones de la imagen con círculos
        versiones = {}
        
        # Calcular el radio máximo para los círculos (que depende del tamaño de la cuadrícula)
        max_radius = self.num_variations  # Dividido por 2 para ajustarse al tamaño de la cuadrícula

        # Invertir el índice para que un valor de gris más alto corresponda a un círculo más pequeño
        for i in range(self.num_variations):
            # Crear una imagen en blanco
            circle_image = Image.new("RGB", (self.grid_dim, self.grid_dim), (255, 255, 255))
            draw = ImageDraw.Draw(circle_image)
            
            # Calcular el radio del círculo
            # Invertimos i para que un valor de gris más alto tenga un radio más pequeño
            inverted_i = self.num_variations - 1 - i
            radius = max_radius * (inverted_i / (self.num_variations - 1))
            
            # Dibujar un círculo negro en el centro de la imagen
            center = self.grid_dim // 2
            draw.ellipse(
                (center - radius, center - radius, center + radius, center + radius),
                fill=(0, 0, 0)
            )
            
            # Asignar la imagen generada a su valor de brillo correspondiente (representativo)
            brightness_value = int((255 * i) / (self.num_variations - 1))
            versiones[brightness_value] = circle_image

        return versiones

    def apply_filter(self):
        """
        Método que aplica el filtro de imágenes recursivas utilizando los círculos generados en `get_palette`.
        :return: Imagen procesada.
        """
        # Obtener las versiones de la imagen con círculos de diferentes tamaños
        gray_variations = self.get_palette()
        
        # Crear una imagen en blanco para la cuadrícula
        result_image = Image.new("RGB", (self.width, self.height))
        
        # Imagen escalada al tamaño de la cuadrícula
        image_upscaled = self.image.resize((self.width, self.height))
        image_upscaled_data = np.array(image_upscaled)
        
        # Extraer el canal de escala de grises (suponiendo que R=G=B)
        gray_data = image_upscaled_data[:, :, 0]
        
        # Calcular las dimensiones de los bloques
        height_blocks = self.height // self.grid_dim
        width_blocks = self.width // self.grid_dim
        
        # Redimensionar los datos de la imagen para crear bloques
        gray_data_blocks = gray_data.reshape(height_blocks, self.grid_dim, width_blocks, self.grid_dim)
        
        # Calcular el brillo promedio para cada bloque
        avg_brightness_blocks = gray_data_blocks.mean(axis=(1, 3))
        
        # Aplanar el array de brillo promedio para facilitar el cálculo
        avg_brightness_flat = avg_brightness_blocks.flatten()
        
        # Obtener los valores de brillo disponibles
        grayscale_values = np.array(list(gray_variations.keys()))
        
        # Calcular las diferencias y encontrar el valor de brillo más cercano
        differences = np.abs(avg_brightness_flat[:, np.newaxis] - grayscale_values[np.newaxis, :])
        indices = np.argmin(differences, axis=1)
        
        # Reconvertir los índices a la forma de la cuadrícula
        indices_grid = indices.reshape(height_blocks, width_blocks)
        
        # Convertir grayscale_values y variation_images a listas para acceso rápido
        grayscale_values_list = grayscale_values.tolist()
        variation_images = [gray_variations[k] for k in grayscale_values_list]
        
        # Pegar las imágenes correspondientes en el resultado
        for i in range(height_blocks):
            for j in range(width_blocks):
                idx = indices_grid[i, j]
                variation_image = variation_images[idx]
                x = j * self.grid_dim
                y = i * self.grid_dim
                result_image.paste(variation_image, (x, y))
                
        return result_image
