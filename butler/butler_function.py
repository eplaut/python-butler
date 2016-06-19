import inspect


class ButlerFunction(object):
    def __init__(self, function_name, function_object):
        self.function_name = function_name
        function_name_parts = self.function_name.split('_', 1)  # handle function that doesn't contains underscore
        self.method, self.name = function_name_parts[0].upper(), function_name_parts[-1]
        self.obj = function_object
        args, _, _, defaults = inspect.getargspec(function_object)
        self.args = args[1:]
        self.defaults = defaults if defaults else []

    def get_urls(self):
        urls = []
        params = ['<{}>'.format(x) for x in self.args]
        args_length = len(self.args) - len(self.defaults)
        for i in range(len(self.defaults) + 1):
            index = -i if i > args_length else None
            urls.append(self._get_url(params[:index]))
        return urls

    def get_default(self, key):
        rargs = [_ for _ in reversed(self.args)]
        rdefaults = [_ for _ in reversed(self.defaults)]
        return rdefaults[rargs.index(key)]

    def _get_base_url(self):
        """returns the prefix for the view function, double underscore changed to slash"""
        return '/{}/'.format(self.name.lower().replace('__', '/'))

    def _get_url(self, params=[]):
        """returns full url, removing ending slashes"""
        base_url = self._get_base_url()
        return str(base_url + '/'.join([str(p) for p in params])).rstrip('/')
