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

# Nueva ruta para aplicar el filtro de escala de grises ponderado
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
