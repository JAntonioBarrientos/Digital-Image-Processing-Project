from PIL import Image
from models.base_filter import BaseFilter  

class GrayscaleFilter(BaseFilter):
    def __init__(self, image):
        # Llamar al constructor de la clase base
        super().__init__(image)

    # Método que aplica el filtro de escala de grises de manera manual
    def apply_filter(self):
        # Convertir la imagen a formato RGB si no lo está
        img = self.image.convert('RGB')
        pixels = img.load()  # Cargar los píxeles de la imagen
        
        width, height = img.size  # Obtener las dimensiones de la imagen
        
        # Iterar sobre cada píxel
        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]  # Obtener los valores RGB del píxel
                p = (r + g + b) // 3  # Promediar los valores RGB para obtener escala de grises
                pixels[i, j] = (p, p, p)  # Asignar el nuevo valor de píxel en escala de grises

        return img  # Retornar la imagen procesada
