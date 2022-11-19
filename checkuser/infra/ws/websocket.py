import logging

from json import loads
from flask_sock import Sock, Server

from checkuser.infra.factories.make_controller import Controllers
from checkuser.infra.adapter import WebSocketAdapter

socketio = Sock()
logger = logging.getLogger(__name__)


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
