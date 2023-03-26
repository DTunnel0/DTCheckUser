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
    def get_by_id(self, id: str) -> Union[Device, None]:
        raise NotImplementedError

    @abstractmethod
    def count(self, username: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def save(self, device: Device) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> List[Device]:
        raise NotImplementedError
