# Tarea 8
Implementación de la función `resize` en la clase `Image` para redimensionar la imagen a una escala dada.
Para esto usamos el algoritmo de interpolación bilineal.

## Algoritmo de interpolación bilineal

La interpolación bilineal es un algoritmo de interpolación para la reconstrucción de una función en dos dimensiones a partir de una cuadrícula regular de muestras. La interpolación bilineal calcula el valor de un píxel desconocido en función de los valores de los píxeles vecinos en la imagen original.

### Pasos del Algoritmo

1. **Calcular las Relaciones de Escala**

   La relación de escala determina cuánto se reducirá o aumentará la imagen en cada dimensión (X e Y) $ \text{scale\_x} = \frac{\text{nuevo\_ancho}}{\text{ancho\_original}} $

   **Relación de escala en X (ancho):** F $ \text{scale\_x} = \frac{\text{nuevo\_ancho}}{\text{ancho\_original}} $

   **Relación de escala en Y (alto):** $ \text{scale\_y} = \frac{\text{nuevo\_alto}}{\text{alto\_original}} $

2. **Crear la Imagen Redimensionada**

   Se crea una matriz vacía para almacenar los valores de los píxeles de la imagen redimensionada, utilizando las nuevas dimensiones calculadas en el paso anterior.

3. **Calcular las Coordenadas en la Imagen Original**

   Para cada píxel en la imagen redimensionada, calculamos las coordenadas correspondientes en la imagen original:

   $$ x_{\text{orig}} = x_{\text{new}} \times \text{scale\_x} $$

   $$ y_{\text{orig}} = y_{\text{new}} \times \text{scale\_y} $$

   Estas coordenadas pueden ser valores decimales.

4. **Identificar los Píxeles Vecinos**

   Para realizar la interpolación bilineal, necesitamos los cuatro píxeles más cercanos en la imagen original. Definimos:

   - $$ x_0 = \lfloor x_{\text{orig}} \rfloor $$
   - $$ y_0 = \lfloor y_{\text{orig}} \rfloor $$
   - $$ x_1 = x_0 + 1 $$
   - $$ y_1 = y_0 + 1 $$

   Para evitar índices fuera de los límites, aplicamos *clipping* en estas coordenadas, ajustándolas al borde más cercano de la imagen si es necesario.

5. **Calcular las Distancias Fraccionarias**

   Calculamos las distancias entre las coordenadas originales y los píxeles vecinos. Estas distancias fraccionarias permiten ponderar cada píxel vecino en la interpolación:

   $$ d_x = x_{\text{orig}} - x_0 $$

   $$ d_y = y_{\text{orig}} - y_0 $$

6. **Interpolar en el Eje X**

   Para cada par de píxeles vecinos verticalmente alineados, calculamos el valor interpolado en el eje X:

   $$ I_{\text{top}} = I(x_0, y_0) \times (1 - d_x) + I(x_1, y_0) \times d_x $$

   $$ I_{\text{bottom}} = I(x_0, y_1) \times (1 - d_x) + I(x_1, y_1) \times d_x $$

7. **Interpolar en el Eje Y**

   Usamos los valores $I_{\text{top}}$ y $I_{\text{bottom}}$ obtenidos en el paso anterior para interpolar en el eje Y y calcular el valor final del píxel en la imagen redimensionada:

   $$ I_{\text{new}} = I_{\text{top}} \times (1 - d_y) + I_{\text{bottom}} \times d_y $$

8. **Asignar el Valor al Píxel de la Imagen Redimensionada**

   Asignamos el valor $I_{\text{new}}$ al píxel correspondiente en la imagen redimensionada en las coordenadas $(x_{\text{new}}, y_{\text{new}} \times o)$.

9. **Repetir para Todos los Píxeles**

   Repetimos el proceso para cada píxel en la imagen redimensionada hasta completar la interpolación.

**Manejo de Múltiples Canales de Color**

Si la imagen tiene varios canales de color (por ejemplo, RGB), aplicamos el mismo proceso de interpolación en cada canal por separado.

## Implementación en Python

El código se puede consultar en el archivo:

- [backend/models/filters/resize.py](../backend/models/filters/resize.py)