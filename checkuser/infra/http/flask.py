from flask import Flask
from checkuser.infra.factories.make_controller import Controllers
from checkuser.infra.adapter import FlaskAdpater

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SECRET_KEY'] = 'secret!'

app.add_url_rule(
    '/check/<string:username>',
    methods=['GET'],
    endpoint='check',
    view_func=FlaskAdpater.adapt(Controllers.get('check')),
)
app.add_url_rule(
    '/kill/<string:username>',
    methods=['GET'],
    endpoint='kill',
    view_func=FlaskAdpater.adapt(Controllers.get('kill')),
)
app.add_url_rule(
    '/all',
    methods=['GET'],
    endpoint='all',
    view_func=FlaskAdpater.adapt(Controllers.get('all')),
)
