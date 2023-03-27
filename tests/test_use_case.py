from checkuser.data.repositories.device.memory import DeviceRepositoryMemory
from checkuser.data.repositories.user.memory import UserRepositoryMemory
from checkuser.domain.usecases.checkuser import CheckUserUseCase


def test_should_check_user():
    user_repository = UserRepositoryMemory()
    device_repository = DeviceRepositoryMemory()

    use_case = CheckUserUseCase(user_repository, device_repository)
    data = use_case.execute('test1', 'abc123')

    assert data.id == 1000
    assert data.username == 'test1'


def test_should_test_device_limit() -> None:
    user_repository = UserRepositoryMemory()
    device_repository = DeviceRepositoryMemory()

    use_case = CheckUserUseCase(user_repository, device_repository)
    data = use_case.execute('test3', 'abc123')
    assert data.count_connections == 1

    data = use_case.execute('test3', 'abc124')
    assert data.count_connections == 2

    data = use_case.execute('test3', 'abc123')
    assert data.count_connections == 1
