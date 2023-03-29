from unittest.mock import Mock
from checkuser.data.connection import (
    AUXOpenVPNConnection,
    ConnectionMemory,
    SSHConnection,
    OpenVPNConnection,
    V2rayConnection,
)
from checkuser.data.executor import CommandExecutor


class AUXOpenVPNConnectionMemory(AUXOpenVPNConnection):
    def __init__(self) -> None:
        self.connected = False
        self.sents = []
        self.data_receive = ''

    def connect(self) -> None:
        self.connected = True

    def send(self, data: str) -> None:
        self.sents.append(data)

    def receive(self, size: int = 1024) -> str:
        return self.data_receive[:size]

    def close(self) -> None:
        self.connected = False


class CommandExecutorMemory(CommandExecutor):
    def __init__(self) -> None:
        self.commands = []
        self.return_data = ''

    def set_return_data(self, return_data: str) -> None:
        self.return_data = return_data

    def execute(self, command: str) -> str:
        self.commands.append(command)
        return self.return_data


def test_should_count_ssh_connections():
    executor = CommandExecutorMemory()
    executor.set_return_data('5')

    connection_count = SSHConnection(executor)

    assert connection_count.count('test') == 5
    assert executor.commands[0] == 'ps -u test | grep sshd | wc -l'

    connection_count.kill('test')

    assert executor.commands[1] == 'kill -9 $(ps -u test | grep sshd | awk \'{print $1}\')'


def test_should_count_openvpn_connections():
    connection = AUXOpenVPNConnectionMemory()
    connection.data_receive = 'test test'

    openvpn = OpenVPNConnection(connection)

    assert openvpn.count('test') == 1
    assert not connection.connected
    assert connection.sents[0] == 'status\n'

    openvpn.kill('test')
    assert not connection.connected
    assert connection.sents[1] == 'kill test\n'


def test_should_count_v2ray_connections():
    service = Mock()
    service.count.return_value = 1
    service.all.return_value = 1

    connection = V2rayConnection(service)

    assert connection.count('test') == 1
    assert connection.all() == 1


def test_should_count_all_connections():
    connection = ConnectionMemory()
    connection.set_next_handler(ConnectionMemory()).set_next_handler(
        ConnectionMemory()
    ).set_next_handler(ConnectionMemory()).set_next_handler(ConnectionMemory())

    assert connection.all() == 5
