from models.filters.grayscale_filter import GrayscaleFilter
from models.filters.gray_filter_weighted import GrayFilterWeighted
from models.filters.mica_filter import MicaFilter
from models.convolutionFilters.filters.blur_filter import BlurFilter
from models.convolutionFilters.filters.custom_diagonal_filter import CustomDiagonalFilter  
from models.convolutionFilters.filters.find_edges_filter import FindEdgesFilter
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

    # Método para aplicar el filtro de mica
    def apply_mica_filter(self, r_value, g_value, b_value):
        mica_filter = MicaFilter(self.image, r_value, g_value, b_value)
        return mica_filter.apply_filter()

    # Método para aplicar el filtro de desenfoque (Blur)
    def apply_blur_filter(self, intensity):
        blur_filter = BlurFilter(self.image)
        return blur_filter.apply_filter(intensity)

    # Método para aplicar un filtro personalizado diagonal
    def apply_custom_diagonal_filter(self, intensity):
        custom_diagonal_filter = CustomDiagonalFilter(self.image)
        return custom_diagonal_filter.apply_filter(intensity)

    # Método para aplicar el filtro de detección de bordes
    def apply_find_edges_filter(self):
        find_edges_filter = FindEdgesFilter(self.image)
        return find_edges_filter.apply_filter()
