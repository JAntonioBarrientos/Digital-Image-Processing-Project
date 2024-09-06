from flask import Blueprint, request, send_file
from services.image_service import ImageService
from io import BytesIO

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
