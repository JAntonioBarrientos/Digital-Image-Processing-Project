from PIL import Image
import numpy as np
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter

class ClusteredDitheringFilter(BaseFilter):

    def __init__(self, image):
        """
        Inicializa el filtro de dithering con matriz "clustered" con una imagen en escala de grises.
        :param image: Objeto de imagen (PIL Image).
        """
        # Convertir la imagen a escala de grises usando el filtro correspondiente
        im_gray = GrayscaleFilter(image)
        super().__init__(im_gray.apply_filter())  # Llamar al constructor de la clase base con la imagen en escala de grises
        
        self.width, self.height = self.image.size
        
        # Definir la matriz "clustered" de 3x3
        self.cluster_matrix = np.array([
            [8, 3, 4],
            [6, 1, 2],
            [7, 5, 9]
        ])
        
        # Escalar la matriz para el rango de 0 a 255 (cada valor de la matriz se multiplica por 255 // 9)
        self.threshold_matrix = self.cluster_matrix * (255 // 9)

    def apply_filter(self):
        """
        Aplica el filtro de dithering utilizando la matriz "clustered" de 3x3.
        :return: Imagen procesada con dithering.
        """
        # Crear una nueva imagen para el resultado en blanco y negro
        result_image = Image.new("L", (self.width, self.height))
        result_pixels = result_image.load()
        
        # Obtener los píxeles de la imagen original
        original_pixels = self.image.load()

        # Iterar sobre cada bloque de 3x3 en la imagen
        for i in range(0, self.width, 3):
            for j in range(0, self.height, 3):
                # Iterar sobre cada píxel en el bloque 3x3
                for x in range(3):
                    for y in range(3):
                        if i + x < self.width and j + y < self.height:
                            # Leer el valor de brillo del píxel original
                            pixel_value = original_pixels[i + x, j + y][0]

                            # Escalar el valor del píxel entre 0 y 9 (dividir por 28)
                            pixel_value_scaled = pixel_value // 28

                            # Comparar con el valor de la matriz
                            threshold_value = self.cluster_matrix[x, y]

                            # Aplicar la regla de dithering
                            if pixel_value_scaled < threshold_value:
                                result_pixels[i + x, j + y] = 0  # Negro
                            else:
                                result_pixels[i + x, j + y] = 255  # Blanco

        return result_image
