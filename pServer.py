from concurrent import futures
from grpc_reflection.v1alpha import reflection
import configparser
import grpc
import p2p_pb2
import p2p_pb2_grpc
import os

# Base de datos de archivos simbólicos (usada temporalmente en memoria)
symbolic_files = {}

class P2PService(p2p_pb2_grpc.P2PServiceServicer):
    def Upload(self, request, context):
        # Aquí manejas la solicitud de carga (upload) recibida del cliente
        # Puedes implementar la lógica para guardar los datos recibidos
        # y luego enviar una respuesta al cliente indicando el éxito o fallo de la operación
        # Por ahora, simplemente añadiremos el archivo simbólico a la lista en memoria
        symbolic_files[request.filename] = request.data
        print("Received upload request for: ", request.filename)

        # Leer la configuración del archivo peerConfig.ini
        config = configparser.ConfigParser()
        config.read('peerConfig.ini')
        # Guardar el archivo recibido en el sistema de archivos
        file_storage_folder = config['peer']['file_storage']
        file_path = os.path.join(file_storage_folder, request.filename)
        with open(file_path, 'wb') as file:
            file.write(request.data)

        success = True  # Asumimos que la carga siempre es exitosa
        return p2p_pb2.UploadResponse(success=success)

    def Download(self, request, context):
        # Aquí manejas la solicitud de descarga (download) recibida del cliente
        # Puedes implementar la lógica para buscar y recuperar el archivo solicitado
        # y luego enviar los datos al cliente en la respuesta
        # Verificamos si el archivo solicitado está en la lista de archivos simbólicos
        print("Received download request for: ", request.filename)
        if request.filename in symbolic_files:
            print("File found")
            # Si está presente, enviamos los datos del archivo al cliente
            file_data = symbolic_files[request.filename]
            # Convertir el contenido del archivo a bytes
            file_data_bytes = file_data.encode('utf-8')
            return p2p_pb2.DownloadResponse(data=file_data_bytes)
            # return p2p_pb2.DownloadResponse(data=file_data)
        else:
            print("File NOTfound")
            # Si no está presente, indicamos al cliente que el archivo no está disponible para descarga
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"El archivo '{request.filename}' no se encontró en el servidor.")
            return p2p_pb2.DownloadResponse()
    
    def ListFiles(self, request, context):
        # Devolver la lista de archivos como respuesta
        return p2p_pb2.ListFilesResponse(files=list(symbolic_files.keys()))


def add_symbolic_files():
    # Leer la configuración del archivo peerConfig.ini
    config = configparser.ConfigParser()
    config.read('peerConfig.ini')

    # Obtener la ruta del directorio de almacenamiento de archivos desde la configuración
    file_storage_folder = config['peer']['file_storage']

    # Combinar la ruta del directorio de almacenamiento de archivos con el directorio actual
    files_dir = os.path.join(os.path.dirname(__file__), file_storage_folder)

    # Verificar si el directorio existe
    if os.path.exists(files_dir):
        # Obtener la lista de archivos en el directorio
        files = os.listdir(files_dir)
        for file_name in files:
            # Leer el contenido de cada archivo y agregarlo a la base de datos simbólica
            file_path = os.path.join(files_dir, file_name)
            with open(file_path, 'r') as file:
                content = file.read()
                symbolic_files[file_name] = content
    else:
        print(f"El directorio '{files_dir}' no existe.")

    # Imprimir los archivos añadidos a la base de datos simbólica
    print("Archivos añadidos a la base de datos simbólica:")
    for file_name, content in symbolic_files.items():
        print(f"Nombre: {file_name}, Contenido: {content}")

def serve():
    add_symbolic_files()

    # Leer la configuración del archivo peerConfig.ini
    config = configparser.ConfigParser()
    config.read('peerConfig.ini')

    # Obtener la dirección IP y el puerto del servidor desde el archivo de configuración
    peer_host = config['peer']['host']
    peer_port = config['peer']['port']
    peer_id = config['peer']['peer_id']
    print("read Pserver host as: ", peer_host)
    print("read Pserver port  as: ", peer_port)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    p2p_pb2_grpc.add_P2PServiceServicer_to_server(P2PService(), server)

    # Agregar el servicio de reflexión
    SERVICE_NAMES = (
        p2p_pb2.DESCRIPTOR.services_by_name['P2PService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)


    # Usar la dirección IP y el puerto leídos del archivo de configuración
    server.add_insecure_port(f"{peer_host}:{peer_port}")
    server.start()
    print(f"Servidor activo y escuchando en: {peer_host}:{peer_port}...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
