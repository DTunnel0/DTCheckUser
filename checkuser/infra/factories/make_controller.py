from checkuser.infra.controller import Controller
from checkuser.infra.controllers.check_user import CheckUserController
from checkuser.infra.controllers.kill_connection import KillConnectionController
from checkuser.infra.controllers.all_connections import AllConnectionsController

from checkuser.data.executor import CommandExecutorImpl
from checkuser.data.driver import DriverImpl, FormatDateUS
from checkuser.data.repository import UserRepositoryImpl, InMemoryUserRepository
from checkuser.domain.use_case import CheckUserUseCase, KillConnectionUseCase, AllConnectionsUseCase
from checkuser.data.connection import (
    AUXOpenVPNConnection,
    ConnectionImpl,
    SSHConnection,
    OpenVPNConnection,
    InMemoryConnection,
)

from checkuser.infra.adapter import WebSocketAdapter


def make_controller() -> CheckUserController:
    repository = UserRepositoryImpl(
        DriverImpl(
            CommandExecutorImpl(),
            FormatDateUS(),
        ),
    )
    connection = ConnectionImpl(
        [
            SSHConnection(CommandExecutorImpl()),
            OpenVPNConnection(AUXOpenVPNConnection()),
        ]
    )

    # return CheckUserController(
    #     CheckUserUseCase(
    #         InMemoryUserRepository(),
    #         InMemoryConnection(),
    #     )
    # )

    return CheckUserController(CheckUserUseCase(repository, connection))


def make_kill_controller() -> KillConnectionController:
    connection = ConnectionImpl(
        [
            SSHConnection(CommandExecutorImpl()),
            OpenVPNConnection(AUXOpenVPNConnection()),
        ]
    )

    # return KillConnectionController(KillConnectionUseCase(InMemoryConnection()))
    return KillConnectionController(KillConnectionUseCase(connection))


def make_all_controller() -> AllConnectionsController:
    connection = ConnectionImpl(
        [
            SSHConnection(CommandExecutorImpl()),
            OpenVPNConnection(AUXOpenVPNConnection()),
        ]
    )

    return AllConnectionsController(AllConnectionsUseCase(connection))
    # return AllConnectionsController(AllConnectionsUseCase(InMemoryConnection()))


class Controllers:
    _controllers = {
        'check': make_controller(),
        'kill': make_kill_controller(),
        'all': make_all_controller(),
    }

    @staticmethod
    def get(controller: str) -> Controller:
        return Controllers._controllers[controller]
