# models/filters/letras_distintas_gris.py

import os
from PIL import Image
import numpy as np
from io import BytesIO
import uuid

class LetrasDistintasGris:
    def __init__(self, image_path, grid_width, grid_height, output_html_name='imagen_distintas_gris.html'):
        """
        Inicializa la clase LetrasDistintasGris.

        :param image_path: Ruta a la imagen de entrada o un objeto de archivo (BytesIO).
        :param grid_width: Ancho de cada celda de la cuadrícula en píxeles.
        :param grid_height: Alto de cada celda de la cuadrícula en píxeles.
        :param output_html_name: Nombre del archivo HTML de salida.
        """
        self.image_path = image_path
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.output_html_name = output_html_name
        self.output_dir = os.path.join('data', 'imagen_con_letras')  # Directorio único
        self.output_html_path = os.path.join(self.output_dir, self.output_html_name)
    
    def get_letra(self, promedio_gris):
        """
        Devuelve la letra correspondiente según el promedio de gris.

        :param promedio_gris: Valor promedio de gris (0-255).
        :return: Carácter asignado.
        """
        if 0 <= promedio_gris <= 15:
            return 'M'
        elif 16 <= promedio_gris <= 31:
            return 'N'
        elif 32 <= promedio_gris <= 47:
            return 'H'
        elif 48 <= promedio_gris <= 63:
            return '#'
        elif 64 <= promedio_gris <= 79:
            return 'Q'
        elif 80 <= promedio_gris <= 95:
            return 'U'
        elif 96 <= promedio_gris <= 111:
            return 'A'
        elif 112 <= promedio_gris <= 127:
            return 'D'
        elif 128 <= promedio_gris <= 143:
            return '0'
        elif 144 <= promedio_gris <= 159:
            return 'Y'
        elif 160 <= promedio_gris <= 175:
            return '2'
        elif 176 <= promedio_gris <= 191:
            return '$'
        elif 192 <= promedio_gris <= 209:
            return '%'
        elif 210 <= promedio_gris <= 225:
            return '+'
        elif 226 <= promedio_gris <= 239:
            return '.'
        elif 240 <= promedio_gris <= 255:
            return ' '
        else:
            return 'M'  # Valor por defecto
    
    def apply_filter(self):
        """
        Aplica el filtro para convertir la imagen en una representación de caracteres
        variados según el promedio de gris de cada celda y genera un archivo HTML
        con el resultado en la carpeta data/imagen_con_letras/.
        """
        try:
            # Verificar si image_path es un objeto de archivo (BytesIO) o una ruta de archivo
            if isinstance(self.image_path, (BytesIO,)):
                image = Image.open(self.image_path)
            else:
                # Verificar si el archivo de imagen existe
                if not os.path.isfile(self.image_path):
                    raise FileNotFoundError(f"La imagen especificada no existe: {self.image_path}")
                
                # Cargar la imagen
                image = Image.open(self.image_path)
                print(f"Imagen cargada: {self.image_path} (Tamaño: {image.size}, Modo: {image.mode})")
            
            # Convertir a escala de grises si no lo está
            if image.mode != 'L':
                image = image.convert('L')
                print("Imagen convertida a escala de grises.")
            else:
                print("La imagen ya está en escala de grises.")
            
            width, height = image.size
            print(f"Dimensiones de la imagen: {width}x{height} píxeles.")
            
            # Convertir la imagen a un arreglo NumPy
            image_array = np.array(image)
            
            # Calcular el número de celdas en las direcciones x e y
            num_cells_x = (width + self.grid_width - 1) // self.grid_width
            num_cells_y = (height + self.grid_height - 1) // self.grid_height
            print(f"Dividiendo la imagen en una cuadrícula de {num_cells_x}x{num_cells_y} celdas.")
            
            # Obtener los promedios de gris para cada celda
            averages = []
            for y in range(0, height, self.grid_height):
                row = []
                for x in range(0, width, self.grid_width):
                    x_end = min(x + self.grid_width, width)
                    y_end = min(y + self.grid_height, height)
                    block = image_array[y:y_end, x:x_end]
                    promedio_gris = int(np.mean(block))
                    row.append(promedio_gris)
                averages.append(row)
            
            print("Cálculo de promedios de gris completado.")
            
            # Generar el contenido HTML
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Imagen con Letras Distintas en Gris</title>
</head>
<body>
    <pre style="font: 10px/5px monospace;">
"""
            # Iterar sobre cada fila de promedios y generar líneas de caracteres
            for row_index, row in enumerate(averages):
                line = ""
                for col_index, promedio_gris in enumerate(row):
                    letra = self.get_letra(promedio_gris)
                    line += letra
                # Añadir la línea al contenido HTML
                html_content += line + "\n"
                if (row_index + 1) % 10 == 0:
                    print(f"Procesadas {row_index + 1} de {len(averages)} filas.")
            
            # Cerrar las etiquetas HTML
            html_content += """
    </pre>
</body>
</html>
"""
            print("Generación de contenido HTML completada.")
            
            # Asegurar que el directorio de salida exista
            os.makedirs(self.output_dir, exist_ok=True)
            print(f"Directorio de salida verificado/creado: {self.output_dir}")
            
            # Escribir el contenido HTML en el archivo de salida
            with open(self.output_html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Archivo HTML generado exitosamente en: {self.output_html_path}")
        
        except Exception as e:
            print(f"Ocurrió un error durante el procesamiento: {e}")
            raise e  # Re-levantar la excepción para que el controlador pueda manejarla
