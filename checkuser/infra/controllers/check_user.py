import datetime

from checkuser.domain.use_case import CheckUserUseCase
from ..controller import Controller, HttpRequest, HttpResponse


class CheckUserController(Controller):
    def __init__(self, use_case: CheckUserUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HttpRequest) -> HttpResponse:
        data = self.use_case.execute(request.query['username'])
        date = data.expiration_date.strftime('%d/%m/%Y') if data.expiration_date else None
        days = (data.expiration_date - datetime.datetime.now()).days if data.expiration_date else None

        return HttpResponse(
            status_code=200,
            body={
                'id': data.id,
                'username': data.username,
                'limit_connections': data.connection_count,
                'expiration_date': date,
                'expiration_days': days,
                'count_connection': data.connection_count,
            },
        )
