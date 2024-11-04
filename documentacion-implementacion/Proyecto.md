# Proyecto

## Descripción

El proyecto consiste en la creación del filtro mosaico, en el que apartir de una biblioteca de imágenes se trata de recrear la imagen procesada con pequeñas imágenes de la biblioteca.

## Ejecución

Antes de construir el proyecto con docker es necesario tener la biblioteca de imágenes en la carpeta:

```
backend/models/data/image_library/
```

No importa si dentro de esa carpeta hay más carpetas, el programa se encargará de buscar todas las imágenes dentro de la carpeta y sus subcarpetas.

Después de tener la biblioteca de imágenes, se puede construir el proyecto con el siguiente comando:

```bash
docker compose up --build
```

## Uso

Dentro de la terminal se indicará la cantidad de núcleos usados y si se esta preprocesando la biblioteca de imágenes o se esta procesando una imagen.

### Características

1. **Upscale Factor de las dimensiones: N**
    - Este factor de escala aumenta las dimensiones de la imagen procesada en un factor de 4. Es decir, cada dimensión (ancho y alto) de la imagen original se multiplica por N, resultando en una imagen procesada mucho más grande.

    **Advertencia**: Valores altos pueden causar que la imagen procesada sea muy grande y si no hay suficiente memoria RAM, el navegador puede congelarse. En caso de que esto suceda, se recomienda reiniciar el contenedor de Docker y probar con un valor más bajo.

2. **Tamaño del Bloque (Ancho en píxeles):**
    - Este parámetro define el ancho de cada bloque de la imagen en píxeles. Cada bloque será reemplazado por una imagen de la biblioteca que mejor se ajuste a esa sección de la imagen original.

3. **Tamaño del Bloque (Alto en píxeles):**
    - Este parámetro define el alto de cada bloque de la imagen en píxeles. Similar al ancho del bloque, cada bloque será reemplazado por una imagen de la biblioteca que mejor se ajuste a esa sección de la imagen original.

Estas características permiten personalizar el filtro de mosaico para obtener una imagen procesada que se asemeje a la original, pero compuesta por pequeñas imágenes de la biblioteca.


### Preprocesamiento de la biblioteca de imágenes

Antes de procesar una imagen, el programa preprocesa la biblioteca de imágenes para extraer características de cada imagen y almacenarlas en un archivo .csv. En caso de agregar nuevas imagenes después de que se procesó la biblioteca, es necesario volver a preprocesar la biblioteca de imágenes. Para ello utiliza el botón "Reiniciar preprocesamiento" en la interfaz de usuario.


## Explicación del algoritmo

### Pseudocódigo del flujo del Filtro de Mosaico

1. **Inicialización**:
    - Inicializa el filtro con la imagen objetivo y las rutas de la biblioteca de imágenes.
    - Si no existe un archivo CSV con los colores promedio de las imágenes de la biblioteca, se preprocesan las imágenes para calcular estos colores y se guardan en el CSV.

2. **Preprocesamiento de la Biblioteca de Imágenes**:
    - Recorre todas las imágenes en la biblioteca.
    - Verifica la integridad de cada imagen.
    - Calcula el color promedio de cada imagen.
    - Guarda los colores promedio y las rutas de las imágenes en un archivo CSV.
    - Registra las imágenes corruptas que no pudieron ser procesadas.

3. **Carga de Datos de la Biblioteca**:
    - Carga los colores promedio y las rutas de las imágenes desde el archivo CSV.
    - Construye un KD-Tree para búsquedas rápidas de los colores promedio.

4. **Aplicación del Filtro de Mosaico**:
    - Convierte la imagen objetivo a un arreglo NumPy.
    - Amplía la imagen según el factor de ampliación (`upscale_factor`).
    - Divide la imagen ampliada en bloques de tamaño especificado (`block_width` y `block_height`).
    - Para cada bloque:
        - Calcula el color promedio del bloque.
        - Utiliza el KD-Tree para encontrar la imagen de la biblioteca cuyo color promedio es el más cercano al color del bloque.
        - Redimensiona la imagen de la biblioteca al tamaño del bloque.
        - Reemplaza el bloque en la imagen ampliada con la imagen redimensionada de la biblioteca.
    - Convierte la imagen final de vuelta a formato PIL.

