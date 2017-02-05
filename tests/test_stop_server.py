from __future__ import absolute_import
from .fixtures import butler_server_client


def test_stop_server(butler_server_client):
    assert butler_server_client.server.butler._stopped is False
    butler_server_client.client.get__butler__stop()
    assert butler_server_client.server.butler._stopped is True
