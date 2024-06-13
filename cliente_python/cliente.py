import socketio
import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
    )

socketio = socketio.Client()

@socketio.event
def connected(data):
    try:
        public_key.verify(
            data['signature'],
            data['message'],
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
            )
    except:
        print("Erro de autenticação")
    print(data['message'])


@socketio.event
def message(data):
    print('Mensagem recebida:', data)

@socketio.event
def evento1(data):
    print('Evento 1 recebido:', data)

@socketio.event
def evento2(data):
    print('Evento 2 recebido:', data)

socketio.connect('http://localhost:5000')

socketio.on('novo_produto', evento1)
socketio.on('estoque_vazio', evento2)

socketio.emit('new_event', {'data': 'Olá do cliente Python!'})

socketio.wait()
