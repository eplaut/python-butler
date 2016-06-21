import slash
import requests

from .fixtures import butler_client


def test_default_variable(butler_client):
    r = requests.get('http://localhost:8888/test__with__slashes')
    assert r.status_code == 404

    r = requests.get('http://localhost:8888/test/with/slashes')
    assert r.status_code == 200
    assert r.content.decode("utf-8") == 'test'