from checkuser.domain.connection import Connection


class AllConnectionsUseCase:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def execute(self) -> int:
        return self.connection.all()
