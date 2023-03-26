from abc import ABCMeta, abstractmethod
from typing import List

from checkuser.domain.user import Device, User


class UserRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError


class DeviceRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_by_id(self, id: str) -> Device:
        raise NotImplementedError

    @abstractmethod
    def save(self, device: Device) -> None:
        raise NotImplementedError
