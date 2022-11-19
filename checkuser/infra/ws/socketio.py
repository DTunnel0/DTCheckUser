# type: ignore

import logging

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


@socketio.on('limiter')
def on_limiter(data: dict) -> None:
    logger.info('-' * 50)
    logger.info('[CONNECTED] IP: %s', request.remote_addr)
    logger.info('[CONNECTED] SID: %s', request.sid)
    logger.info('-' * 50)

    username = data['data']['username']
    if username in connections and len(connections[username]) >= 1:
        logger.info('Numero de conexões excedido')
        emit('limiter', {'status': 'reached', 'message': 'Numero de conexões excedido'})
        return

    if not connections.get(username):
        connections[username] = []

    connections[username].append(request.sid)
    emit('limiter', {'status': 'success', 'message': 'Conexão realizada com sucesso'})
    logger.info('Conexão realizada com sucesso')


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
