import flask
import flask_session 
import tempfile

class TestFileSystem:

    def setup_method(self, _):
        pass

    def test_basic(self, app):
        app.config['SESSION_TYPE'] = 'filesystem'
        app.config['SESSION_FILE_DIR'] = tempfile.gettempdir()
        flask_session.Session(app)

        # Should be using Redis class
        with app.test_request_context():
            isinstance(flask.session, flask_session.sessions.FileSystemSession)

        client = app.test_client()
        assert client.post('/set', data={'value': '42'}).data == b'value set'
        assert client.get('/get').data ==  b'42'
        client.post('/delete')