import inspect
from flask import Flask, request
from logbook import debug

from .butler_function import ButlerFunction
from .client import ButlerClient


class Butler(object):
    """Butler is ease to use Flask wrapper.

    It allows to develop and maintain small http server, with no need to handle flask app,
    and provide a client which communicate with it.
    Moreover, using Butler as a app container,allows you to change the data of the object
    and reload the http server without losing you data.

    To add more views to the Butler object, you need to add a method starting with the method
    name (supported method are get, post, put and delete), and the view name (double-underscore
    will interpate to slash

    The following example will add route `/api/get_data`:

        class MyButler(Butler):
            def get_api__get_data(self):
            return self.data
    """

    def __init__(self):
        """init all parameters."""
        # create Flask application
        self._app = Flask(__name__)

        # register functions to app routes
        self.functions = []
        self._register_urls()

        # Flask defaults
        self.protocol = 'http'
        self.host = '127.0.0.1'
        self.port = '5000'
        self.client = ButlerClient(self)

    @property
    def base_url(self):
        """Get base url of application."""
        return '{0.protocol}://{0.host}:{0.port}'.format(self)

    def _register_urls(self):
        """Read class functions and register the matching routes."""
        functions = inspect.getmembers(self, predicate=inspect.ismethod)
        for function_name, function_object in functions:
            function = ButlerFunction(function_name, function_object)
            if function.method in ['GET', 'POST', 'PUT', 'DELETE']:
                self.functions.append(function)
                for url in function.get_urls():
                    debug('Adding view {}, url {}'.format(function_name, url))
                    self._app.add_url_rule(url, methods=[function.method], view_func=function_object)

    def run(self, *args, **kwargs):
        """Start flask application, get all paramters as Flask.run method."""
        self._update_app_paramters(*args, **kwargs)
        kwargs.pop('host', None)
        kwargs.pop('port', None)
        self._app.run(host=self.host, port=self.port, *args, **kwargs)

    def _update_app_paramters(self, *args, **kwargs):
        """Parse `run` function parameters and updates `host`, `port` and `protocol` properties."""
        args = list(args)  # args is tuple, which is immutable
        try:
            self.host = args[0]
            self.port = args[1]
        except IndexError:
            pass
        if 'host' in kwargs:
            self.host = kwargs['host']
        if 'port' in kwargs:
            self.port = kwargs['port']
        if 'ssl_context' in kwargs and kwargs['ssl_context']:
            self.protocol = 'https'
        else:
            self.protocol = 'http'

    def get_stop(self):
        """Stop the Flask application."""
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')  # pragma: no cover
        func()
        return 'stoped'
