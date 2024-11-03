from PIL import Image
from models.base_filter import BaseFilter
import numpy as np

class RecursiveImagesColor(BaseFilter):

    def __init__(self, image, upscale_factor, grid_rows, grid_cols):
        """
        Inicializa el filtro de imágenes recursivas con una imagen,
        escala la imagen según el factor de aumento proporcionado,
        y establece las dimensiones de la cuadrícula.

        :param image: Objeto de imagen (PIL Image).
        :param upscale_factor: Factor por el cual se multiplicará el ancho y altura de la imagen.
        :param grid_rows: Número de filas en la cuadrícula.
        :param grid_cols: Número de columnas en la cuadrícula.
        """
        super().__init__(image)

        # Validar el factor de escala
        if upscale_factor < 1:
            raise ValueError("El factor de escala (upscale_factor) debe ser al menos 1")

        # Validar las dimensiones de la cuadrícula
        if grid_rows < 1 or grid_cols < 1:
            raise ValueError("Las dimensiones de la cuadrícula deben ser al menos 1")

        # Obtener dimensiones originales de la imagen
        original_width, original_height = self.image.size

        # Escalar la imagen
        self.width = int(upscale_factor * original_width)
        self.height = int(upscale_factor * original_height)

        # Calcular el tamaño de cada celda de la cuadrícula
        self.grid_width = self.width // grid_cols
        self.grid_height = self.height // grid_rows

        # Ajustar las dimensiones de la imagen al tamaño exacto de la cuadrícula
        self.width = self.grid_width * grid_cols
        self.height = self.grid_height * grid_rows

        # Actualizar las dimensiones de la cuadrícula
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols

    def apply_filter(self):
        """
        Aplica el filtro de imágenes recursivas. Consiste en calcular el promedio de los valores RGB
        en cada celda de la cuadrícula, aplicar una operación AND con el color promedio
        a una imagen redimensionada, y ensamblar la imagen final.

        :return: Imagen procesada.
        """
        # Crear una imagen vacía para la cuadrícula
        recursive_image = Image.new("RGB", (self.width, self.height))

        # Imagen escalada al tamaño total
        image_upscaled = self.image.resize((self.width, self.height))

        # Redimensionar la imagen al tamaño de la celda de la cuadrícula (para usar en cada celda)
        img_resize = self.image.resize((self.grid_width, self.grid_height))

        # Convertir la imagen escalada a un arreglo NumPy
        image_array = np.array(image_upscaled, dtype=np.uint8)

        # Reestructurar el arreglo para separar las celdas de la cuadrícula
        # Nueva forma: (grid_rows, grid_height, grid_cols, grid_width, 3)
        image_array = image_array.reshape(
            self.grid_rows, self.grid_height, self.grid_cols, self.grid_width, 3
        )

        # Transponer para que las dimensiones de la cuadrícula estén en los dos primeros ejes
        # Forma resultante: (grid_rows, grid_cols, grid_height, grid_width, 3)
        image_array = image_array.transpose(0, 2, 1, 3, 4)

        # Calcular el promedio de color para cada celda
        # Resultado: (grid_rows, grid_cols, 3)
        average_colors = image_array.mean(axis=(2, 3)).astype(np.uint8)

        # Convertir la imagen redimensionada a un arreglo NumPy
        img_resize_array = np.array(img_resize, dtype=np.uint8)

        # Aplicar el filtro en cada celda
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x_start = col * self.grid_width
                y_start = row * self.grid_height

                # Obtener el promedio de color para esta celda
                r_val, g_val, b_val = average_colors[row, col]

                # Aplicar el AND lógico con los valores de color promedio
                processed_block = self._apply_and_filter(img_resize_array, r_val, g_val, b_val)

                # Convertir el arreglo procesado a imagen PIL
                processed_image = Image.fromarray(processed_block, mode='RGB')

                # Pegar la imagen procesada en la posición correspondiente
                recursive_image.paste(processed_image, (x_start, y_start))

        return recursive_image

    @staticmethod
    def _apply_and_filter(block, r_val, g_val, b_val):
        """
        Aplica el filtro Mica a un bloque de la imagen usando operaciones vectorizadas.
        """
        # Crear una copia del bloque para no modificar el original
        processed_block = block.copy()

        # Aplicar el AND lógico con los valores proporcionados
        processed_block[:, :, 0] = processed_block[:, :, 0] & r_val
        processed_block[:, :, 1] = processed_block[:, :, 1] & g_val
        processed_block[:, :, 2] = processed_block[:, :, 2] & b_val

        return processed_block
