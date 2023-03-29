from datetime import datetime
from typing import Union, NamedTuple

from checkuser.domain.entities.device import Device
from checkuser.domain.interfaces.device_repository import DeviceRepository
from checkuser.domain.interfaces.user_repository import UserRepository


class OutputDTO(NamedTuple):
    id: int
    username: str
    expiration_date: Union[None, datetime]
    limit_connections: int
    count_connections: int

    def get_date_string(self) -> Union[None, str]:
        if self.expiration_date is None:
            return None
        return self.expiration_date.strftime('%d/%m/%Y')

    def get_days_from_date(self) -> Union[None, int]:
        if self.expiration_date is None:
            return None
        return (self.expiration_date - datetime.now()).days + 1


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

        device_exists = self.device_repository.exists(username, device_id)
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
