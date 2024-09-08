import numpy as np
from PIL import Image
from models.base_filter import BaseFilter

import numpy as np
from PIL import Image

class ConvolutionFilterRGB(BaseFilter):
    def replicate_borders(self, pixels, pad):
        """
        Replicar los bordes de la imagen de acuerdo al tamaño del kernel.
        Se añadirá una capa de píxeles replicando los valores de los bordes.
        
        :param pixels: Array de Numpy que representa la imagen.
        :param pad: Tamaño del padding (la cantidad de filas/columnas a añadir).
        :return: Imagen con bordes replicados.
        """
        height, width, channels = pixels.shape
        # Crear una nueva imagen con espacio para el padding
        padded_image = np.zeros((height + 2 * pad, width + 2 * pad, channels), dtype=pixels.dtype)

        # Copiar la imagen original en el centro de la imagen con padding
        padded_image[pad:pad + height, pad:pad + width] = pixels

        # Replicar las filas superiores e inferiores
        for i in range(pad):
            # Replicar la fila superior
            padded_image[i, pad:pad + width] = pixels[0, :]
            # Replicar la fila inferior
            padded_image[pad + height + i, pad:pad + width] = pixels[height - 1, :]

        # Replicar las columnas izquierda y derecha
        for j in range(pad):
            # Replicar la columna izquierda
            padded_image[pad:pad + height, j] = pixels[:, 0]
            # Replicar la columna derecha
            padded_image[pad:pad + height, pad + width + j] = pixels[:, width - 1]

        # Replicar las esquinas
        # Esquina superior izquierda
        padded_image[:pad, :pad] = pixels[0, 0]
        # Esquina superior derecha
        padded_image[:pad, pad + width:] = pixels[0, width - 1]
        # Esquina inferior izquierda
        padded_image[pad + height:, :pad] = pixels[height - 1, 0]
        # Esquina inferior derecha
        padded_image[pad + height:, pad + width:] = pixels[height - 1, width - 1]

        return padded_image

    def apply_convolution(self, kernel):
        """
        Aplica un filtro de convolución a la imagen en los tres canales (R, G, B) utilizando el kernel proporcionado.
        
        :param kernel: Matriz (numpy array) que representa el kernel de convolución. Sus dimensiones deben ser impares y cuadradas.
        :return: Imagen procesada.
        """
        img = self.image.convert('RGB')  # Convertimos la imagen a RGB
        pixels = np.array(img)  # Convertimos la imagen a un array de Numpy (alto, ancho, 3)
        kernel_size = kernel.shape[0]  # Asumimos que el kernel es cuadrado (n x n)
        pad = kernel_size // 2  # Tamaño del padding

        # Replicar los bordes 
        padded_image = self.replicate_borders(pixels, pad)

        # Crear una imagen de salida con las mismas dimensiones que la imagen original
        output_image = np.zeros_like(pixels)

        # Realizar la convolución en los tres canales
        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                for c in range(3):  # Canales R, G, B
                    # Extraer la región de la imagen correspondiente al tamaño del kernel
                    region = padded_image[i:i + kernel_size, j:j + kernel_size, c]
                    # Aplicar el kernel sobre la región y sumar los resultados
                    output_value = np.sum(region * kernel)
                    # Asignar el valor calculado a la imagen de salida (con clipping para mantener [0,255])
                    output_image[i, j, c] = min(max(int(output_value), 0), 255)

        # Convertir de nuevo a imagen PIL
        return Image.fromarray(output_image)
