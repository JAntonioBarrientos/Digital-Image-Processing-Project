from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from models.base_filter import BaseFilter

class WatermarkFilter(BaseFilter):
    def __init__(self, image, texto, coordenadas, alpha, tamaño_fuente):
        """
        Inicializa el filtro de marca de agua con los parámetros necesarios.
        
        :param image: Objeto de imagen (PIL Image).
        :param texto: Texto de la marca de agua.
        :param coordenadas: Coordenadas (x, y) para posicionar el texto.
        :param alpha: Valor de transparencia (0.0 completamente transparente, 1.0 completamente opaco).
        :param tamaño_fuente: Tamaño de la fuente del texto de la marca de agua.
        """
        super().__init__(image)
        self.texto = texto
        self.coordenadas = coordenadas
        self.alpha = alpha
        self.tamaño_fuente = tamaño_fuente

    def apply_filter(self):
        """
        Aplica el filtro de marca de agua con el texto y transparencia especificados.
        Realiza la composición manualmente usando la fórmula proporcionada.
        :return: Imagen con la marca de agua aplicada.
        """
        # Crear una imagen de texto del mismo tamaño que la imagen original (sin alpha aún)
        marca_de_agua = Image.new('RGB', self.image.size, color=(255, 255, 255))  # Fondo blanco
        dibujar = ImageDraw.Draw(marca_de_agua)

        # Definir la fuente del texto
        try:
            fuente = ImageFont.truetype("fonts/Roboto-Regular.ttf", self.tamaño_fuente)
        except IOError:
            fuente = ImageFont.load_default()

        # Dibujar el texto en la imagen de marca de agua
        dibujar.text(self.coordenadas, self.texto, font=fuente, fill="black")  # Texto en negro

        # Convertir las imágenes a 'RGB' si no lo están
        imagen_original = self.image.convert('RGB')
        imagen_marca = marca_de_agua.convert('RGB')

        # Obtener los píxeles de ambas imágenes
        pixeles_original = imagen_original.load()
        pixeles_marca = imagen_marca.load()

        # Crear una nueva imagen donde almacenaremos el resultado
        imagen_resultante = Image.new('RGB', self.image.size)
        pixeles_resultantes = imagen_resultante.load()

        # Aplicar la fórmula para cada píxel
        for y in range(self.image.size[1]):  # Iterar sobre el alto
            for x in range(self.image.size[0]):  # Iterar sobre el ancho
                r1, g1, b1 = pixeles_original[x, y]  # Píxel de la imagen original
                r2, g2, b2 = pixeles_marca[x, y]  # Píxel de la imagen de marca de agua
                # Solo aplicar el blend si el píxel de la marca de agua no es blanco
                if (r2, g2, b2) != (255, 255, 255):
                    # Aplicar la fórmula para cada componente de color (R, G, B)
                    r = int(r1 * self.alpha + r2 * (1 - self.alpha))
                    g = int(g1 * self.alpha + g2 * (1 - self.alpha))
                    b = int(b1 * self.alpha + b2 * (1 - self.alpha))

                    # Guardar el nuevo píxel en la imagen resultante
                    pixeles_resultantes[x, y] = (r, g, b)
                else:
                    # Si el píxel es blanco, mantener el píxel original
                    pixeles_resultantes[x, y] = (r1, g1, b1)

        return imagen_resultante
