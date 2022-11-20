import socket

from typing import List
from checkuser.data.executor import CommandExecutor
from checkuser.domain.connection import Connection


class SSHConnection(Connection):
    def __init__(self, executor: CommandExecutor):
        self.executor = executor

    def count(self, username: str) -> int:
        cmd = 'ps -u {} | grep sshd | wc -l'.format(username)
        return int(self.executor.execute(cmd))

    def kill(self, username: str) -> None:
        cmd = 'kill -9 $(ps -u {} | grep sshd | awk \'{{print $1}}\')'.format(username)
        self.executor.execute(cmd)

    def all(self) -> int:
        cmd = 'ps -ef | grep sshd | grep -v grep | grep -v root | wc -l'
        return int(self.executor.execute(cmd))


class AUXOpenVPNConnection:
    __socket: socket.socket

    def __init__(self, host: str = '127.0.0.1', port: int = 7505) -> None:
        self.host = host
        self.port = port

    def send(self, data: str) -> None:
        self.__socket.send(data.encode())

    def receive(self, size: int = 1024) -> str:
        data = b''
        chunk = self.__socket.recv(size)
        while chunk.count(b'\r\nEND\r\n') == 0:
            data += chunk
            chunk = self.__socket.recv(size)
        data += chunk
        return data.decode()

    def close(self) -> None:
        self.__socket.close()

    def __enter__(self) -> 'AUXOpenVPNConnection':
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.host, self.port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


class OpenVPNConnection(Connection):
    def __init__(self, connection: AUXOpenVPNConnection) -> None:
        self.connection = connection

    def count(self, username: str) -> int:
        try:
            with self.connection:
                self.connection.send('status\n')
                data = self.connection.receive()
                count = data.count(username)
                return count // 2 if count > 0 else 0
        except Exception:
            raise
            return 0

    def kill(self, username: str) -> None:
        with self.connection:
            self.connection.send('kill {}\n'.format(username))

    def all(self) -> int:
        try:
            with self.connection:
                self.connection.send('status\n')
                data = self.connection.receive()
                return len(data.splitlines()) - 2
        except Exception:
            return 0


class ConnectionImpl(Connection):
    def __init__(self, counters: List[Connection]) -> None:
        self.counters = counters

    def count(self, username: str) -> int:
        return sum([count.count(username) for count in self.counters])

    def kill(self, username: str) -> None:
        for count in self.counters:
            count.kill(username)

    def all(self) -> int:
        return sum([count.all() for count in self.counters])


class InMemoryConnection(Connection):
    def count(self, username: str) -> int:
        return len(username)

    def kill(self, username: str) -> None:
        pass

    def all(self) -> int:
        return 100
