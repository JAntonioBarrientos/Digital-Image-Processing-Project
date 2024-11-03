# Tarea 3
Filtros incluidos en Tarea 3:


- Imagenes recursivas en escala de grises
- Imagenes recursivas en escala de grises ponderada


## Imagenes recursivas en escala de grises

### Descripción:

El filtro de imágenes recursivas en escala de grises aplica un efecto de repetición de la imagen original, creando una composición visual que se asemeja a un mosaico. Este efecto es útil para resaltar patrones y texturas en la imagen, y puede ser utilizado para crear efectos artísticos y abstractos.


### Pseudocódigo del algoritmo:

```python
# Inicializar RecursiveImagesGray con los parámetros:
imagen_original = ...  # Cargar imagen original
num_variaciones = ...  # Número de variaciones
upscale_factor = ...  # Factor de aumento
grid_rows = ...  # Filas de la cuadrícula
grid_cols = ...  # Columnas de la cuadrícula

# Validar los parámetros de entrada:
if not (2 <= num_variaciones <= 256):
    raise ValueError("El número de variaciones debe estar entre 2 y 256")
if upscale_factor < 1:
    raise ValueError("El factor de aumento debe ser al menos 1")
if grid_rows < 1 or grid_cols < 1:
    raise ValueError("Las dimensiones de la cuadrícula deben ser al menos 1")

# Escalar la imagen original según el factor de aumento
original_width, original_height = imagen_original.size
width = int(upscale_factor * original_width)
height = int(upscale_factor * original_height)

# Calcular el tamaño de cada celda de la cuadrícula
grid_width = width // grid_cols
grid_height = height // grid_rows

# Redimensionar la imagen al tamaño exacto de la cuadrícula
width = grid_width * grid_cols
height = grid_height * grid_rows

# Generar una paleta de variaciones en escala de grises:
variaciones = {}
for brillo in range(num_variaciones):
    # Redimensionar la imagen a las dimensiones de una celda
    img_celda = imagen_original.resize((grid_width, grid_height))
    
    # Aplicar el filtro de escala de grises
    img_gris = aplicar_filtro_gris(img_celda)
    
    # Calcular el brillo promedio de la imagen
    brillo_promedio = calcular_brillo_promedio(img_gris)
    
    # Generar valores representativos de brillo utilizando una distribución lineal
    factor_escala = brillo / (num_variaciones - 1)
    
    # Ajustar el brillo de la imagen
    img_ajustada = ajustar_brillo(img_gris, factor_escala)
    
    # Asegurar que los valores de píxel estén en el rango [0, 255]
    img_ajustada = np.clip(img_ajustada, 0, 255)
    
    # Convertir el arreglo de píxeles ajustados a una imagen RGB
    img_rgb = Image.fromarray(img_ajustada.astype('uint8'), 'RGB')
    
    # Almacenar la imagen en el diccionario de variaciones
    variaciones[brillo] = img_rgb

# Aplicar el filtro de imágenes recursivas:
# Obtener las variaciones en escala de grises
# Redimensionar la imagen original al tamaño total de la cuadrícula
imagen_escalada = imagen_original.resize((width, height))

# Convertir la imagen escalada a un arreglo NumPy
imagen_array = np.array(imagen_escalada)

# Dividir el arreglo en celdas según la cuadrícula
imagen_array = imagen_array.reshape(grid_rows, grid_height, grid_cols, grid_width, 3)
imagen_array = imagen_array.transpose(0, 2, 1, 3, 4)

# Calcular el promedio de los valores RGB en cada celda
promedios_rgb = imagen_array.mean(axis=(2, 3))

# Calcular el brillo promedio de cada celda
brillos_promedio = calcular_brillos_promedio(promedios_rgb)

# Para cada celda en la cuadrícula:
for row in range(grid_rows):
    for col in range(grid_cols):
        # Encontrar el valor de brillo más cercano en las variaciones
        brillo_celda = brillos_promedio[row, col]
        variacion_cercana = encontrar_variacion_cercana(variaciones, brillo_celda)
        
        # Seleccionar la imagen de variación correspondiente
        img_variacion = variaciones[variacion_cercana]
        
        # Pegar la imagen seleccionada en la posición adecuada de la imagen final
        x_start = col * grid_width
        y_start = row * grid_height
        imagen_final.paste(img_variacion, (x_start, y_start))

# Retornar la imagen procesada con las variaciones en escala de grises aplicadas
return imagen_final
```

### Implementación en Python:

El código se puede consultar en:

- [backend/models/recursiveImage/recursive_images_gray.py](../backend/models/recursiveImage/recursive_images_gray.py)



