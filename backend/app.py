from flask import Flask
from controllers.image_controller import image_controller
from flask_cors import CORS
import os

app = Flask(__name__)

# Habilitar CORS para permitir solicitudes desde cualquier origen
CORS(app)

# Registrar el controlador
app.register_blueprint(image_controller)

# Asegurar que la carpeta data/imagen_con_letras exista
data_dir = os.path.join('data', 'imagen_con_letras')
os.makedirs(data_dir, exist_ok=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

