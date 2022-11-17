import subprocess
from abc import ABCMeta, abstractmethod


class CommandExecutor(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, command: str) -> str:
        raise NotImplementedError


class CommandExecutorImpl(CommandExecutor):
    def execute(self, command: str) -> str:
        return subprocess.check_output(command, shell=True).decode('utf-8')
