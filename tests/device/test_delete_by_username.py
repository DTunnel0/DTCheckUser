from checkuser.data.repositories.device.memory import DeviceRepositoryMemory
from checkuser.domain.entities.device import Device
from checkuser.domain.usecases.device.delete_by_username import DeleteByUsernameUseCase


def test_deve_deletar_todos_os_devices_apartir_de_um_usuario() -> None:
    device_repository = DeviceRepositoryMemory()
    device_repository.devices = [
        Device(id='ID1', username='test'),
        Device(id='ID2', username='test'),
        Device(id='ID3', username='test1'),
    ]

    delete_by_username_use_case = DeleteByUsernameUseCase(device_repository)
    delete_by_username_use_case.execute('test')

    assert len(device_repository.devices) == 1
