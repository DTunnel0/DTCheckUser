from checkuser.data.database.sqlite import create_connection
from checkuser.data.repositories.device.sql import DeviceRepositorySQL
from checkuser.domain.usecases.device.delete_by_username import DeleteByUsernameUseCase
from checkuser.domain.usecases.device.list_all_devices import ListAllDevicesUseCase
from checkuser.domain.usecases.device.list_by_username import ListDeviceUseCase


def make_list_devices_use_case() -> ListDeviceUseCase:
    device_repository = DeviceRepositorySQL(create_connection())
    return ListDeviceUseCase(device_repository)


def make_delete_devices_use_case() -> DeleteByUsernameUseCase:
    device_repository = DeviceRepositorySQL(create_connection())
    return DeleteByUsernameUseCase(device_repository)


def make_list_all_devices_use_case() -> ListAllDevicesUseCase:
    device_repository = DeviceRepositorySQL(create_connection())
    return ListAllDevicesUseCase(device_repository)
