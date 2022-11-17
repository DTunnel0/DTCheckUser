from unittest.mock import Mock
from checkuser.checker import ConnectionCountSSH, ConnectionCountOpenVPN, OpenVPNConnection


def test_should_count_ssh_connections():
    executor = Mock()
    executor.execute.return_value = '5'
    connection_count = ConnectionCountSSH(executor, 'test')
    assert connection_count.count() == 5


def test_should_count_openvpn_connections():
    connection = Mock()
    connection.receive.return_value = 'test test test test'
    connection_count = ConnectionCountOpenVPN(connection, 'test')
    assert connection_count.count() == 2
