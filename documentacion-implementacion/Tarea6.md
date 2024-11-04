# Tarea 6

Esta tarea corresponde al filtro oleo.


## Descripción del filtro

El filtro oleo es un filtro que se aplica a una imagen para darle un aspecto de pintura al óleo. Este filtro se logra mediante una suavización de la imagen original.


## Optimizaciones en el código

El código para aplicar el filtro oleo incluye varias optimizaciones para mejorar su rendimiento y eficiencia:

1. **Uso de NumPy**:
    - La imagen se convierte a un arreglo NumPy para aprovechar las operaciones vectorizadas y la manipulación eficiente de datos.

2. **Multiprocesamiento**:
    - Se utiliza la librería `multiprocessing` para procesar las filas de la imagen en paralelo, aprovechando múltiples núcleos de CPU. Esto reduce significativamente el tiempo de procesamiento para imágenes grandes.

3. **Padding de la imagen**:
    - Se añade padding a la imagen para manejar los bordes al crear bloques de píxeles, evitando así condiciones de borde complicadas y simplificando el acceso a los píxeles vecinos.

4. **Conversión de colores a enteros**:
    - Los colores RGB de cada píxel se combinan en un solo entero para facilitar el conteo de colores únicos en cada bloque. Esto permite utilizar `np.unique` de manera eficiente para encontrar el color más común.

5. **Uso de `np.unique`**:
    - La función `np.unique` se utiliza para contar la frecuencia de cada color en un bloque de píxeles, lo que es más eficiente que implementar un contador manualmente.


## Implementación en Python

El código en Python para aplicar el filtro oleo se encuentra en:

[backend/models/oleo/oleo_filter.py](../backend/models/oleo/oleo_filter.py)