import socketio
import json

socketio = socketio.Client()

@socketio.event
def connect():
    print('Conectado ao servidor!')

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

socketio.on('evento1', evento1)
socketio.on('evento2', evento2)

socketio.emit('new_event', {'data': 'Olá do cliente Python!'})

socketio.wait()
