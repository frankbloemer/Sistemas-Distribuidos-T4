import base64

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Carregar a chave privada do servidor
with open('private_key.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None)

@socketio.on('connect')
def handle_connect():
    message = b"Conectado ao servidor! Mensagem autenticada!"
    # Criar a assinatura
    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    data = {'message': message.decode(), 'signature': signature.hex()}
    emit('connected', data)

DATA_FILE = 'produtos.json'

def read_produtos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def write_produtos(produtos):
    with open(DATA_FILE, 'w') as file:
        json.dump(produtos, file, indent=4)

@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = read_produtos()
    return jsonify(produtos)

@app.route('/produtos/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    produtos = read_produtos()
    produto = next((produto for produto in produtos if produto['id'] == produto_id), None)
    if produto:
        return jsonify(produto)
    return jsonify({'error': 'Produto não encontrado'}), 404

@app.route('/produtos', methods=['POST'])
def add_produto():
    if not request.is_json:
        return jsonify({'error': 'Requisição deve ser JSON'}), 400
    novo_produto = request.get_json()
    produtos = read_produtos()
    maior_id = max([produto['id'] for produto in produtos], default=0)
    novo_produto['id'] = maior_id + 1
    produtos.append(novo_produto)
    write_produtos(produtos)
    socketio.emit("novo_produto", f"Novo produto: {novo_produto['nome']} adicionado")
    return jsonify(novo_produto), 201

@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    if not request.is_json:
        return jsonify({'error': 'Requisição deve ser JSON'}), 400
    update_data = request.get_json()
    produtos = read_produtos()
    produto = next((produto for produto in produtos if produto['id'] == produto_id), None)
    if produto:
        produto.update(update_data)
        write_produtos(produtos)
        nome = produto.get('nome')
        if produto['estoque'] == 0:
            socketio.emit("estoque_vazio", f"Estoque vazio de {nome}")
        return jsonify(produto)
    return jsonify({'error': 'Produto não encontrado'}), 404

@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    produtos = read_produtos()
    novo_produtos = [produto for produto in produtos if produto.get('id') != produto_id]
    if len(produtos) == len(novo_produtos):
        return jsonify({'error': 'Produto não encontrado'}), 404
    write_produtos(novo_produtos)
    return ('', 204)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost', port=5000)
