import sys
sys.path.append('src')
import flask_session

import flask
import pytest

@pytest.fixture(scope='function')
def app_utils():
    class Utils:
        def create_app(self, config_dict=None):
            app = flask.Flask(__name__)
            if config_dict:
                app.config.update(config_dict)

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

            flask_session.Session(app)
            return app

        def test_session_set(self, app):
            client = app.test_client()
            assert client.post('/set', data={'value': '42'}).data == b'value set'
            assert client.get('/get').data ==  b'42'
            client.post('/delete')

    return Utils()
