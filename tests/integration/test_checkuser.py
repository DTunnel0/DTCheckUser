import pytest
import os

os.environ['DRIVEN_ENV'] = 'TEST'

from flask.testing import FlaskClient

from checkuser.infra.main import create_app
from checkuser.data.database.sqlite import delete_database


@pytest.fixture()
def client():
    app = create_app()
    app.config.update({'TESTING': True})
    return app.test_client()


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    delete_database()

    yield

    delete_database()


def test_check_user(client: FlaskClient) -> None:
    url = '/check/test?deviceId=1000'
    data = client.get(url)

    assert data.status_code == 200
    assert data.json['username'] == 'test'
    assert data.json['limit_connections'] == 1
    assert data.json['count_connections'] == 1


def test_check_user_not_exsists(client: FlaskClient) -> None:
    url = '/check/test01?deviceId=1000'
    data = client.get(url)

    assert data.status_code == 500
    assert data.json['error'] == 'Could not find'
