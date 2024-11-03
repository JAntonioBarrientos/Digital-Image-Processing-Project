from models.filters.grayscale_filter import GrayscaleFilter
from models.filters.gray_filter_weighted import GrayFilterWeighted
from models.filters.mica_filter import MicaFilter
from models.convolutionFilters.filters.blur_filter import BlurFilter
from models.convolutionFilters.filters.custom_diagonal_filter import CustomDiagonalFilter  
from models.convolutionFilters.filters.find_edges_filter import FindEdgesFilter
from models.convolutionFilters.filters.sharpen_filter import SharpenFilter
from models.convolutionFilters.filters.emboss_filter import EmbossFilter
from models.convolutionFilters.filters.mean_filter import MeanFilter
from utils.image_loader import ImageLoader
from models.recursiveImage.recursive_images_gray import RecursiveImagesGray
from models.recursiveImage.recursive_images_color import RecursiveImagesColor
from models.watermark.water_mark_filter import WatermarkFilter
from models.watermark.water_mark_filter_diagonal import WatermarkFilterDiagonal
from models.dithering.halftones_filter import HalftonesFilter
from models.dithering.random_dithering_filter import RandomDitheringFilter
from models.dithering.clustered_dithering import ClusteredDitheringFilter
from models.dithering.dispersed_dithering import DispersedDitheringFilter
from models.dithering.floyd_steinberg import FloydSteinbergDitheringFilter
from models.oleo.oleo_filter import OleoFilter
from models.erosion.min_max import MinMaxKernelFilter
from models.mosaico.mosaic_filter import MosaicFilter

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

    # Método para aplicar el filtro de sharpen
    def apply_sharpen_filter(self):
        sharpen_filter = SharpenFilter(self.image)
        return sharpen_filter.apply_filter()

    # Método para aplicar el filtro de emboss
    def apply_emboss_filter(self):
        emboss_filter = EmbossFilter(self.image)
        return emboss_filter.apply_filter()
    
    # Método para aplicar el filtro de media
    def apply_mean_filter(self):
        mean_filter = MeanFilter(self.image)
        return mean_filter.apply_filter()

    # Método para aplicar el filtro de imágenes recursivas en escala de grises
    def apply_recursive_gray_filter(self, n_variantes, upscale_factor, grid_rows, grid_cols):
        # Lógica para aplicar el filtro con los nuevos parámetros
        recursive_filter = RecursiveImagesGray(
            self.image, n_variantes, upscale_factor, grid_rows, grid_cols
        )
        return recursive_filter.apply_filter()

    # Método para aplicar el filtro de imágenes recursivas en color
    def apply_recursive_color_filter(self, upscale_factor, grid_rows, grid_cols):
        recursive_image = RecursiveImagesColor(self.image, upscale_factor, grid_rows, grid_cols)
        return recursive_image.apply_filter()

    # Método para aplicar el filtro de marca de agua
    def apply_watermark_filter(self, texto, coordenadas, alpha, tamaño_fuente):
        watermark_filter = WatermarkFilter(self.image, texto, coordenadas, alpha, tamaño_fuente)
        return watermark_filter.apply_filter()

    # Método para aplicar el filtro de marca de agua diagonal
    def apply_watermark_diagonal_filter(self, texto, alpha, tamaño_fuente):
        watermark_filter_diagonal = WatermarkFilterDiagonal(self.image, texto, alpha, tamaño_fuente)
        return watermark_filter_diagonal.apply_filter()

    # Método para aplicar el filtro de dithering
    def apply_halftones_filter(self, num_variaciones, full_resolution):
        halftones_filter = HalftonesFilter(self.image, num_variaciones, full_resolution)
        return halftones_filter.apply_filter()

    def apply_random_dithering_filter(self):
        random_dithering_filter = RandomDitheringFilter(self.image)
        return random_dithering_filter.apply_filter()

    def apply_clustered_dithering_filter(self):
        clustered_dithering_filter = ClusteredDitheringFilter(self.image)
        return clustered_dithering_filter.apply_filter()

    def apply_dispersed_dithering_filter(self):
        dispersed_dithering_filter = DispersedDitheringFilter(self.image)
        return dispersed_dithering_filter.apply_filter()

    def apply_floyd_steinberg_dithering_filter(self):
        floyd_steinberg_dithering_filter = FloydSteinbergDitheringFilter(self.image)
        return floyd_steinberg_dithering_filter.apply_filter()

    def apply_oleo_filter(self, color, blur, block_size):
        oleo_filter = OleoFilter(self.image)
        return oleo_filter.apply_filter(color, blur, block_size)
    
    def apply_min_max_filter(self, radius, mode):
        min_max_filter = MinMaxKernelFilter(self.image)
        return min_max_filter.apply_filter(radius, mode)


    def apply_mosaic_filter(self, block_width, block_height, upscale_factor):
        mosaic_filter = MosaicFilter(self.image)
        return mosaic_filter.apply_filter(block_width, block_height, upscale_factor)


