from flask import Flask, request, jsonify
import sys
import configparser

app = Flask(__name__)

# Base de datos de peers y archivos (usada temporalmente en memoria)
peers_database = {}
files_database = {}

@app.route('/addPeer', methods=['POST'])
def add_peer():
    data = request.get_json()
    peer_id = data.get('peer_id')
    ip_address = data.get('ip_address')
    peers_database[peer_id] = ip_address
    return jsonify({'message': 'Peer added successfully'})

@app.route('/deletePeer', methods=['DELETE'])
def delete_peer():
    peer_id = request.args.get('peer_id')
    if peer_id in peers_database:
        del peers_database[peer_id]
        return jsonify({'message': 'Peer deleted successfully'})
    else:
        return jsonify({'error': 'Peer not found'})

@app.route('/addFile', methods=['POST'])
def add_file():
    data = request.get_json()
    peer_id = data.get('peer_id')
    file_name = data.get('file_name')
    print(peers_database)
    print(peer_id,file_name)
    if peer_id in peers_database:
        if file_name not in files_database:
            files_database[file_name] = [peer_id]  # Cambiamos a una lista de pares que tienen el archivo para permitir duplicados de files
            return jsonify({'message': 'File added successfully'})
        else:
            files_database[file_name].append(peer_id)  # Agregamos el nuevo par a la listaaaa
            return jsonify({'message': 'File added successfully'})
    else:
        return jsonify({'error': 'Peer not found'})

@app.route('/deleteFile', methods=['DELETE'])
def delete_file():
    file_name = request.args.get('file_name')
    if file_name in files_database:
        del files_database[file_name]
        return jsonify({'message': 'File deleted successfully'})
    else:
        return jsonify({'error': 'File not found'})

@app.route('/searchFile', methods=['GET'])
def search_file():
    file_name = request.args.get('file_name')
    if file_name in files_database:
        peer_ids = files_database[file_name]  # Obtenemos la lista de pares que tienen el archivo
        peer_ids.sort()  # Ordenamos alfabéticamente los IDs de los pares
        chosen_peer_id = peer_ids[0]  # Tomamos el primero en la lista ordenada
        peer_ip = peers_database[chosen_peer_id]  # Obtenemos la dirección IP del par
        return jsonify({'message': 'File found', 'peer_id': chosen_peer_id, 'ip_address': peer_ip})
    else:
        return jsonify({'error': 'File not found'})

# --- AUX METHODS ----
    
@app.route('/getPeers', methods=['GET'])
def get_peers():
    return jsonify(peers_database)

@app.route('/getFiles', methods=['GET'])
def get_files():
    return jsonify(files_database)


# --- RUN LOOP

def run(host='127.0.0.1', port=5000):
    app.run(debug=True, host=host, port=port)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('ServerConfig.ini')
    host = config['server']['host']
    port = int(config['server']['port'])
    run(host, port)
