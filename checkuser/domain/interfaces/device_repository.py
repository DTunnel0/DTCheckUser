from abc import ABCMeta, abstractmethod
from typing import List

from checkuser.domain.entities.device import Device


class DeviceRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, device: Device) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(self, username: str, id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def count(self, username: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def delete_by_username(self, username: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_devices(self, username: str) -> List[Device]:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[Device]:
        raise NotImplementedError
