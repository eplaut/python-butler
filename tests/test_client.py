import slash
import requests

from .fixtures import butler_client


def test_client_sanity(butler_client):
    r = butler_client.get_test_get()
    assert r.status_code == 200

    with slash.assert_raises(AttributeError):
        r = butler_client.get_no_such_view()

def test_client_method(butler_client):
    r = butler_client.delete_test_delete()
    assert r.content.decode("utf-8") == 'test delete'

def test_client_var(butler_client):
    r = butler_client.get_test_var(100)
    assert r.content.decode("utf-8") == 'test 100'
    
    r = butler_client.get_test_defaultvar()
    assert r.content.decode("utf-8") == 'test 5'
    
    r = butler_client.get_test_defaultvar(200)
    assert r.content.decode("utf-8") == 'test 200'

def test_client_not_exits_function(butler_client):
    with slash.assert_raises(AttributeError):
        butler_client.not_exits_function()

def test_client_unsupported_function(butler_client):
    with slash.assert_raises(AttributeError):
        butler_client.init_functions()
