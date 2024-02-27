import requests

import sys
import configparser

# URL del servidor principal
SERVER_URL = "http://localhost:5000"


def join(ip_address):
    # Datos a enviar al servidor principal
    data = {
        'peer_id': 'my_peer_id',  # Puedes autoasignar un ID aquí si lo deseas
        'ip_address': ip_address
    }

    # Enviar la solicitud POST al servidor principal para unirse a la red
    response = requests.post(f"{SERVER_URL}/addPeer", json=data)
    if response.status_code == 200:
        print("Joined the network successfully.")
    else:
        print("Failed to join the network.")

def index_file():
    # Datos a enviar al servidor principal
    data = {
        'file_name': 'file1',  # Nombre del archivo a indexar
        'peer_id': 'autoassigned_id'  # Puedes usar el mismo ID autoasignado
    }

    # Enviar la solicitud POST al servidor principal para indexar el archivo
    response = requests.post(f"{SERVER_URL}/addFile", json=data)
    if response.status_code == 200:
        print("File indexed successfully.")
    else:
        print("Failed to index the file.")

def main():
    config = configparser.ConfigParser()
    config.read('ServerConfig.ini')
    host = config['server']['host']
    port = int(config['server']['port'])

    # Unirse a la red
    join(port)

    # Indexar un archivo
    index_file()

if __name__ == "__main__":
    main()
