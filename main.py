# from checkuser.infra.http.flask import app
from checkuser.infra.http.websocket import app

if __name__ == '__main__':
    app.run()
