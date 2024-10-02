from PIL import Image
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter

class RecursiveImagesGray(BaseFilter):
    def __init__(self, image, num_variations, grid_factor):
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
        self.width = width
        self.height = height
        self.grid_width = width // grid_factor
        self.grid_height = height // grid_factor
        self.grid_factor = grid_factor

        # Validar el factor de cuadrícula este en el rango correcto
        if not (1 <= grid_factor <= min(width, height)):
            raise ValueError("El factor de cuadrícula debe estar entre 1 y el alto o ancho de la imagen en píxeles") 

        # Validar el numero de variantes este en el rango correcto
        if not (2 <= num_variations <= 256):
            raise ValueError("El número de variaciones debe estar entre 2 y 256")

        # Definir el número de variaciones
        self.num_variations = num_variations

    def get_palette(self):
        """
        Genera n variantes de la imagen en escala de grises, ajustando el brillo de cada píxel
        para que el valor esté más cerca del valor representativo en cada variante.
        :return: Diccionario con las versiones de la imagen. 
                Las claves son los valores representativos de brillo y los valores son las imágenes correspondientes.
        """
        # Reescalar la imagen al tamaño de la cuadrícula calculada
        img_resize = self.image.resize((self.grid_width, self.grid_height))
        
        img_rescaled = GrayscaleFilter(img_resize).apply_filter()        
        
        # Diccionario para almacenar las versiones de la imagen
        versiones = {}
        
        # Calcular el salto entre cada variante en la escala de 0 a 255
        paso = 255 // self.num_variations
        
        # Recorrer el rango de 0 a 255 con saltos de 'paso'
        for i in range(0, 256, paso):
            # Crear una copia de la imagen original
            imagen_variante = img_rescaled.copy()
            
            # Obtener los píxeles de la imagen
            pixels = imagen_variante.load()
            
            # Ajustar el brillo de cada píxel para acercarlo al valor representativo 'i'
            for x in range(imagen_variante.width):
                for y in range(imagen_variante.height):
                    # Obtener el valor de brillo actual del píxel (en escala de grises)
                    brillo_actual = pixels[x, y]
                    
                    # Calcular el nuevo brillo ajustado:
                    # Desplazar el brillo actual hacia el valor representativo 'i'
                    # Manteniendo la proporción de la imagen
                    nuevo_brillo = int(brillo_actual[0] + (i - brillo_actual[0]) * (i / 255.0))
                    
                    # Asegurarse de que el nuevo valor esté en el rango [0, 255]
                    nuevo_brillo = max(0, min(255, nuevo_brillo))
                    
                    # Asignar el nuevo brillo al píxel
                    pixels[x, y] = (nuevo_brillo, nuevo_brillo, nuevo_brillo)
            
            # Almacenar la imagen modificada en el diccionario
            versiones[i] = imagen_variante
        
        return versiones

    def apply_filter(self):
        """
        Método que aplica el filtro de imágenes recursivas. Que consiste en hacer un promedio de los valores RGB por el tamaño de la imagen y seleccionar la imagen en escala de grises que más se asemeje a la original.
        :return: Imagen procesada.
        """
        # Obtener las versiones de la imagen en escala de grises
        gray_variations = self.get_palette()

        # Crear una imagen en blanco para la cuadrícula
        recursive_image = Image.new("RGB", (self.grid_width*self.grid_factor, self.grid_height*self.grid_factor))

        # Cargar los píxeles de la imagen
        pixels = recursive_image.load()

        # Iterar sobre cada cuadrícula
        for i in range(0, self.grid_width*self.grid_factor, self.grid_width):
            for j in range(0, self.grid_height*self.grid_factor, self.grid_height):
                # Obtener el promedio de los valores RGB de la cuadrícula
                r, g, b = self.calculate_average_color(self.image, i, j)
                # Calcular el promedio de los valores RGB
                p = (r + g + b) // 3
                # Calcular el valor de escala de grises más cercano
                grayscale_value = min(gray_variations, key=lambda x: abs(x - p))
                # Pegar la imagen correspondiente del diccionario de nuestra variaciones en la imagen recursiva
                recursive_image.paste(gray_variations[grayscale_value], (i, j))

        return recursive_image

    def calculate_average_color(self, image, x, y):
        """
        Método que calcula el promedio de los valores RGB de una cuadrícula en la imagen.
        :param image: Imagen original.
        :param x: Coordenada x de la cuadrícula.
        :param y: Coordenada y de la cuadrícula.
        :return: Tupla con los valores de los canales RGB.
        """
        # Inicializar las variables para los valores de los canales RGB
        r, g, b = 0, 0, 0

        # Iterar sobre la cuadrícula
        for i in range(x, x + self.grid_width):
            for j in range(y, y + self.grid_height):
                # Obtener los valores RGB de cada píxel
                pixel = image.getpixel((i, j))
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]

        # Calcular el promedio de los valores RGB
        total_pixels = self.grid_width * self.grid_height
        return r // total_pixels, g // total_pixels, b // total_pixels
        