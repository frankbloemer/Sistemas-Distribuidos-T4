import socketio
socketio = socketio.Client()

@socketio.event
def connected(data):
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
