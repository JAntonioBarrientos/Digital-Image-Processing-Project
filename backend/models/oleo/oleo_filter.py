import numpy as np
from PIL import Image
from numba import njit, prange
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter
from models.convolutionFilters.filters.blur_filter import BlurFilter
from numpy.lib.stride_tricks import sliding_window_view

class OleoFilter(BaseFilter):
    def apply_filter(self, color, blur, block_size):
        """
        Aplica el filtro que establece el color más frecuente en cada bloque de block_size x block_size píxeles
        en el píxel objetivo (esquina superior izquierda del bloque).
        """
        if not color:
            grayscale_filter = GrayscaleFilter(self.image)
            self.image = grayscale_filter.apply_filter()
        
        # Convertir la imagen a un arreglo NumPy
        image_array = np.array(self.image, dtype=np.uint8)
        height, width = image_array.shape[:2]

        # Convertir los colores RGB a un solo entero para facilitar el conteo
        colors = (image_array[:, :, 0].astype(np.int32) << 16) + \
                 (image_array[:, :, 1].astype(np.int32) << 8) + \
                  image_array[:, :, 2].astype(np.int32)

        # Padding para manejar los bordes
        padded_colors = np.pad(colors, ((0, block_size - 1), (0, block_size - 1)), mode='edge')

        # Crear una vista deslizante de bloques superpuestos
        blocks = sliding_window_view(padded_colors, (block_size, block_size))
        blocks = blocks.reshape(-1, block_size * block_size)

        # Función JIT optimizada para encontrar el color más común en cada bloque de forma eficiente.
        @njit(parallel=True)
        def compute_most_common_colors(blocks):
            n_blocks = blocks.shape[0]
            most_common_colors = np.empty(n_blocks, dtype=np.int32)
            for i in prange(n_blocks):
                block = blocks[i]
                # Ordenar el bloque
                sorted_block = np.sort(block)
                max_count = 1
                current_count = 1
                max_value = sorted_block[0]
                current_value = sorted_block[0]
                for j in range(1, block.size):
                    if sorted_block[j] == current_value:
                        current_count += 1
                    else:
                        if current_count > max_count:
                            max_count = current_count
                            max_value = current_value
                        current_value = sorted_block[j]
                        current_count = 1
                # Verificar al final del bloque
                if current_count > max_count:
                    max_value = current_value
                most_common_colors[i] = max_value
            return most_common_colors

        # Calcular el color más común para cada bloque
        most_common_colors = compute_most_common_colors(blocks)
        most_common_colors = most_common_colors.reshape(height, width)

        # Reconstruir la imagen a partir de los colores
        r = ((most_common_colors >> 16) & 0xFF).astype(np.uint8)
        g = ((most_common_colors >> 8) & 0xFF).astype(np.uint8)
        b = (most_common_colors & 0xFF).astype(np.uint8)
        output_array = np.stack((r, g, b), axis=-1)

        # Convertir el arreglo NumPy de vuelta a una imagen PIL
        processed_image = Image.fromarray(output_array, mode='RGB')

        if blur:
            blur_filter = BlurFilter(processed_image)
            processed_image = blur_filter.apply_filter(2)

        return processed_image
