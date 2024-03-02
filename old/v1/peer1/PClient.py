import sys
import configparser
import grpc
import p2p_pb2
import p2p_pb2_grpc
import requests

# URL del servidor principal
SERVER_URL = "http://localhost:5000" 


def join(peer_id, ip_address, server_url):
    # Datos a enviar al servidor principal
    data = {
        'peer_id': peer_id,  # Usar el ID del peer proporcionado por el archivo de configuración
        'ip_address': ip_address
    }

    # Enviar la solicitud POST al servidor principal para unirse a la red
    response = requests.post(f"{SERVER_URL}/addPeer", json=data)
    if response.status_code == 200:
        print("Joined the network successfully.")
        print("Server response:", response.json())
    else:
        print("Failed to join the network.")
        print("Server response:", response.json())


def index_file(peer_id, file_name, server_url):
    # Datos a enviar al servidor principal
    data = {
        'file_name': file_name,  # Nombre del archivo a indexar
        'peer_id': peer_id  # Puedes usar el mismo ID autoasignado
    }

    # Enviar la solicitud POST al servidor principal para indexar el archivo
    response = requests.post(f"{SERVER_URL}/addFile", json=data)
    if response.status_code == 200:
        print("File indexed successfully.")
        print("Server response:", response.json())
    else:
        print("Failed to index the file.")
        print("Server response:", response.json())



def leave(peer_id, ip_address, server_url):
    # Datos a enviar al servidor principal
    data = {
        'peer_id': peer_id,  # Usar el ID del peer proporcionado por el archivo de configuración
        'ip_address': ip_address
    }

    # Enviar la solicitud DELETE al servidor principal para abandonar la red
    response = requests.delete(f"{SERVER_URL}/deletePeer", params=data)
    if response.status_code == 200:
        print("Left the network successfully.")
        print("Server response:", response.json())
    else:
        print("Failed to leave the network.")
        print("Server response:", response.json())

def search_file(file_name, server_url):
    # Enviar la solicitud GET al servidor principal para buscar el archivo
    response = requests.get(f"{SERVER_URL}/searchFile", params={'file_name': file_name})
    if response.status_code == 200:
        data = response.json()
        if 'peer_id' in data:
            print(f"File found. Peer ID: {data['peer_id']} and address: {data['ip_address']}" )
            target_ip = data['ip_address']
            print("Server response:", response.json())
            # aqui deberiamos llamar a download para que baje el archivo de la direccion ip que le devolvieron
            #download(file_name, target_ip)
        else:
            print("File not found.")
            print("Server response:", response.json())
    else:
        print("Failed to search for the file.")
        print("Server response:", response.json())


# --- --- --- ---

def upload(data, server_url):
    # Crea un canal gRPC para la comunicación con el servidor
    with grpc.insecure_channel(server_url) as channel:
        # Crea un cliente para el servicio gRPC
        stub = p2p_pb2_grpc.P2PServiceStub(channel)
        # Crea una solicitud de carga
        request = p2p_pb2.UploadRequest(data=data)
        # Envía la solicitud al servidor
        response = stub.Upload(request)
        # Maneja la respuesta del servidor
        if response.success:
            print("Upload successful.")
        else:
            print("Upload failed.")

def download(file_name, server_url):
    # Crea un canal gRPC para la comunicación con el servidor
    with grpc.insecure_channel(server_url) as channel:
        # Crea un cliente para el servicio gRPC
        stub = p2p_pb2_grpc.P2PServiceStub(channel)
        # Crea una solicitud de descarga con el nombre del archivo
        request = p2p_pb2.DownloadRequest(file_name=file_name)
        # Envía la solicitud al servidor
        response = stub.Download(request)
        # Maneja la respuesta del servidor
        if response.data:
            print("Downloaded data:", response.data)
        else:
            print("Download failed.")


def get_peer_config():
    # Implementa la lógica para obtener la configuración del archivo de configuración
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
    join(peer_id, ip_address, SERVER_URL)

    # Indexar un archivo
    index_file(peer_id,"file_01",SERVER_URL)
    index_file(peer_id,"file_11",SERVER_URL)
    index_file(peer_id,"file_10",SERVER_URL)

    # Buscar un archivo llamado "file2"
    search_file("file_02", SERVER_URL)
    search_file("file_ss", SERVER_URL)

    # Upload de datos al servidor
    #upload("file1", SERVER_URL)

    # Descarga de datos del servidor
    #download(SERVER_URL)

if __name__ == "__main__":
    main()
