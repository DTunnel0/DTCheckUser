from typing import Callable
from flask import request, Response
from json import dumps

from checkuser.infra.controller import Controller, HttpRequest


class FlaskAdpater:
    @staticmethod
    def adapt(controller: Controller) -> Callable[..., Response]:
        def wrapper(*args, **kwargs):
            try:
                response = controller.handle(
                    HttpRequest(
                        query={
                            **request.args,
                            **(request.view_args or {}),
                        },
                        body={
                            **request.form,
                            **(request.get_json(silent=True) or {}),
                        },
                    )
                )
                return Response(
                    response=dumps(response.body, indent=4),
                    status=response.status_code,
                    mimetype='application/json',
                )
            except Exception as e:
                return Response(
                    response=dumps({'error': str(e)}),
                    status=500,
                    mimetype='application/json',
                )

        return wrapper


class WebSocketAdapter:
    @staticmethod
    def adapt(controller: Controller, data: dict) -> str:
        try:
            response = controller.handle(
                HttpRequest(
                    query=data,
                    body=data,
                )
            )
            return dumps(response.body, indent=4)
        except Exception as e:
            return dumps({'error': str(e)})
