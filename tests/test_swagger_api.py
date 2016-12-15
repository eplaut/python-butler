import time
import slash
import tempfile
from .fixtures import ButlerTest, butler_client


DATA = """First line is the summary
All following lines until the hyphens is added to description
the format of the first lines until 3 hyphens will be not yaml compliant
but everything below the 3 hyphens should be.
---
tags:
  - users
parameters:
  - in: path
    name: username
    type: string
    required: true
responses:
  200:
    description: A single user item
    schema:
      id: rec_username
      properties:
        username:
          type: string
          description: The name of the user
          default: 'steve-harris'"""  # from flasgger README.md

@slash.yield_fixture
def swagge_file():
    fh = tempfile.NamedTemporaryFile('w+')
    fh.file.write(DATA)
    fh.file.close()
    yield fh.name  # using yield, since file been deleted when function ends


def test_swagger_file_on(butler_client, swagge_file):
    # get new server with swagger_file
    # butler_client.get__butler__stop()
    # time.sleep(0.3)
    butler_server = ButlerTest.Server('http://localhost:8888', swagger_file=swagge_file)
    butler_client.session.adapters['http://'].client = butler_server._app.test_client()
    # butler_server.run_async()
    # time.sleep(0.3)
    response = butler_client.get__butler___api()
    assert response.status_code == 200
    assert response.content.decode("utf-8") == DATA
    response = butler_client.get__butler__api()
    assert response.status_code == 200
    assert response.url == 'http://localhost:8888/apidocs/index.html?url=/_butler/_api'
    assert len(response.history) == 1
    assert response.history[0].status_code == 302


def test_swagger_file_off(butler_client):
    response = butler_client.get__butler___api()
    assert response.status_code == 404
    response = butler_client.get__butler__api()
    assert response.status_code == 404
