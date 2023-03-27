import datetime

from typing import Union, NamedTuple
from checkuser.domain.connection import Connection
from checkuser.domain.repository import UserRepository, DeviceRepository
from checkuser.domain.user import Device


class OutputDTO(NamedTuple):
    id: int
    username: str
    expiration_date: Union[None, datetime.datetime]
    limit_connections: int
    count_connections: int

    def string_date(self) -> Union[None, str]:
        if self.expiration_date is None:
            return None
        return self.expiration_date.strftime('%d/%m/%Y')

    def days(self) -> Union[None, int]:
        if self.expiration_date is None:
            return None
        return (datetime.datetime.now() - self.expiration_date).days + 1


class CheckUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        device_repository: DeviceRepository,
    ) -> None:
        self.user_repository = user_repository
        self.device_repository = device_repository

    def execute(self, username: str, device_id: str) -> OutputDTO:
        user = self.user_repository.get(username)
        devices = self.device_repository.count(username)

        device_exists = self.device_repository.get_by_id(device_id) is not None
        limit_reached = not device_exists and user.limit_reached(devices)

        if not device_exists and not limit_reached:
            self.device_repository.save(Device(device_id, username))
            devices += 1

        connections = devices if not limit_reached else user.connection_limit + 1
        return OutputDTO(
            id=user.id,
            username=user.username,
            expiration_date=user.expiration_date,
            limit_connections=user.connection_limit,
            count_connections=connections,
        )
