from checkuser.domain.interfaces.device_repository import DeviceRepository


class DeleteByUsernameUseCase:
    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    def execute(self, username: str) -> None:
        self.device_repository.delete_by_username(username)
