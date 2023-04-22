import logging
import os

from checkuser.data.database.sqlite import delete_database

from checkuser.infra.factories.make_device_use_case import (
    make_delete_devices_use_case,
    make_list_all_devices_use_case,
    make_list_devices_use_case,
)

from checkuser.infra.presenter.delete_devices import DeleteDevicesPresenter
from checkuser.infra.presenter.list_all_devices import ListAllDevicesPresenter
from checkuser.infra.presenter.list_devices import ListDevicesPresenter

from . import args
from .infra.http.flask import app
from .infra.ws.websocket import ws
from .infra.ws.socketio import io

try:
    from eventlet import monkey_patch

    monkey_patch()
except ImportError:
    pass

args.add_argument('--host', type=str, help='Host to listen', default='0.0.0.0')
args.add_argument('--port', '-p', type=int, help='Port', default=5000)
args.add_argument('--start', action='store_true', help='Start the daemon')
args.add_argument('--log', '-l', type=str, help='LogLevel', default='INFO')
args.add_argument('--log-file', type=str, help='Log file', default='/var/log/checkuser.log')

args.add_argument('--list-all-devices', action='store_true', help='List all devices')
args.add_argument('--list-devices', type=str, help='List devices from a user')
args.add_argument('--delete-devices', type=str, help='Delete devices from a user')
args.add_argument('--delete-db', action='store_true', help='Delete database of devices')


def main(debug: bool = os.getenv('APP_DEBUG') == '1') -> None:
    data = args.parse_args()

    if data.list_all_devices:
        presenter = ListAllDevicesPresenter(make_list_all_devices_use_case())
        print(presenter.present())
        return

    if data.list_devices:
        presenter = ListDevicesPresenter(make_list_devices_use_case())
        print(presenter.present(data.list_devices))
        return

    if data.delete_devices:
        presenter = DeleteDevicesPresenter(make_delete_devices_use_case())
        print(presenter.present(data.delete_devices))
        return

    if data.delete_db:
        delete_database()
        return

    try:
        logging.basicConfig(
            level=getattr(logging, data.log.upper()),
            format='%(asctime)s - %(message)s',
            filename=data.log_file,
        )
        logging.info('Log file: %s' % data.log_file)
    except PermissionError:
        logging.basicConfig(
            level=getattr(logging, data.log.upper()),
            format='%(asctime)s - %(message)s',
        )
        logging.warn('Failed to create log file: %s', data.log_file)

    if data.start:
        io.init_app(app)
        ws.init_app(app)
        io.run(app, host=data.host, port=data.port, debug=debug)
        return

    args.print_help()


if __name__ == '__main__':
    main()
