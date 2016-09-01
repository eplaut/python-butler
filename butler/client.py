import requests


class ButlerClient(object):
    """ButlerClient is function factory for a Butler server.

    for each function in the Butler server, there is equvivalent function in the client
    with the same parameters, and can send the request to the Butler instance
    """

    def __init__(self, butler, url, *args, **kwargs):
        """Init properties.

        :param server: Butler instance
        """
        self.url = url.rstrip('/')
        self.butler = butler(*args, **kwargs)
        self.functions = {}
        self.session = requests.Session()
        self.response = None
        self.butler._init_client(*args, **kwargs)  # pylint: disable=protected-access

    def _get_function(self, function_name):
        """Get ButlerFunction instance by it's name."""
        for func in self.butler.functions:
            if func.function_name == function_name:
                return func

    def __getattr__(self, name):
        """Override the original __getattr__ to have auto-generated function.

        :param name: name of required function
        """
        # use cache functions
        if name in self.functions:
            return self.functions[name]

        # validae function in Butler Server
        func = self._get_function(name)
        if not func:
            raise AttributeError

        # create new function from ButlerFunction object
        def client_func(*args, **kwargs):
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

            url = self.url + func.get_url(params)
            self.response = self.session.request(func.method, url, *args, **kwargs)
            return self.response

        client_func.__name__ = name
        client_func.__doc__ = func.obj.__doc__
        self.functions[name] = client_func
        return client_func
