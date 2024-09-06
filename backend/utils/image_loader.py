from PIL import Image

class ImageLoader:
    def __init__(self, file):
        self.file = file

    def load_image(self):
        try:
            image = Image.open(self.file)
            return image
        except Exception as e:
            raise ValueError("Invalid image file")
