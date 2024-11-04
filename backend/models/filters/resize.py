from PIL import Image
import numpy as np
from models.base_filter import BaseFilter

class ResizeFilter(BaseFilter):
    def __init__(self, image, percent_x, percent_y):
        """
        Inicializa el filtro de redimensionamiento con una imagen y porcentajes para los ejes X e Y.

        :param image: Objeto de imagen (PIL Image).
        :param percent_x: Porcentaje de cambio en el eje X (ancho).
        :param percent_y: Porcentaje de cambio en el eje Y (alto).
        """
        super().__init__(image)

        # Validar que los porcentajes sean números positivos
        if percent_x <= 0 or percent_y <= 0:
            raise ValueError("Los porcentajes deben ser números positivos mayores que cero.")

        self.percent_x = percent_x
        self.percent_y = percent_y

    def apply_filter(self):
        """
        Aplica el filtro de redimensionamiento a la imagen utilizando interpolación bilineal.

        :return: Imagen redimensionada.
        """
        # Obtener dimensiones originales de la imagen
        original_width, original_height = self.image.size

        # Calcular nuevas dimensiones basadas en los porcentajes
        new_width = int(original_width * (self.percent_x / 100))
        new_height = int(original_height * (self.percent_y / 100))

        # Convertir la imagen a un array NumPy
        image_array = np.array(self.image)

        # Manejar imágenes en escala de grises y en color
        if len(image_array.shape) == 2:
            # Imagen en escala de grises
            resized_array = self._bilinear_interpolation_gray(image_array, new_width, new_height)
        else:
            # Imagen en color
            print("Color")
            resized_array = self._bilinear_interpolation_color(image_array, new_width, new_height)

        # Convertir el array NumPy de vuelta a una imagen PIL
        resized_image = Image.fromarray(resized_array.astype(np.uint8))

        return resized_image

    def _bilinear_interpolation_gray(self, image_array, new_width, new_height):
        """
        Realiza la interpolación bilineal en una imagen en escala de grises.

        :param image_array: Array NumPy de la imagen original en escala de grises.
        :param new_width: Ancho de la imagen redimensionada.
        :param new_height: Alto de la imagen redimensionada.
        :return: Array NumPy de la imagen redimensionada.
        """
        original_height, original_width = image_array.shape

        # Crear una matriz vacía para la imagen redimensionada
        resized_array = np.zeros((new_height, new_width))

        # Calcular las relaciones de escala
        scale_x = original_width / new_width
        scale_y = original_height / new_height

        # Crear una malla de coordenadas para la imagen redimensionada
        x_new = np.arange(new_width)
        y_new = np.arange(new_height)
        x_new_mesh, y_new_mesh = np.meshgrid(x_new, y_new)

        # Mapear las coordenadas de la nueva imagen a las coordenadas de la imagen original
        x_orig = x_new_mesh * scale_x
        y_orig = y_new_mesh * scale_y

        # Calcular las coordenadas de los píxeles vecinos
        x0 = np.floor(x_orig).astype(int)
        x1 = x0 + 1
        y0 = np.floor(y_orig).astype(int)
        y1 = y0 + 1

        # Clipping para evitar índices fuera de los límites
        x0 = np.clip(x0, 0, original_width - 1)
        x1 = np.clip(x1, 0, original_width - 1)
        y0 = np.clip(y0, 0, original_height - 1)
        y1 = np.clip(y1, 0, original_height - 1)

        # Obtener los valores de los píxeles vecinos
        Ia = image_array[y0, x0]
        Ib = image_array[y1, x0]
        Ic = image_array[y0, x1]
        Id = image_array[y1, x1]

        # Calcular las distancias fraccionarias
        dx = x_orig - x0
        dy = y_orig - y0

        # Realizar la interpolación bilineal
        resized_array = (Ia * (1 - dx) * (1 - dy) +
                         Ic * dx * (1 - dy) +
                         Ib * (1 - dx) * dy +
                         Id * dx * dy)

        return resized_array

    def _bilinear_interpolation_color(self, image_array, new_width, new_height):
        """
        Realiza la interpolación bilineal en una imagen en color.

        :param image_array: Array NumPy de la imagen original en color.
        :param new_width: Ancho de la imagen redimensionada.
        :param new_height: Alto de la imagen redimensionada.
        :return: Array NumPy de la imagen redimensionada.
        """
        original_height, original_width, num_channels = image_array.shape

        # Crear una matriz vacía para la imagen redimensionada
        resized_array = np.zeros((new_height, new_width, num_channels))

        # Calcular las relaciones de escala
        scale_x = original_width / new_width
        scale_y = original_height / new_height

        # Crear una malla de coordenadas para la imagen redimensionada
        x_new = np.arange(new_width)
        y_new = np.arange(new_height)
        x_new_mesh, y_new_mesh = np.meshgrid(x_new, y_new)

        # Mapear las coordenadas de la nueva imagen a las coordenadas de la imagen original
        x_orig = x_new_mesh * scale_x
        y_orig = y_new_mesh * scale_y

        # Calcular las coordenadas de los píxeles vecinos
        x0 = np.floor(x_orig).astype(int)
        x1 = x0 + 1
        y0 = np.floor(y_orig).astype(int)
        y1 = y0 + 1

        # Clipping para evitar índices fuera de los límites
        x0 = np.clip(x0, 0, original_width - 1)
        x1 = np.clip(x1, 0, original_width - 1)
        y0 = np.clip(y0, 0, original_height - 1)
        y1 = np.clip(y1, 0, original_height - 1)

        # Calcular las distancias fraccionarias
        dx = x_orig - x0
        dy = y_orig - y0

        # Realizar la interpolación bilineal en cada canal
        for c in range(num_channels):
            channel = image_array[:, :, c]

            # Obtener los valores de los píxeles vecinos para el canal actual
            Ia = channel[y0, x0]
            Ib = channel[y1, x0]
            Ic = channel[y0, x1]
            Id = channel[y1, x1]

            # Realizar la interpolación bilineal
            resized_channel = (Ia * (1 - dx) * (1 - dy) +
                               Ic * dx * (1 - dy) +
                               Ib * (1 - dx) * dy +
                               Id * dx * dy)

            # Asignar el canal interpolado a la imagen redimensionada
            resized_array[:, :, c] = resized_channel

        return resized_array
