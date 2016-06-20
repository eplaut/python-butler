import slash
import requests

from .fixtures import run_server


def test_client_sanity(run_server):
    r = run_server.client.get_test_get()
    assert r.status_code == 200

    with slash.assert_raises(AttributeError):
        r = run_server.client.get_no_such_view()

def test_client_method(run_server):
    r = run_server.client.delete_test_delete()
    assert r.content.decode("utf-8") == 'test delete'

def test_client_var(run_server):
    r = run_server.client.get_test_var(100)
    assert r.content.decode("utf-8") == 'test 100'
    
    r = run_server.client.get_test_defaultvar()
    assert r.content.decode("utf-8") == 'test 5'
    
    r = run_server.client.get_test_defaultvar(200)
    assert r.content.decode("utf-8") == 'test 200'
