from PIL import Image
import random
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter

class RandomDitheringFilter(BaseFilter):

    def __init__(self, image):
        """
        Inicializa el filtro de dithering aleatorio con una imagen en escala de grises.
        :param image: Objeto de imagen (PIL Image).
        """
        im_gray = GrayscaleFilter(image)
        super().__init__(im_gray.apply_filter())
        
        # Obtener dimensiones originales de la imagen
        width, height = self.image.size
        self.width = width
        self.height = height


    def apply_filter(self):
        """
        Método que aplica el dithering aleatorio a la imagen en escala de grises.
        :return: Imagen procesada con dithering aleatorio.
        """
        # Crear una nueva imagen para el resultado en blanco y negro
        result_image = Image.new("RGB", (self.width, self.height))

        # Obtener los píxeles de la imagen original
        pixels = self.image.load()

        # Cargar los píxeles de la imagen de resultado
        result_pixels = result_image.load()

        # Iterar sobre cada píxel de la imagen
        for i in range(self.width):
            for j in range(self.height):
                # Obtener el valor de brillo (en escala de grises, r = g = b)
                brightness = pixels[i, j][0]  # Solo necesitamos un canal, ya que es en escala de grises

                # Generar un número aleatorio entre 0 y 255
                random_value = random.randint(0, 255)

                # Si el brillo es menor o igual al valor aleatorio, pintamos el píxel de negro
                if brightness <= random_value:
                    result_pixels[i, j] = (0, 0, 0)  # Negro
                else:
                    result_pixels[i, j] = (255, 255, 255)  # Blanco

        return result_image
