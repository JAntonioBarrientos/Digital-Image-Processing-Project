from flask import Blueprint, request, send_file
from services.image_service import ImageService
from io import BytesIO
from flask import Flask, jsonify, request
from status import preprocessing_status
from models.mosaico.mosaic_filter import MosaicFilter
import os
from PIL import Image
import time

# Definir el controlador como un Blueprint para manejar las rutas de la imagen
image_controller = Blueprint('image_controller', __name__)

@image_controller.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        'preprocessing': preprocessing_status.get_preprocessing()
    })


# Ruta para aplicar el filtro de escala de grises
@image_controller.route('/apply-grayscale', methods=['POST'])
def apply_grayscale():
    if 'image' not in request.files:
        return "No image file uploaded", 400
    
    image_file = request.files['image']

    # Medir el tiempo de procesamiento
    start_time = time.time()


    image_service = ImageService(image_file)
    processed_image = image_service.apply_grayscale_filter()

    # Calcular el tiempo transcurrido
    elapsed_time = time.time() - start_time
    print(f"Tiempo de procesamiento del filtro grayscale: {elapsed_time:.2f} segundos")


    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

# Ruta para aplicar el filtro de escala de grises ponderado
@image_controller.route('/apply-gray-weighted', methods=['POST'])
def apply_gray_weighted():
    if 'image' not in request.files:
        return "No image file uploaded", 400
    
    image_file = request.files['image']

    start_time = time.time()

    image_service = ImageService(image_file)
    processed_image = image_service.apply_gray_filter_weighted()

    elapsed_time = time.time() - start_time
    print(f"Tiempo de procesamiento del filtro grayscale weighted: {elapsed_time:.2f} segundos")

    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

# Ruta para aplicar el filtro de mica
@image_controller.route('/apply-mica-filter', methods=['POST'])
def apply_mica_filter():
    if 'image' not in request.files:
        return "No image file uploaded", 400

    # Obtener los valores R, G, B del formulario
    try:
        r_value = int(request.form['r_value'])
        g_value = int(request.form['g_value'])
        b_value = int(request.form['b_value'])
    except (ValueError, KeyError):
        return "Valores RGB inválidos o faltantes", 400

    # Validar que los valores estén en el rango correcto
    if not (0 <= r_value <= 255 and 0 <= g_value <= 255 and 0 <= b_value <= 255):
        return "Los valores de RGB deben estar entre 0 y 255", 400
    
    image_file = request.files['image']

    time_start = time.time()
    image_service = ImageService(image_file)
    processed_image = image_service.apply_mica_filter(r_value, g_value, b_value)

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro mica: {elapsed_time:.2f} segundos")

    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')


# Ruta para aplicar el filtro de desenfoque (Blur)
@image_controller.route('/apply-blur', methods=['POST'])
def apply_blur():
    if 'image' not in request.files:
        return "No image file uploaded", 400
    
    image_file = request.files['image']
    
    # Obtener la intensidad del blur desde el formulario
    try:
        intensity = int(request.form['intensity'])
    except (ValueError, KeyError):
        return "Intensidad inválida o faltante", 400

    # Validar que la intensidad esté en el rango correcto
    if not (1 <= intensity <= 25):
        return "La intensidad debe estar entre 1 y 25", 400

    # Procesar la imagen aplicando el filtro de Blur
    start_time = time.time()

    image_service = ImageService(image_file)
    processed_image = image_service.apply_blur_filter(intensity)

    elapsed_time = time.time() - start_time
    print(f"Tiempo de procesamiento del filtro blur: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)  # Mover el cursor al inicio del flujo

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')

# Ruta para aplicar el filtro diagonal personalizado
@image_controller.route('/apply-custom-diagonal-filter', methods=['POST'])
def apply_custom_diagonal_filter():
    if 'image' not in request.files:
        return "No image file uploaded", 400

    image_file = request.files['image']

    # Obtener la intensidad del filtro desde el formulario
    try:
        intensity = int(request.form['intensity'])
    except (ValueError, KeyError):
        return "Intensidad inválida o faltante", 400

    # Validar que la intensidad esté en el rango correcto
    if not (1 <= intensity <= 25):
        return "La intensidad debe estar entre 1 y 25", 400

    # Procesar la imagen aplicando el filtro diagonal personalizado
    time_start = time.time()

    image_service = ImageService(image_file)
    processed_image = image_service.apply_custom_diagonal_filter(intensity)

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro diagonal personalizado: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)  # Mover el cursor al inicio del flujo

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')

