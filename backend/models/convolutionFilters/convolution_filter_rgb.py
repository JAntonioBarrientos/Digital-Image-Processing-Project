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

# import numpy as np
# from PIL import Image
# from models.base_filter import BaseFilter

# import numpy as np
# from PIL import Image

# class ConvolutionFilterRGB(BaseFilter):
#     def replicate_borders(self, pixels, pad):
#         """
#         Replicar los bordes de la imagen de acuerdo al tamaño del kernel.
#         Se añadirá una capa de píxeles replicando los valores de los bordes.
        
#         :param pixels: Array de Numpy que representa la imagen.
#         :param pad: Tamaño del padding (la cantidad de filas/columnas a añadir).
#         :return: Imagen con bordes replicados.
#         """
#         height, width, channels = pixels.shape
#         # Crear una nueva imagen con espacio para el padding
#         padded_image = np.zeros((height + 2 * pad, width + 2 * pad, channels), dtype=pixels.dtype)

#         # Copiar la imagen original en el centro de la imagen con padding
#         padded_image[pad:pad + height, pad:pad + width] = pixels

#         # Replicar las filas superiores e inferiores
#         for i in range(pad):
#             # Replicar la fila superior
#             padded_image[i, pad:pad + width] = pixels[0, :]
#             # Replicar la fila inferior
#             padded_image[pad + height + i, pad:pad + width] = pixels[height - 1, :]

#         # Replicar las columnas izquierda y derecha
#         for j in range(pad):
#             # Replicar la columna izquierda
#             padded_image[pad:pad + height, j] = pixels[:, 0]
#             # Replicar la columna derecha
#             padded_image[pad:pad + height, pad + width + j] = pixels[:, width - 1]

#         # Replicar las esquinas
#         # Esquina superior izquierda
#         padded_image[:pad, :pad] = pixels[0, 0]
#         # Esquina superior derecha
#         padded_image[:pad, pad + width:] = pixels[0, width - 1]
#         # Esquina inferior izquierda
#         padded_image[pad + height:, :pad] = pixels[height - 1, 0]
#         # Esquina inferior derecha
#         padded_image[pad + height:, pad + width:] = pixels[height - 1, width - 1]

#         return padded_image

#     def apply_convolution(self, kernel):
#         """
#         Aplica un filtro de convolución a la imagen en los tres canales (R, G, B) utilizando el kernel proporcionado.
        
#         :param kernel: Matriz (numpy array) que representa el kernel de convolución. Sus dimensiones deben ser impares y cuadradas.
#         :return: Imagen procesada.
#         """
#         img = self.image.convert('RGB')  # Convertimos la imagen a RGB
#         pixels = np.array(img)  # Convertimos la imagen a un array de Numpy (alto, ancho, 3)
#         kernel_size = kernel.shape[0]  # Asumimos que el kernel es cuadrado (n x n)
#         pad = kernel_size // 2  # Tamaño del padding

#         # Replicar los bordes 
#         padded_image = self.replicate_borders(pixels, pad)

#         # Crear una imagen de salida con las mismas dimensiones que la imagen original
#         output_image = np.zeros_like(pixels)

#         # Realizar la convolución en los tres canales
#         for i in range(pixels.shape[0]):
#             for j in range(pixels.shape[1]):
#                 for c in range(3):  # Canales R, G, B
#                     # Extraer la región de la imagen correspondiente al tamaño del kernel
#                     region = padded_image[i:i + kernel_size, j:j + kernel_size, c]
#                     # Aplicar el kernel sobre la región y sumar los resultados
#                     output_value = np.sum(region * kernel)
#                     # Asignar el valor calculado a la imagen de salida (con clipping para mantener [0,255])
#                     output_image[i, j, c] = min(max(int(output_value), 0), 255)

#         # Convertir de nuevo a imagen PIL
#         return Image.fromarray(output_image)
