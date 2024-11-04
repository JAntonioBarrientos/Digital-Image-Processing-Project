# Tarea 5
Filtros incluidos en Tarea 5:

- Semitonos
- Dithering azar
- Dithering ordenado
- Dithering disperso
- Dithering Floyd-Steinberg

## Semitonos

### Descripción:

El filtro de semitonos aplica un efecto de tonos de grises a una imagen utilizando patrones de puntos de diferentes tamaños y densidades. Este efecto es útil para imprimir imágenes

### Pseudocódigo del algoritmo:

El filtro de semitonos implementado en la clase `HalftoneFilter` convierte una imagen en escala de grises utilizando un patrón de puntos de diferentes tamaños y densidades. Este efecto simula la técnica de semitonos utilizada en la impresión para representar tonos continuos mediante puntos discretos. A continuación, se detalla el algoritmo empleado:

#### 1. Inicialización

- **Conversión a Escala de Grises:**
  - Se utiliza la clase `GrayscaleFilter` para convertir la imagen original a escala de grises, asegurando que los valores de los canales Rojo, Verde y Azul (RGB) sean iguales.

- **Configuración de Dimensiones:**
  - Se obtienen las dimensiones originales de la imagen.
  - Se establece el tamaño de la cuadrícula (`grid_dim`) basado en el número de variaciones de semitonos deseadas.
  
- **Validación de Parámetros:**
  - Se verifica que el número de variaciones (`num_variations`) esté dentro del rango permitido (2 a 256).

#### 2. Generación de la Paleta de Semitonos

- **Creación de Variaciones de Semitonos:**
  - Se genera un diccionario que contiene múltiples versiones de la imagen en escala de grises, cada una con círculos de diferentes tamaños.
  - Para cada variación:
    - Se crea una imagen en blanco del tamaño de la cuadrícula.
    - Se dibuja un círculo negro en el centro, cuyo radio varía inversamente con el nivel de brillo correspondiente. Es decir, niveles de gris más altos tienen círculos más pequeños.
    - Cada imagen de círculo se asocia con un valor de brillo representativo en el diccionario `versiones`.

#### 3. Aplicación del Filtro de Semitonos

- **Preparación de la Imagen Resultante:**
  - Se crea una nueva imagen en blanco que servirá como lienzo para los semitonos.
  - La imagen en escala de grises se redimensiona al tamaño total de la cuadrícula.

- **División en Bloques:**
  - La imagen redimensionada se divide en bloques de tamaño `grid_dim x grid_dim`.
  - Se calcula el brillo promedio de cada bloque.

- **Mapeo de Brillo a Variaciones de Semitonos:**
  - Para cada bloque, se determina el valor de brillo más cercano en la paleta de variaciones generada previamente.
  - Se selecciona la imagen de círculo correspondiente a este valor de brillo.

- **Composición de la Imagen Final:**
  - Se pega cada imagen de círculo seleccionada en la posición adecuada de la imagen resultante, formando así el patrón de semitonos sobre toda la imagen.

### Implementación en Python:

El código de la clase `HalftoneFilter` se encuentra en el archivo [backend/models/dithering/halftones_filter.py](../backend/models/dithering/halftones_filter.py).


## Dithering Azar

### Descripción:

El filtro de dithering azar aplica un efecto de ruido aleatorio a una imagen para simular tonos de grises adicionales. Este efecto es útil para reducir la apariencia de bandas en gradientes suaves.

### Algoritmo:

#### 1. Inicialización

- **Conversión a Escala de Grises:**
  - Utiliza la clase `GrayscaleFilter` para convertir la imagen original a escala de grises, asegurando que los valores de los canales Rojo, Verde y Azul (RGB) sean iguales.

- **Obtención de Dimensiones:**
  - Obtiene el ancho y alto de la imagen una vez convertida a escala de grises.

#### 2. Aplicación del Filtro de Dithering Aleatorio

- **Creación de la Imagen Resultado:**
  - Crea una nueva imagen en blanco y negro (`RGB`) con las mismas dimensiones que la imagen original en escala de grises.

- **Iteración Sobre Cada Píxel:**
  - Recorre cada píxel de la imagen en escala de grises.
  - Para cada píxel:
    - **Obtención del Brillo:**
      - Obtiene el valor de brillo del píxel actual (en escala de grises, R = G = B).
    - **Generación de Valor Aleatorio:**
      - Genera un número aleatorio entre 0 y 255.
    - **Asignación de Color:**
      - Si el brillo del píxel es menor o igual al valor aleatorio generado, establece el píxel en negro `(0, 0, 0)`.
      - De lo contrario, establece el píxel en blanco `(255, 255, 255)`.

#### 3. Finalización

- **Retorno de la Imagen Procesada:**
  - Devuelve la imagen resultante con el efecto de dithering aleatorio aplicado, la cual contiene una simulación de tonos de gris adicionales a través de una distribución de puntos negros y blancos.

### Implementación en python

El código se puede consultar en el archivo:

[backend/models/dithering/random_dithering_filter.py](../backend/models/dithering/random_dithering_filter.py)


## Dithering ordenado

