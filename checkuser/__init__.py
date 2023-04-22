import argparse
import logging

try:
    __import__('dotenv').load_dotenv()
except Exception:
    pass

logger = logging.getLogger(__name__)

__version__ = '1.4.7'
__author__ = 'Glemison C. Dutra'
__email__ = 'glemyson20@gmail.com'

__description__ = (
    'DTChecker - CHECKUSER | '
    'BY ' + __author__ + ' <' + __email__ + '> | '
    'VERSION: ' + __version__
)

args = argparse.ArgumentParser(description=__description__)
args.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s ' + __version__,
)
