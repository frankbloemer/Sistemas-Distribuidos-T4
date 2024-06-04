from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'produtos.json'

def read_produtos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def write_produtos(produtos):
    with open(DATA_FILE, 'w') as file:
        json.dump(produtos, file)

# Rota para obter todos os produtos
@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = read_produtos()
    return jsonify(produtos)

@app.route('/produtos/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    produtos = read_produtos()
    produto = next((produto for produto in produtos if produto['id'] == produto_id), None)
    return jsonify(produto) if produto else ('', 404)


# Rota para adicionar um novo produto
@app.route('/produtos', methods=['POST'])
def add_produto():
    produtos = read_produtos()
    novo_produto = request.get_json()
    produtos.append(novo_produto)
    write_produtos(produtos)
    return jsonify(novo_produto), 201

# Rota para atualizar um produto existente pelo ID
@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    produtos = read_produtos()
    update_data = request.get_json()
    produto = next((produto for produto in produtos if produto['id'] == produto_id), None)
    if produto:
        produto.update(update_data)
        write_produtos(produtos)
        return jsonify(produto)
    return ('', 404)

# Rota para deletar um produto pelo ID
@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    produtos = read_produtos()
    produtos = [produto for produto in produtos if produto['id'] != produto_id]
    write_produtos(produtos)
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
