import sqlite3
import os


CREATE_DEVICE_TABLE = '''
CREATE TABLE IF NOT EXISTS 'devices' (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id VARCHAR(256),
    username VARCHAR(255)
);
'''

DEFAULT_URI = os.path.join(os.path.expanduser('~'), 'db.sqlite3')
if os.getenv('DEBUG'):
    DEFAULT_URI = './db.sqlite3'


def create_connection(db_uri: str = DEFAULT_URI) -> sqlite3.Connection:
    conn = sqlite3.connect(db_uri)
    conn.row_factory = sqlite3.Row
    conn.executescript(CREATE_DEVICE_TABLE)
    return conn


def delete_database(db_uri: str = DEFAULT_URI) -> None:
    if os.path.exists(db_uri):
        os.remove(db_uri)
