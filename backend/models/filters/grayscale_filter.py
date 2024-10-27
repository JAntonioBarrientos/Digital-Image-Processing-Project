import numpy as np
from PIL import Image
from models.base_filter import BaseFilter  

class GrayscaleFilter(BaseFilter):
    def __init__(self, image):
        super().__init__(image)

    def apply_filter(self):
        # Convertir la imagen a formato RGB si no lo está
        img = self.image.convert('RGB')
        
        # Convertir la imagen a un arreglo NumPy
        image_array = np.array(img, dtype=np.uint8)
        
        # Calcular los valores en escala de grises utilizando el promedio
        # Usando la fórmula promedio (R + G + B) / 3
        gray_array = image_array.mean(axis=2).astype(np.uint8)
        
        # Replicar el arreglo de escala de grises en los tres canales para formar una imagen RGB
        gray_array_rgb = np.stack((gray_array,)*3, axis=-1)
        
        # Convertir el arreglo de vuelta a una imagen PIL en modo 'RGB'
        gray_image_rgb = Image.fromarray(gray_array_rgb, mode='RGB')
        
        return gray_image_rgb
