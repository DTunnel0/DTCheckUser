import sqlite3


CREATE_DEVICE_TABLE = '''
CREATE TABLE IF NOT EXISTS 'devices' (
    id VARCHAR(256) PRIMARY KEY,
    username VARCHAR(255)
);
'''

DEFAULT_URI = './db.sqlite3'


def create_connection(db_uri: str = DEFAULT_URI) -> sqlite3.Connection:
    conn = sqlite3.connect(db_uri)
    conn.row_factory = sqlite3.Row
    conn.executescript(CREATE_DEVICE_TABLE)
    return conn
