from checkuser.data.repositories.device.memory import DeviceRepositoryMemory
from checkuser.domain.entities.device import Device
from checkuser.domain.usecases.device.list_all_devices import ListAllDevicesUseCase


def test_list_all_devices() -> None:
    device_repository = DeviceRepositoryMemory()
    device_repository.devices = [
        Device(id='ID1', username='test'),
        Device(id='ID2', username='test'),
        Device(id='ID3', username='test1'),
    ]

    list_all_devices_use_case = ListAllDevicesUseCase(device_repository)
    data = list_all_devices_use_case.execute()

    assert len(data) == 3
