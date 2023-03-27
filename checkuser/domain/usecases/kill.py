from checkuser.domain.connection import ConnectionKill


class KillConnectionUseCase:
    def __init__(self, connection: ConnectionKill) -> None:
        self.connection = connection

    def execute(self, username: str) -> None:
        self.connection.kill(username)
