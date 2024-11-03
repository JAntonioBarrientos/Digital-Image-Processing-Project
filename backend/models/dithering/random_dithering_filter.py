from PIL import Image
import numpy as np
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
        self.width, self.height = self.image.size

    def apply_filter(self):
        """
        Método que aplica el dithering aleatorio a la imagen en escala de grises.
        :return: Imagen procesada con dithering aleatorio.
        """
        # Convertir la imagen a un arreglo NumPy
        image_array = np.array(self.image)

        # Generar una matriz aleatoria del mismo tamaño que la imagen
        random_matrix = np.random.randint(0, 256, (self.height, self.width), dtype=np.uint8)

        # Obtener el canal de brillo (asumiendo escala de grises, R=G=B)
        brightness = image_array[:, :, 0]

        # Crear una máscara donde el brillo es MENOR o IGUAL al valor aleatorio
        mask = brightness <= random_matrix

        # Inicializar el arreglo de resultado con blanco
        result_array = np.ones_like(image_array) * 255

        # Asignar negro donde la máscara es verdadera
        result_array[mask] = [0, 0, 0]

        # Convertir el arreglo de resultado a una imagen PIL
        result_image = Image.fromarray(result_array.astype('uint8'), 'RGB')

        return result_image