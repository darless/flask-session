import flask_session

class TestMemcached:
    """This requires package: memcached
       This needs to be running before test runs
    """
    def test_basic(self, app):
        app.config['SESSION_TYPE'] = 'memcached'
        flask_session.Session(app)

        client = app.test_client()
        assert client.post('/set', data={'value': '42'}).data == b'value set'
        assert client.get('/get').data ==  b'42'
        client.post('/delete')