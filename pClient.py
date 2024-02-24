from flask import Flask, jsonify

import grpc
import pserver_pb2
import pserver_pb2_grpc

# URL del servidor principal
SERVER_URL = "http://localhost:5000"

# Inicializar la aplicación Flask
app = Flask(__name__)

# Funciones para comunicarse con el servidor principal usando API REST

@app.route('/join', methods=['POST'])
def join():
    # Implementa la lógica para unirse a la red en el servidor principal
    # Puedes manejar la lógica de unión aquí y devolver una respuesta adecuada
    return jsonify({'message': 'Joined the network successfully.'}), 200

@app.route('/leave', methods=['POST'])
def leave():
    # Implementa la lógica para abandonar la red en el servidor principal
    # Puedes manejar la lógica de abandono aquí y devolver una respuesta adecuada
    return jsonify({'message': 'Left the network successfully.'}), 200

@app.route('/addFile', methods=['POST'])
def add_file_to_server():
    # Implementa la lógica para agregar un archivo al servidor principal
    # Puedes manejar la lógica de agregar archivo aquí y devolver una respuesta adecuada
    return jsonify({'message': 'File added to the server successfully.'}), 200

@app.route('/index', methods=['POST'])
def index():
    # Implementa la lógica para indexar los archivos en el servidor principal
    # Puedes manejar la lógica de indexación aquí y devolver una respuesta adecuada
    return jsonify({'message': 'Server indexed successfully.'}), 200




# Funciones para comunicarse con el pserver usando gRPC

def upload_file_to_pserver(file_name):
    # Implementa la lógica para cargar un archivo al pserver usando gRPC
    pass

def download_file_from_pserver(file_name):
    # Implementa la lógica para descargar un archivo del pserver usando gRPC
    pass

def main():
    # Ejecutar la aplicación Flask en un hilo separado
    app.run(debug=True, port=5001)

if __name__ == "__main__":
    main()
