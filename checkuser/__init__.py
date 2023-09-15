from argparse import ArgumentParser
from checkuser.infra.main import create_app

try:
    __import__('dotenv').load_dotenv()
except Exception:
    pass

__version__ = '1.5.2'
__author__ = 'Glemison C. Dutra'
__email__ = 'glemyson20@gmail.com'

__description__ = (
    'DTChecker - CHECKUSER | '
    'BY ' + __author__ + ' <' + __email__ + '> | '
    'VERSION: ' + __version__
)


def create_argparse() -> ArgumentParser:
    args = ArgumentParser(description=__description__)
    args.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s ' + __version__,
    )
    return args
