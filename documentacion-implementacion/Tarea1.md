# Tarea 1
Filtros incluidos en Tarea 1:

- Escala de grises
- Escala de grises ponderada
- Efecto mica RGB


## Filtro escala de grises:

### Descripción
El filtro de escala de grises convierte una imagen colorida a una versión en tonos de gris. Este proceso implica transformar cada píxel de la imagen original, que contiene información de color en los canales Rojo, Verde y Azul (RGB), a un solo valor de luminancia que representa la intensidad de la luz. El resultado es una imagen monocromática que mantiene las variaciones de brillo de la imagen original sin la información de color.

### Pseudocódigo del Algoritmo
```
Para cada píxel en la imagen:
    Obtener los valores de los canales Rojo (R), Verde (G) y Azul (B)
    Calcular el promedio de R, G y B
    Asignar el valor promedio a cada uno de los canales R, G y B del píxel
Fin
```

### Implementación en Python

El código se puede consultar en:

- [backend/models/filters/grayscale_filter.py](../backend/models/filters/grayscale_filter.py)


Nuestra implementación del filtro se diferencia del pseudocódigo básico al incorporar las optimizaciones que mejoran la eficiencia y el rendimiento.



## Filtro escala de grises ponderada:

### Descripción:
El filtro de escala de grises ponderada convierte una imagen colorida en una versión monocromática utilizando una ponderación específica para cada canal de color (Rojo, Verde y Azul). Esta ponderación se basa en la percepción humana de la luminosidad, donde el ojo humano es más sensible al verde, seguido del rojo y menos al azul. El resultado es una imagen en tonos de gris que refleja más fielmente las variaciones de brillo percibidas en la imagen original.

### Pseudocódigo del algoritmo:
```
Para cada píxel en la imagen:
    Obtener los valores de los canales Rojo (R), Verde (G) y Azul (B)
    Calcular el valor ponderado usando la fórmula: P = 0.299 * R + 0.587 * G + 0.114 * B
    Asignar el valor P a cada uno de los canales R, G y B del píxel
Fin Para
```


### Implementación en Python:
El código se puede consultar en:

- [backend/models/filters/gray_filter_weighted.py](../backend/models/filters/gray_filter_weighted.py)

Nuestra implementación del filtro se diferencia del pseudocódigo básico al incorporar las optimizaciones que mejoran la eficiencia y el rendimiento.


## Filtro efecto mica RGB:


### Descripción:

El filtro efecto mica RGB aplica una operación de AND lógico a cada uno de los canales de color (Rojo, Verde y Azul) de una imagen. Este efecto realza ciertos componentes de color según los valores proporcionados para cada canal. Es útil para resaltar o suprimir colores específicos en una imagen, creando efectos visuales interesantes y personalizados.


### Pseudocódigo del algoritmo:

```
Para cada píxel en la imagen:
    Obtener los valores de los canales Rojo (R), Verde (G) y Azul (B)
    Aplicar el AND lógico con los valores proporcionados: 
        Nuevo_R = R AND r_val
        Nuevo_G = G AND g_val
        Nuevo_B = B AND b_val
    Asignar los nuevos valores (Nuevo_R, Nuevo_G, Nuevo_B) al píxel
Fin Para
```


### Implementación en Python:

El código se puede consultar en:

- [backend/models/filters/mica_filter.py](../backend/models/filters/mica_filter.py)


## Optimizaciones Implementadas

Para mejorar la eficiencia y el rendimiento de los filtros, implementamos las siguientes optimizaciones:

- **Operaciones Vectorizadas con NumPy:**
Utilizamos las capacidades de procesamiento en vectores de NumPy para calcular el promedio de los canales RGB de manera eficiente. Esto permite procesar grandes cantidades de datos de píxeles simultáneamente, aprovechando las optimizaciones a nivel de bajo nivel de la biblioteca.

- **Multiprocesamiento:**
Implementamos el procesamiento paralelo dividiendo la imagen en bloques y utilizando múltiples procesos para aplicar el proceso a cada bloque de manera simultánea. Esta técnica aprovecha los múltiples núcleos de CPU disponibles, reduciendo significativamente el tiempo de procesamiento, especialmente en imágenes de gran tamaño.


- **Reensamblaje de la Imagen:**
Después de procesar los bloques en paralelo, los combinamos para formar la imagen final, asegurando que la estructura de la imagen original se mantenga intacta.