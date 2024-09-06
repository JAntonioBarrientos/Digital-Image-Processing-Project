from flask import Blueprint, request
from services.image_service import ImageService

image_controller = Blueprint('image_controller', __name__)

@image_controller.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    image_service = ImageService(file)
    return image_service.process_image()