5. **Resultado**:
    - Devuelve la imagen procesada con el filtro de mosaico aplicado.


### Explicación del Algoritmo

Para determinar la imagen de la biblioteca que mejor se ajusta a un bloque de la imagen objetivo, se utiliza la distancia euclidiana entre los colores promedio de las imágenes. El algoritmo busca la imagen de la biblioteca cuyo color promedio es el más cercano al el color promedio del bloque de entre todas las imágenes de la biblioteca. Definido por la fórmula:

```
distancia = sqrt((R1 - R2)^2 + (G1 - G2)^2 + (B1 - B2)^2)
```

Para acelerar la búsqueda de la imagen más cercana, se utiliza un KD-Tree que almacena los colores promedio de las imágenes de la biblioteca. El KD-Tree permite realizar búsquedas rápidas de los colores promedio más cercanos a un color dado. Esto reduce la complejidad de la búsqueda de O(n) a O(log n), donde n es el número de imágenes en la biblioteca.

### Implementación en Python

El código del filtro mosaico se encuentra en el archivo:

[backend/models/mosaico/mosaic_filter.py](../backend/models/mosaico/mosaic_filter.py)

### Explicación de un KD-Tree. Optimización de la búsqueda de colores promedio

Un KD-Tree (K-Dimensional Tree) es una estructura de datos utilizada para organizar puntos en un espacio k-dimensional. En el contexto del filtro de mosaico, el KD-Tree se utiliza para realizar búsquedas rápidas de los colores promedio de las imágenes en la biblioteca que podemos pensar como puntos en un espacio tridimensional (R, G, B).

El KD-Tree divide el espacio k-dimensional en regiones más pequeñas, de modo que los puntos cercanos en el espacio se encuentran cerca en el árbol. Esto permite realizar búsquedas eficientes de los puntos más cercanos a un punto dado en el espacio.

La forma en que se divide el espacio k-dimensional depende de la dimensión actual del árbol. Por ejemplo, si el árbol está en la dimensión x, se divide el espacio en regiones verticales. Si el árbol está en la dimensión y, se divide el espacio en regiones horizontales. Este proceso se repite hasta que se alcanza una profundidad máxima o se han insertado todos los puntos en el árbol.

Cuando se realiza una búsqueda en el KD-Tree, se comienza en la raíz y se desciende por el árbol hasta llegar a una hoja. En cada paso, se elige la rama que está más cerca del punto de búsqueda. Una vez que se llega a una hoja, se compara el punto en la hoja con el punto de búsqueda y se actualiza el punto más cercano si es necesario. Luego, se retrocede por el árbol, verificando si hay regiones no exploradas que puedan contener puntos más cercanos.

El uso de un KD-Tree en el filtro de mosaico permite realizar búsquedas eficientes de los colores promedio más cercanos a un color dado, lo que acelera significativamente el proceso de encontrar la imagen de la biblioteca que mejor se ajusta a un bloque de la imagen objetivo.

### Optimizaciones Aplicadas en el Código

1. **Multiprocesamiento con `multiprocessing.Pool`**
   - **Descripción**: Se utiliza el módulo `multiprocessing` para paralelizar el procesamiento de imágenes y bloques, aprovechando múltiples núcleos de CPU.
   - **Implementación**:
     - **Preprocesamiento de la Biblioteca de Imágenes**: La función `preprocess_image_library` utiliza un `Pool` para calcular los colores promedio de múltiples imágenes en paralelo.
     - **Procesamiento de Bloques**: Durante la aplicación del filtro mosaico, se distribuyen los bloques de la imagen a través de varios procesos para acelerar la búsqueda y reemplazo de bloques.
   - **Beneficios**:
     - **Reducción del Tiempo de Ejecución**: Al distribuir las tareas entre múltiples procesos, se reduce significativamente el tiempo total de procesamiento, especialmente en sistemas con múltiples núcleos.
     - **Eficiencia en el Uso de Recursos**: Se aprovechan al máximo los recursos disponibles del sistema, mejorando la velocidad sin necesidad de incrementar la complejidad del código.

