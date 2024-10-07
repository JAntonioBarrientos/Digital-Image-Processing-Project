from flask import Blueprint, request, send_file
from services.image_service import ImageService
from io import BytesIO
from flask import jsonify

# Definir el controlador como un Blueprint para manejar las rutas de la imagen
image_controller = Blueprint('image_controller', __name__)

# Ruta para aplicar el filtro de escala de grises
@image_controller.route('/apply-grayscale', methods=['POST'])
def apply_grayscale():
    if 'image' not in request.files:
        return "No image file uploaded", 400
    
    image_file = request.files['image']
    image_service = ImageService(image_file)
    processed_image = image_service.apply_grayscale_filter()

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
    image_service = ImageService(image_file)
    processed_image = image_service.apply_gray_filter_weighted()

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
    image_service = ImageService(image_file)
    processed_image = image_service.apply_mica_filter(r_value, g_value, b_value)

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
    image_service = ImageService(image_file)
    processed_image = image_service.apply_blur_filter(intensity)

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
    image_service = ImageService(image_file)
    processed_image = image_service.apply_custom_diagonal_filter(intensity)

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
    image_service = ImageService(image_file)
    processed_image = image_service.apply_find_edges_filter()

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
    image_service = ImageService(image_file)
    processed_image = image_service.apply_sharpen_filter()

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
    image_service = ImageService(image_file)
    processed_image = image_service.apply_emboss_filter()

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
    image_service = ImageService(image_file)
    processed_image = image_service.apply_mean_filter()

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

    try:
        grid_factor = int(request.form['grid_factor'])
    except ValueError:
        grid_factor = 50  # Si no puede convertir a entero, usar valor por defecto

    # Procesar la imagen aplicando el filtro de imagen recursiva escala de grises
    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_recursive_gray_filter(n_variantes, grid_factor)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')


# Ruta para aplicar el filtro de imagen recursiva escala de grises

@image_controller.route('/apply-recursive-image-color', methods=['POST'])
def apply_recursive_image_color():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    image_file = request.files['image']

    try:
        grid_factor = int(request.form['grid_factor'])
    except ValueError:
        grid_factor = 50  # Si no puede convertir a entero, usar valor por defecto

    # Procesar la imagen aplicando el filtro de imagen recursiva escala de grises
    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_recursive_color_filter(grid_factor)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

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
    image_service = ImageService(image_file)
    processed_image = image_service.apply_watermark_filter(texto, coordenadas, alpha, tamaño_fuente)

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
    image_service = ImageService(image_file)
    processed_image = image_service.apply_watermark_diagonal_filter(texto, alpha, tamaño_fuente)

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

    # Obtener el valor de full_resolution desde el formulario
    try:
        full_resolution = request.form['full_resolution'].lower() == 'true'
    except KeyError:
        full_resolution = False  # Valor por defecto si no se envía la bandera

    # Procesar la imagen aplicando el filtro de imagen recursiva escala de grises
    image_service = ImageService(image_file)
    try:
        # Llamar al método de procesamiento con full_resolution en lugar de grid_factor
        processed_image = image_service.apply_halftones_filter(n_variantes, full_resolution)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

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
    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_random_dithering_filter()
    except Exception as e:
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

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
    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_clustered_dithering_filter()
    except Exception as e:
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

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
    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_dispersed_dithering_filter()
    except Exception as e:
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

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
    image_service = ImageService(image_file)
    try:
        processed_image = image_service.apply_floyd_steinberg_dithering_filter()
    except Exception as e:
        return jsonify({"error": "Error al aplicar el filtro: " + str(e)}), 500

    # Guardar la imagen procesada en un flujo de bytes
    img_io = BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Enviar la imagen procesada de vuelta al frontend
    return send_file(img_io, mimetype='image/jpeg')