import os
import sys
import json
import hashlib
import inspect
from flask import request, jsonify, redirect, abort
from flask.helpers import send_from_directory

from .butler_function import ButlerFunction
from .client import ButlerClient
from .server import ButlerServer
from .__version__ import __version__ as butler_version


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

        >>> class MyButler(Butler):
        ...     def get_api__get_data(self):
        ...         return 'ok'
        ...

        >>> MyButler.Server('0.0.0.0:6789').run_async()  # use threading for non-blocking run

        >>> print(MyButler.Client('http://0.0.0.0:6789').get_api__get_data().content.decode('utf-8'))
        ok

    """

    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Init Butler functions."""
        super(Butler, self).__init__()
        self.functions = []
        self.init_functions()
        self._swagger_api_file = kwargs.get('swagger_file', None)

    @property
    def json(self):
        """Load request body."""
        try:
            return json.loads(request.data.decode('utf-8'))
        except (RuntimeError, ValueError):
            return None

    @property
    def params(self):
        """Get requests arguments."""
        try:
            return request.args
        except RuntimeError:  # cannot inspect this function
            return {}

    @property
    def has_swagger_file(self):
        """Return True if _swagger_api_file defined and exists."""
        return self._swagger_api_file and os.path.isfile(self._swagger_api_file)

    @classmethod
    def Server(cls, url, *args, **kwargs):
        """Return ButlerServer class."""
        return ButlerServer(cls, url, *args, **kwargs)

    def _init_server(self, *args, **kwargs):
        """Init function to run only on server instance."""
        pass

    @classmethod
    def Client(cls, url, *args, **kwargs):
        """Return ButlerClient class.

        :rtype: self
        """
        return ButlerClient(cls, url, *args, **kwargs)

    def _init_client(self, *args, **kwargs):
        """Init function to run only on client instance."""
        pass

    def init_functions(self):
        """Read class functions and register the matching routes."""
        functions = inspect.getmembers(self, predicate=inspect.ismethod)
        for function_name, function_object in functions:
            function = ButlerFunction(function_name, function_object)
            if function.method in ['GET', 'POST', 'PUT', 'DELETE']:
                self.functions.append(function)

    def get__butler__stop(self):
        """Stop the Flask application."""
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')  # pragma: no cover
        func()
        return 'stoped'

    get_stop = get__butler__stop

    def get__butler__version(self):
        """Return versions of python, buttler and current class."""
        data = {}
        data['python'] = '{version.major}.{version.minor}.{version.micro}'.format(version=sys.version_info)
        data['butler'] = butler_version
        with open(sys.modules[self.__class__.__module__].__file__) as fh:
            md5_obj = hashlib.md5()
            md5_obj.update(fh.read().encode('utf-8'))
            data[type(self).__name__] = md5_obj.hexdigest()
        return jsonify(data)

    def get__butler__ping(self):
        """Return `ok` validation server is up."""
        return 'ok'

    def get__butler___api(self):
        """Serve _swagger_api_file as is."""
        if self.has_swagger_file:
            return send_from_directory(*os.path.split(self._swagger_api_file))
        abort(404)

    def get__butler__api(self):
        """Redirect to swagger-ui with _swagger_api_file."""
        if self.has_swagger_file:
            return redirect('apidocs/index.html?url=/_butler/_api')
        abort(404)
