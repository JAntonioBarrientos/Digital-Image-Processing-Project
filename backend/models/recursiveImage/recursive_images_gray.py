from PIL import Image
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter
import numpy as np

class RecursiveImagesGray(BaseFilter):

    def __init__(self, image, num_variations, upscale_factor, grid_rows, grid_cols):
        """
        Inicializa el filtro de imágenes recursivas con una imagen,
        escala la imagen según el factor de aumento proporcionado,
        y establece el número de variaciones en escala de grises y las dimensiones de la cuadrícula.

        :param image: Objeto de imagen (PIL Image).
        :param num_variations: Número de versiones en escala de grises (entre 2 y 256).
        :param upscale_factor: Factor por el cual se multiplicará el ancho y altura de la imagen.
        :param grid_rows: Número de filas en la cuadrícula.
        :param grid_cols: Número de columnas en la cuadrícula.
        """
        super().__init__(image)
        
        # Validar el número de variaciones
        if not (2 <= num_variations <= 256):
            raise ValueError("El número de variaciones debe estar entre 2 y 256")

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

        # Definir el número de variaciones
        self.num_variations = num_variations

    def get_palette(self):
        """
        Genera n variantes de la imagen en escala de grises, ajustando el brillo de cada píxel
        para que el brillo promedio de la imagen coincida con cada valor representativo.

        :return: Diccionario con las versiones de la imagen.
                 Las claves son los valores representativos de brillo y los valores son las imágenes correspondientes.
        """
        # Redimensionar la imagen al tamaño de la celda de la cuadrícula
        img_resize = self.image.resize((self.grid_width, self.grid_height))
        
        # Aplicar filtro de escala de grises
        img_rescaled = GrayscaleFilter(img_resize).apply_filter()
        
        # Convertir la imagen a un arreglo NumPy para operaciones eficientes
        img_array = np.array(img_rescaled.convert('L'), dtype=np.float32)
        
        # Calcular el brillo promedio de la imagen original
        brillo_promedio = img_array.mean()
        
        # Evitar división por cero
        if brillo_promedio == 0:
            brillo_promedio = 1

        # Generar los valores representativos de brillo
        valores_brillo = np.linspace(0, 255, self.num_variations)
        
        # Diccionario para almacenar las versiones de la imagen
        versiones = {}

        # Generar las variaciones utilizando operaciones vectorizadas
        for i in valores_brillo:
            # Calcular el factor de escala
            factor_escala = i / brillo_promedio

            # Ajustar el brillo de la imagen
            imagen_variante_array = img_array * factor_escala

            # Asegurarse de que los valores estén en el rango [0, 255]
            imagen_variante_array = np.clip(imagen_variante_array, 0, 255).astype(np.uint8)

            # Convertir de nuevo a imagen PIL en modo 'L' y luego a 'RGB'
            imagen_variante = Image.fromarray(imagen_variante_array, mode='L').convert('RGB')

            # Almacenar la imagen modificada en el diccionario
            versiones[int(i)] = imagen_variante

        return versiones

    def apply_filter(self):
        """
        Aplica el filtro de imágenes recursivas. Consiste en calcular el promedio de los valores RGB
        en cada celda de la cuadrícula y seleccionar la variante en escala de grises que más se asemeje.

        :return: Imagen procesada.
        """
        # Obtener las versiones de la imagen en escala de grises
        gray_variations = self.get_palette()
        gray_keys = np.array(list(gray_variations.keys()))

        # Imagen escalada al tamaño total
        image_upscaled = self.image.resize((self.width, self.height))

        # Convertir la imagen a un arreglo NumPy
        image_array = np.array(image_upscaled, dtype=np.float32)

        # Reshape para obtener las celdas
        image_array = image_array.reshape(
            self.grid_rows, self.grid_height, self.grid_cols, self.grid_width, 3
        )

        # Calcular el promedio de los valores RGB en cada celda
        cell_means = image_array.mean(axis=(1, 3))  # Shape: (grid_rows, grid_cols, 3)

        # Calcular el brillo promedio de cada celda
        cell_brightness = cell_means.mean(axis=2)  # Shape: (grid_rows, grid_cols)

        # Encontrar el valor de brillo más cercano en las variaciones para cada celda
        # Expandir dimensiones para broadcasting
        cell_brightness_expanded = cell_brightness[:, :, np.newaxis]  # Shape: (grid_rows, grid_cols, 1)
        gray_keys_expanded = gray_keys[np.newaxis, np.newaxis, :]     # Shape: (1, 1, num_variations)

        # Calcular la diferencia absoluta
        diff = np.abs(gray_keys_expanded - cell_brightness_expanded)

        # Encontrar el índice del valor mínimo
        idx_min = diff.argmin(axis=2)  # Shape: (grid_rows, grid_cols)

        # Obtener los valores de brillo seleccionados
        selected_gray_values = gray_keys[idx_min]  # Shape: (grid_rows, grid_cols)

        # Crear una imagen vacía para la cuadrícula
        recursive_image = Image.new("RGB", (self.width, self.height))

        # Pegar las imágenes correspondientes en la posición adecuada
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x_start = col * self.grid_width
                y_start = row * self.grid_height
                grayscale_value = selected_gray_values[row, col]
                gray_image = gray_variations[grayscale_value]
                recursive_image.paste(gray_image, (x_start, y_start))

        return recursive_image

