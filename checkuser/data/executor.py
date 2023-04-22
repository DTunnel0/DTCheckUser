import subprocess
import os


from abc import ABCMeta, abstractmethod


class CommandExecutor(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, command: str) -> str:
        raise NotImplementedError


class CommandExecutorImpl(CommandExecutor):
    def execute(self, command: str) -> str:
        data = subprocess.check_output(command, shell=True, timeout=5)
        return data.decode('utf-8')


class CommandExecutorMemory(CommandExecutor):
    def __init__(self) -> None:
        self.commands: str = []

    def execute(self, command: str) -> str:
        self.commands.append(command)
        return command


class CommandExecutorFactory:
    @staticmethod
    def create() -> CommandExecutor:
        return (
            CommandExecutorImpl()
            if os.getenv('COMMAND_EXECUTOR_ENV') != 'TEST'
            else CommandExecutorMemory()
        )
