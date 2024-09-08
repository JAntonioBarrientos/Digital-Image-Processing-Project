import numpy as np
from models.convolutionFilters.convolution_filter_rgb import ConvolutionFilterRGB

class CustomDiagonalFilter(ConvolutionFilterRGB):
    def apply_filter(self, intensity=1):
        """
        Aplica un filtro personalizado con un kernel diagonal basado en la intensidad (radio).
        :param intensity: Intensidad del filtro que determina el tamaño del kernel (radio).
        """
        # Generar el kernel basado en la intensidad
        custom_kernel = self.generate_kernel(intensity)
        
        # Aplicar la convolución utilizando el kernel generado
        self.image = self.apply_convolution(custom_kernel)

        return self.image

    def generate_kernel(self, r):
        """
        Genera un kernel diagonal en función del radio r.
        El tamaño del kernel es (2r + 1) x (2r + 1) y se normaliza.
        
        :param r: Radio del kernel.
        :return: Un kernel 2D diagonal normalizado.
        """
        # Tamaño del kernel
        n = 2 * r + 1
        
        # Crear un kernel de ceros de tamaño n x n
        kernel = np.zeros((n, n))
        
        # Llenar el kernel en la diagonal
        for i in range(n):
            kernel[i, i] = 1  # Asigna 1 en la diagonal
        
        # Normalizar el kernel: dividir cada elemento por la suma total (para que el factor sea 1.0/n)
        kernel_sum = np.sum(kernel)
        if kernel_sum > 0:
            kernel = kernel / kernel_sum
        
        return kernel
