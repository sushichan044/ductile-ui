import functools
import threading
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def debounce(*, wait: float = 10.0) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator that limits the execution of a specific function to once every specified seconds.

    Parameters
    ----------
    wait : `float`
        Seconds to wait before the function can be called again. Defaults to 10.0.
    """

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        last_called = threading.Event()
        last_called.set()  # set the event to allow the first call
        last_result: R  # must set by the first call

        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal last_called
            nonlocal last_result

            if last_called.is_set():
                last_called.clear()  # clear the event to prevent the next call
                result = fn(*args, **kwargs)
                last_result = result
                threading.Timer(wait, last_called.set).start()  # set the event after the specified seconds
                return result

            # rate limited. returning the last result
            return last_result

        return wrapper

    return decorator
