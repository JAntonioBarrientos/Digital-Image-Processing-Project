from PIL import Image
import numpy as np
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter

class DispersedDitheringFilter(BaseFilter):

    def __init__(self, image):
        """
        Inicializa el filtro de dithering con matriz "dispersed" optimizada utilizando NumPy.
        :param image: Objeto de imagen (PIL Image).
        """
        # Convertir la imagen a escala de grises usando el filtro correspondiente
        im_gray = GrayscaleFilter(image)
        gray_image = im_gray.apply_filter().convert('L')  # Asegurar que esté en modo 'L'
        super().__init__(gray_image)  # Llamar al constructor de la clase base con la imagen en escala de grises

        self.width, self.height = self.image.size

        # Definir la matriz "dispersed" de 3x3
        self.cluster_matrix = np.array([
            [1, 7, 4],
            [5, 8, 3],
            [6, 2, 9]
        ])

        # Escalar la matriz para el rango de 0 a 255
        self.threshold_matrix = self.cluster_matrix * (255 / (self.cluster_matrix.max() + 1))

    def apply_filter(self):
        """
        Aplica el filtro de dithering utilizando la matriz "dispersed" de 3x3 de manera optimizada con NumPy.
        :return: Imagen procesada con dithering.
        """
        # Convertir la imagen a un arreglo NumPy
        image_array = np.array(self.image, dtype=np.uint8)

        # Crear mapas de índices para las posiciones en la matriz 3x3
        Y, X = np.indices((self.height, self.width))
        cluster_indices_x = X % 3
        cluster_indices_y = Y % 3

        # Obtener el mapa de umbrales correspondiente a cada píxel
        threshold_map = self.threshold_matrix[cluster_indices_y, cluster_indices_x]

        # Escalar los valores de píxeles al rango de 0 a 255 si no están ya escalados
        # Si la imagen ya está en escala de grises de 0 a 255, este paso se omite
        pixel_values = image_array.astype(np.float32)

        # Crear la máscara donde el valor del píxel es menor al umbral correspondiente
        mask = pixel_values < threshold_map

        # Asignar 0 (negro) donde la máscara es verdadera, 255 (blanco) donde es falsa
        result_array = np.where(mask, 0, 255).astype(np.uint8)

        # Convertir el arreglo de resultado a una imagen PIL en modo 'L'
        result_image = Image.fromarray(result_array, mode='L')

        return result_image