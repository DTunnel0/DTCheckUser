import logging

from json import loads, dumps
from flask_sock import Sock, Server

from checkuser.infra.factories.make_controller import Controllers
from checkuser.infra.adapter import WebSocketAdapter

socketio = Sock()
logger = logging.getLogger(__name__)
connections = {}


@socketio.route('/')
def handle_message(ws: Server):
    logger.info('Cliente %s:%d conectado', ws.sock.getpeername()[0], ws.sock.getpeername()[1])

    while True:
        body = ws.receive()

        if body is None:
            break

        data = loads(body)
        response = WebSocketAdapter.adapt(Controllers.get(data['action']), data['data'])
        ws.send(response)

    logger.info('Cliente %s:%d desconectado', ws.sock.getpeername()[0], ws.sock.getpeername()[1])


@socketio.route('/limiter')
def handle_limiter(ws: Server):
    while True:
        body = ws.receive()

        if body is None:
            break

        data = loads(body)
        username = data['data']['username']

        if username in connections:
            ws.send(dumps({'status': 'error', 'message': 'Limite de conexões atingido'}))
            return

        connections[username] = ws
        ws.send(dumps({'status': 'success', 'message': 'Conexão realizada com sucesso'}))
