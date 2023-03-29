from checkuser.domain.interfaces.connection import ConnectionKiller


class KillConnectionUseCase:
    def __init__(self, connection: ConnectionKiller) -> None:
        self.connection = connection

    def execute(self, username: str) -> None:
        self.connection.kill(username)