# Ruta para aplicar el filtro de detección de bordes (Find Edges)
@image_controller.route('/apply-find-edges', methods=['POST'])
def apply_find_edges():
    if 'image' not in request.files:
        return "No image file uploaded", 400

    image_file = request.files['image']

    # Procesar la imagen aplicando el filtro de detección de bordes
    time_start = time.time()

    image_service = ImageService(image_file)
    processed_image = image_service.apply_find_edges_filter()

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de detección de bordes: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)  # Mover el cursor al inicio del flujo

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')

# Ruta para aplicar el filtro de afilado (Sharpen)
@image_controller.route('/apply-sharpen', methods=['POST'])
def apply_sharpen():
    if 'image' not in request.files:
        return "No image file uploaded", 400

    image_file = request.files['image']

    # Procesar la imagen aplicando el filtro de afilado

    time_start = time.time()
    image_service = ImageService(image_file)
    processed_image = image_service.apply_sharpen_filter()

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de afilado: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)  # Mover el cursor al inicio del flujo

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')


# Ruta para aplicar el filtro de emboss (Emboss)
@image_controller.route('/apply-emboss', methods=['POST'])
def apply_emboss():
    if 'image' not in request.files:
        return "No image file uploaded", 400

    image_file = request.files['image']

    # Procesar la imagen aplicando el filtro de Emboss
    time_start = time.time()
    image_service = ImageService(image_file)
    processed_image = image_service.apply_emboss_filter()

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de emboss: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)  # Mover el cursor al inicio del flujo

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')

# Ruta para aplicar el filtro de promedio (Mean Filter)
@image_controller.route('/apply-mean-filter', methods=['POST'])
def apply_mean_filter():
    if 'image' not in request.files:
        return "No image file uploaded", 400
    
    image_file = request.files['image']

    # Procesar la imagen aplicando el filtro de promedio

    time_start = time.time()
    image_service = ImageService(image_file)
    processed_image = image_service.apply_mean_filter()

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de promedio: {elapsed_time:.2f} segundos")
    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)  # Mover el cursor al inicio del flujo

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')

# Ruta para aplicar el filtro de imagen recursiva escala de grises

