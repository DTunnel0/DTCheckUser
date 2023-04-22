from typing import Callable

from checkuser.data.database.sqlite import create_connection
from checkuser.data.repositories.device.sql import DeviceRepositorySQL
from checkuser.data.repositories.user.impl import UserRepositoryImpl

from checkuser.domain.usecases.all import AllConnectionsUseCase
from checkuser.domain.usecases.checkuser import CheckUserUseCase
from checkuser.domain.usecases.kill import KillConnectionUseCase

from checkuser.infra.controller import Controller
from checkuser.infra.controllers.check_user import CheckUserController
from checkuser.infra.controllers.kill_connection import KillConnectionController
from checkuser.infra.controllers.all_connections import AllConnectionsController

from checkuser.data.executor import CommandExecutorFactory
from checkuser.data.driven import DrivenFactory
from checkuser.data.connection import (
    AUXOpenVPNConnectionImpl,
    SSHConnection,
    OpenVPNConnection,
    V2rayConnection,
    V2RayService,
)


def make_controller() -> CheckUserController:
    user_repository = UserRepositoryImpl(DrivenFactory.create())
    device_repository = DeviceRepositorySQL(create_connection())

    return CheckUserController(
        CheckUserUseCase(
            user_repository=user_repository,
            device_repository=device_repository,
        )
    )


def make_kill_controller() -> KillConnectionController:
    cmd = CommandExecutorFactory.create()
    aux = AUXOpenVPNConnectionImpl()
    ssh = SSHConnection(cmd)
    ssh.set_next_handler(OpenVPNConnection(aux))
    return KillConnectionController(KillConnectionUseCase(ssh))


def make_all_controller() -> AllConnectionsController:
    cmd = CommandExecutorFactory.create()
    aux = AUXOpenVPNConnectionImpl()
    v2 = V2RayService(cmd)

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
