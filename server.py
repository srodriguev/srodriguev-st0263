import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc

# Implementación del servidor P2P
class P2PServicer(Servicio_pb2_grpc.P2PServiceServicer):
    def BuscarRecurso(self, request, context):
        # Lógica para buscar el recurso en el peer
        nombre_recurso = request.nombre_recurso
        # Supongamos que encontramos la dirección del peer que tiene el recurso
        direccion_peer = "192.168.1.10"
        return Servicio_pb2.BuscarRecursoResponse(direccion_peer=direccion_peer)

    def TransferirRecurso(self, request, context):
        # Lógica para transferir el recurso al peer solicitante
        nombre_recurso = request.nombre_recurso
        contenido_recurso = "Contenido del recurso..."
        return Servicio_pb2.TransferirRecursoResponse(contenido_recurso=contenido_recurso)

def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Servicio_pb2_grpc.add_P2PServiceServicer_to_server(P2PServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    start_server()
