import numpy as np
from models.convolutionFilters.convolution_filter_rgb import ConvolutionFilterRGB

class FindEdgesFilter(ConvolutionFilterRGB):
    def apply_filter(self):
        # Definir el kernel para detectar bordes
        find_edges_kernel = np.array([
            [-1, -1, -1],
            [-1,  8, -1],
            [-1, -1, -1]
        ])

        # Aplicar la convolución utilizando el kernel de detección de bordes
        self.image = self.apply_convolution(find_edges_kernel)

        return self.image
