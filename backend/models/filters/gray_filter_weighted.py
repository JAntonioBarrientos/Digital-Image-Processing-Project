from PIL import Image

class GrayFilterWeighted:
    def __init__(self, image):
        self.image = image

    # Método que aplica el filtro de escala de grises ponderado
    def apply_filter(self):
        img = self.image.convert('RGB')  # Convertimos la imagen a RGB
        pixels = img.load()  # Cargamos los píxeles de la imagen
        
        width, height = img.size  # Obtenemos las dimensiones de la imagen
        
        # Iteramos sobre cada píxel de la imagen
        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]  # Obtenemos los valores RGB
                # Calculamos el valor ponderado según la percepción del ojo humano
                p = int(0.299 * r + 0.587 * g + 0.114 * b)
                pixels[i, j] = (p, p, p)  # Asignamos el valor en escala de grises
                
        return img  # Retornamos la imagen procesada
