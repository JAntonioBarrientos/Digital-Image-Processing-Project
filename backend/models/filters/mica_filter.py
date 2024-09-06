from PIL import Image

class MicaFilter:
    def __init__(self, image, r_value, g_value, b_value):
        self.image = image
        self.r_value = r_value
        self.g_value = g_value
        self.b_value = b_value

    # Método que aplica el filtro de mica (AND lógico con los valores RGB)
    def apply_filter(self):
        img = self.image.convert('RGB')  # Convertimos la imagen a RGB
        pixels = img.load()  # Cargamos los píxeles de la imagen
        
        width, height = img.size  # Obtenemos las dimensiones de la imagen
        
        # Iteramos sobre cada píxel de la imagen
        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]  # Obtenemos los valores RGB
                # AND lógico con los valores proporcionados por el usuario
                new_r = r & self.r_value
                new_g = g & self.g_value
                new_b = b & self.b_value
                pixels[i, j] = (new_r, new_g, new_b)  # Asignamos el nuevo valor de píxel
        
        return img  # Retornamos la imagen procesada