2. **Uso de `scipy.spatial.cKDTree` para Búsquedas Eficientes**
   - **Descripción**: Se implementa un KD-Tree (`cKDTree`) para realizar búsquedas rápidas del color más cercano en la biblioteca de imágenes.
   - **Implementación**:
     - **Construcción del KD-Tree**: Después de calcular los colores promedio de las imágenes de la biblioteca, se construye un `cKDTree` a partir de estos colores.
     - **Consultas Rápidas**: Durante la aplicación del filtro, se utiliza el KD-Tree para encontrar la imagen más cercana al color promedio de cada bloque de manera eficiente.
   - **Beneficios**:
     - **Optimización de Búsquedas**: Las búsquedas de vecinos más cercanos son mucho más rápidas en comparación con métodos de fuerza bruta, especialmente cuando se trabaja con grandes conjuntos de datos.
     - **Escalabilidad**: Permite manejar bibliotecas de imágenes de gran tamaño sin un incremento significativo en el tiempo de búsqueda.

3. **Caché con `functools.lru_cache`**
   - **Descripción**: Se utiliza el decorador `@lru_cache` para almacenar en caché los resultados de funciones costosas que se llaman repetidamente con los mismos argumentos.
   - **Implementación**:
     - **Redimensionamiento de Imágenes de Biblioteca**: La función `get_resized_tile` está decorada con `@lru_cache` para almacenar en caché las imágenes redimensionadas, evitando recalcular tamaños ya procesados.
   - **Beneficios**:
     - **Reducción de Cálculos Redundantes**: Al almacenar en caché los resultados, se evita el procesamiento repetido de las mismas imágenes, lo que mejora la eficiencia.
     - **Mejora en el Rendimiento**: Disminuye el tiempo de ejecución al reutilizar resultados previamente calculados.

4. **Gestión Eficiente de la Memoria**
   - **Descripción**: Se implementan técnicas para gestionar y liberar memoria de manera efectiva, evitando el consumo excesivo durante el procesamiento de imágenes.
   - **Implementación**:
     - **Liberación de Recursos**: Uso de `del` para eliminar variables que ya no son necesarias y `gc.collect()` para forzar la recolección de basura.
     - **Optimización de Datos**: Conversión de datos a tipos más eficientes (e.g., `np.float32` en lugar de `int` donde es apropiado).
   - **Beneficios**:
     - **Prevención de Fugas de Memoria**: Garantiza que la memoria se libere adecuadamente, evitando que el programa consuma más memoria de la necesaria.
     - **Mejora en la Escalabilidad**: Permite procesar imágenes de mayor tamaño o mayor cantidad sin exceder los límites de memoria del sistema.

5. **Manejo de Errores y Registro de Imágenes Corruptas**
   - **Descripción**: Se implementa un sistema robusto para manejar imágenes corruptas o errores durante el procesamiento.
   - **Implementación**:
     - **Verificación de Integridad**: Uso de `PIL.Image.verify()` para verificar la integridad de las imágenes antes de procesarlas.
     - **Registro de Errores**: Captura y registro de imágenes que no pudieron ser procesadas, almacenándolas en un archivo de log y moviéndolas a una carpeta específica.
   - **Beneficios**:
     - **Robustez del Programa**: Evita que errores en imágenes individuales detengan todo el proceso de preprocesamiento.
     - **Facilidad de Depuración**: Permite identificar y manejar fácilmente las imágenes problemáticas, mejorando la fiabilidad del sistema.

