import numpy as np
from models.convolutionFilters.convolution_filter_rgb import ConvolutionFilterRGB

class MeanFilter(ConvolutionFilterRGB):
    def apply_filter(self):
        # Definir un kernel de 7x7 lleno de unos
        kernel_size = 7
        mean_kernel = np.ones((kernel_size, kernel_size), dtype=np.float32)

        # Normalizar el kernel dividiendo por el número total de elementos (49 en este caso)
        mean_kernel /= kernel_size * kernel_size

        # Aplicar la convolución utilizando el kernel de promedio
        smoothed_image = self.apply_convolution(mean_kernel)

        return smoothed_image
