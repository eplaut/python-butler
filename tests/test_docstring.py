import sys
import time
import slash
import doctest
import butler.butler as mut


def add_sleep(func):
    def ret_func(*args, **kwargs):
        ret = func(*args, **kwargs)
        time.sleep(0.3)
        return ret
    return ret_func


@slash.requires(sys.version_info.major == 2, 'docstring test should run only on python 2 environment')
def test_docstring():
    mut.ButlerServer.run_async = add_sleep(mut.ButlerServer.run_async)
    doctest.testmod(mut, raise_on_error=True, verbose=False)
