# Tarea 9
Implementación del filtro de imagenes con letras que incluye las siguientes variantes:
- Imagenes con letra M en escala de grises
- Imagenes con letra M en color
- Imagenes con las letras "MNH#QUAD0Y2$%+. " en escala de grises
- Imagenes con las letras "MNH#QUAD0Y2$%+. " en color
- Imagenes con frase proporcionada por el usuario en escala de grises
- Imagenes con frase proporcionada por el usuario en color

## Imagenes con letra M
### Algoritmo utilizado

El algoritmo utilizado en ambas implementaciones (`LetrasMColor` y `LetrasMsGris`) sigue los siguientes pasos:

1. **División de la Imagen en una Cuadrícula:**
   - La imagen de entrada se divide en una cuadrícula compuesta por celdas de dimensiones especificadas (`grid_width` y `grid_height`).
   
2. **Cálculo del Promedio de Colores:**
   - Para cada celda de la cuadrícula, se calcula el color promedio:
     - En `LetrasMColor`, se obtiene el promedio de los canales RGB.
     - En `LetrasMsGris`, se calcula el promedio de los tonos de gris.
   
3. **Representación con Letras:**
   - Se genera una representación de la imagen utilizando el carácter 'M':
     - Cada 'M' se colorea de acuerdo con el color promedio calculado para su respectiva celda.
     - En el caso de imágenes en escala de grises, las 'M's reflejarán los tonos de gris promedio.
   
4. **Generación del Archivo HTML:**
   - Se crea un archivo HTML que contiene las 'M's coloreadas, estructuradas de manera que reproduzcan la cuadrícula original de la imagen.
   - Este archivo permite visualizar la representación estilizada de la imagen mediante letras.


### Implementación en Python

El código se puede consultar en los siguientes archivos:

- [backend/models/imagenesConLetras/letras_m_gris.py](../backend/models/imagenesConLetras/letras_m_gris.py)
- [backend/models/imagenesConLetras/letras_m_color.py](../backend/models/imagenesConLetras/letras_m_color.py)



## Imagenes con letras "MNH#QUAD0Y2$%+. "
Ambos archivos, `letras_distintas_color.py` y `letras_distintas_gris.py`, implementan un algoritmo para convertir una imagen en una representación de caracteres ASCII. 

### Algoritmo Común para `letras_distintas_color.py` y `letras_distintas_gris.py`

1. **Inicialización de la Clase**:
   - Se inicializa la clase con la ruta de la imagen, el tamaño de la cuadrícula (ancho y alto de cada celda en píxeles), y el nombre del archivo HTML de salida.

2. **División en Celdas**:
   - Se calcula el número de celdas en las direcciones x e y, basándose en el tamaño de la imagen y el tamaño de la cuadrícula.

3. **Cálculo de Promedios**:
   - Se divide la imagen en bloques (celdas) según el tamaño de la cuadrícula.
   - Para cada celda, se calcula el promedio de gris:
     - En `letras_distintas_color.py`, también se calcula el promedio RGB para cada celda.

4. **Asignación de Caracteres**:
   - Se asigna un carácter a cada celda basado en el promedio de gris utilizando la función `get_letra`.
    - Para obtener la letra correspondiente se hace apartir de la siguiente lista de caracteres "MNH#QUAD0Y2$%+. ". Donde la letra M es la que representa el color mas oscuro y el espacio el color mas claro.

5. **Generación del Contenido HTML**:
   - Se genera el contenido HTML que representa la imagen utilizando caracteres ASCII.
   - En `letras_distintas_color.py`, los caracteres también se colorean según el promedio RGB de cada celda.


### Implementación en Python

El código se puede consultar en los siguientes archivos:

- [backend/models/imagenesConLetras/letras_distintas_gris.py](../backend/models/imagenesConLetras/letras_distintas_gris.py)

- [backend/models/imagenesConLetras/letras_distintas_color.py](../backend/models/imagenesConLetras/letras_distintas_color.py)




## Imagenes con frase proporcionada por el usuario
Ambos archivos, `letras_frase_color.py` y `letras_frase_gris.py`, implementan un algoritmo para convertir una imagen en una representación de caracteres ASCII utilizando una frase proporcionada por el usuario. 

### Algoritmo Común para `letras_frase_color.py` y `letras_frase_gris.py`

1. **Inicialización de la Clase**:
   - Se inicializa la clase con la ruta de la imagen, el tamaño de la cuadrícula (ancho y alto de cada celda en píxeles), la frase a utilizar para asignar caracteres, y el nombre del archivo HTML de salida.

2. **Carga de la Imagen**:
   - Se verifica si la imagen es un objeto de archivo (`BytesIO`) o una ruta de archivo.
   - Se carga la imagen utilizando la biblioteca PIL (Python Imaging Library).

3. **Conversión de la Imagen**:
   - En `letras_frase_color.py`, la imagen se convierte a modo RGB si no lo está.
   - En `letras_frase_gris.py`, la imagen se convierte a escala de grises si no lo está.

4. **División en Celdas**:
   - Se calcula el número de celdas en las direcciones x e y, basándose en el tamaño de la imagen y el tamaño de la cuadrícula.

5. **Cálculo de Promedios**:
   - Se divide la imagen en bloques (celdas) según el tamaño de la cuadrícula.
   - Para cada celda, se calcula el promedio de gris:
     - En `letras_frase_color.py`, se calcula el promedio RGB para cada celda.
     - En `letras_frase_gris.py`, se calcula el promedio de gris para cada celda.

6. **Asignación de Caracteres**:
   - Se asigna un carácter de la frase a cada celda de manera cíclica utilizando la función `get_next_letra`.

7. **Generación del Contenido HTML**:
   - Se genera el contenido HTML que representa la imagen utilizando caracteres de la frase proporcionada.
   - En `letras_frase_color.py`, los caracteres también se colorean según el promedio RGB de cada celda.
   - En `letras_frase_gris.py`, los caracteres se colorean en escala de grises según el promedio de gris de cada celda.

8. **Escritura del Archivo HTML**:
   - Se asegura que el directorio de salida exista.
   - Se escribe el contenido HTML en el archivo de salida.

### Implementación en Python

El código se puede consultar en los siguientes archivos:

- [backend/models/imagenesConLetras/letras_frase_gris.py](../backend/models/imagenesConLetras/letras_frase_gris.py)
- [backend/models/imagenesConLetras/letras_frase_color.py](../backend/models/imagenesConLetras/letras_frase_color.py)