### Descripción

El filtro de dithering agrupado (`ClusteredDitheringFilter`) convierte una imagen en escala de grises utilizando una matriz de umbralización "clustered" de 3x3. Este método mejora la representación de tonos de gris al distribuir los píxeles blancos y negros de manera más uniforme, reduciendo así la aparición de patrones repetitivos y mejorando la calidad visual de la imagen resultante.

### Algoritmo

1. **Inicialización:**
    - **Conversión a Escala de Grises:**  
      Utiliza la clase `GrayscaleFilter` para convertir la imagen original a escala de grises, asegurando que los valores de los canales Rojo, Verde y Azul (RGB) sean iguales.
    - **Definición de la Matriz Clustered:**  
      Define una matriz de umbralización "clustered" de 3x3 que determina la distribución de píxeles blancos y negros en cada bloque de la imagen.
    - **Escalado de la Matriz:**  
      Escala la matriz "clustered" para el rango de 0 a 255 multiplicando cada valor de la matriz original por `255 // 9`.

2. **Aplicación del Filtro de Dithering:**
    - **Creación de la Imagen Resultado:**  
      Crea una nueva imagen en blanco y negro (`L` mode) con las mismas dimensiones que la imagen original en escala de grises.
    - **Iteración sobre Bloques 3x3:**  
      Recorre la imagen en bloques de 3x3 píxeles.
        - **Procesamiento de Cada Píxel en el Bloque:**  
          Para cada píxel dentro del bloque:
            - **Obtención del Valor de Brillo:**  
              Lee el valor de brillo del píxel original.
            - **Escalado del Valor de Brillo:**  
              Escala el valor de brillo dividiéndolo por 28 para obtener un índice entre 0 y 9.
            - **Comparación con la Matriz Clustered:**  
              Compara el valor escalado con el valor correspondiente en la matriz "clustered".
            - **Asignación de Color:**  
              Si el valor escalado es menor que el umbral de la matriz, asigna negro al píxel resultante; de lo contrario, asigna blanco.

3. **Finalización:**
    - **Retorno de la Imagen Procesada:**  
      Devuelve la imagen resultante con el efecto de dithering agrupado aplicado.

### Implementacion python

El código se puede consultar en el archivo:

[backend/models/dithering/clustered_dithering.py](../backend/models/dithering/clustered_dithering.py)


## Dithering disperso

Se realiza el mismo proceso que en el dithering ordenado pero ahora usando la matriz:

```python
        self.cluster_matrix = np.array([
            [1, 7, 4],
            [5, 8, 3],
            [6, 2, 9]
        ])
```

### Implementacion python

El código se puede consultar en el archivo:

[backend/models/dithering/dispersed_dithering.py](../backend/models/dithering/dispersed_dithering.py)


## Dithering Floyd-Steinberg

### Descripcion

El algoritmo de dithering Floyd-Steinberg es una técnica de procesamiento de imágenes utilizada para convertir imágenes en escala de grises (o imágenes a color) a una representación binaria (blanco y negro) manteniendo una apariencia visual más suave y detallada. Este método pertenece a la categoría de dithering difuso, que distribuye el error de cuantización de cada píxel a sus píxeles vecinos, creando así una ilusión de más niveles de gris a partir de píxeles binarios.

El principal objetivo del dithering Floyd-Steinberg es reducir la aparición de bandas de color o degradados no deseados que pueden surgir al reducir el número de niveles de intensidad en una imagen. Al dispersar el error de cuantización, el algoritmo logra una transición más natural entre diferentes tonos, manteniendo detalles y texturas que serían difíciles de representar en una imagen binaria pura.


### Pasos del Algoritmo:

1. **Inicialización:**
    - Convertir la imagen original a escala de grises.
    - Obtener las dimensiones (ancho y alto) de la imagen en escala de grises.

2. **Aplicación del Dithering Floyd-Steinberg:**
    - Convertir la imagen en escala de grises a un arreglo NumPy de tipo `float32`.
    - Iterar sobre cada píxel de la imagen:
        - Obtener el valor de intensidad (`old_pixel`) del píxel actual.
        - Determinar el nuevo valor del píxel (`new_pixel`) redondeando a 0 o 255.
        - Calcular el error de cuantización (`quant_error`) como la diferencia entre `old_pixel` y `new_pixel`.
        - Distribuir el error de cuantización a los píxeles vecinos:
            - **Píxel a la derecha:** recibir `7/16` del error.
            - **Píxel inferior izquierdo:** recibir `3/16` del error.
            - **Píxel inferior:** recibir `5/16` del error.
            - **Píxel inferior derecho:** recibir `1/16` del error.
        - Asegurarse de que los valores de los píxeles se mantengan en el rango `[0, 255]`.

3. **Finalización:**
    - Convertir el arreglo NumPy modificado de vuelta a una imagen PIL en modo de escala de grises.
    - Retornar la imagen procesada con el efecto de dithering aplicado.



### Implementacion python

El código se puede consultar en el archivo:

[backend/models/dithering/floyd_steinberg_dithering.py](../backend/models/dithering/floyd_steinberg_dithering.py)
