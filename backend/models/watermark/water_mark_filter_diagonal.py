from PIL import Image, ImageDraw, ImageFont
from models.base_filter import BaseFilter
import math

class WatermarkFilterDiagonal(BaseFilter):
    def __init__(self, image, texto, alpha, tamaño_fuente):
        """
        Inicializa el filtro de marca de agua con los parámetros necesarios.
        
        :param image: Objeto de imagen (PIL Image).
        :param texto: Texto de la marca de agua.
        :param alpha: Valor de transparencia (0.0 completamente transparente, 1.0 completamente opaco).
        :param tamaño_fuente: Tamaño de la fuente del texto de la marca de agua.
        """
        super().__init__(image)
        self.texto = texto
        self.alpha = alpha
        self.tamaño_fuente = tamaño_fuente

    def apply_filter(self):
        """
        Aplica el filtro de marca de agua con el texto y transparencia especificados.
        Realiza la composición manualmente usando la fórmula proporcionada.
        :return: Imagen con la marca de agua aplicada.
        """
        # Tamaño de la marca de agua (doble del tamaño de la imagen original)
        size_watermark = (self.image.size[0] * 2, self.image.size[1] * 2)

        # Crear una imagen de marca de agua del doble del tamaño de la imagen original
        marca_de_agua = Image.new('RGBA', size_watermark, color=(255, 255, 255, 0))  # Fondo transparente
        dibujar = ImageDraw.Draw(marca_de_agua)

        # Definir la fuente del texto
        try:
            fuente = ImageFont.truetype("fonts/Roboto-Regular.ttf", self.tamaño_fuente)
        except IOError:
            fuente = ImageFont.load_default()

        # Medir el tamaño del texto
        bbox = dibujar.textbbox((0, 0), self.texto, font=fuente)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # Crear el patrón de marca de agua diagonal
        step_x = text_width + 100
        step_y = text_height + 100

        # Dibujar el texto repetidamente en diagonal
        for y in range(0, size_watermark[1], step_y):  # Iterar en la dirección vertical
            for x in range(0, size_watermark[0], step_x):  # Iterar en la dirección horizontal
                # Crear una imagen temporal para el texto rotado
                text_img = Image.new('RGBA', (2*text_width, 2*text_height), (255, 255, 255, 0))  # Transparente
                text_draw = ImageDraw.Draw(text_img)
                
                # Dibujar el texto en la imagen temporal
                text_draw.text((0, 0), self.texto, font=fuente, fill="black")
                
                # Rotar la imagen del texto
                text_img_rotada = text_img.rotate(35, expand=True)

                # Pegar el texto rotado en la imagen principal de marca de agua
                marca_de_agua.paste(text_img_rotada, (x, y), text_img_rotada)

        # Calcular la posición para centrar la parte de la marca de agua en la imagen original
        x_offset = (size_watermark[0] - self.image.size[0]) // 2
        y_offset = (size_watermark[1] - self.image.size[1]) // 2

        # Convertir las imágenes a 'RGB' si no lo están
        imagen_original = self.image.convert('RGB')
        imagen_marca = marca_de_agua.convert('RGBA')

        # Obtener los píxeles de ambas imágenes
        pixeles_original = imagen_original.load()
        pixeles_marca = imagen_marca.load()

        # Crear una nueva imagen donde almacenaremos el resultado
        imagen_resultante = Image.new('RGB', self.image.size)
        pixeles_resultantes = imagen_resultante.load()

        # Aplicar la fórmula para cada píxel en la parte central de la marca de agua
        for y in range(self.image.size[1]):  # Iterar sobre el alto
            for x in range(self.image.size[0]):  # Iterar sobre el ancho
                # Obtener los píxeles de la parte central de la marca de agua
                wm_x = x + x_offset
                wm_y = y + y_offset
                
                r1, g1, b1 = pixeles_original[x, y]  # Píxel de la imagen original
                r2, g2, b2, a2 = pixeles_marca[wm_x, wm_y]  # Píxel de la imagen de marca de agua

                # Solo aplicar el blend si el píxel de la marca de agua no es transparente o blanco
                if a2 > 0 and (r2, g2, b2) != (255, 255, 255):
                    # Aplicar la fórmula para cada componente de color (R, G, B)
                    r = int(r1 * self.alpha + r2 * (1 - self.alpha))
                    g = int(g1 * self.alpha + g2 * (1 - self.alpha))
                    b = int(b1 * self.alpha + b2 * (1 - self.alpha))

                    # Guardar el nuevo píxel en la imagen resultante
                    pixeles_resultantes[x, y] = (r, g, b)
                else:
                    # Si el píxel es blanco o transparente, mantener el píxel original
                    pixeles_resultantes[x, y] = (r1, g1, b1)

        return imagen_resultante
