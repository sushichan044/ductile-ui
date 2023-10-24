from collections.abc import Generator
from typing import TypeVar

_T = TypeVar("_T")


def chunks(iterable: list[_T], size: int) -> Generator[list[_T], None, None]:
    """Yield successive chunks from iterable of size."""
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]
