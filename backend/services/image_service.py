from models.filters.tarea1_filters import GrayPromedio, EfectoMicaRGB

class ImageService:
    def __init__(self, image):
        self.image = image

    def process_image(self, filter_name):
        if filter_name == 'gray_promedio':
            filter = GrayPromedio(self.image)
        elif filter_name == 'mica_rgb':
            filter = EfectoMicaRGB(self.image)
        # Aplicar el filtro
        return filter.apply_filter()
