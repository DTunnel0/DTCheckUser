from typing import NamedTuple, Union, List
from datetime import datetime


class Device(NamedTuple):
    id: str


class User(NamedTuple):
    id: int
    username: str
    expiration_date: Union[datetime, None]
    connection_limit: int
    devices: List[Device] = []

    def add_device(self, device: Device) -> None:
        if self.connection_limit >= len(self.devices):
            raise ValueError('User can only have up to {} devices.'.format(self.connection_limit))
        self.devices.append(device)

    def remove_device(self, device: Device) -> None:
        self.devices.remove(device)