6. **Optimización con `contextlib.redirect_stderr`**
   - **Descripción**: Se utiliza `contextlib.redirect_stderr` para suprimir mensajes de error no críticos durante el procesamiento de imágenes.
   - **Implementación**:
     - **Silenciamiento de Errores de OpenCV**: Redirige la salida de errores de OpenCV a `os.devnull`, evitando que mensajes de error no esenciales se impriman en la consola.
   - **Beneficios**:
     - **Salida Limpia**: Mejora la legibilidad de los logs al evitar la contaminación con mensajes de error irrelevantes.
     - **Enfoque en Errores Relevantes**: Permite centrarse en errores críticos que realmente afectan al procesamiento.

7. **Uso Eficiente de `os.walk` para Recorrer Directorios**
   - **Descripción**: Se emplea `os.walk` para recorrer de manera eficiente los directorios y subdirectorios en busca de imágenes.
   - **Implementación**:
     - **Filtrado de Extensiones**: Solo se consideran archivos con extensiones válidas (`.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.tiff`), reduciendo el tiempo de procesamiento al ignorar archivos no pertinentes.
   - **Beneficios**:
     - **Eficiencia en la Búsqueda**: Minimiza el número de archivos procesados, enfocándose únicamente en aquellos que son relevantes para el filtro mosaico.
     - **Escalabilidad**: Permite manejar grandes cantidades de archivos de manera efectiva sin incurrir en sobrecarga innecesaria.

8. **Conversión Eficiente de Colores con NumPy**
   - **Descripción**: Se utiliza NumPy para realizar operaciones vectorizadas en los arreglos de imágenes, optimizando el cálculo de colores promedio.
   - **Implementación**:
     - **Cálculo de Promedios**: Uso de `np.mean` para calcular los colores promedio de manera eficiente sobre ejes específicos de los arreglos.
     - **Conversión de Formatos**: Transformación entre formatos de color (e.g., RGB a BGR) utilizando funciones optimizadas como `cv2.cvtColor`.
   - **Beneficios**:
     - **Velocidad de Cálculo**: Las operaciones vectorizadas de NumPy son significativamente más rápidas que los bucles explícitos en Python.
     - **Simplicidad del Código**: Reduce la complejidad del código al aprovechar operaciones predefinidas y altamente optimizadas.

9. **Uso de Tipos y Anotaciones (`typing`)**
   - **Descripción**: Se incorporan anotaciones de tipo para mejorar la claridad del código y facilitar el mantenimiento.
   - **Implementación**:
     - **Anotaciones de Funciones**: Uso de `Optional`, `Dict`, `Tuple`, y `List` para especificar los tipos de parámetros y valores de retorno.
   - **Beneficios**:
     - **Legibilidad**: Mejora la comprensión del código para otros desarrolladores y para futuras revisiones.
     - **Herramientas de Desarrollo**: Facilita el uso de herramientas de análisis estático y entornos de desarrollo integrados (IDEs) que aprovechan las anotaciones de tipo para ofrecer mejores sugerencias y detección de errores.

10. **Optimización de Lectura y Escritura con Pandas**
    - **Descripción**: Se utiliza `pandas` para manejar de manera eficiente la lectura y escritura de datos en formato CSV.
    - **Implementación**:
      - **Lectura Eficiente**: Especificación de tipos de datos al leer el CSV para optimizar el uso de memoria y la velocidad de carga.
      - **Escritura Eficiente**: Uso de `pandas.DataFrame.to_csv` para escribir los datos procesados de manera rápida y organizada.
    - **Beneficios**:
      - **Rendimiento Mejorado**: `pandas` está altamente optimizado para manejar grandes conjuntos de datos de manera eficiente.
      - **Facilidad de Uso**: Simplifica las operaciones de manipulación de datos, permitiendo escribir código más limpio y conciso.

11. **Gestión de Variables Globales para Procesos**
    - **Descripción**: Se manejan variables globales para compartir datos entre procesos en el pool de `multiprocessing`.
    - **Implementación**:
      - **Inicialización de Trabajadores**: La función `init_worker` establece el `KD-Tree` y las rutas de imágenes como variables globales en cada proceso.
    - **Beneficios**:
      - **Reducción de Overhead**: Evita la necesidad de pasar grandes estructuras de datos a través de la memoria compartida, ya que cada proceso tiene acceso a las variables globales.
      - **Simplicidad en el Acceso a Datos**: Facilita el acceso a datos compartidos sin complicaciones adicionales en la lógica de la función.

