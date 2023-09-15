from flask import Blueprint, render_template_string

from checkuser.infra.factories.make_controller import ControllerFactory
from checkuser.infra.adapter import FlaskAdpater
from checkuser.utils.page import get_page_content


def register_route(app: Blueprint):
    app.add_url_rule(
        '/check/<string:username>',
        methods=['GET'],
        endpoint='check',
        view_func=FlaskAdpater.adapt(ControllerFactory.get('check')),
    )
    app.add_url_rule(
        '/kill/<string:username>',
        methods=['GET'],
        endpoint='kill',
        view_func=FlaskAdpater.adapt(ControllerFactory.get('kill')),
    )
    app.add_url_rule(
        '/all',
        methods=['GET'],
        endpoint='all',
        view_func=FlaskAdpater.adapt(ControllerFactory.get('all')),
    )
    app.add_url_rule(
        '/',
        methods=['GET'],
        endpoint='page',
        view_func=lambda: render_template_string(get_page_content()),
    )
