import slash
import requests

from .fixtures import butler_client


@slash.parametrize('method', ['get', 'post', 'put', 'delete'])
def test_methods(butler_client, method):
    base_url = 'http://localhost:8888'
    r = getattr(requests, method)('{}/test_{}'.format(base_url, method))
    assert r.content.decode("utf-8") == 'test {}'.format(method)

