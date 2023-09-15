from json import loads
from flask import Blueprint
from flask_sock import Sock, Server

from checkuser.infra.factories.make_controller import ControllerFactory
from checkuser.infra.adapter import WebSocketAdapter


def handle_message(server: Server):
    while True:
        body = server.receive()

        if body is None:
            break

        data = loads(body)
        response = WebSocketAdapter.adapt(ControllerFactory.get(data['action']), data['data'])
        server.send(response)


def register_ws(ws: Sock, bp: Blueprint):
    ws.route('/', bp)(handle_message)
