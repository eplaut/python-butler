import requests

class ButlerClient(object):
    def __init__(self, server):
        self._server = server
        self.functions = {}
        self.session = requests.Session()
        self.response = None

    def _get_function(self, function_name):
        for func in self._server.functions:
            if func.function_name == function_name:
                return func

    def __getattr__(self, name):
        if name in self.functions:
            return self.functions[name]

        func = self._get_function(name)
        if not func:
            raise AttributeError

        def client_func(*args, **kwargs):
            _dict = {}
            params = []
            args = list(args)  # args is tuple, which is immutable
            for arg in func.args:
                if arg in kwargs or not args:
                    try:
                        params.append(kwargs.pop(arg))
                    except KeyError:
                        params.append(func.get_default(arg))  # adding default to avoid missing parameter
                else:
                    params.append(args.pop(0))
            url = self._server.base_url + func._get_url(params)
            self.response = self.session.request(func.method, url, *args, **kwargs)
            return self.response

        client_func.__name__ = name
        self.functions[name] = client_func
        return client_func
