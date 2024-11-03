# Tarea 4
Filtros incluidos en Tarea 4:

- Creación de marcas de agua
- Creación de marcas de agua con patrones diagonales
- Eliminación de marcas de agua de color rojo


## Creación de marcas de agua   

### Descripción:

El filtro de creación de marcas de agua aplica un efecto de superposición del texto de la marca de agua sobre la imagen original, utilizando un nivel de transparencia para integrar la información visual de manera sutil y legible. Este efecto es útil para agregar marcas de agua personalizadas a las imágenes, que pueden ser utilizadas para identificación, protección de derechos de autor o branding.

### Pseudocódigo del algoritmo:

```python
# Inicializar Watermark con los parámetros:
imagen_original = ...  # Cargar imagen original
texto = ...  # Texto de la marca de agua
coordenadas = ...  # Coordenadas de la marca de agua
transparencia = ...  # Nivel de transparencia

# Fusionar pixeles de la siguiente manera:
for x in range(imagen_original.width):
    for y in range(imagen_original.height):
        # Obtener el color del pixel original
        color_original = imagen_original.getpixel((x, y))
        
        # Obtener el color del pixel de la marca de agua
        color_marca_agua = obtener_color_marca_agua(texto, coordenadas, x, y)
        
        # Fusionar los colores de los pixeles
        R, G, B = fusionar_colores(color_original, color_marca_agua, transparencia)
```

Para fusionar los colores de los pixeles, se utiliza la siguiente función:

```python
def fusionar_colores(color_original, color_marca_agua, transparencia):
    # Desempaquetar los componentes de color
    R_original, G_original, B_original = color_original
    R_marca_agua, G_marca_agua, B_marca_agua = color_marca_agua
    
    # Calcular los componentes de color fusionados
    R_fusionado = (1 - transparencia) * R_original + transparencia * R_marca_agua
    G_fusionado = (1 - transparencia) * G_original + transparencia * G_marca_agua
    B_fusionado = (1 - transparencia) * B_original + transparencia * B_marca_agua

    return R_fusionado, G_fusionado, B_fusionado
```

### Implementación en Python:

El código de implementación del filtro de creación de marcas de agua se encuentra en:

- [backend/models/watermark/water_mark_filter.py](../backend/models/watermark/water_mark_filter.py)


## Creación de marcas de agua con patrones diagonales

### Descripción:

El filtro de creación de marcas de agua con patrones diagonales aplica un efecto de superposición del texto de la marca de agua sobre la imagen original, utilizando un patrón de líneas diagonales para resaltar y proteger la información visual. Este efecto es útil para agregar marcas de agua discretas y estéticamente agradables a las imágenes, que pueden ser utilizadas para identificación, protección de derechos de autor o branding.


### Pseudocódigo del algoritmo:

```
# Inicialización:
    - Crear una imagen de marca de agua del doble del tamaño de la imagen original.
    - Definir la fuente del texto para la marca de agua.

# Crear patrón de marca de agua diagonal:
    - Calcular los pasos en x e y para la superposición del texto.
    - Para cada posición (x, y) en la imagen de marca de agua:
        - Crear una imagen temporal para el texto rotado.
        - Dibujar el texto en la imagen temporal.
        - Rotar la imagen del texto.
        - Pegar el texto rotado en la posición correspondiente de la imagen de marca de agua.

# Composición de la marca de agua con la imagen original:
    - Calcular el desplazamiento para centrar la marca de agua en la imagen original.
    - Convertir ambas imágenes a arreglos de píxeles.
    - Crear una nueva imagen para el resultado.
    - Para cada píxel de la imagen original:
        - Obtener el píxel correspondiente de la marca de agua.
        - Si el píxel de la marca de agua no es transparente o blanco:
            - Combinar los componentes RGB del píxel original y del píxel de la marca de agua utilizando el valor alpha.
        - De lo contrario:
            - Mantener el píxel original.
        - Asignar el píxel resultante a la imagen resultante.

# Finalización:
    - Retornar la imagen resultante con la marca de agua aplicada.
```

### Implementación en python

El código de implementación del filtro de creación de marcas de agua con patrones diagonales se encuentra en:

- [backend/models/watermark/water_mark_filter_diagonal.py](../backend/models/watermark/water_mark_filter_diagonal.py)


## Eliminación de marcas de agua de color rojo

### Descripción:

El filtro de eliminación de marcas de agua de color rojo detecta y elimina las marcas de agua de color rojo presentes en una imagen.

### Pseudocódigo del algoritmo:

### a. Conversión de la Imagen a Formatos Adecuados

#### Carga y Conversión de la Imagen

- **Entrada:**  
  Imagen en formato PIL Image.

- **Proceso:**  
  1. Convierte la imagen de PIL a un arreglo NumPy en formato RGB.  
  2. Luego, convierte este arreglo de RGB a BGR porque OpenCV maneja las imágenes en formato BGR.

- **Salida:**  
  Arreglo NumPy de la imagen en formato BGR.

### b. Detección del Color Rojo en la Imagen

#### Conversión de BGR a HSV

- **Entrada:**  
  Imagen en formato BGR.

- **Proceso:**  
  Utiliza una función personalizada (`bgr_to_hsv`) para convertir la imagen de BGR a HSV (Hue, Saturation, Value).

- **Salida:**  
  Arreglo NumPy de la imagen en formato HSV.

#### Definición de Rangos de Color Rojo

- **Proceso:**  
  Define dos rangos en el espacio HSV para capturar todas las tonalidades de rojo:
  1. **Rango 1:** Hue entre 0 y 15, Saturation y Value elevados.
  2. **Rango 2:** Hue entre 165 y 180, Saturation y Value elevados.

  **Objetivo:**  
  Capturar completamente las áreas rojas de la imagen, ya que el rojo en HSV se distribuye en dos segmentos.

