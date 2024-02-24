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
    file_name = data.get('file_name')
    peer_id = data.get('peer_id')
    if peer_id in peers_database:
        if file_name not in files_database:
            files_database[file_name] = peer_id
            return jsonify({'message': 'File added successfully'})
        else:
            return jsonify({'error': 'File already exists'})
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
        peer_id = files_database[file_name]
        return jsonify({'message': 'File found', 'peer_id': peer_id})
    else:
        return jsonify({'error': 'File not found'})



def run(host='127.0.0.1', port=5000):
    app.run(debug=True, host=host, port=port)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('ServerConfig.ini')
    host = config['server']['host']
    port = int(config['server']['port'])
    run(host, port)
