import requests

from .fixtures import run_server


def test_required_variable(run_server):
    r = requests.get('http://localhost:8888/test_var')
    assert r.status_code == 404

    r = requests.get('http://localhost:8888/test_var/1')
    assert r.status_code == 200
    assert r.content == 'test 1'


def test_default_variable(run_server):
    r = requests.get('http://localhost:8888/test_defaultvar')
    assert r.status_code == 200
    assert r.content == 'test 5'

    r = requests.get('http://localhost:8888/test_defaultvar/1')
    assert r.status_code == 200
    assert r.content == 'test 1'
