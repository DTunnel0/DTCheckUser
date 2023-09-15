from uuid import uuid4
from flask import Blueprint, Flask
from flask_sock import Sock

from checkuser.infra.http.flask import register_route
from checkuser.infra.ws.websocket import register_ws


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['SECRET_KEY'] = str(uuid4().hex)

    route = Blueprint('route', 'route')
    sock = Sock()

    register_route(route)
    register_ws(sock, route)

    app.register_blueprint(route)

    return app
