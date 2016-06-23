import time
import slash
import threading

from butler import Butler


class ButlerTest(Butler):
    def get_test_get(self):
        return 'test get'

    def post_test_post(self):
        return 'test post'
        
    def put_test_put(self):
        return 'test put'
        
    def delete_test_delete(self):
        return 'test delete'

    def get_test_var(self, var):
        return 'test {}'.format(var)

    def get_test_defaultvar(self, var=5):
        return 'test {}'.format(var)

    def get_test__with__slashes(self):
        return 'test'

    def post_test_json(self):
        return 'test {}'.format(self.json['test'])

    def post_test_params(self):
        return 'test {}'.format(self.params['test'])


@slash.fixture(scope='session')
def butler_client():
    butler_server = ButlerTest.Server('http://localhost:8888')
    butler_client = ButlerTest.Client('http://localhost:8888')
    butler_server.run_async()
    time.sleep(1)

    def stop_server():
        butler_client.get_stop()
        time.sleep(1)

    slash.add_cleanup(stop_server, scope='session')
    return butler_client
