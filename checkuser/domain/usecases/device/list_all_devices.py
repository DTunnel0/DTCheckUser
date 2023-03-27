from typing import List, NamedTuple

from checkuser.domain.interfaces.device_repository import DeviceRepository


class ListAllDeviceOuputDTO(NamedTuple):
    id: str
    username: str


class ListAllDevicesUseCase:
    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    def execute(self) -> List[ListAllDeviceOuputDTO]:
        data = self.device_repository.list_all()
        return [ListAllDeviceOuputDTO(device.id, device.username) for device in data]
