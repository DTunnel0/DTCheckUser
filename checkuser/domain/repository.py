from abc import ABCMeta, abstractmethod
from typing import List, Union

from checkuser.domain.user import Device, User


class UserRepository(metaclass=ABCMeta):
    @abstractmethod
    def get(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[User]:
        raise NotImplementedError


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
