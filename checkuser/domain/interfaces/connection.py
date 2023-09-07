from abc import ABCMeta, abstractmethod
from typing import Union


class Connection(metaclass=ABCMeta):
    _next_handler: Union['Connection', None] = None

    def set_next_handler(self, handler: 'Connection') -> 'Connection':
        self._next_handler = handler
        return handler

    @abstractmethod
    def count(self, username: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> int:
        raise NotImplementedError


class ConnectionKiller(Connection):
    _next_handler: Union['ConnectionKiller', None] = None

    @abstractmethod
    def kill(self, username: str) -> None:
        raise NotImplementedError