@image_controller.route('/apply-recursive-image-gray', methods=['POST'])
def apply_recursive_image_gray():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    image_file = request.files['image']

    # Obtener el número de variantes de la imagen desde el formulario
    try:
        n_variantes = int(request.form['n_variantes'])
    except (ValueError, KeyError):
        return jsonify({"error": "Valor inválido o faltante para 'n_variantes'"}), 400

    # Obtener el upscale_factor
    try:
        upscale_factor = float(request.form['upscale_factor'])
        if upscale_factor < 1:
            raise ValueError
    except (ValueError, KeyError):
        return jsonify({"error": "Valor inválido o faltante para 'upscale_factor'. Debe ser un número mayor o igual a 1."}), 400

    # Obtener grid_rows
    try:
        grid_rows = int(request.form['grid_rows'])
        if grid_rows < 1:
            raise ValueError
    except (ValueError, KeyError):
        return jsonify({"error": "Valor inválido o faltante para 'grid_rows'. Debe ser un entero mayor o igual a 1."}), 400

    # Obtener grid_cols
    try:
        grid_cols = int(request.form['grid_cols'])
        if grid_cols < 1:
            raise ValueError
    except (ValueError, KeyError):
        return jsonify({"error": "Valor inválido o faltante para 'grid_cols'. Debe ser un entero mayor o igual a 1."}), 400

    # Procesar la imagen aplicando el filtro de imagen recursiva escala de grises
    time_start = time.time()

    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_recursive_gray_filter(
            n_variantes, upscale_factor, grid_rows, grid_cols
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de imagen recursiva escala de grises: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')


# Ruta para aplicar el filtro de imagen recursiva a color

@image_controller.route('/apply-recursive-image-color', methods=['POST'])
def apply_recursive_image_color():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    image_file = request.files['image']

    # Obtener el upscale_factor
    try:
        upscale_factor = float(request.form['upscale_factor'])
        if upscale_factor < 1:
            raise ValueError
    except (ValueError, KeyError):
        return jsonify({"error": "Valor inválido o faltante para 'upscale_factor'. Debe ser un número mayor o igual a 1."}), 400

    # Obtener grid_rows
    try:
        grid_rows = int(request.form['grid_rows'])
        if grid_rows < 1:
            raise ValueError
    except (ValueError, KeyError):
        return jsonify({"error": "Valor inválido o faltante para 'grid_rows'. Debe ser un entero mayor o igual a 1."}), 400

    # Obtener grid_cols
    try:
        grid_cols = int(request.form['grid_cols'])
        if grid_cols < 1:
            raise ValueError
    except (ValueError, KeyError):
        return jsonify({"error": "Valor inválido o faltante para 'grid_cols'. Debe ser un entero mayor o igual a 1."}), 400

    # Procesar la imagen aplicando el filtro de imagen recursiva escala de grises
    time_start = time.time()

    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_recursive_color_filter(
            upscale_factor, grid_rows, grid_cols
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de imagen recursiva escala de grises: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')



# Ruta para aplicar el filtro de watermark

@image_controller.route('/apply-watermark-filter', methods=['POST'])
def apply_watermark():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    image_file = request.files['image']

    # Obtener el texto de la marca de agua desde el formulario
    try:
        texto = request.form['text']
    except KeyError:
        return jsonify({"error": "Texto de marca de agua faltante"}), 400

    # Obtener las coordenadas (x, y) de la marca de agua desde el formulario
    try:
        x = int(request.form['x_coord'])
        y = int(request.form['y_coord'])
        coordenadas = (x, y)
    except (ValueError, KeyError):
        return jsonify({"error": "Coordenadas de marca de agua inválidas o faltantes"}), 400

    # Obtener el valor de transparencia (alpha) desde el formulario
    try:
        alpha = float(request.form['alpha'])
    except (ValueError, KeyError):
        return jsonify({"error": "Valor de transparencia (alpha) inválido o faltante"}), 400

    # Obtener el tamaño de la fuente desde el formulario
    try:
        tamaño_fuente = int(request.form['font_size'])
    except (ValueError, KeyError):
        return jsonify({"error": "Tamaño de fuente inválido o faltante"}), 400

    # Procesar la imagen aplicando el filtro de marca de agua
    time_start = time.time()

    image_service = ImageService(image_file)
    processed_image = image_service.apply_watermark_filter(texto, coordenadas, alpha, tamaño_fuente)

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de marca de agua: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')

@image_controller.route('/remove-red-watermark', methods=['POST'])
def remove_red_watermark():
    # Verificar si se ha subido una imagen
    if 'image' not in request.files:
        return jsonify({"error": "No se ha subido ningún archivo de imagen"}), 400
    
    image_file = request.files['image']
    
    # Obtener el valor de sensibilidad desde el formulario, con un valor por defecto
    sensitivity = 100  # Valor por defecto
    if 'sensitivity' in request.form:
        try:
            sensitivity = int(request.form['sensitivity'])
            if not (0 <= sensitivity <= 255):
                raise ValueError
        except ValueError:
            return jsonify({"error": "El valor de sensibilidad debe ser un entero entre 0 y 255"}), 400
    
    # Procesar la imagen aplicando el filtro de eliminación de marcas de agua rojas
    time_start = time.time()
    
    try:
        image_service = ImageService(image_file)
        processed_image = image_service.remove_red_watermark(sensitivity)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de eliminación de marca de agua roja: {elapsed_time:.2f} segundos")
    
    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)
    
    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')

    
# Ruta para aplicar el filtro de watermark diagonal

@image_controller.route('/apply-watermark-filter-diagonal', methods=['POST'])
def apply_watermark_diagonal():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    image_file = request.files['image']

    # Obtener el texto de la marca de agua desde el formulario
    try:
        texto = request.form['text']
    except KeyError:
        return jsonify({"error": "Texto de marca de agua faltante"}), 400

    
    # Obtener el valor de transparencia (alpha) desde el formulario
    try:
        alpha = float(request.form['alpha'])
    except (ValueError, KeyError):
        return jsonify({"error": "Valor de transparencia (alpha) inválido o faltante"}), 400

    # Obtener el tamaño de la fuente desde el formulario
    try:
        tamaño_fuente = int(request.form['font_size'])
    except (ValueError, KeyError):
        return jsonify({"error": "Tamaño de fuente inválido o faltante"}), 400

    # Procesar la imagen aplicando el filtro de marca de agua
    time_start = time.time()

    image_service = ImageService(image_file)
    processed_image = image_service.apply_watermark_diagonal_filter(texto, alpha, tamaño_fuente)

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de marca de agua diagonal: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')


# Ruta para aplicar el filtro de semitonos con circulos de varios tamaños
@image_controller.route('/apply-halftones-filter', methods=['POST'])
def apply_halftones_filter():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    image_file = request.files['image']

    # Obtener el número de variantes de la imagen desde el formulario
    try:
        n_variantes = int(request.form['n_variantes'])
    except (ValueError, KeyError):
        return jsonify({"error": "Valor inválido o faltante para 'n_variantes'"}), 400


    # Procesar la imagen aplicando el filtro de imagen recursiva escala de grises
    time_start = time.time()

    image_service = ImageService(image_file)
    try:
        # Llamar al método de procesamiento con full_resolution en lugar de grid_factor
        processed_image = image_service.apply_halftones_filter(n_variantes)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de semitonos: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')

# Ruta para aplicar el filtro de dithering aleatorio
@image_controller.route('/apply-random-dithering', methods=['POST'])
def apply_random_dithering():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    # Obtener la imagen del formulario
    image_file = request.files['image']

    # Procesar la imagen aplicando el filtro de dithering aleatorio
    time_start = time.time()

    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_random_dithering_filter()
    except Exception as e:
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de dithering aleatorio: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')


# Ruta para aplicar el filtro de dithering ordenado
@image_controller.route('/apply-clustered-dithering', methods=['POST'])
def apply_clustered_dithering():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    # Obtener la imagen del formulario
    image_file = request.files['image']

    # Procesar la imagen aplicando el filtro de dithering ordenado
    time_start = time.time()

    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_clustered_dithering_filter()
    except Exception as e:
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de dithering ordenado: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')


# Ruta para aplicar el filtro de dithering disperso
@image_controller.route('/apply-dispersed-dithering', methods=['POST'])
def apply_dispersed_dithering():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    # Obtener la imagen del formulario
    image_file = request.files['image']

    # Procesar la imagen aplicando el filtro de dithering disperso
    start_time = time.time()

    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_dispersed_dithering_filter()
    except Exception as e:
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

    elapsed_time = time.time() - start_time
    print(f"Tiempo de procesamiento del filtro de dithering disperso: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')

# Ruta para aplicar el filtro de dithering Floyd-Steinberg
@image_controller.route('/apply-floyd-steinberg-dithering', methods=['POST'])
def apply_floyd_steinberg_dithering():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    # Obtener la imagen del formulario
    image_file = request.files['image']

    # Procesar la imagen aplicando el filtro de dithering Floyd-Steinberg
    time_start = time.time()

    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_floyd_steinberg_dithering_filter()
    except Exception as e:
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de dithering Floyd-Steinberg: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')


# Ruta para aplicar el filtro de Oleo
@image_controller.route('/apply-oleo-filter', methods=['POST'])
def apply_oleo_filter():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    # Obtener la imagen del formulario
    image_file = request.files['image']
    color = request.form['color'].lower() == 'true'
    blur = request.form['blur'].lower() == 'true'
    block_size = int(request.form['blockSize'])

    # Procesar la imagen aplicando el filtro de Oleo
    time_start = time.time()

    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_oleo_filter(color, blur, block_size)
    except Exception as e:
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de Oleo: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')


# Ruta para aplicar el filtro de erosion minimo maximo
@image_controller.route('/apply-min-filter', methods=['POST'])
def apply_min_filter():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    # Obtener la imagen del formulario
    image_file = request.files['image']
    radius = int(request.form['radius'])

    # Procesar la imagen aplicando el filtro minimo
    time_start = time.time()

    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_min_max_filter(radius, 'min')
    except Exception as e:
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

    elapsed_time = time.time() - time_start

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')


# Ruta para aplicar el filtro de erosión máximo
@image_controller.route('/apply-max-filter', methods=['POST'])
def apply_max_filter():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    # Obtener la imagen del formulario
    image_file = request.files['image']
    radius = int(request.form['radius'])

    # Procesar la imagen aplicando el filtro máximo
    time_start = time.time()

    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_min_max_filter(radius, 'max')
    except Exception as e:
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

    elapsed_time = time.time() - time_start
    print(f"Tiempo de procesamiento del filtro de erosión máximo: {elapsed_time:.2f} segundos")

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')

# Ruta para aplicar el filtro mosaico
@image_controller.route('/apply-mosaic-filter', methods=['POST'])
def apply_mosaic_filter():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    # Obtener la imagen del formulario
    image_file = request.files['image']

    # Obtener los parámetros enviados en el formulario
    try:
        block_width = int(request.form.get('block_width', 10))
        block_height = int(request.form.get('block_height', 10))
        upscale_factor = int(request.form.get('upscale_factor', 1))
    except ValueError:
        return jsonify({"error": "Los parámetros deben ser números enteros"}), 400

    # Procesar la imagen aplicando el filtro mosaico

    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_mosaic_filter(block_width, block_height, upscale_factor)
    except Exception as e:
        print("Error al aplicar el filtro: " + str(e))
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')

# Ruta para reiniciar el preprocesamiento de la biblioteca de imágenes
@image_controller.route('/reset-preprocessing', methods=['POST'])
def reset_preprocessing():
    mosaic_filter = MosaicFilter(Image.new('RGB', (1, 1), color='white'))
    try:
        if os.path.exists(mosaic_filter.csv_file):
            os.remove(mosaic_filter.csv_file)  # Eliminar el archivo CSV
        mosaic_filter = MosaicFilter(Image.new('RGB', (1, 1), color='white')) # Ejecutar el preprocesamiento nuevamente
        return jsonify({"status": "Preprocesamiento reiniciado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

