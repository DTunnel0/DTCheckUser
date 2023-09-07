import datetime
import re
import logging
import os

from abc import ABCMeta, abstractmethod
from typing import Union, List

from checkuser.data.executor import CommandExecutor
from checkuser.data.executor import CommandExecutorFactory

logger = logging.getLogger(__name__)


class Driven(metaclass=ABCMeta):
    @abstractmethod
    def get_id(self, username: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_expiration_date(self, username: str) -> Union[datetime.datetime, None]:
        raise NotImplementedError

    @abstractmethod
    def get_connection_limit(self, username: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_users(self) -> List[str]:
        raise NotImplementedError


class FormatDate(metaclass=ABCMeta):
    @abstractmethod
    def format(self, date: str) -> datetime.datetime:
        raise NotImplementedError


class FormatDateUS(FormatDate):
    def format(self, date: str) -> datetime.datetime:
        return datetime.datetime.strptime(date, '%b %d, %Y')


class FormatDateBR(FormatDate):
    def format(self, date: str) -> datetime.datetime:
        return datetime.datetime.strptime(date, '%b %d, %Y')


class DrivenImpl(Driven):
    def __init__(self, executor: CommandExecutor, format_date: FormatDate):
        self.executor = executor
        self.format_date = format_date

    def get_id(self, username: str) -> int:
        try:
            command = 'id -u {}'.format(username)
            return int(self.executor.execute(command))
        except Exception as err:
            logger.exception(err)
            return -1

    def get_expiration_date(self, username: str) -> Union[datetime.datetime, None]:
        try:
            command = 'chage -l {}'.format(username)
            output = self.executor.execute(command)
            search = re.search(r'Account expires\s*:\s*(.*)', output)
            expiration_date = self.format_date.format(search.group(1)) if search else None
            return expiration_date
        except Exception as err:
            logger.exception(err)
            return None

    def get_connection_limit(self, username: str) -> int:
        try:
            logger.info('Checking limit with DTunnelManager')
            cmd = 'vps view -u {} | grep connection_limit: | cut -d\' \' -f2'.format(username)
            return int(self.executor.execute(cmd))
        except Exception as err:
            logger.exception(err)

        try:
            archive = '/root/usuarios.db'
            logger.debug('Checking limit with {}'.format(archive))
            with open(archive) as f:
                data = f.read()
                search = re.search(r'{}\s+(\d+)'.format(username), data)
                return int(search.group(1)) if search else 1
        except Exception as err:
            logger.exception(err)
            return 1

    def get_users(self) -> List[str]:
        command = 'cat /etc/passwd'
        output = self.executor.execute(command)
        return re.findall(r'^([^:]+):', output, re.MULTILINE)


class DrivenMemory(Driven):
    def __init__(self) -> None:
        self.users: List[dict] = [
            {
                'id': 1000,
                'username': 'test',
                'password': 'test',
                'expiration_date': datetime.datetime.now(),
                'connection_limit': 1,
            }
        ]

    def get_id(self, username: str) -> int:
        for user in self.users:
            if user['username'] == username:
                return user['id']
        raise ValueError('Could not find')

    def get_expiration_date(self, username: str) -> Union[datetime.datetime, None]:
        for user in self.users:
            if user['username'] == username:
                return user['expiration_date']
        return None

    def get_connection_limit(self, username: str) -> int:
        for user in self.users:
            if user['username'] == username:
                return user['connection_limit']
        return 0

    def get_users(self) -> List[str]:
        return [user['username'] for user in self.users]


class DrivenFactory:
    @staticmethod
    def create() -> Driven:
        return (
            DrivenImpl(CommandExecutorFactory.create(), FormatDateUS())
            if os.getenv('DRIVEN_ENV') != 'TEST'
            else DrivenMemory()
        )