## Imagenes recursivas a color

### Descripción:

El filtro de imágenes recursivas a color aplica un efecto de repetición de la imagen original, en donde se aplica una mica del color promedio de la imagen original. 

### Pseudocódigo del algoritmo:

```python
# Inicialización:

# Validar parámetros de entrada:
if upscale_factor < 1:
    # Manejar error: upscale_factor debe ser ≥ 1
if grid_rows < 1 or grid_cols < 1:
    # Manejar error: grid_rows y grid_cols deben ser ≥ 1

# Obtener dimensiones de la imagen original:
original_width, original_height = obtener_dimensiones(imagen_original)

# Calcular dimensiones escaladas:
width = original_width * upscale_factor
height = original_height * upscale_factor

# Calcular tamaño de cada celda de la cuadrícula:
grid_width = width / grid_cols
grid_height = height / grid_rows

# Ajustar dimensiones escaladas para que sean múltiplos exactos de la cuadrícula:
width = grid_width * grid_cols
height = grid_height * grid_rows

# Preparación de Imágenes:

# Crear imagen vacía para la cuadrícula:
recursive_image = crear_imagen_vacía(width, height)

# Escalar imagen original al tamaño total:
image_upscaled = redimensionar_imagen(imagen_original, width, height)

# Redimensionar imagen original al tamaño de una celda:
img_resize = redimensionar_imagen(imagen_original, grid_width, grid_height)

# Conversión a Arreglos NumPy:

# Convertir image_upscaled a arreglo NumPy:
image_array = convertir_a_numpy(image_upscaled)

# Convertir img_resize a arreglo NumPy:
img_resize_array = convertir_a_numpy(img_resize)

# Procesamiento de la Cuadrícula:

# Reestructurar image_array para separar celdas:
image_array = image_array.reshape(grid_rows, grid_height, grid_cols, grid_width, 3)
image_array = image_array.transpose(0, 2, 1, 3, 4)

# Calcular promedio de color para cada celda:
average_colors = image_array.mean(axis=(2, 3))

# Iterar sobre cada celda de la cuadrícula:
for row in range(grid_rows):
    for col in range(grid_cols):
        # Obtener posición de inicio de la celda:
        x_start = col * grid_width
        y_start = row * grid_height

        # Obtener promedio de color de la celda:
        r_val, g_val, b_val = average_colors[row, col]

        # Aplicar filtro AND al bloque:
        processed_block = copiar(img_resize_array)
        processed_block[:, :, 0] &= r_val
        processed_block[:, :, 1] &= g_val
        processed_block[:, :, 2] &= b_val

        # Convertir processed_block a imagen:
        processed_image = convertir_a_PIL(processed_block)

        # Pegar processed_image en recursive_image:
        recursive_image.paste(processed_image, (x_start, y_start))

# Finalización:

# Retornar imagen procesada:
return recursive_image

```

### Implementación en Python:

El código se puede consultar en:

- [backend/models/recursiveImage/recursive_images_color.py](../backend/models/recursiveImage/recursive_images_color.py)


## Optimizaciones:
### Operaciones Vectorizadas con NumPy:
Se utilizan para procesar grandes conjuntos de datos de forma eficiente, evitando bucles explícitos en Python y aprovechando optimizaciones a nivel de bajo nivel.

### Reestructuración y Transposición de Arreglos:
- **reshape y transpose**: Permiten reorganizar el arreglo de la imagen para que las celdas de la cuadrícula sean accesibles directamente y se puedan procesar en bloque.

### Cálculo Simultáneo de Promedios:
- **mean(axis=(2, 3))**: Calcula el promedio de los valores RGB de todas las celdas de la cuadrícula en una sola operación, mejorando la eficiencia.

### Aplicación Directa de Operaciones Lógicas:
- **Operación AND Vectorizada**: La operación lógica AND se aplica directamente sobre los canales de color del arreglo NumPy para todo el bloque, sin necesidad de iterar píxel por píxel.

### Minimización de Copias y Uso Eficiente de Memoria:
- **Evitar Copias Innecesarias**: Se crean copias de los bloques solo cuando es necesario, reduciendo el consumo de memoria y evitando modificaciones no deseadas en los datos originales.

### Eliminación de Dependencias Externas:
- **Integración de la Lógica del Filtro**: Al incorporar directamente la lógica del filtro (operación AND), se evita el overhead de llamadas a funciones o clases externas, mejorando el rendimiento y simplificando el código.

### Optimización de Tipos de Datos:
- **Uso de uint8**: Se utiliza el tipo de dato uint8 para representar valores de color, lo que es más eficiente en memoria y adecuado para el rango de valores [0, 255].