import inspect
from flask import Flask, request
from logbook import debug

from .butler_function import ButlerFunction

class Butler(object):
    def __init__(self):
        self._app = Flask(__name__)
        self.data = {}
        self.functions = []
        self._register_urls()

    def _get_urls(self, function_name, function_object):
        urls = []
        args, _, _, defaults = inspect.getargspec(function_object)
        params = ['<{}>'.format(x) for x in args]
        base_url = '/{}/'.format(function_name.split('_', 1)[1].lower().replace('__', '/'))
        url = str(base_url + '/'.join(params[1:])).rstrip('/')
        urls.append(url)
        if defaults is not None:
            for i in range(1, len(defaults)+1):
                url = str(base_url + '/'.join(params[1:-i])).rstrip('/')
                urls.append(url)
        return urls

    def _register_urls(self):
        functions = inspect.getmembers(self, predicate=inspect.ismethod)
        for function_name, function_object in functions:
            function = ButlerFunction(function_name, function_object)
            if function.method in ['GET', 'POST', 'PUT', 'DELETE']:
                self.functions.append(function)
                for url in function.get_urls():
                    debug('Adding view {}, url {}'.format(function_name, url))
                    self._app.add_url_rule(url, methods=[function.method], view_func=function_object)

    def run(self, *args, **kwargs):
        self._app.run(*args, **kwargs)

    def get_stop(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')  # pragma: no cover
        func()
        return 'stoped'
