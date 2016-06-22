import slash
import requests

from .fixtures import butler_client


@slash.parametrize('key', ['params', 'json'])
def test_methods(butler_client, key):
    d = {key: {'test': key}}
    r = getattr(butler_client, 'post_test_{}'.format(key))(**d)
    assert r.content.decode("utf-8") == 'test {}'.format(key)

