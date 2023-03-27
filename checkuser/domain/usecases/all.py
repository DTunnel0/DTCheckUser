from checkuser.domain.interfaces.connection import Connection


class AllConnectionsUseCase:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def execute(self) -> int:
        return self.connection.all()
