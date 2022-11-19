import argparse
import logging

from .infra.http.flask import app
from .infra.ws.websocket import ws
from .infra.ws.socketio import io

logger = logging.getLogger(__name__)

__version__ = '2.2.14'
__author__ = 'Glemison C. Dutra'
__email__ = 'glemyson20@gmail.com'

args = argparse.ArgumentParser(description='Checker for OpenVPN and SSH')
args.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s ' + __version__,
)
