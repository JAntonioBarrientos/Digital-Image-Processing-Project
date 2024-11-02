import numpy as np
from PIL import Image
from models.base_filter import BaseFilter
from multiprocessing import Pool, cpu_count

class GrayscaleFilter(BaseFilter):
    def __init__(self, image, num_processes=None):
        super().__init__(image)
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
            # Aplicar la conversión a escala de grises en paralelo
            gray_blocks = pool.map(self._process_block, blocks)
        
        # Combinar los bloques procesados
        gray_array = np.vstack(gray_blocks)  # Forma: (altura_total, ancho, 3)
        
        # **Eliminar la siguiente línea redundante:**
        # gray_array_rgb = np.repeat(gray_array[:, :, np.newaxis], 3, axis=2)
        
        # **Usar directamente gray_array para crear la imagen PIL**
        gray_image_rgb = Image.fromarray(gray_array, mode='RGB')
        
        return gray_image_rgb
    
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
    def _process_block(block):
        """
        Convierte un bloque de la imagen a escala de grises usando el promedio simple.
        """
        # Calcular el promedio de los canales R, G y B
        gray = block.mean(axis=2).astype(np.uint8)  # Forma: (bloque_altura, ancho)
        # Expandir las dimensiones para tener tres canales
        gray = np.expand_dims(gray, axis=2)        # Forma: (bloque_altura, ancho, 1)
        # Replicar el arreglo en los tres canales
        gray_rgb = np.repeat(gray, 3, axis=2)      # Forma: (bloque_altura, ancho, 3)
        return gray_rgb
