import datetime

from typing import Union, NamedTuple
from checkuser.domain.connection import Connection
from checkuser.domain.repository import UserRepository


class OutputDTO(NamedTuple):
    id: int
    username: str
    expiration_date: Union[None, datetime.datetime]
    connection_count: int


class CheckUserUseCase:
    def __init__(self, repository: UserRepository, connection: Connection):
        self.repository = repository
        self.connection = connection

    def execute(self, username: str) -> OutputDTO:
        user = self.repository.get_by_username(username)
        count = self.connection.count(username)
        return OutputDTO(
            id=user.id,
            username=user.username,
            expiration_date=user.expiration_date,
            connection_count=count,
        )


class KillConnectionUseCase:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, username: str) -> None:
        self.connection.kill(username)


class AllConnectionsUseCase:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self) -> int:
        return self.connection.all()
