from unittest.mock import Mock
from checkuser.data.connection import SSHConnection, OpenVPNConnection


def test_should_count_ssh_connections():
    executor = Mock()
    executor.execute.return_value = '5'
    connection_count = SSHConnection(executor)
    assert connection_count.count('test') == 5


def test_should_count_openvpn_connections():
    connection = Mock()
    connection.__enter__ = Mock()
    connection.__exit__ = Mock()
    connection.receive.return_value = 'test test test test'
    connection_count = OpenVPNConnection(connection)
    assert connection_count.count('test') == 2
