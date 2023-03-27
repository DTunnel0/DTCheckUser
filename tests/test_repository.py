from checkuser.data.repositories.user.impl import UserRepositoryImpl
from checkuser.data.driven import DrivenMemory


def test_should_get_user_by_username():
    driver = DrivenMemory()
    repository = UserRepositoryImpl(driver)

    username = 'test'
    user = repository.get(username)
    assert user.id == 1000
    assert user.username == username
    assert user.expiration_date is not None
    assert user.connection_limit == 1
