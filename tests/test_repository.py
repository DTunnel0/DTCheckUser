import pytest
import sqlite3

from unittest.mock import Mock
from datetime import datetime, timedelta
from checkuser.data.driver import FormatDateUS

from checkuser.data.executor import CommandExecutorImpl
from checkuser.data.repository import UserRepositoryImpl
from checkuser.domain.user import User


# @pytest.mark.skip
def test_should_get_user_by_username():
    username = 'test'

    executor = CommandExecutorImpl()
    format_date = FormatDateUS()
    # driver = DriverImpl(executor, format_date)
    driver = Mock()
    driver.get_id.return_value = 1000
    driver.get_expiration_date.return_value = datetime.now() + timedelta(days=1)
    driver.get_connection_limit.return_value = 1
    driver.get_users.return_value = [username]
    conn = sqlite3.connect('db.sqlite3')
    repository = UserRepositoryImpl(driver, conn)

    user = repository.get_by_username(username)
    assert user.id == 1000
    assert user.username == username
    assert user.expiration_date is not None
    assert user.connection_limit == 1


@pytest.mark.skip
def test_should_save_user():
    user = User(1002, 'test', datetime.now(), 1)

    conn = sqlite3.connect('db.sqlite3')
    # cmd = '''
    #     CREATE TABLE users (
    #         id INTEGER PRIMARY KEY,
    #         username TEXT NOT NULL,
    #         expiration_date DATE NOT NULL,
    #         connection_limit INTEGER NOT NULL
    #     );
    # '''
    # conn.execute(cmd)
    # conn.commit()

    # cmd = '''
    #     CREATE TABLE devices (
    #         id TEXT PRIMARY KEY
    #     );
    # '''
    # conn.execute(cmd)
    # conn.commit()

    # cmd = '''
    #     CREATE TABLE user_device (
    #         user_id INTEGER NOT NULL,
    #         device_id TEXT NOT NULL,
    #         FOREIGN KEY (user_id) REFERENCES users (id),
    #         FOREIGN KEY (device_id) REFERENCES devices (id),
    #         PRIMARY KEY (user_id, device_id)
    #     );
    # '''
    # conn.execute(cmd)
    # conn.commit()

    driver = Mock()
    driver.get_id.return_value = 1000
    driver.get_expiration_date.return_value = datetime.now() + timedelta(days=1)
    driver.get_connection_limit.return_value = 0
    driver.get_users.return_value = ['test']

    repo = UserRepositoryImpl(driver, conn)
    repo.save(user)
