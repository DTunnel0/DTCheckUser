import flask

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
from checkuser.infra.controllers.check_user import CheckUserController
from checkuser.infra.controllers.kill_connection import KillConnectionController
from checkuser.infra.controllers.all_connections import AllConnectionsController

from checkuser.infra.adapter import FlaskAdpater

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


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


@app.route('/check/<username>')
def check_user(username):
    return FlaskAdpater.adapt(make_controller())


@app.route('/kill/<username>')
def kill_user(username):
    return FlaskAdpater.adapt(make_kill_controller())


@app.route('/all')
def all_connections():
    return FlaskAdpater.adapt(make_all_controller())
