import slash

from butler import Butler

def do_nothing(*args, **kwargs):
    pass

@slash.fixture
def butler():
    butler = Butler()
    butler._app.run = do_nothing
    return butler

def test_defaults(butler):
    butler.run()
    # Flask defaults
    assert butler.host == '127.0.0.1'
    assert int(butler.port) == 5000
    assert butler.protocol == 'http'

def test_args(butler):
    butler.run('localhost', 6789)
    # Flask defaults
    assert butler.host == 'localhost'
    assert int(butler.port) == 6789
    assert butler.protocol == 'http'

def test_kwargs(butler):
    butler.run(port=5678, host='0.0.0.0', ssl_context='adhoc')
    # Flask defaults
    assert butler.host == '0.0.0.0'
    assert int(butler.port) == 5678
    assert butler.protocol == 'https'
