from datetime import datetime
from typing import List
from checkuser.domain.entities.user import User
from checkuser.domain.interfaces.user_repository import UserRepository


class UserRepositoryMemory(UserRepository):
    def __init__(self):
        self.users = [
            User(1000, 'test1', datetime(2023, 1, 1), 10),
            User(1002, 'test2', datetime(2023, 1, 1), 10),
            User(1003, 'test3', datetime(2023, 1, 1), 1),
        ]

    def get(self, username: str) -> User:
        try:
            return next(user for user in self.users if user.username == username)
        except StopIteration:
            raise ValueError('User not found')

    def get_all(self) -> List[User]:
        return self.users

    def save(self, user: User) -> None:
        self.users.append(user)
