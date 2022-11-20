from os import getenv
from checkuser.__main__ import main


if __name__ == '__main__':
    main(debug=getenv('APP_DEBUG') == 'True')
