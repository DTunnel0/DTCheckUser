# type: ignore

import logging
import pprint

from flask import request
from flask_socketio import SocketIO, emit
from checkuser.infra.factories.make_controller import Controllers
from checkuser.infra.adapter import WebSocketAdapter

socketio = SocketIO(cors_allowed_origins='*')
logger = logging.getLogger(__name__)

connections = {}


@socketio.on('message')
def on_message(data: dict) -> None:
    logger.info('IP: %s', request.remote_addr)
    logger.info('SID: %s', request.sid)

    response = WebSocketAdapter.adapt(Controllers.get(data['action']), data['data'])
    emit('message', response)


@socketio.on('limiter', namespace='/limiter')
def on_limiter(data: dict) -> None:
    logger.info('-' * 50)
    logger.info('[CONNECTED] IP: %s', request.remote_addr)
    logger.info('[CONNECTED] SID: %s', request.sid)
    logger.info('-' * 50)

    username = data['data']['username']
    if username in connections:
        emit('limiter', {'status': 'error', 'message': 'Limite de conexões atingido'})
        return

    connections[username] = request.sid
    emit('limiter', {'status': 'success', 'message': 'Conexão realizada com sucesso'})


@socketio.on('disconnect')
def on_disconnect() -> None:
    for username, sid in connections.items():
        if sid == request.sid:
            del connections[username]
            break

    logger.info('-' * 50)
    logger.info('[DISCONNECT] IP: %s', request.remote_addr)
    logger.info('[DISCONNECT] SID: %s', request.sid)
    logger.info('-' * 50)

    emit('message', {'status': 'success', 'message': 'Desconectado com sucesso'})
