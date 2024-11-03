# Tarea 7

Esta tarea corresponde máximos y mínimos.


## Descripción del filtro

El filtro lo que hace es buscar los máximos y mínimos de una imagen. Es útil en textos para aclarar o oscurecer las letras y en imágenes para resaltar o disminuir el brillo de las zonas más claras o más oscuras.

## Algoritmo

El algoritmo para aplicar el filtro de máximos y mínimos a una imagen es el siguiente:

1. Seleccionar un tamaño de ventana `W` y un radio `R`.
2. Para cada píxel `p` en la imagen:
    1. Seleccionar una ventana de tamaño `W` alrededor del píxel `p`.
    2. Calcular el color minimo/máximo en cada ventana.
    3. Asignar este color al píxel `p`.


## Implementación en Python

El código en Python para aplicar el filtro oleo se consulta en:

[backend/models/oleo/oleo_filter.py](../backend/models/oleo/oleo_filter.py)

## Optimizaciones en el código


