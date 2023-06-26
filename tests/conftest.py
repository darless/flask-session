import sys
sys.path.append('src')

import flask
import pytest

@pytest.fixture(scope='function')
def app():
    app = flask.Flask(__name__)

    @app.route('/set', methods=['POST'])
    def app_set():
        flask.session['value'] = flask.request.form['value']
        return 'value set'
    @app.route('/delete', methods=['POST'])
    def app_del():
        del flask.session['value']
        return 'value deleted'

    @app.route('/get')
    def app_get():
        return flask.session.get('value')

    yield app