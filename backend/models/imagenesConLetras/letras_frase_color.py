# models/filters/letras_frase_color.py

import os
from PIL import Image
import numpy as np
from io import BytesIO
import uuid

class LetrasFraseColor:
    def __init__(self, image_path, grid_width, grid_height, phrase, output_html_name='imagen_frase_color.html'):
        """
        Inicializa la clase LetrasFraseColor.

        :param image_path: Ruta a la imagen de entrada o un objeto de archivo (BytesIO).
        :param grid_width: Ancho de cada celda de la cuadrícula en píxeles.
        :param grid_height: Alto de cada celda de la cuadrícula en píxeles.
        :param phrase: Frase a utilizar para asignar caracteres.
        :param output_html_name: Nombre del archivo HTML de salida.
        """
        self.image_path = image_path
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.phrase = phrase
        self.output_html_name = output_html_name
        self.output_dir = os.path.join('data', 'imagen_con_letras')  # Directorio único
        self.output_html_path = os.path.join(self.output_dir, self.output_html_name)
        self.phrase_length = len(self.phrase)
        self.current_char_index = 0  # Índice para iterar sobre la frase
    
    def get_next_letra(self):
        """
        Devuelve el siguiente carácter de la frase, repitiendo si es necesario.

        :return: Carácter asignado.
        """
        letra = self.phrase[self.current_char_index]
        self.current_char_index = (self.current_char_index + 1) % self.phrase_length
        return letra
    
    def apply_filter(self):
        """
        Aplica el filtro para convertir la imagen en una representación de caracteres
        basados en una frase proporcionada y pinta cada carácter con un color basado en el promedio RGB.
        Genera un archivo HTML con el resultado en la carpeta data/imagen_con_letras/.
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
            
            # Convertir a RGB si no lo está
            if image.mode != 'RGB':
                image = image.convert('RGB')
                print("Imagen convertida a RGB.")
            else:
                print("La imagen ya está en modo RGB.")
            
            width, height = image.size
            print(f"Dimensiones de la imagen: {width}x{height} píxeles.")
            
            # Convertir la imagen a arreglos NumPy
            image_array = np.array(image)
            
            # Calcular el número de celdas en las direcciones x e y
            num_cells_x = (width + self.grid_width - 1) // self.grid_width
            num_cells_y = (height + self.grid_height - 1) // self.grid_height
            print(f"Dividiendo la imagen en una cuadrícula de {num_cells_x}x{num_cells_y} celdas.")
            
            # Obtener los promedios RGB para cada celda
            averages_rgb = []
            for y in range(0, height, self.grid_height):
                row_rgb = []
                for x in range(0, width, self.grid_width):
                    x_end = min(x + self.grid_width, width)
                    y_end = min(y + self.grid_height, height)
                    
                    # Bloque RGB
                    block_rgb = image_array[y:y_end, x:x_end, :]
                    promedio_rgb = tuple(int(np.mean(block_rgb[:, :, channel])) for channel in range(3))  # (R, G, B)
                    row_rgb.append(promedio_rgb)
                averages_rgb.append(row_rgb)
            
            print("Cálculo de promedios RGB completado.")
            
            # Generar el contenido HTML
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Imagen con Frase y Color</title>
</head>
<body>
    <pre style="font: 10px/10px monospace;">
"""
            # Iterar sobre cada fila de promedios y generar líneas de caracteres con color
            for row_index, row_rgb in enumerate(averages_rgb):
                line = ""
                for col_index, promedio_rgb in enumerate(row_rgb):
                    letra = self.get_next_letra()
                    # Convertir el promedio RGB a un color hexadecimal
                    hex_color = f'#{promedio_rgb[0]:02x}{promedio_rgb[1]:02x}{promedio_rgb[2]:02x}'
                    line += f'<span style="color: {hex_color};">{letra}</span>'
                # Añadir la línea al contenido HTML
                html_content += line + "\n"
                if (row_index + 1) % 10 == 0:
                    print(f"Procesadas {row_index + 1} de {len(averages_rgb)} filas.")
            
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
