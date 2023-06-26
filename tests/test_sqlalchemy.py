import flask
import flask_session 

class TestSQLAlchemy:

    def test_basic(self, app):
        app.config['SESSION_TYPE'] = 'sqlalchemy'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        flask_session.Session(app)

        with app.test_request_context():
            isinstance(flask.session, flask_session.sessions.SqlAlchemySession)
            app.session_interface.db.create_all()

        client = app.test_client()
        assert client.post('/set', data={'value': '42'}).data == b'value set'
        assert client.get('/get').data ==  b'42'
        client.post('/delete')

    def test_use_signer(self, app):
        app.config['SESSION_TYPE'] = 'sqlalchemy'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['SQLALCHEMY_USE_SIGNER'] = True
        flask_session.Session(app)

        with app.test_request_context():
            isinstance(flask.session, flask_session.sessions.SqlAlchemySession)
            app.session_interface.db.create_all()

        client = app.test_client()
        assert client.post('/set', data={'value': '42'}).data == b'value set'
        assert client.get('/get').data ==  b'42'
        client.post('/delete')