#### Creación de Máscaras para Detectar Rojo

- **Proceso:**  
  1. Crea dos máscaras binarias utilizando `cv2.inRange` para cada uno de los rangos de rojo definidos.  
  2. Combina ambas máscaras para obtener una máscara final que resalte todas las áreas rojas.

- **Salida:**  
  Máscara binaria donde los píxeles rojos son blancos (255) y el resto es negro (0).

### c. Preprocesamiento de la Máscara

#### Ajuste de la Máscara según Sensibilidad

- **Proceso:**  
  Aplica un umbral a la máscara para controlar la sensibilidad de detección de rojo.  
  - Un valor de sensibilidad más bajo detecta más tonos de rojo.  
  - Un valor más alto es más restrictivo.

- **Salida:**  
  Máscara binaria ajustada según la sensibilidad.

#### Dilación de la Máscara

- **Proceso:**  
  Aplica una dilatación a la máscara utilizando un kernel de 3x3.

  **Objetivo:**  
  Expandir las áreas blancas en la máscara para asegurar que las marcas de agua rojas sean completamente cubiertas y no queden bordes finos sin procesar.

- **Salida:**  
  Máscara binaria dilatada.

### d. Inpainting para Rellenar las Áreas Rojas Detectadas

#### Aplicación del Inpainting Iterativo

- **Proceso:**  
  Utiliza la función personalizada `inpaint_iterative` para rellenar las áreas rojas detectadas en la imagen.  
  **Iteraciones:** Se ejecuta múltiples veces (según el parámetro `iterations`) para mejorar la eliminación de restos rojos persistentes.

- **Salida:**  
  Imagen procesada con las áreas rojas rellenadas.

### e. Conversión Final y Retorno de la Imagen Procesada

#### Conversión de BGR a RGB y a PIL Image

- **Proceso:**  
  1. Convierte la imagen resultante de BGR a RGB.  
  2. Luego, convierte el arreglo NumPy de vuelta a una imagen PIL Image.

- **Salida:**  
  Imagen final sin la marca de agua roja, lista para ser mostrada o guardada.


### b. Función bgr_to_hsv

### Normalización de Valores

Convierte los valores de píxeles de BGR de rango [0, 255] a [0, 1] para facilitar los cálculos.

### Cálculo de Cmax, Cmin y Delta

- **Cmax**: Máximo valor entre R, G y B para cada píxel.
- **Cmin**: Mínimo valor entre R, G y B para cada píxel.
- **Delta**: Diferencia entre Cmax y Cmin.

### Cálculo de Hue (H)

Hue representa el tono de color.
Se calcula de manera diferente dependiendo de cuál de los componentes (R, G, B) es el máximo.
El resultado se escala de [0, 360] a [0, 180] para coincidir con la escala utilizada por OpenCV.

### Cálculo de Saturation (S)

Saturation representa la pureza del color.
Se calcula como Delta / Cmax, escalado a [0, 255].

### Cálculo de Value (V)

Value representa la luminosidad.
Directamente se asigna el valor de Cmax, escalado a [0, 255].

### Combinación de Canales

Se combinan los tres canales H, S y V en una sola imagen HSV.


### Función inpaint_iterative

Esta es una implementación personalizada de inpainting que rellena píxeles enmascarados utilizando el promedio de sus vecinos.

### Preparación Inicial

- **Copia de la Imagen:** Se crea una copia de la imagen original para no modificarla directamente.
- **Máscara Booleana:** Convierte la máscara binaria a una máscara booleana donde `True` indica los píxeles que deben ser rellenados.

### Definición del Kernel de Vecinos

Un kernel de 3x3 que representa los 8 píxeles vecinos alrededor de un píxel central.

### Proceso Iterativo de Inpainting

- **Iteraciones:** Se realizan múltiples pasadas (según `max_iterations`) para rellenar progresivamente los píxeles enmascarados.

#### Para Cada Iteración:

1. **Identificación de Píxeles enmascarados:** Se localizan las coordenadas `(y, x)` de los píxeles que aún necesitan ser rellenados.

2. **Procesamiento de Cada Píxel enmascarado:**
   
   - **Ventana de Vecinos:** Se extrae una ventana de 3x3 alrededor del píxel actual, asegurando que los índices no se salgan de los límites de la imagen.
   
   - **Detección de Vecinos Válidos:** Se identifica cuáles de los píxeles en la ventana no están enmascarados (es decir, ya tienen un valor válido).
   
   - **Cálculo del Promedio de Vecinos:** Si hay vecinos válidos, se calcula el promedio de sus valores de color.
   
   - **Actualización del Píxel:** Se reemplaza el valor del píxel enmascarado con este promedio.
   
   - **Marcado como Procesado:** Se actualiza la máscara booleana para indicar que este píxel ya ha sido rellenado.

3. **Indicador de Actualización:** Si al menos un píxel se ha actualizado durante la iteración, se marca `updated = True`.

4. **Terminación Temprana:** Si en una iteración no se realizan actualizaciones (`updated = False`), el proceso de inpainting se detiene anticipadamente para evitar iteraciones innecesarias.

### Salida

- **Imagen Rellenada:** La imagen con las áreas rojas rellenadas mediante el promedio de sus vecinos.



### Implementación en Python:

El código de implementación del filtro de eliminación de marcas de agua de color rojo se encuentra en:

- [backend/models/watermark/remove_red_watermark.py](../backend/models/watermark/remove_red_watermark.py)
