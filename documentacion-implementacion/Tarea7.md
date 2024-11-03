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

[backend/models/erosion/min_max.py](../backend/models/erosion/min_max.py)

## Optimizaciones en comparación con el algoritmo original

El código optimizado para aplicar el filtro de máximos y mínimos incluye varias mejoras en comparación con el algoritmo original:

1. **Multiprocesamiento por bloques**:
    - En lugar de procesar cada píxel individualmente en paralelo, el código optimizado divide la imagen en bloques de filas (`chunks`) y procesa cada bloque en paralelo. Esto reduce la sobrecarga de crear y gestionar múltiples procesos, mejorando la eficiencia.

2. **Reducción de la sobrecarga de procesos**:
    - Al procesar bloques de filas en lugar de píxeles individuales, se reduce la cantidad de tareas que deben ser gestionadas por el `Pool` de procesos, lo que disminuye la sobrecarga y mejora el rendimiento.

3. **Uso eficiente de la memoria**:
    - El código optimizado utiliza arreglos NumPy para almacenar y manipular los datos de la imagen, lo que es más eficiente en términos de memoria y velocidad en comparación con las estructuras de datos estándar de Python.

4. **Padding de la imagen**:
    - Se añade padding a la imagen para manejar los bordes, lo que simplifica el acceso a los píxeles vecinos y evita condiciones de borde complicadas.

5. **Conversión a escala de grises**:
    - La imagen se convierte a escala de grises antes de aplicar el filtro, lo que reduce la cantidad de datos a procesar y mejora la velocidad del algoritmo.

6. **Determinación dinámica del tamaño de los bloques**:
    - El tamaño de los bloques (`chunk_size`) se determina dinámicamente en función del número de núcleos de CPU disponibles y la altura de la imagen, lo que permite un balance de carga más eficiente entre los procesos.
