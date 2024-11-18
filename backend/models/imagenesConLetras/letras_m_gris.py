import os
from PIL import Image
import numpy as np
from io import BytesIO  # Asegúrate de importar BytesIO
import uuid

class LetrasMsGris:
    def __init__(self, image_path, grid_width, grid_height, output_html_name='imagen_en_m.html'):
        """
        Inicializa la clase LetrasMsGris.

        :param image_path: Ruta a la imagen de entrada o un objeto de archivo (BytesIO).
        :param grid_width: Ancho de cada celda de la cuadrícula en píxeles.
        :param grid_height: Alto de cada celda de la cuadrícula en píxeles.
        :param output_html_name: Nombre del archivo HTML de salida. Por defecto es 'imagen_en_m.html'.
        """
        self.image_path = image_path
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.output_html_name = output_html_name
        self.output_dir = os.path.join('data', 'imagen_con_letras')  # Nueva ruta de salida
        self.output_html_path = os.path.join(self.output_dir, self.output_html_name)
    
    def apply_filter(self):
        """
        Aplica el filtro para convertir la imagen en una representación de 'M's coloreadas
        y genera un archivo HTML con el resultado en la carpeta data/imagen_con_letras/.
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
            
            # Convertir a escala de grises 'L' si no lo está
            if image.mode != 'L':
                image = image.convert('L')
                print("Imagen convertida a escala de grises ('L').")
            else:
                print("La imagen ya está en modo de escala de grises ('L').")
            
            width, height = image.size
            print(f"Dimensiones de la imagen: {width}x{height} píxeles.")
            
            # Convertir la imagen a un arreglo NumPy
            image_array = np.array(image)
            
            # Calcular el número de celdas en las direcciones x e y
            num_cells_x = (width + self.grid_width - 1) // self.grid_width
            num_cells_y = (height + self.grid_height - 1) // self.grid_height
            print(f"Dividiendo la imagen en una cuadrícula de {num_cells_x}x{num_cells_y} celdas.")
            
            # Obtener los tonos de gris promedio para cada celda
            averages = []
            for y in range(0, height, self.grid_height):
                row = []
                for x in range(0, width, self.grid_width):
                    x_end = min(x + self.grid_width, width)
                    y_end = min(y + self.grid_height, height)
                    block = image_array[y:y_end, x:x_end]
                    average = int(np.mean(block))
                    row.append(average)
                averages.append(row)
            
            print("Cálculo de tonos de gris promedio completado.")
            
            # Generar el contenido HTML
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Imagen en M</title>
</head>
<body>
    <pre style="font: 10px/5px monospace;">
"""
            # Iterar sobre cada fila de promedios y generar líneas de 'M's coloreadas
            for row_index, row in enumerate(averages):
                line = ""
                for col_index, gray in enumerate(row):
                    # Convertir el tono de gris a formato hexadecimal
                    hex_color = f'#{gray:02x}{gray:02x}{gray:02x}'
                    # Añadir el carácter 'M' con el color correspondiente
                    line += f'<span style="color: {hex_color};">M</span>'
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
