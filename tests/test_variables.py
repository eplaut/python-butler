import requests

from .fixtures import butler_client


def test_required_variable(butler_client):
    r = requests.get('http://localhost:8888/test_var')
    assert r.status_code == 404

    r = requests.get('http://localhost:8888/test_var/1')
    assert r.status_code == 200
    assert r.content.decode("utf-8") == 'test 1'


def test_default_variable(butler_client):
    r = requests.get('http://localhost:8888/test_defaultvar')
    assert r.status_code == 200
    assert r.content.decode("utf-8") == 'test 5'

    r = requests.get('http://localhost:8888/test_defaultvar/1')
    assert r.status_code == 200
    assert r.content.decode("utf-8") == 'test 1'
