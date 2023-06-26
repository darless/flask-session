import flask
import flask_session 

class TestMongoDB:

    def test_basic(self, app):
        app.config['SESSION_TYPE'] = 'mongodb'
        flask_session.Session(app)

        # Should be using Redis class
        with app.test_request_context():
            isinstance(flask.session, flask_session.sessions.MongoDBSession)