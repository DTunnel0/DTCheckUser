from checkuser.domain.usecases.device.list_by_username import ListDeviceUseCase


class ListDevicesPresenter:
    def __init__(self, list_devices_use_case: ListDeviceUseCase) -> None:
        self.list_devices_use_case = list_devices_use_case

    def present(self, username: str) -> None:
        data = self.list_devices_use_case.execute(username)

        if not data:
            print('Devices not founds')
            return

        print('-' * 50)
        for device in data:
            print('%s - %s ' % (device.id, device.username))
            print('-' * 50)
