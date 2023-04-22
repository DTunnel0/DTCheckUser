from checkuser.domain.usecases.device.list_all_devices import ListAllDevicesUseCase


class ListAllDevicesPresenter:
    def __init__(self, list_all_devices_use_case: ListAllDevicesUseCase) -> None:
        self.list_all_devices_use_case = list_all_devices_use_case

    def present(self) -> str:
        data = self.list_all_devices_use_case.execute()

        if not data:
            return 'Devices not found'

        message = '-' * 50 + '\n'
        message += '{0:<33} {1}'.format('ID', 'NOME DE USUARIO') + '\n'
        message += '-' * 50 + '\n'
        for device in data:
            message += '%-33s %s ' % (device.id, device.username) + '\n'
            message += '-' * 50

        return message
