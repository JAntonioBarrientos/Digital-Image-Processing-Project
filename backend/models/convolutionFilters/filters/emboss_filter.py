import numpy as np
from models.convolutionFilters.convolution_filter_rgb import ConvolutionFilterRGB
from PIL import Image

class EmbossFilter(ConvolutionFilterRGB):
    def apply_filter(self):
        # Definir el kernel para el filtro de emboss
        emboss_kernel = np.array([
            [-1, -1,  0],
            [-1,  0,  1],
            [ 0,  1,  1]
        ])

        # Definir el bias para el efecto de relieve
        bias = 128.0

        # Aplicar la convolución utilizando el kernel de emboss
        # y agregar el bias a cada valor resultante
        embossed_image = self.apply_convolution(emboss_kernel)

        # Convertir la imagen a numpy array y agregar el bias
        embossed_image = np.array(embossed_image) + bias
        embossed_image = np.clip(embossed_image, 0, 255)  # Asegurar que los valores están en el rango [0, 255]
        
        return Image.fromarray(embossed_image.astype(np.uint8))
