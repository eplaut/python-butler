import inspect
from flask import Flask

class Butler(object):
    def __init__(self):
        self._app = Flask(__name__)
        self.data = {}
        self._register_urls()

    @staticmethod
    def _get_urls(function_name, function_object):
        urls = []
        args, _, _, defaults = inspect.getargspec(function_object)
        params = map('<{}>'.format, args)
        base_url = '/{}/'.format(function_name.split('_', 1)[1].lower())
        urls.append(base_url + '/'.join(params[1:]))
        if defaults is not None:
            for i in range(1, len(defaults)+1):
                urls.append(base_url + '/'.join(params[1:-i]))
        return urls

    def _register_urls(self):
        functions = inspect.getmembers(self, predicate=inspect.ismethod)
        for function_name, function_object in functions:
            method = function_name.split('_', 1)[0].upper()
            if method in ['GET', 'POST', 'PUT', 'DELETE']:
                for url in self._get_urls(function_name, function_object):
                    print url
                    self._app.add_url_rule(url, methods=[method], view_func=function_object)

    def run(self, *args, **kwargs):
        self._app.run(*args, **kwargs)

