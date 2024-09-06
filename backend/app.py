from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para evitar problemas de acceso desde React

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="¡Hola desde el backend en Flask!")

if __name__ == '__main__':
    app.run(debug=True)
