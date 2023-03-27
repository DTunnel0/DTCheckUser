from checkuser.domain.usecases.device.list_all_devices import ListAllDevicesUseCase


class ListAllDevicesPresenter:
    def __init__(self, list_all_devices_use_case: ListAllDevicesUseCase) -> None:
        self.list_all_devices_use_case = list_all_devices_use_case

    def present(self) -> None:
        data = self.list_all_devices_use_case.execute()

        if not data:
            print('Devices not founds')
            return

        print('-' * 50)
        print('{0:<33} {1}'.format('ID', 'NOME DE USUARIO'))
        print('-' * 50)
        for device in data:
            print('%-33s %s ' % (device.id, device.username))
            print('-' * 50)
