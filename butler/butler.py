import inspect
from flask import Flask, request
from logbook import debug

from .butler_function import ButlerFunction
from .client import ButlerClient

class Butler(object):
    def __init__(self):
        self._app = Flask(__name__)
        self.data = {}
        self.functions = []
        self._register_urls()
        # Flask defaults
        self.protocol = 'http'
        self.host = '127.0.0.1'
        self.port = '5000'
        self.client = ButlerClient(self)

    @property
    def base_url(self):
        return '{0.protocol}://{0.host}:{0.port}'.format(self)

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
        args = list(args)
        try:
            self.host = args[0]
            self.port = args[1]
        except IndexError:
            pass
        if 'host' in kwargs:
            self.host = kwargs['host']
        if 'port' in kwargs:
            self.port = kwargs['port']
        if 'ssl_context' in kwargs:
            self.protocol = 'https'
        self._app.run(*args, **kwargs)

    def get_stop(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')  # pragma: no cover
        func()
        return 'stoped'
