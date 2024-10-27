import numpy as np
from PIL import Image
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter

class MinMaxKernelFilter(BaseFilter):
    def apply_filter(self, radius, operation='max'):
        """
        Aplica un filtro que reemplaza cada píxel por el valor máximo o mínimo encontrado en el kernel.

        :param radius: Radio del kernel (entero positivo).
        :param operation: 'max' para máximo, 'min' para mínimo.
        :return: Imagen procesada (PIL Image).
        """
        if radius <= 0:
            raise ValueError("El radio debe ser un entero positivo.")
        if operation not in ['max', 'min']:
            raise ValueError("La operación debe ser 'max' o 'min'.")

        # Convertir la imagen a escala de grises si no lo está
        gray_convert = GrayscaleFilter(self.image)
        gray_image = gray_convert.apply_filter().convert('L')

        # Convertir la imagen a un arreglo NumPy
        image_array = np.array(gray_image, dtype=np.uint8)

        # Obtener las dimensiones de la imagen
        height, width = image_array.shape

        # Crear una copia para almacenar la imagen procesada
        processed_array = np.zeros_like(image_array)

        # Padding para manejar los bordes
        pad_width = radius
        padded_array = np.pad(image_array, pad_width, mode='edge')

        # Procesar la imagen
        for y in range(height):
            for x in range(width):
                # Extraer el kernel
                kernel = padded_array[y : y + 2*radius + 1, x : x + 2*radius + 1]
                if operation == 'max':
                    # Encontrar el valor máximo en el kernel
                    value = np.max(kernel)
                else:  # operation == 'min'
                    # Encontrar el valor mínimo en el kernel
                    value = np.min(kernel)
                # Asignar el valor al píxel central
                processed_array[y, x] = value

        # Convertir el arreglo procesado de vuelta a una imagen PIL
        processed_image = Image.fromarray(processed_array, mode='L')

        return processed_image