12. **Uso de `gc.collect` para Recolección de Basura**
    - **Descripción**: Se llama explícitamente a `gc.collect()` para forzar la recolección de objetos no referenciados, liberando memoria de manera proactiva.
    - **Implementación**:
      - **Liberación de Memoria Innecesaria**: Después de operaciones pesadas como el redimensionamiento de imágenes, se elimina el arreglo original y se invoca `gc.collect()`.
    - **Beneficios**:
      - **Gestión Proactiva de Memoria**: Ayuda a liberar memoria de manera inmediata, evitando la acumulación de objetos no utilizados que podrían llevar a un consumo excesivo de memoria.
      - **Estabilidad del Programa**: Mantiene el uso de memoria bajo control, mejorando la estabilidad y la capacidad del programa para manejar grandes volúmenes de datos.

13. **Supresión de Salida de Errores No Críticos**
    - **Descripción**: Se utiliza `contextlib.redirect_stderr` para redirigir la salida de errores no críticos a `os.devnull`, evitando que mensajes irrelevantes ensucien la salida estándar.
    - **Implementación**:
      - **Silenciamiento de Mensajes de Error**: Durante la carga de imágenes con OpenCV, se redirige la salida de errores para mantener la consola limpia.
    - **Beneficios**:
      - **Claridad en los Logs**: Permite centrarse en mensajes de error relevantes y evita la sobrecarga de información innecesaria.
      - **Experiencia de Usuario Mejorada**: Proporciona una salida más limpia y profesional, especialmente útil en entornos de producción.

14. **Optimización en la Construcción de Bloques para el Filtro Mosaico**
    - **Descripción**: Se optimiza la creación y procesamiento de bloques de la imagen para aplicar el filtro mosaico de manera eficiente.
    - **Implementación**:
      - **Determinación de Tamaños de Bloque Correctos**: Calcula dinámicamente el tamaño de los bloques para manejar los bordes de la imagen sin errores.
      - **Estructuración de Datos para Multiprocesamiento**: Organiza las coordenadas y datos necesarios para cada bloque de manera estructurada para su procesamiento paralelo.
    - **Beneficios**:
      - **Eficiencia en el Procesamiento**: Asegura que cada bloque se procese correctamente sin redundancias ni errores, optimizando el uso de recursos.
      - **Flexibilidad**: Permite manejar imágenes de diversos tamaños y formatos de manera robusta y adaptable.

15. **Uso de Tipos de Datos Específicos en Pandas**
    - **Descripción**: Al leer el CSV, se especifican los tipos de datos para optimizar la carga y el uso de memoria.
    - **Implementación**:
      - **Especificación de `dtype` en `pd.read_csv`**: Define explícitamente los tipos de datos para cada columna (`'image_path': str, 'B': np.float32, 'G': np.float32, 'R': np.float32`).
    - **Beneficios**:
      - **Reducción del Uso de Memoria**: Tipos de datos más pequeños (`float32` en lugar de `float64`) disminuyen el consumo de memoria.
      - **Aceleración de la Lectura**: La especificación de tipos permite a `pandas` optimizar la lectura del archivo, mejorando la velocidad.

16. **Evitación de Reprocesamiento Innecesario con Verificación de Existencia de CSV**
    - **Descripción**: Antes de preprocesar la biblioteca de imágenes, se verifica si el archivo CSV con los colores promedio ya existe.
    - **Implementación**:
      - **Comprobación de Existencia de CSV**: Si el CSV no existe, se procede al preprocesamiento; de lo contrario, se carga directamente.
    - **Beneficios**:
      - **Ahorro de Tiempo**: Evita recalcular colores promedio para una biblioteca de imágenes que ya ha sido procesada previamente.
      - **Eficiencia en el Flujo de Trabajo**: Permite reutilizar datos existentes, mejorando la eficiencia del proceso general.
