from PIL import Image
from models.base_filter import BaseFilter
from models.filters.mica_filter import MicaFilter
import math

class RecursiveImagesColor(BaseFilter):

    def __init__(self, image, grid_factor):
        """
        Inicializa el filtro de imágenes recursivas con una imagen,
        calcula el tamaño de la cuadrícula en función del tamaño de la imagen y un factor de escala,
        y establece el número de variaciones en escala de grises.

        :param image: Objeto de imagen (PIL Image).
        :param grid_factor: Factor por el cual se dividirá el ancho y altura de la imagen.
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

        # Validar el factor de cuadrícula este en el rango correcto
        if not (1 <= grid_factor <= min(width, height)):
            raise ValueError("El factor de cuadrícula debe estar entre 1 y el alto o ancho de la imagen en píxeles") 

    def apply_filter(self):
        """
        Método que aplica el filtro de imágenes recursivas. Que consiste en hacer un promedio de los valores RGB por el tamaño de la imagen y seleccionar la imagen en escala de grises que más se asemeje a la original.
        :return: Imagen procesada.
        """

        # Crear una imagen en blanco para la cuadrícula
        recursive_image = Image.new("RGB", (self.grid_width*self.grid_factor, self.grid_height*self.grid_factor))

        # Cargar los píxeles de la imagen
        pixels = recursive_image.load()

        # Imagen escalada al tamaño de la cuadrícula
        image_upscaled = self.image.resize((self.width, self.height))

        img_resize = self.image.resize((self.grid_width, self.grid_height))
        

        # Iterar sobre cada cuadrícula
        for i in range(0, self.grid_width*self.grid_factor, self.grid_width):
            for j in range(0, self.grid_height*self.grid_factor, self.grid_height):
                # Obtener el promedio de los valores RGB de la cuadrícula
                r, g, b = self.calculate_average_color(image_upscaled, i, j)

                # Aplicar el filtro de mica a la imagen
                mica_filter = MicaFilter(img_resize, r, g, b)
                processed_image = mica_filter.apply_filter()

                # Pegar la imagen correspondiente del diccionario de nuestra variaciones en la imagen recursiva
                recursive_image.paste(processed_image, (i, j))

        return recursive_image

    def calculate_average_color(self, image, x, y):
        """
        Método que calcula el promedio de los valores RGB de una cuadrícula en la imagen.
        :param image: Imagen original.
        :param x: Coordenada x de la cuadrícula.
        :param y: Coordenada y de la cuadrícula.
        :return: Tupla con los valores de los canales RGB.
        """
        # Inicializar las variables para los valores de los canales RGB
        r, g, b = 0, 0, 0

        # Iterar sobre la cuadrícula
        for i in range(x, x + self.grid_width):
            for j in range(y, y + self.grid_height):
                # Obtener los valores RGB de cada píxel
                pixel = image.getpixel((i, j))
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]

        # Calcular el promedio de los valores RGB
        total_pixels = self.grid_width * self.grid_height
        return r // total_pixels, g // total_pixels, b // total_pixels
        