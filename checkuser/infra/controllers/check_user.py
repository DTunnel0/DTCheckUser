from checkuser.domain.usecases.checkuser import CheckUserUseCase
from checkuser.infra.controller import Controller, HttpRequest, HttpResponse


class CheckUserController(Controller):
    def __init__(self, use_case: CheckUserUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HttpRequest) -> HttpResponse:
        data = self.use_case.execute(request.query['username'], request.query['deviceId'])
        return HttpResponse(
            status_code=200,
            body={
                'id': data.id,
                'username': data.username,
                'expiration_date': data.get_date_string(),
                'expiration_days': data.get_days_from_date(),
                'limit_connections': data.limit_connections,
                'count_connections': data.count_connections,
            },
        )
