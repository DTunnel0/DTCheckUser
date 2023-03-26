from checkuser.data.driver import DriverMemory

from checkuser.data.repository import UserRepositoryImpl


def test_should_get_user_by_username():
    driver = DriverMemory()
    repository = UserRepositoryImpl(driver)

    username = 'test'
    user = repository.get(username)
    assert user.id == 1000
    assert user.username == username
    assert user.expiration_date is not None
    assert user.connection_limit == 1
