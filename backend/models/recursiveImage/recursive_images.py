from PIL import Image
from models.base_filter import BaseFilter

class RecursiveImages(BaseFilter):
    def __init__(self, image, grid_factor=50, num_variations):
        """
        Inicializa el filtro de imágenes recursivas con una imagen,
        calcula el tamaño de la cuadrícula en función del tamaño de la imagen y un factor de escala,
        y establece el número de variaciones en escala de grises.

        :param image: Objeto de imagen (PIL Image).
        :param grid_factor: Factor por el cual se dividirá el ancho y altura de la imagen.
        :param num_variations: Número de versiones en escala de grises.
        """
        super().__init__(image)
        
        # Obtener dimensiones originales de la imagen
        width, height = self.image.size

        self.grid_width = width // grid_factor
        self.grid_height = height // grid_factor

        # Definir el número de variaciones
        self.num_variations = num_variations

    def get_palette(self):
        """
        Aplica el filtro reescalando la imagen al tamaño de la cuadrícula calculado,
        y luego crea `num_variations` versiones en escala de grises con diferentes
        niveles de brillo.
        :return: Un diccionario con `num_variations` imágenes en escala de grises.
        """
        # Reescalar la imagen al tamaño de la cuadrícula calculada
        img_rescaled = self.image.resize((self.grid_width, self.grid_height))

        # Diccionario para almacenar las versiones de la imagen
        gray_variations = {}

        # Iterar para crear `p` versiones de la imagen en escala de grises
        for i in range(self.num_variations):
            # Copiar la imagen reducida
            img_copy = img_rescaled.copy()
            pixels = img_copy.load()
            width, height = img_copy.size

            # Escala de brillo en función de `i`
            brightness_factor = i / (self.num_variations - 1)  # Valor entre 0 y 1

            # Procesar los píxeles para aplicar escala de grises y ajustar el brillo
            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y]
                    # Convertir a escala de grises promedio
                    grayscale_value = (r + g + b) // 3
                    # Aplicar el factor de brillo
                    adjusted_value = int(grayscale_value * brightness_factor)
                    pixels[x, y] = (adjusted_value, adjusted_value, adjusted_value)

            # Guardar la imagen procesada en el diccionario
            gray_variations[f"variation_{i+1}"] = img_copy

        return gray_variations

    def apply_filter(self):
        """
        Método que aplica el filtro de imágenes recursivas. Que consiste en poner 
        las imágenes en escala de grises en una cuadrícula y devolver la imagen resultante.
        :return: Imagen procesada.
        """
        