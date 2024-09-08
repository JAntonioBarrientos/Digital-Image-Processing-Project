from abc import ABC, abstractmethod
from PIL import Image

class BaseFilter(ABC):
    def __init__(self, image):
        """
        Inicializa el filtro con una imagen.
        
        :param image: Objeto de imagen (PIL Image).
        """
        if not isinstance(image, Image.Image):
            raise ValueError("El objeto proporcionado no es una imagen válida.")
        self.image = image

    @abstractmethod
    def apply_filter(self):
        """
        Método abstracto que debe ser implementado por las subclases.
        Debe aplicar el filtro a la imagen y devolver la imagen procesada.
        """
        pass
