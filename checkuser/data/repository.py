import datetime
import sqlite3

from typing import List

from checkuser.data.driver import Driver
from checkuser.domain.user import Device, User
from checkuser.domain.repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, driver: Driver, conn: sqlite3.Connection):
        self.driver = driver
        self.sqlite = conn

    def get_by_username(self, username: str) -> User:
        cmd = 'SELECT * FROM users WHERE username = ?'
        res = self.sqlite.execute(cmd, (username,))
        data = res.fetchall()
        print(data[0])

        if data:
            user = User(
                data[0][0],
                data[0][1],
                datetime.datetime.fromisoformat(data[0][2]),
                data[0][3],
            )

            cmd = 'SELECT * FROM user_device WHERE user_id = ?'
            res = self.sqlite.execute(cmd, (user.id,))
            data = res.fetchall()

            for device_id in data:
                cmd = 'SELECT * FROM devices WHERE id = ?'
                res = self.sqlite.execute(cmd, (device_id[0],))
                device = res.fetchall()
                user.add_device(Device(device[0][0]))

            return user

        user_id = self.driver.get_id(username)
        expiration_date = self.driver.get_expiration_date(username)
        connection_limit = self.driver.get_connection_limit(username)
        user = User(user_id, username, expiration_date, connection_limit)
        self.save(user)
        return user

    def get_all(self) -> List[User]:
        users = self.driver.get_users()
        return [self.get_by_username(user) for user in users]

    def save(self, user: User) -> None:
        cmd = 'INSERT INTO users (id, username, expiration_date, connection_limit) VALUES (?, ?, ?, ?)'
        self.sqlite.execute(
            cmd, (user.id, user.username, user.expiration_date, user.connection_limit)
        )
        self.sqlite.commit()

        for device in user.devices:
            cmd = 'INSERT INTO user_device (user_id, device_id) VALUES (?, ?)'
            self.sqlite.execute(cmd, (user.id, device.id))
            self.sqlite.commit()


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = [
            User(1000, 'user1', datetime.datetime(2023, 1, 1), 10),
            User(1002, 'user2', datetime.datetime(2023, 1, 1), 10),
        ]

    def get_by_username(self, username: str) -> User:
        try:
            return next(user for user in self.users if user.username == username)
        except StopIteration:
            raise ValueError('User not found')

    def get_all(self) -> List[User]:
        return self.users

    def save(self, user: User) -> None:
        self.users.append(user)
