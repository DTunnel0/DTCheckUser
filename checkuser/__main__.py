import sys
import asyncio

from . import args
from .daemon import Daemon

try:
    use_flask = True
    from .infra.http.flask import app as flask_app
except ImportError:
    use_flask = False

try:
    websocket_app = True
    from .infra.http.websocket import create_app as create_websocket_app
except ImportError:
    websocket_app = False

if not use_flask and not websocket_app:
    print('Please install Flask or Websocket')
    sys.exit(1)


args.add_argument('--host', type=str, help='Host to listen', default='0.0.0.0')
args.add_argument('--port', '-p', type=int, help='Port', default=5000)

args.add_argument('--start', action='store_true', help='Start the daemon')
args.add_argument('--stop', '-t', action='store_true', help='Stop server')
args.add_argument('--restart', '-r', action='store_true', help='Restart server')
args.add_argument('--flask', '-f', action='store_true', help='Run flask server')
args.add_argument('--websocket', '-w', action='store_true', help='Run websockets server')

args.add_argument('--daemon', '-d', action='store_true', help='Run as daemon')


def main():
    data = args.parse_args()

    class ServerDaemon(Daemon):
        def run(self):
            if data.flask:
                flask_app.run(host=data.host, port=data.port, debug=True)
            elif data.websocket:
                asyncio.get_event_loop().run_until_complete(
                    create_websocket_app(
                        data.host,
                        data.port,
                    )
                )
                asyncio.get_event_loop().run_forever()
            else:
                raise Exception('No server selected')

    daemon = ServerDaemon('/tmp/checkuser.pid')
    if not data.daemon and data.start:
        daemon.run()
        return

    if data.start:
        daemon.start()
        return

    if data.stop:
        daemon.stop()
        return

    if data.restart:
        daemon.restart()
        return

    args.print_help()


if __name__ == '__main__':
    main()
