import logging

from json import loads
from flask_sock import Sock, Server

from checkuser.infra.factories.make_controller import Controllers
from checkuser.infra.adapter import WebSocketAdapter

ws = Sock()
logger = logging.getLogger(__name__)


@ws.route('/')
def handle_message(server: Server):
    logger.info(
        'Cliente %s:%d conectado', server.sock.getpeername()[0], server.sock.getpeername()[1]
    )

    while True:
        body = server.receive()

        if body is None:
            break

        data = loads(body)
        response = WebSocketAdapter.adapt(Controllers.get(data['action']), data['data'])
        server.send(response)

    logger.info(
        'Cliente %s:%d desconectado', server.sock.getpeername()[0], server.sock.getpeername()[1]
    )
