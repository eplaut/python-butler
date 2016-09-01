from __future__ import absolute_import
from .fixtures import ButlerTest


def test_init_server():
    butler_server = ButlerTest.Server('http://localhost:8888', 'a', 'b', 'c', x=1, y=2, z=3)
    assert butler_server.butler._check_args == ('a', 'b', 'c')
    assert butler_server.butler._check_kwargs == {'x': 1, 'y': 2, 'z': 3}
    assert butler_server.butler._is_server is True
    assert butler_server.butler._is_client is False


def test_init_client():
    butler_client = ButlerTest.Client('http://localhost:8888', 'a', 'b', 'c', x=1, y=2, z=3)
    assert butler_client.butler._check_args == ('a', 'b', 'c')
    assert butler_client.butler._check_kwargs == {'x': 1, 'y': 2, 'z': 3}
    assert butler_client.butler._is_server is False
    assert butler_client.butler._is_client is True
