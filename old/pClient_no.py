import requests
import sys
import configparser
from flask import Flask

# Crear la aplicación Flask
app = Flask(__name__)

def join(peer_id, ip_address, server_url):
    # Datos a enviar al servidor principal
    data = {
        'peer_id': peer_id,
        'ip_address': ip_address
    }

    # Enviar la solicitud POST al servidor principal para unirse a la red
    response = requests.post(f"{server_url}/addPeer", json=data)
    if response.status_code == 200:
        print("Joined the network successfully.")
    else:
        print("Failed to join the network.")

def index_file(server_url):
    # Datos a enviar al servidor principal
    data = {
        'file_name': 'file1',
        'peer_id': 'autoassigned_id'
    }

    # Enviar la solicitud POST al servidor principal para indexar el archivo
    response = requests.post(f"{server_url}/addFile", json=data)
    if response.status_code == 200:
        print("File indexed successfully.")
    else:
        print("Failed to index the file.")

def get_peer_config():
    config = configparser.ConfigParser()
    config.read('peerConfig.ini')
    peer_id = config['peer']['peer_id']
    host = config['peer']['host']
    port = int(config['peer']['port'])  # Convertir el puerto a entero
    server_host = config['server']['host']
    server_port = int(config['server']['port'])  # Convertir el puerto a entero
    return peer_id, host, port, server_host, server_port

@app.route('/')
def index():
    return "Hello, World!"

def main():
    # Obtener la configuración del archivo de configuración
    peer_id, host, port, server_host, server_port = get_peer_config()
    ip_address = f"{host}:{port}"
    server_url = f"http://{server_host}:{server_port}"  # Construir la URL del servidor

    print("Peer ID from config:", peer_id)
    print("IP address from config:", ip_address)
    print("Server URL from config:", server_url)

    # Unirse a la red
    join(peer_id, ip_address, server_url)

    # Indexar un archivo
    index_file(server_url)

    # Ejecutar la aplicación Flask en el puerto especificado en el archivo de configuración
    app.run(debug=True, host=host, port=port)

if __name__ == "__main__":
    main()
