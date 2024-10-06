from PIL import Image, ImageDraw
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter
import math

class HalftonesFilter(BaseFilter):

    def __init__(self, image, num_variations, grid_factor):
        """
        Inicializa el filtro de imágenes recursivas con una imagen,
        calcula el tamaño de la cuadrícula en función del tamaño de la imagen y un factor de escala,
        y establece el número de variaciones en escala de grises.

        :param image: Objeto de imagen (PIL Image).
        :param grid_factor: Factor por el cual se dividirá el ancho y altura de la imagen.
        :param num_variations: Número de versiones en escala de grises.
        """
        super().__init__(image)
        
        # Obtener dimensiones originales de la imagen
        width, height = self.image.size
        ## Calcular el upscale factor
        upscale_factor = int(math.sqrt(grid_factor))

        self.width = upscale_factor * width
        self.height = upscale_factor * height
        self.grid_width = self.width // grid_factor
        self.grid_height = self.height // grid_factor
        self.grid_factor = grid_factor

        # Validar el factor de cuadrícula esté en el rango correcto
        if not (1 <= grid_factor <= min(width, height)):
            raise ValueError("El factor de cuadrícula debe estar entre 1 y el alto o ancho de la imagen en píxeles") 

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
        max_radius = self.grid_factor // 2
        
        # Calcular el salto en el tamaño del radio según el número de variaciones
        for i in range(self.num_variations):
            # Crear una imagen en blanco
            circle_image = Image.new("RGB", (self.grid_width, self.grid_height), (255, 255, 255))
            draw = ImageDraw.Draw(circle_image)
            
            # Calcular el radio del círculo
            radius = max_radius * ((i + 1) / self.num_variations)
            
            # Dibujar un círculo negro en el centro de la imagen
            center_x, center_y = self.grid_width // 2, self.grid_height // 2
            draw.ellipse(
                (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
                fill=(0, 0, 0)
            )
            
            # Asignar la imagen generada a su valor de brillo correspondiente (representativo)
            versiones[i * (255 // self.num_variations)] = circle_image

        return versiones

    def apply_filter(self):
        """
        Método que aplica el filtro de imágenes recursivas utilizando los círculos generados en `get_palette`.
        :return: Imagen procesada.
        """
        # Obtener las versiones de la imagen con círculos de diferentes tamaños
        gray_variations = self.get_palette()

        # Crear una imagen en blanco para la cuadrícula
        recursive_image = Image.new("RGB", (self.grid_width*self.grid_factor, self.grid_height*self.grid_factor))

        # Imagen escalada al tamaño de la cuadrícula
        image_upscaled = self.image.resize((self.width, self.height))

        # Iterar sobre cada cuadrícula
        for i in range(0, self.grid_width*self.grid_factor, self.grid_width):
            for j in range(0, self.grid_height*self.grid_factor, self.grid_height):
                # Obtener el promedio del valor de brillo de la cuadrícula
                avg_brightness = self.calculate_average_brightness(image_upscaled, i, j)
                # Calcular el valor de escala de grises más cercano
                grayscale_value = min(gray_variations, key=lambda x: abs(x - avg_brightness))
                # Pegar la imagen correspondiente del diccionario de nuestra variaciones en la imagen recursiva
                recursive_image.paste(gray_variations[grayscale_value], (i, j))

        return recursive_image

    def calculate_average_brightness(self, image, x, y):
        """
        Método que calcula el brillo promedio de una cuadrícula en la imagen en escala de grises.
        :param image: Imagen original.
        :param x: Coordenada x de la cuadrícula.
        :param y: Coordenada y de la cuadrícula.
        :return: Valor promedio del brillo de la cuadrícula.
        """
        # Inicializar la variable para el brillo promedio
        total_brightness = 0

        # Iterar sobre la cuadrícula
        for i in range(x, x + self.grid_width):
            for j in range(y, y + self.grid_height):
                # Obtener el valor de brillo (en escala de grises, r = g = b)
                pixel = image.getpixel((i, j))
                total_brightness += pixel[0]  # Solo necesitamos un canal, ya que es escala de grises

        # Calcular el promedio de los valores de brillo
        total_pixels = self.grid_width * self.grid_height
        return total_brightness // total_pixels
