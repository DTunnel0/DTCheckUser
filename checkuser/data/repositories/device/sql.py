from sqlite3 import Connection
from typing import List
from checkuser.domain.entities.device import Device
from checkuser.domain.interfaces.device_repository import DeviceRepository


class DeviceRepositorySQL(DeviceRepository):
    def __init__(self, conn: Connection):
        self.sqlite = conn

    def exists(self, username: str, id: str) -> bool:
        cmd = 'SELECT * FROM devices WHERE username = ? AND device_id = ?'
        data = self.sqlite.execute(cmd, (username, id)).fetchall()
        return bool(data)

    def save(self, device: Device) -> None:
        cmd = 'INSERT INTO devices (device_id, username) VALUES (?,?)'
        self.sqlite.execute(cmd, (device.id, device.username))
        self.sqlite.commit()

    def list_devices(self, username: str) -> List[Device]:
        cmd = 'SELECT * FROM devices WHERE username = ?'
        data = self.sqlite.execute(cmd, (username,)).fetchall()
        return [Device(device[1], device[2]) for device in data]

    def count(self, username: str) -> int:
        cmd = 'SELECT COUNT(*) FROM devices WHERE username = ?'
        return self.sqlite.execute(cmd, (username,)).fetchone()[0]

    def delete_by_username(self, username: str) -> None:
        cmd = 'DELETE FROM devices WHERE username = ?'
        self.sqlite.execute(cmd, (username,))
        self.sqlite.commit()

    def list_all(self) -> List[Device]:
        cmd = 'SELECT * FROM devices'
        data = self.sqlite.execute(cmd).fetchall()
        return [Device(device[1], device[2]) for device in data]
