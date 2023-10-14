from collections.abc import Awaitable, Callable
from inspect import iscoroutinefunction
from typing import ParamSpec, TypeGuard, TypeVar

_P = ParamSpec("_P")
_R = TypeVar("_R")


def is_async_func(func: Callable[_P, _R | Awaitable[_R]]) -> TypeGuard[Callable[_P, Awaitable[_R]]]:
    """
    Check if a function is an asynchronous function.

    Args
    ----
        func (`Callable`): The function to check.

    Returns
    -------
        `True` if the function is an asynchronous, `False` otherwise.
    """
    return callable(func) and iscoroutinefunction(func)


def is_sync_func(func: Callable[_P, _R | Awaitable[_R]]) -> TypeGuard[Callable[_P, _R]]:
    """
    Check if a function is synchronous.

    Args
    ----
        func (`Callable`): The function to check.

    Returns
    -------
        `True` if the function is synchronous, `False` otherwise.
    """
    return callable(func) and not iscoroutinefunction(func)
