# Tarea 2
Filtros incluidos en Tarea 2:

- Efecto Blur
- Efecto Motion Blur
- Efecto Sharpen
- Efecto Emboss
- Efecto Find Edges
- Efecto Promedio

## Convolución

### Descripción:
El filtro de convolución aplica una operación matemática que combina una imagen con un kernel (matriz pequeña) para producir una nueva imagen. Este proceso se utiliza para realizar diversas operaciones de procesamiento de imágenes, como el desenfoque, la detección de bordes y el realce de características. La convolución implica mover el kernel sobre cada píxel de la imagen y calcular un valor ponderado basado en los valores de los píxeles vecinos y los valores del kernel.

### Pseudocódigo del algoritmo:
```
Para cada píxel en la imagen:
    nuevo_valor = 0
    Para cada valor en el kernel:
        nuevo_valor += valor_kernel * valor_píxel_correspondiente
    Asignar nuevo_valor a la posición correspondiente en la nueva imagen
Fin Para
```


### Implementación en Python:
El código se puede consultar en:

- [backend/models/convolutionFilters/convolution_filter_rgb.py](../backend/models/convolutionFilters/convolution_filter_rgb.py)


Nuestra implementación del filtro se diferencia del pseudocódigo básico al incorporar las optimizaciones que mejoran la eficiencia y el rendimiento.

### Optimizaciones Implementadas en la Convolución:

- **Multiprocesamiento**: Utiliza el módulo `multiprocessing` de Python para dividir la imagen en bloques y procesarlos en paralelo. Esto aprovecha múltiples núcleos de CPU, reduciendo significativamente el tiempo de procesamiento en imágenes de gran tamaño.

- **Operaciones Vectorizadas con NumPy**: Emplea operaciones vectorizadas para realizar cálculos de convolución de manera eficiente. Por ejemplo, utiliza `np.einsum` para realizar multiplicaciones elemento a elemento y sumas sobre los bloques de la imagen.

- **Uso de Stride Tricks**: Utiliza `numpy.lib.stride_tricks.as_strided` para crear una vista deslizante (sliding window) de la imagen, permitiendo acceder a todas las regiones de interés (ROIs) necesarias para la convolución sin copiar datos, lo que mejora el rendimiento y reduce el uso de memoria.

- **Optimización de Memoria**: Aplica padding a la imagen solo una vez y divide la imagen en bloques que incluyen el padding necesario para cada proceso. Esto evita recalcular el padding para cada bloque individualmente y optimiza el acceso a la memoria cache.

- **Limitación de Procesos**: Ajusta dinámicamente el número de procesos utilizados para que no exceda la altura de la imagen, asegurando un uso eficiente de los recursos del sistema sin sobrecargar la CPU.

Estas optimizaciones combinadas mejoran la eficiencia y el rendimiento del filtro de convolución, permitiendo un procesamiento más rápido y eficiente de imágenes de alta resolución.



## Filtro Efecto Blur

### Descripción:
El filtro de desenfoque (Blur) suaviza una imagen reduciendo los detalles y las variaciones bruscas de color. Este efecto es útil para eliminar el ruido o para crear un fondo desenfocado que destaque elementos específicos de la imagen.

### Kernel usado:
El kernel de desenfoque se genera en función de la intensidad (radio) y tiene un tamaño de (2r + 1) x (2r + 1). El patrón del kernel asigna un valor de 1 a las posiciones que están dentro de una distancia Manhattan determinada por el radio, y luego se normaliza para que la suma de todos los elementos sea 1.

```python
# Ejemplo de un kernel de desenfoque con intensidad=1 (radio=1)
blur_kernel = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]) / 5
```

### Implementación en Python:

El código se puede consultar en:

- [backend/models/convolutionFilters/filters/blur_filter.py](../backend/models/convolutionFilters/filters/blur_filter.py)

## Filtro Efecto Motion Blur

### Descripción:

El filtro de desenfoque de movimiento (Motion Blur) simula el efecto de una cámara moviéndose mientras se toma una foto, creando una sensación de movimiento en una dirección específica. Este efecto es útil para enfatizar la dirección del movimiento en una imagen.

