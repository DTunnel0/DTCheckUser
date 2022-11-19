import logging

from flask import request
from flask_socketio import SocketIO, emit
from checkuser.infra.factories.make_controller import Controllers
from checkuser.infra.adapter import WebSocketAdapter

socketio = SocketIO(cors_allowed_origins='*')
logger = logging.getLogger(__name__)


@socketio.on('message')
def handle_message(data: dict):
    logger.info('IP: %s', request.remote_addr)
    logger.info('SID: %s', request.sid)  # type: ignore

    response = WebSocketAdapter.adapt(Controllers.get(data['action']), data['data'])
    emit('message', response)
