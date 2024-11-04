import numpy as np
from PIL import Image
from models.base_filter import BaseFilter
from multiprocessing import Pool, cpu_count

class MicaFilter(BaseFilter):
    def __init__(self, image, r_value, g_value, b_value, num_processes=None):
        super().__init__(image)
        self.r_value = r_value
        self.g_value = g_value
        self.b_value = b_value
        self.num_processes = num_processes or cpu_count()

    def apply_filter(self):
        # Convertir la imagen a formato RGB si no lo está
        img = self.image.convert('RGB')

        # Convertir la imagen a un arreglo NumPy
        image_array = np.array(img, dtype=np.uint8)

        # Dividir el arreglo en bloques para multiprocessing
        blocks = self._split_into_blocks(image_array, self.num_processes)

        # Crear un pool de procesos
        with Pool(self.num_processes) as pool:
            # Preparar los argumentos para cada bloque
            args = [(block, self.r_value, self.g_value, self.b_value) for block in blocks]
            # Aplicar el filtro Mica en paralelo
            processed_blocks = pool.map(self._process_block, args)

        # Combinar los bloques procesados
        processed_array = np.vstack(processed_blocks)

        # Crear la imagen PIL directamente desde el arreglo procesado
        processed_img = Image.fromarray(processed_array, mode='RGB')

        return processed_img

    def _split_into_blocks(self, array, num_blocks):
        """
        Divide el arreglo en bloques a lo largo del eje vertical.
        """
        height = array.shape[0]
        block_size = height // num_blocks
        blocks = []
        for i in range(num_blocks):
            start = i * block_size
            # Asegurarse de que el último bloque incluya cualquier fila restante
            end = (i + 1) * block_size if i != num_blocks - 1 else height
            blocks.append(array[start:end, :, :])
        return blocks

    @staticmethod
    def _process_block(args):
        """
        Aplica el filtro Mica a un bloque de la imagen usando operaciones vectorizadas.
        """
        block, r_val, g_val, b_val = args
        # Aplicar el AND lógico con los valores proporcionados
        block[:, :, 0] &= r_val
        block[:, :, 1] &= g_val
        block[:, :, 2] &= b_val
        return block
