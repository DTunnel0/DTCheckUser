from checkuser.data.repositories.device.memory import DeviceRepositoryMemory
from checkuser.domain.entities.device import Device
from checkuser.domain.usecases.device.list_by_username import ListDeviceUseCase


def test_deve_listar_todos_os_devices_apartir_de_um_usuario() -> None:
    device_repository = DeviceRepositoryMemory()
    device_repository.devices = [
        Device(id='ID1', username='test'),
        Device(id='ID2', username='test'),
    ]

    device_list_use_case = ListDeviceUseCase(device_repository)
    data = device_list_use_case.execute('test')

    assert data[0].id == 'ID1'
    assert data[1].id == 'ID2'
