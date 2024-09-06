from PIL import Image
from io import BytesIO

class ImageLoader:
    def __init__(self, image_file):
        self.image_file = image_file

    # Método para cargar la imagen desde el archivo
    def load_image(self):
        try:
            image = Image.open(self.image_file)  # Cargar la imagen usando PIL
            return image
        except Exception as e:
            raise ValueError("Invalid image file")