### Kernel usado:

El kernel de Motion Blur es una matriz lineal que tiene valores no nulos a lo largo de una dirección diagonal, horizontal o vertical, dependiendo de la dirección del movimiento deseado. Este kernel también se normaliza para mantener la intensidad de la imagen.

```python
# Ejemplo de un kernel de Motion Blur diagonal
motion_blur_kernel = np.array([
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1]
]) / 5
```

### Implementación en Python:

El código se puede consultar en:

- [backend/models/convolutionFilters/filters/custom_diagonal_filter.py](../backend/models/convolutionFilters/filters/custom_diagonal_filter.py)

## Filtro Efecto Sharpen



### Descripción:

El filtro de afilado (Sharpen) realza los bordes y detalles de una imagen aumentando el contraste entre píxeles adyacentes. Este efecto es útil para mejorar la nitidez y definir mejor las características de la imagen.

### Kernel usado:
El kernel de afilado tiene un valor alto en el centro y valores negativos en los alrededores. Al aplicar este kernel, se realzan los cambios abruptos en la intensidad de los píxeles, lo que resulta en una imagen más nítida.

```python
# Kernel de afilado
sharpen_kernel = np.array([
    [-1, -1, -1],
    [-1,  9, -1],
    [-1, -1, -1]
])
```

### Implementación en Python:

El código se puede consultar en:

- [backend/models/convolutionFilters/filters/sharpen_filter.py](../backend/models/convolutionFilters/filters/sharpen_filter.py)

## Filtro Efecto Emboss

### Descripción:

El filtro de relieve (Emboss) da a la imagen una apariencia tridimensional, resaltando los bordes y creando sombras que simulan una iluminación desde una dirección específica. Este efecto es útil para destacar la textura y profundidad de los objetos en la imagen.


### Kernel usado:

El kernel de emboss tiene valores asimétricos que crean sombras en una dirección y luces en otra, logrando el efecto de relieve. Se utiliza un bias para ajustar los valores de intensidad y asegurar que los colores se mantengan dentro del rango válido.

```python
# Kernel de emboss
emboss_kernel = np.array([
    [-1, -1,  0],
    [-1,  0,  1],
    [ 0,  1,  1]
])

# Bias aplicado
bias = 128.0
```

### Implementación en Python:

El código se puede consultar en:

- [backend/models/convolutionFilters/filters/emboss_filter.py](../backend/models/convolutionFilters/filters/emboss_filter.py)


## Filtro Efecto Find Edges

### Descripción:
El filtro de detección de bordes (Find Edges) identifica y resalta los bordes de los objetos dentro de una imagen. Este efecto es útil para análisis de contornos y para resaltar las estructuras principales de la imagen.


### Kernel usado:

El kernel de detección de bordes tiene un valor central alto y valores negativos alrededor. Al aplicar este kernel, se destacan las transiciones abruptas en la intensidad de los píxeles, lo que resalta los bordes de los objetos.

```python
# Kernel de detección de bordes
find_edges_kernel = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
])
```

### Implementación en Python:

El código se puede consultar en:

- [backend/models/convolutionFilters/filters/find_edges_filter.py](../backend/models/convolutionFilters/filters/find_edges_filter.py)


## Filtro Efecto Promedio

### Descripción:

El filtro de promedio (Mean Filter) suaviza la imagen calculando el promedio de los píxeles en una ventana determinada. Este efecto reduce el ruido y las variaciones de intensidad, produciendo una imagen más uniforme.

### Kernel usado:

El kernel de promedio es una matriz de tamaño fijo (por ejemplo, 7x7) donde todos los elementos tienen el mismo valor, y luego se normaliza dividiendo por el número total de elementos. Esto asegura que la suma de todos los elementos del kernel sea 1.


```python
# Kernel de promedio 7x7
mean_kernel = np.ones((7, 7), dtype=np.float32) / 49
```

### Implementación en Python:

El código se puede consultar en:

- [backend/models/convolutionFilters/filters/mean_filter.py](../backend/models/convolutionFilters/filters/mean_filter.py)