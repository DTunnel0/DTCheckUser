import socket
import re

from abc import ABCMeta, abstractmethod
from typing import List

from checkuser.data.executor import CommandExecutor
from checkuser.domain.interfaces.connection import Connection, ConnectionKiller


class SSHConnection(ConnectionKiller):
    def __init__(self, executor: CommandExecutor):
        self.executor = executor

    def count(self, username: str) -> int:
        cmd = 'ps -u {} | grep sshd | wc -l'.format(username)
        count = int(self.executor.execute(cmd))
        if self._next_handler:
            count += self._next_handler.count(username)
        return count

    def kill(self, username: str) -> None:
        cmd = 'kill -9 $(ps -u {} | grep sshd | awk \'{{print $1}}\')'.format(username)
        self.executor.execute(cmd)

        if self._next_handler:
            self._next_handler.kill(username)

    def all(self) -> int:
        cmd = 'ps -ef | grep sshd | grep -v grep | grep -v root | wc -l'
        all = int(self.executor.execute(cmd))
        if self._next_handler:
            all += self._next_handler.all()
        return all


class AUXOpenVPNConnection(metaclass=ABCMeta):
    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def send(self, data: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def receive(self, size: int = 1024) -> str:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    def __enter__(self) -> 'AUXOpenVPNConnection':
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


class AUXOpenVPNConnectionImpl(AUXOpenVPNConnection):
    __socket: socket.socket

    def __init__(self, host: str = '127.0.0.1', port: int = 7505) -> None:
        self.host = host
        self.port = port

    def connect(self) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.host, self.port))

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


class OpenVPNConnection(ConnectionKiller):
    def __init__(self, connection: AUXOpenVPNConnection) -> None:
        self.connection = connection

    def count(self, username: str) -> int:
        try:
            with self.connection:
                self.connection.send('status\n')
                data = self.connection.receive()
                count = data.count(username)
                count = count // 2 if count > 0 else 0
                if self._next_handler:
                    count += self._next_handler.count(username)
                return count
        except Exception:
            return 0

    def kill(self, username: str) -> None:
        with self.connection:
            self.connection.send('kill {}\n'.format(username))

        if self._next_handler:
            self._next_handler.kill(username)

    def all(self) -> int:
        try:
            with self.connection:
                self.connection.send('status\n')
                data = self.connection.receive()
                pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3},\w+,)')
                all = len(pattern.findall(data))
                if self._next_handler:
                    all += self._next_handler
                return all
        except Exception:
            return 0


class V2RayService:
    __log_file = '/var/log/v2ray/access.log'

    def __init__(self, executor: CommandExecutor):
        self.executor = executor

    def __find_v2ray_port(self) -> str:
        cmd = 'netstat -tlpn | grep v2ray'
        data = self.executor.execute(cmd).splitlines()[-1]
        return data.split()[3].split(':')[-1]

    def __find_addresses(self) -> list:
        addresses = []
        try:
            cmd = (
                'netstat -np 2>/dev/null | grep :%s | grep ESTABLISHED | awk \'{print $5}\' | sort | uniq'
                % self.__find_v2ray_port()
            )
            addresses.extend(self.executor.execute(cmd).splitlines())
        except Exception:
            pass

        return addresses

    def count(self, username: str) -> int:
        try:
            data = self.executor.execute('tail -n 1000 %s' % self.__log_file)
            for address in self.__find_addresses():
                pattern = r'%s.*email: %s' % (address, username)
                if re.search(pattern, data):
                    return 1
            return 0
        except Exception:
            return 0

    def all(self) -> int:
        try:
            data = self.executor.execute('tail -n 1000 %s' % self.__log_file)
            emails = []
            for address in self.__find_addresses():
                pattern = r'%s.*email: (\S+)' % address
                email = re.search(pattern, data)
                if email and email.group(1) not in emails:
                    emails.append(email.group(1))
            return len(emails)
        except Exception:
            return 0


class V2rayConnection(Connection):
    def __init__(self, service: V2RayService):
        self.service = service

    def count(self, username: str) -> int:
        count = self.service.count(username)
        if self._next_handler:
            count += self._next_handler.count(username)
        return count

    def all(self) -> int:
        all = self.service.all()
        if self._next_handler:
            all += self._next_handler.all()
        return all


class ConnectionMemory(ConnectionKiller):
    def __init__(self):
        self.users: List[dict] = [
            {
                'name': 'test',
                'connections': 1,
                'killed': False,
            }
        ]

    def count(self, username: str) -> int:
        count = next((user['connections'] for user in self.users if user['name'] == username), 0)
        return count

    def kill(self, username: str) -> None:
        for user in self.users:
            if user['name'] == username:
                user['killed'] = True

        if self._next_handler:
            self._next_handler.kill(username)

    def all(self) -> int:
        all = sum(user['connections'] for user in self.users)
        if self._next_handler:
            all += self._next_handler.all()
        return all
