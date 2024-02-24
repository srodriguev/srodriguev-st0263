from concurrent import futures
import grpc
import time

# Importar los módulos generados por gRPC
import pserver_pb2
import pserver_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

# Definir la clase que implementa los métodos del servidor del peer
class PeerServerServicer(pserver_pb2_grpc.PeerServerServicer):
    def __init__(self):
        # Inicializar cualquier configuración necesaria
        pass

    def upload(self, request, context):
        # Método para que un peer cargue un archivo en este peer
        # Implementa la lógica para recibir y almacenar el archivo enviado por el cliente
        pass

    def download(self, request, context):
        # Método para que un peer descargue un archivo de otro peer
        # Implementa la lógica para buscar y enviar el archivo solicitado al cliente
        pass

# Función para iniciar el servidor del peer
def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pserver_pb2_grpc.add_PeerServerServicer_to_server(PeerServerServicer(), server)
    server.add_insecure_port('[::]:50052')  # Elige un puerto diferente al del servidor central
    server.start()
    print("Peer server started. Listening on port 50052...")  # Mensaje de confirmación

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    run()
