from checkuser.domain.usecases.device.delete_by_username import DeleteByUsernameUseCase


class DeleteDevicesPresenter:
    def __init__(self, delete_devices_use_case: DeleteByUsernameUseCase):
        self.delete_devices_use_case = delete_devices_use_case

    def present(self, username: str) -> None:
        self.delete_devices_use_case.execute(username)
        print('All deleted devices')
