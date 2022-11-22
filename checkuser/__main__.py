import logging
import os

from . import args, logger
from .infra.http.flask import app
from .infra.ws.websocket import ws
from .infra.ws.socketio import io
from .daemon import Daemon

try:
    from engineio.async_drivers import eventlet
    from eventlet import monkey_patch

    monkey_patch()
except ImportError:
    pass

args.add_argument('--host', type=str, help='Host to listen', default='0.0.0.0')
args.add_argument('--port', '-p', type=int, help='Port', default=5000)

args.add_argument('--start', action='store_true', help='Start the daemon')
args.add_argument('--status', '-s', action='store_true', help='Server status')
args.add_argument('--stop', '-t', action='store_true', help='Stop server')
args.add_argument('--restart', '-r', action='store_true', help='Restart server')

args.add_argument('--daemon', '-d', action='store_true', help='Run as daemon')

args.add_argument('--log', '-l', type=str, help='LogLevel', default='INFO')


def main(debug: bool = os.getenv('APP_DEBUG') == '1') -> None:
    data = args.parse_args()

    logging.basicConfig(
        level=getattr(logging, data.log.upper()),
        format='%(asctime)s - %(message)s',
    )

    class ServerDaemon(Daemon):
        def run(self):
            io.init_app(app)
            ws.init_app(app)
            io.run(app, host=data.host, port=data.port, debug=debug)

    daemon = ServerDaemon('/tmp/checkuser.pid')
    if data.status:
        if daemon.is_running():
            logger.info('Server is running')
            logger.info('PID: {}'.format(daemon.get_pid()))
            return

        logger.info('Server is not running')
        return

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
