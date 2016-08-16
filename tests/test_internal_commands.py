from __future__ import absolute_import
import os
import sys
import hashlib
from butler.__version__ import __version__ as butler_version

from .fixtures import butler_client


def test_internal_commands_version(butler_client):
    data = butler_client.get__butler__version().json()
    assert data['python'] in sys.version
    assert data['butler'] == butler_version

    fixtures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures.py')
    with open(fixtures_path) as fh:
        md5_obj = hashlib.md5()
        md5_obj.update(fh.read().encode('utf-8'))
        fixtures_hash = md5_obj.hexdigest()
    assert 'ButlerTest' in data
    assert data['ButlerTest'] == fixtures_hash


def test_internal_commands_ping(butler_client):
    assert butler_client.get__butler__ping().content.decode("utf-8") == 'ok'
