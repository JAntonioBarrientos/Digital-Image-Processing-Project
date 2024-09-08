import numpy as np
from models.convolutionFilters.convolution_filter_rgb import ConvolutionFilterRGB

class SharpenFilter(ConvolutionFilterRGB):
    def apply_filter(self):
        # Definir el kernel para afilar la imagen
        sharpen_kernel = np.array([
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ])

        # Aplicar la convolución utilizando el kernel de afilado
        self.image = self.apply_convolution(sharpen_kernel)

        return self.image
