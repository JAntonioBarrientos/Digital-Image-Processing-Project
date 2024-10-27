import numpy as np
from PIL import Image
from models.base_filter import BaseFilter

class MaxKernelFilter(BaseFilter):
    def apply_filter(self, radius):
        """
        Aplica un filtro que reemplaza cada píxel por el valor máximo encontrado en el kernel.

        :param radius: Radio del kernel (entero positivo).
        :return: Imagen procesada (PIL Image).
        """
        if radius <= 0:
            raise ValueError("El radio debe ser un entero positivo.")

        # Convertir la imagen a escala de grises si no lo está
        gray_image = self.image.convert('L')

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
                # Encontrar el valor máximo en el kernel
                max_value = np.max(kernel)
                # Asignar el valor máximo al píxel central
                processed_array[y, x] = max_value

        # Convertir el arreglo procesado de vuelta a una imagen PIL
        processed_image = Image.fromarray(processed_array, mode='L')

        return processed_image
