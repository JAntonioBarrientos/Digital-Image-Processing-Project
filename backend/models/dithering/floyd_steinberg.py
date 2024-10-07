from PIL import Image
import numpy as np
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter

class FloydSteinbergDitheringFilter(BaseFilter):

    def __init__(self, image):
        """
        Inicializa el filtro de dithering Floyd-Steinberg con una imagen en escala de grises.
        :param image: Objeto de imagen (PIL Image).
        """
        # Convertir la imagen a escala de grises usando el filtro correspondiente
        im_gray = GrayscaleFilter(image)
        # Convertir la imagen devuelta de RGB a escala de grises (modo 'L')
        gray_image = im_gray.apply_filter().convert('L')
        super().__init__(gray_image)  # Llamar al constructor de la clase base con la imagen en escala de grises

        self.width, self.height = self.image.size

    def apply_filter(self):
        """
        Aplica el filtro de dithering Floyd-Steinberg a la imagen.
        :return: Imagen procesada con dithering.
        """
        # Convertir la imagen a un arreglo numpy para manipular los píxeles
        pixels = np.array(self.image, dtype=np.float32)
        
        # Iterar sobre cada píxel de la imagen
        for y in range(self.height):
            for x in range(self.width):
                # Obtener el valor del píxel original
                old_pixel = pixels[y, x]
                
                # Redondear al color más cercano (0 o 255)
                new_pixel = 255 if old_pixel > 128 else 0
                pixels[y, x] = new_pixel
                
                # Calcular el error de cuantización
                quant_error = old_pixel - new_pixel
                
                # Distribuir el error a los píxeles vecinos
                if x + 1 < self.width:
                    pixels[y, x + 1] += quant_error * 7 / 16
                if x - 1 >= 0 and y + 1 < self.height:
                    pixels[y + 1, x - 1] += quant_error * 3 / 16
                if y + 1 < self.height:
                    pixels[y + 1, x] += quant_error * 5 / 16
                if x + 1 < self.width and y + 1 < self.height:
                    pixels[y + 1, x + 1] += quant_error * 1 / 16

        # Convertir el arreglo de píxeles de vuelta a una imagen en escala de grises
        result_image = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8), mode='L')
        return result_image

