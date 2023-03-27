from typing import Union, List
from checkuser.domain.entities.device import Device
from checkuser.domain.interfaces.device_repository import DeviceRepository


class DeviceRepositoryMemory(DeviceRepository):
    def __init__(self):
        self.devices: List[Device] = []

    def save(self, device: Device) -> None:
        self.devices.append(device)

    def exists(self, username: str, id: str) -> Union[Device, None]:
        return any(device.id == id and device.username == username for device in self.devices)

    def list_devices(self, username: str) -> List[Device]:
        return [device for device in self.devices if device.username == username]

    def count(self, username: str) -> int:
        return len([device for device in self.devices if device.username == username])

    def delete_by_username(self, username: str) -> None:
        self.devices = [device for device in self.devices if device.username != username]

    def list_all(self) -> List[Device]:
        return self.devices
