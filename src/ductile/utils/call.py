from asyncio import iscoroutinefunction
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

__all__ = [
    "call_any_function",
]


async def call_any_function(fn: "Callable[P, R]", *args: P.args, **kwargs: P.kwargs) -> R:
    if iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    return fn(*args, **kwargs)
