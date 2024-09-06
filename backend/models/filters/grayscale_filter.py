from PIL import ImageOps

class GrayscaleFilter:
    def __init__(self, image):
        self.image = image

    # Método que aplica el filtro de escala de grises
    def apply_filter(self):
        return ImageOps.grayscale(self.image)
