import time
import slash
import requests
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


@slash.fixture(scope='session')
def run_server():
    butler = ButlerTest()
    t = threading.Thread(target=butler.run, kwargs={'host': 'localhost', 'port': '8888'})
    t.daemon = True
    t.start()
    time.sleep(1)

    def stop_server():
        requests.get('http://localhost:8888/stop')
        time.sleep(1)

    slash.add_cleanup(stop_server, scope='session')

