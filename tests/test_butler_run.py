import slash

from butler import Butler

def do_nothing(*args, **kwargs):
    pass

@slash.fixture
def butler():
    butler = Butler.Server('http://127.0.0.1:5000')
    butler._app.run = do_nothing
    return butler

def test_butler_http_port_80():
    butler = Butler.Server('http://127.0.0.1')
    assert butler.host == '127.0.0.1'
    assert int(butler.port) == 80

def test_butler_https_port_443():
    butler = Butler.Server('https://127.0.0.1')
    assert butler.host == '127.0.0.1'
    assert int(butler.port) == 443

def test_init_args(butler):
    butler.run()
    assert butler.host == '127.0.0.1'
    assert int(butler.port) == 5000

def test_args(butler):
    butler.run('localhost', 6789)
    assert butler.host == 'localhost'
    assert int(butler.port) == 6789

def test_kwargs(butler):
    butler.run(port=5678, host='0.0.0.0')
    assert butler.host == '0.0.0.0'
    assert int(butler.port) == 5678
