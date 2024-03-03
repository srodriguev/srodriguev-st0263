import sys
import configparser
import grpc
import p2p_pb2
import p2p_pb2_grpc
import requests

#ip de este peer
peer_ip_address = ""
# nombre del peer
peer_id = ""
# URL (fallback) del servidor principal
SERVER_URL = "http://localhost:5000"  
server_url = SERVER_URL

def join(peer_id, ip_address, server_url):
    # Datos a enviar al servidor principal
    data = {
        'peer_id': peer_id,  # Usar el ID del peer proporcionado por el archivo de configuración
        'ip_address': ip_address
    }

    # Enviar la solicitud POST al servidor principal para unirse a la red
    response = requests.post(f"http://{server_url}/addPeer", json=data)
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
    response = requests.post(f"http://{server_url}/addFile", json=data)
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
    response = requests.delete(f"http://{server_url}/deletePeer", params=data)
    if response.status_code == 200:
        print("Left the network successfully.")
        print("Server response:", response.json())
    else:
        print("Failed to leave the network.")
        print("Server response:", response.json())

def search_file(file_name, server_url):
    # Enviar la solicitud GET al servidor principal para buscar el archivo
    response = requests.get(f"http://{server_url}/searchFile", params={'file_name': file_name})
    if response.status_code == 200:
        data = response.json()
        if 'peer_id' in data:
            print(f"File found. Peer ID: {data['peer_id']} and address: {data['ip_address']}" )
            target_ip = data['ip_address']
            print("Server response:", response.json())
            # aqui deberiamos llamar a download para que baje el archivo de la direccion ip que le devolvieron
            print("Since data was found, will download: ")
            download(file_name, target_ip)
        else:
            print("File not found.")
            print("Server response:", response.json())
    else:
        print("Failed to search for the file.")
        print("Server response:", response.json())


# --- --- --- ---

def upload(filename, data, server_url):
    # Crea un canal gRPC para la comunicación con el servidor
    with grpc.insecure_channel(server_url) as channel:
        # Crea un cliente para el servicio gRPC
        stub = p2p_pb2_grpc.P2PServiceStub(channel)
        # Crea una solicitud de carga con el nombre del archivo y los datos
        request = p2p_pb2.UploadRequest(filename=filename, data=data)
        # Envía la solicitud al servidor
        response = stub.Upload(request)
        # Maneja la respuesta del servidor
        if response.success:
            print("Upload successful. Files available are:")
            list_files(server_url)
            index_file(peer_ip_address,filename,server_url)
        else:
            print("Upload failed.")

def download(file_name, server_url):
    # Crea un canal gRPC para la comunicación con el servidor
    with grpc.insecure_channel(server_url) as channel:
        # Crea un cliente para el servicio gRPC
        stub = p2p_pb2_grpc.P2PServiceStub(channel)
        # Crea una solicitud de descarga con el nombre del archivo
        request = p2p_pb2.DownloadRequest(filename=file_name)
        # Envía la solicitud al servidor
        response = stub.Download(request)
        # Maneja la respuesta del servidor
        if response.data:
            print("Downloaded data:", response.data)
            print("will upload: ", response.data, "to: ", peer_ip_address, "direction")
            upload(response.data,peer_ip_address)
        else:
            print("Download failed.")

def list_files(server_url):
    # Crea un canal gRPC para la comunicación con el servidor
    with grpc.insecure_channel(server_url) as channel:
        # Crea un cliente para el servicio gRPC
        stub = p2p_pb2_grpc.P2PServiceStub(channel)
        # Crea una solicitud para listar archivos
        request = p2p_pb2.ListFilesRequest()
        # Envía la solicitud al servidor y recibe la respuesta
        response = stub.ListFiles(request)
        # Maneja la respuesta del servidor
        print("Lista de archivos en el servidor:")
        for file_name in response.files:
            print(file_name)


# -------

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
    global peer_id
    peer_id, host, port, server_host, server_port = get_peer_config()
    
    global peer_ip_address
    peer_ip_address = f"{host}:{port}"

    global server_url
    server_url = f"{server_host}:{server_port}"
    
    print("Server url from config: ", server_url)
    print("Peer ID from config:", peer_id)
    print("IP address from config:", peer_ip_address)

    # Unirse a la red
    join(peer_id, peer_ip_address, server_url)

    # Indexar un archivo
    index_file(peer_id,"file_01A.txt",server_url)
    index_file(peer_id,"file_01B.txt",server_url)
    index_file(peer_id,"file_01C.txt",server_url)

    # Buscar un archivo por su nombre
    #search_file("file1.txt", server_url)

    # Imprimir la lista de métodos disponibles
    print("\nMétodos disponibles:")
    print("1. Listar archivos")
    print("2. Subir archivo")
    print("3. Descargar archivo")
    print("4. Buscar en la red")
    print("5. Salir")

    # Esperar instrucciones del usuario
    while True:
        choice = input("\nSeleccione un método (1-4): ")
        if choice == "1":
            list_files(peer_ip_address)
        elif choice == "2":
            file_name = input("Ingrese el nombre del archivo a subir: ")
            file_data = input("Ingrese los datos del archivo a subir: ")
            upload(file_name, file_data, peer_ip_address)
        elif choice == "3":
            file_name = input("Ingrese el nombre del archivo a descargar: ")
            download(file_name, peer_ip_address)   
        elif choice == "4":
            file_name = input("Ingrese el nombre del archivo a buscar: ")
            search_file(file_name, server_url)
        elif choice == "5":
            print("Saliendo del programa...")
            # Abandonar la red antes de salir
            leave(peer_id, peer_ip_address, server_url)
            break
            #break
        else:
            print("Opción no válida. Por favor, seleccione un número del 1 al 5.")


if __name__ == "__main__":
    main()
        