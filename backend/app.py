from flask import Flask
from controllers.image_controller import image_controller
from flask_cors import CORS

app = Flask(__name__)

# Habilitar CORS para permitir solicitudes desde cualquier origen
CORS(app)

# Registrar el controlador
app.register_blueprint(image_controller)

if __name__ == '__main__':
    app.run(debug=True)
