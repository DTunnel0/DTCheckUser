from typing import List
from checkuser.data.driven import Driven
from checkuser.domain.entities.user import User
from checkuser.domain.interfaces.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, driver: Driven):
        self.driver = driver

    def get(self, username: str) -> User:
        user_id = self.driver.get_id(username)
        expiration_date = self.driver.get_expiration_date(username)
        connection_limit = self.driver.get_connection_limit(username)
        user = User(user_id, username, expiration_date, connection_limit)
        return user

    def get_all(self) -> List[User]:
        users = self.driver.get_users()
        return [self.get(user) for user in users]
