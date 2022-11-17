from abc import ABCMeta, abstractmethod

class Connection(metaclass=ABCMeta):
    @abstractmethod
    def count(self, username: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def kill(self, username: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> int:
        raise NotImplementedError
