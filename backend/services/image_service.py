from models.filters.grayscale_filter import GrayscaleFilter
from models.filters.gray_filter_weighted import GrayFilterWeighted
from utils.image_loader import ImageLoader

class ImageService:
    def __init__(self, image_file):
        self.image_loader = ImageLoader(image_file)
        self.image = self.image_loader.load_image()

    # Método para aplicar el filtro de escala de grises
    def apply_grayscale_filter(self):
        grayscale_filter = GrayscaleFilter(self.image)
        return grayscale_filter.apply_filter()

    # Método para aplicar el filtro de escala de grises ponderado
    def apply_gray_filter_weighted(self):
        gray_filter_weighted = GrayFilterWeighted(self.image)
        return gray_filter_weighted.apply_filter()
