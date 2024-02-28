import requests
import sys
import configparser

# URL del servidor principal
SERVER_URL = "http://localhost:5000"

def join(peer_id, ip_address):
    # Datos a enviar al servidor principal
    data = {
        'peer_id': peer_id,  # Usar el ID del peer proporcionado por el archivo de configuración
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

def get_peer_config():
    config = configparser.ConfigParser()
    config.read('peerConfig.ini')
    peer_id = config['peer']['peer_id']
    host = config['peer']['host']
    port = config['peer']['port']
    server_host = config['server']['host']
    server_port = config['server']['port']
    return peer_id, host, port, server_host, server_port



def main():
    # Obtener la configuración del archivo de configuración
    peer_id, host, port, server_host, server_port = get_peer_config()
    ip_address = f"{host}:{port}"
    SERVER_URL = f"{server_host}:{server_port}"
    
    print("Server url from config: ", SERVER_URL)
    print("Peer ID from config:", peer_id)
    print("IP address from config:", ip_address)

    # Unirse a la red
    join(peer_id, ip_address)

    # Indexar un archivo
    index_file()

if __name__ == "__main__":
    main()
