import numpy as np
from PIL import Image
from models.base_filter import BaseFilter
from multiprocessing import Pool, cpu_count

class ConvolutionFilterRGB(BaseFilter):
    def __init__(self, image, kernel=None, num_processes=None):
        super().__init__(image)
        self.kernel = kernel
        self.num_processes = num_processes or cpu_count()

    def apply_convolution(self, kernel=None):
        kernel = kernel if kernel is not None else self.kernel
        if kernel is None:
            raise ValueError("Se requiere un kernel para aplicar la convolución.")

        # Convertir la imagen a formato RGB si no lo está
        img = self.image.convert('RGB')
        pixels = np.array(img, dtype=np.float32)

        kernel_size = kernel.shape[0]
        pad = kernel_size // 2

        # Asegurarse de que el número de procesos no exceda la altura de la imagen
        self.num_processes = min(self.num_processes, pixels.shape[0])

        # Aplicar padding a la imagen
        padded_image = np.pad(pixels, ((pad, pad), (pad, pad), (0, 0)), mode='edge')

        # Dividir la imagen en bloques para multiprocesamiento
        blocks = self._split_into_blocks(padded_image, self.num_processes, pad, kernel_size)

        # Procesar los bloques
        if len(blocks) == 1:
            # Si solo hay un bloque, procesar sin multiprocesamiento
            processed_blocks = [self._process_block((blocks[0], kernel))]
        else:
            with Pool(self.num_processes) as pool:
                processed_blocks = pool.map(self._process_block, [(block, kernel) for block in blocks])

        # Combinar los bloques procesados
        output_image = np.vstack(processed_blocks)
        output_image = np.clip(output_image, 0, 255).astype(np.uint8)
        return Image.fromarray(output_image, mode='RGB')

    def _split_into_blocks(self, array, num_blocks, pad, kernel_size):
        height = array.shape[0] - 2 * pad  # Altura original
        block_size = height // num_blocks
        blocks = []
        for i in range(num_blocks):
            start = i * block_size + pad
            end = start + block_size
            if i == num_blocks - 1:
                end = height + pad
            block = array[start - pad:end + pad, :, :]
            blocks.append(block)
        return blocks

    @staticmethod
    def _process_block(args):
        block, kernel = args
        kernel_height, kernel_width = kernel.shape
        pad_h = kernel_height // 2
        pad_w = kernel_width // 2

        # Obtener las dimensiones del bloque
        block_height, block_width, _ = block.shape

        # Calcular las dimensiones de la salida
        output_height = block_height - 2 * pad_h
        output_width = block_width - 2 * pad_w

        # Inicializar el bloque de salida
        output_block = np.zeros((output_height, output_width, 3), dtype=np.float32)

        # Realizar la convolución manualmente utilizando operaciones vectorizadas
        for c in range(3):  # Para cada canal (R, G, B)
            channel = block[:, :, c]

            # Extraer todas las regiones de interés (ROIs) de la imagen en una sola operación
            strides = (
                channel.strides[0],
                channel.strides[1],
                channel.strides[0],
                channel.strides[1]
            )
            shape = (
                output_height,
                output_width,
                kernel_height,
                kernel_width
            )
            # Crear una vista de la imagen con todas las regiones necesarias
            sub_matrices = np.lib.stride_tricks.as_strided(
                channel,
                shape=shape,
                strides=strides
            )

            # Realizar la multiplicación elemento a elemento y sumar
            output_block[:, :, c] = np.einsum('ijkl,kl->ij', sub_matrices, kernel)

        return output_block
