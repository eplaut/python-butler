import slash

from butler import Butler

def do_nothing(*args, **kwargs):
    pass

@slash.fixture
def hostname():
    return '192.168.1.10'

@slash.fixture
def port():
    return 2345

@slash.fixture
def butler(hostname, port):
    butler = Butler.Server('http://{}:{}'.format(hostname, port))
    butler._app.run = do_nothing
    return butler

def test_butler_http_port_80(hostname):
    butler = Butler.Server('http://{}'.format(hostname))
    assert butler.host == hostname
    assert int(butler.port) == 80

def test_butler_https_port_443(hostname):
    butler = Butler.Server('https://{}'.format(hostname))
    assert butler.host == hostname
    assert int(butler.port) == 443

def test_butler_http_no_scheme(hostname, port):
    butler = Butler.Server('{}:{}'.format(hostname, port))
    assert butler.host == hostname
    assert int(butler.port) == port

def test_init_args(butler, hostname, port):
    butler.run()
    assert butler.host == hostname
    assert int(butler.port) == port

def test_args(butler, hostname, port):
    hostname = hostname + '1'
    port = port + 1
    butler.run(hostname, port)
    assert butler.host == hostname
    assert int(butler.port) == port

def test_kwargs(butler, hostname, port):
    hostname = hostname + '2'
    port = port + 2
    butler.run(port=port, host=hostname)
    assert butler.host == hostname
    assert int(butler.port) == port
