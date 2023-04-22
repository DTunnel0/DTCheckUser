from checkuser.domain.usecases.device.list_by_username import ListDeviceUseCase


class ListDevicesPresenter:
    def __init__(self, list_devices_use_case: ListDeviceUseCase) -> None:
        self.list_devices_use_case = list_devices_use_case

    def present(self, username: str) -> str:
        data = self.list_devices_use_case.execute(username)

        if not data:
            return 'Devices not founds'

        message = '-' * 50 + '\n'
        message += '{0:<33} {1}'.format('ID', 'NOME DE USUARIO') + '\n'
        message += '-' * 50 + '\n'
        for device in data:
            message += '%-33s %s ' % (device.id, device.username) + '\n'
            message += '-' * 50

        return message
