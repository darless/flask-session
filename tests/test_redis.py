import flask
from redis import Redis
import flask_session

class TestRedisSession:

    def setup_method(self, method):
        # Clear redis
        r = Redis()
        r.flushall()

    def _has_redis_prefix(self, prefix):
        r = Redis()
        for key in r.keys():
            if key.startswith(prefix):
                return True
        return False

    def test_redis_default(self, app):
        app.config['SESSION_TYPE'] = 'redis'
        flask_session.Session(app)

        # Should be using Redis class
        with app.test_request_context():
            isinstance(flask.session, flask_session.sessions.RedisSession)

        client = app.test_client()
        assert client.post('/set', data={'value': '42'}).data == b'value set'
        assert client.get('/get').data ==  b'42'
        client.post('/delete')

        # There should be a session:<UUID> object
        assert self._has_redis_prefix(b'session:')

    def test_redis_key_prefix(self, app):
        #app = self._create_app()
        app.config['SESSION_TYPE'] = 'redis'
        app.config['SESSION_KEY_PREFIX'] = 'sess-prefix:'
        flask_session.Session(app)

        client = app.test_client()
        assert client.post('/set', data={'value': 'test2'}).data == b'value set'
        assert client.get('/get').data ==  b'test2'

        # There should be a key in Redis that starts with the prefix set
        assert not self._has_redis_prefix(b'session:')
        assert self._has_redis_prefix(b'sess-prefix:')

    def test_redis_with_signer(self, app):
        app.config['SESSION_TYPE'] = 'redis'
        app.config['SESSION_USE_SIGNER'] = True
        app.secret_key = 'test_key'
        flask_session.Session(app)

        client = app.test_client()
        assert client.post('/set', data={'value': 'test'}).data == b'value set'
        assert client.get('/get').data ==  b'test'

        # There should be a key in Redis that starts with the prefix set
        assert self._has_redis_prefix(b'session:')