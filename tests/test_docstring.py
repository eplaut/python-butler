import time
import doctest
import butler.butler as mut


def add_sleep(func):
    def ret_func(*args, **kwargs):
        ret = func(*args, **kwargs)
        time.sleep(0.3)
        return ret
    return ret_func


def test_docstring():
    mut.ButlerServer.run_async = add_sleep(mut.ButlerServer.run_async)
    doctest.testmod(mut, raise_on_error=True, verbose=True)
