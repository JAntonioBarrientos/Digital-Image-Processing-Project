import numpy as np
from models.convolutionFilters.convolution_filter_rgb import ConvolutionFilterRGB  

class BlurFilter(ConvolutionFilterRGB):
    def apply_filter(self, intensity=1):
        """
        Aplica un filtro de desenfoque con un kernel generado en función de la intensidad (radio).
        :param intensity: Intensidad de desenfoque que determina el radio del kernel.
        """
        # Generar el kernel de desenfoque basado en la intensidad
        blur_kernel = self.generate_kernel(intensity)
        
        # Aplicar la convolución utilizando el kernel generado
        self.image = self.apply_convolution(blur_kernel)

        return self.image

    def generate_kernel(self, r):
        """
        Genera un kernel de desenfoque en función del radio r.
        El tamaño del kernel es (2r + 1) x (2r + 1).
        El patrón sigue la estructura descrita y el kernel se normaliza.
        
        :param r: Radio del kernel.
        :return: Un kernel 2D normalizado.
        """
        # Tamaño del kernel
        n = 2 * r + 1
        
        # Crear un kernel de ceros de tamaño n x n
        kernel = np.zeros((n, n))
        
        # Llenar el kernel siguiendo el patrón
        for i in range(n):
            for j in range(n):
                # Calcular la distancia manhattan del centro
                if abs(i - r) + abs(j - r) <= r:
                    kernel[i, j] = 1
        
        # Normalizar el kernel: dividir cada elemento por la suma total
        kernel_sum = np.sum(kernel)
        if kernel_sum > 0:
            kernel = kernel / kernel_sum
        
        return kernel

