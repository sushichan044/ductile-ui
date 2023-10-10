from asyncio import iscoroutinefunction
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

__all__ = [
    "call_any_function",
]


async def call_any_function(fn: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    """
    Call a function, whether it is a coroutine or not.

    This function is used internally to call functions that may or may not be coroutines.

    Parameters
    ----------
    fn : Callable[P, R]
        The function to call.
    *args : P.args
        The positional arguments to pass to the function.
    **kwargs : P.kwargs
        The keyword arguments to pass to the function.

    Returns
    -------
    R
        The return value of the function.
    """
    if iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    return fn(*args, **kwargs)
