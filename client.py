import grpc
import service_pb2
import service_pb2_grpc

def buscar_recurso(nombre_recurso, direccion_peer):
    with grpc.insecure_channel(direccion_peer) as channel:
        stub = Servicio_pb2_grpc.P2PServiceStub(channel)
        response = stub.BuscarRecurso(Servicio_pb2.BuscarRecursoRequest(nombre_recurso=nombre_recurso))
        return response.direccion_peer

def transferir_recurso(nombre_recurso, direccion_peer_destino):
    with grpc.insecure_channel(direccion_peer_destino) as channel:
        stub = Servicio_pb2_grpc.P2PServiceStub(channel)
        response = stub.TransferirRecurso(Servicio_pb2.TransferirRecursoRequest(
            direccion_peer_solicitante="192.168.1.20", nombre_recurso=nombre_recurso))
        return response.contenido_recurso

if __name__ == '__main__':
    # Ejemplo de uso
    nombre_recurso = "archivo.txt"
    direccion_peer = "192.168.1.30"  # Dirección del peer con el recurso buscado
    direccion_peer_destino = "192.168.1.40"  # Dirección del peer destino para la transferencia
    resultado_busqueda = buscar_recurso(nombre_recurso, direccion_peer)
    print("El recurso se encuentra en el peer con dirección:", resultado_busqueda)
    contenido_recurso = transferir_recurso(nombre_recurso, direccion_peer_destino)
    print("El contenido del recurso es:", contenido_recurso)
