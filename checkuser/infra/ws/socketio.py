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
    logger.info('-' * 50)
    logger.info('[IP] -> %s', request.remote_addr)
    logger.info('[SID] -> %s', request.sid)
    logger.info('[ACTION] -> %s', data['action'])
    logger.info('-' * 50)

    response = WebSocketAdapter.adapt(Controllers.get(data['action']), data['data'])
    emit('message', response)


@socketio.on('limiter')
def on_limiter(data: dict) -> None:
    username = data['data']['username']

    logger.info('-' * 50)
    logger.info('[CONNECTED] IP: %s', request.remote_addr)
    logger.info('[CONNECTED] SID: %s', request.sid)
    logger.info('[CONNECTED] USERNAME: %s', username)

    if username in connections and len(connections[username]) >= 1:
        logger.info('[ERROR] NUMERO DE CONEXOES EXCEDIDO')
        logger.info('-' * 50)
        emit('limiter', {'status': 'reached', 'message': 'Numero de conexões excedido'})
        return

    if not connections.get(username):
        connections[username] = []

    connections[username].append(request.sid)
    emit('limiter', {'status': 'success', 'message': 'Conexão realizada com sucesso'})
    logger.info('[SUCCESS] CONEXAO REALIZADA COM SUCESSO')
    logger.info('-' * 50)


@socketio.on('disconnect')
def on_disconnect() -> None:
    for username, sids in connections.items():
        if request.sid in sids:
            connections[username].remove(request.sid)
            logger.info('-' * 50)
            logger.info('[DISCONNECTED] IP: %s', request.remote_addr)
            logger.info('[DISCONNECTED] SID: %s', request.sid)
            logger.info('[DISCONNECTED] USERNAME: %s', username)
            logger.info('[DISCONNECTED] CONEXOES RESTANTES: %s', len(connections[username]))
            logger.info('-' * 50)
            break

    emit('message', {'status': 'success', 'message': 'Desconectado com sucesso'})
