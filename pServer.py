from concurrent import futures
from grpc_reflection.v1alpha import reflection
import grpc
import p2p_pb2
import p2p_pb2_grpc

# Base de datos de archivos simbólicos (usada temporalmente en memoria)
symbolic_files = {}

class P2PService(p2p_pb2_grpc.P2PServiceServicer):
    def Upload(self, request, context):
        # Aquí manejas la solicitud de carga (upload) recibida del cliente
        # Puedes implementar la lógica para guardar los datos recibidos
        # y luego enviar una respuesta al cliente indicando el éxito o fallo de la operación
        # Por ahora, simplemente añadiremos el archivo simbólico a la lista en memoria
        symbolic_files[request.filename] = request.data
        success = True  # Asumimos que la carga siempre es exitosa
        return p2p_pb2.UploadResponse(success=success)

    def Download(self, request, context):
        # Aquí manejas la solicitud de descarga (download) recibida del cliente
        # Puedes implementar la lógica para buscar y recuperar el archivo solicitado
        # y luego enviar los datos al cliente en la respuesta
        # Verificamos si el archivo solicitado está en la lista de archivos simbólicos
        if request.filename in symbolic_files:
            # Si está presente, enviamos los datos del archivo al cliente
            file_data = symbolic_files[request.filename]
            return p2p_pb2.DownloadResponse(data=file_data)
        else:
            # Si no está presente, indicamos al cliente que el archivo no está disponible para descarga
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"El archivo '{request.filename}' no se encontró en el servidor.")
            return p2p_pb2.DownloadResponse()
    
    def ListFiles(self, request, context):
        # Devolver la lista de archivos como respuesta
        return p2p_pb2.ListFilesResponse(files=list(symbolic_files.keys()))

def add_symbolic_files():
    # Agregar los nombres de los archivos a la base de datos simbólica
    symbolic_files["file1"] = "Contenido del archivo 1"
    symbolic_files["file2"] = "Contenido del archivo 2"
    symbolic_files["file3"] = "Contenido del archivo 3"

def serve():
    add_symbolic_files()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    p2p_pb2_grpc.add_P2PServiceServicer_to_server(P2PService(), server)

    # Agregar el servicio de reflexión
    SERVICE_NAMES = (
        p2p_pb2.DESCRIPTOR.services_by_name['P2PService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:6000')
    server.start()
    print("Servidor activo y escuchando en el puerto 6000...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
