from typing import Callable

from checkuser.data.database.sqlite import create_connection

from checkuser.domain.usecases.all import AllConnectionsUseCase
from checkuser.domain.usecases.checkuser import CheckUserUseCase
from checkuser.domain.usecases.kill import KillConnectionUseCase

from checkuser.infra.controller import Controller
from checkuser.infra.controllers.check_user import CheckUserController
from checkuser.infra.controllers.kill_connection import KillConnectionController
from checkuser.infra.controllers.all_connections import AllConnectionsController

from checkuser.data.executor import CommandExecutorImpl
from checkuser.data.driver import DriverImpl, FormatDateUS
from checkuser.data.repository import DeviceRepositorySQL, UserRepositoryImpl
from checkuser.data.connection import (
    AUXOpenVPNConnection,
    SSHConnection,
    OpenVPNConnection,
    V2rayConnection,
    V2RayService,
)


def make_controller() -> CheckUserController:
    user_repository = UserRepositoryImpl(
        DriverImpl(
            CommandExecutorImpl(),
            FormatDateUS(),
        ),
    )

    device_repository = DeviceRepositorySQL(create_connection())

    return CheckUserController(
        CheckUserUseCase(
            user_repository=user_repository,
            device_repository=device_repository,
        )
    )


def make_kill_controller() -> KillConnectionController:
    cmd = CommandExecutorImpl()
    aux = AUXOpenVPNConnection()
    ssh = SSHConnection(cmd)
    ssh.set_next_handler(OpenVPNConnection(aux))
    return KillConnectionController(KillConnectionUseCase(ssh))


def make_all_controller() -> AllConnectionsController:
    cmd = CommandExecutorImpl()
    aux = AUXOpenVPNConnection()
    v2 = V2RayService(CommandExecutorImpl())

    ssh = SSHConnection(cmd)
    ssh.set_next_handler(OpenVPNConnection(aux)).set_next_handler(V2rayConnection(v2))
    return AllConnectionsController(AllConnectionsUseCase(ssh))


class ControllerFactory:
    @staticmethod
    def get(controller: str) -> Callable[..., Controller]:
        __controllers = {
            'check': make_controller,
            'kill': make_kill_controller,
            'all': make_all_controller,
        }
        return __controllers[controller]
