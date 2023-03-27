from abc import ABCMeta, abstractmethod
from typing import List

from checkuser.domain.entities.user import User


class UserRepository(metaclass=ABCMeta):
    @abstractmethod
    def get(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[User]:
        raise NotImplementedError
