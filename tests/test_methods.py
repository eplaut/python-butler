import slash
import requests

from .fixtures import run_server


@slash.parametrize('method', ['get', 'post', 'put', 'delete'])
def test_methods(run_server, method):
    base_url = 'http://localhost:8888'
    r = getattr(requests, method)('{}/test_{}'.format(base_url, method))
    assert r.content == 'test {}'.format(method)

