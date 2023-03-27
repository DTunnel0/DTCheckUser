from typing import List, NamedTuple

from checkuser.domain.interfaces.device_repository import DeviceRepository


class ListDeviceOuputDTO(NamedTuple):
    id: str
    username: str


class ListDeviceUseCase:
    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    def execute(self, username: str) -> List[ListDeviceOuputDTO]:
        devices = self.device_repository.list_devices(username)
        return [ListDeviceOuputDTO(device.id, device.username) for device in devices]
