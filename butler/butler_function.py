import inspect


class ButlerFunction(object):
    """ButlerFunction is object to parse Butler's functions' properties."""

    def __init__(self, function_name, function_object):
        """Init properties, using inspect to get function's parameters.

        :param function_name: name of the function.
        :param function_object: the object of the function.
        """
        self.function_name = function_name
        function_name_parts = self.function_name.split('_', 1)  # handle function that doesn't contains underscore
        self.method, self.name = function_name_parts[0].upper(), function_name_parts[-1]
        self.obj = function_object
        args, _, _, defaults = inspect.getargspec(function_object)  # pylint: disable=deprecated-method
        self.args = args[1:]
        self.defaults = defaults if defaults else []

    def get_urls(self):
        """Returns all available paths for function.

        starts with the function name (without leading method, and double underscores changed to slashes
        and than functions parameters by there order, parameters with default values can be ommitted
        by their order
        """
        urls = []
        params = ['<{}>'.format(x) for x in self.args]
        args_length = len(self.args) - len(self.defaults)
        for i in range(len(self.defaults) + 1):
            index = -i if i > args_length else None
            urls.append(self.get_url(params[:index]))
        return urls

    def get_default(self, name):
        """Returns default value for argument by `name`.

        :param name: the name of the required parameter
        """
        rargs = [_ for _ in reversed(self.args)]
        rdefaults = [_ for _ in reversed(self.defaults)]
        return rdefaults[rargs.index(name)]

    def _get_base_url(self):
        """Returns the prefix for the view function, double underscore changed to slash."""
        return '/{}/'.format(self.name.lower().replace('__', '/'))

    def get_url(self, params):
        """Returns full url, removing ending slashes."""
        base_url = self._get_base_url()
        return str(base_url + '/'.join([str(p) for p in params])).rstrip('/')
