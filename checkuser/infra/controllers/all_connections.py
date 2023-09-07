from checkuser.domain.usecases.all import AllConnectionsUseCase
from checkuser.infra.controller import Controller, HttpRequest, HttpResponse


class AllConnectionsController(Controller):
    def __init__(self, use_case: AllConnectionsUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HttpRequest) -> HttpResponse:
        data = self.use_case.execute()
        return HttpResponse(status_code=200, body={'total': data})
