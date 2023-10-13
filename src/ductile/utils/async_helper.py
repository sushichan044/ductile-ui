import asyncio
from typing import Any


def get_all_tasks(*, loop: asyncio.AbstractEventLoop | None = None, only_undone: bool = False) -> set[asyncio.Task]:
    """
    Return a set of all tasks running on the given event loop.

    Args:
        loop `(asyncio.AbstractEventLoop | None)`: The event loop to get tasks from.
        If None, the current running loop is used.
        only_undone `(bool)`: If True, only tasks that are not done are returned.

    Returns
    -------
        `set[asyncio.Task]`: A set of all tasks running on the given event loop.
    """
    _loop: asyncio.AbstractEventLoop | None = loop or safe_get_running_loop()

    if _loop is None:
        return set()

    tasks = asyncio.all_tasks(loop=_loop)

    if only_undone:
        return {t for t in tasks if not t.done()}

    return tasks


async def wait_tasks_by_name(names: list[str]) -> list[asyncio.Future[Any]]:
    """
    Wait for all tasks with the given names to complete.

    Args:
        names `(list[str])`: A list of task names to wait for.

    Returns
    -------
        `list[asyncio.Future[Any]]`: A list of futures representing the results of the completed tasks.
    """
    tasks = [t for t in get_all_tasks() if t.get_name() in names]
    return await asyncio.gather(*tasks, return_exceptions=True)


def safe_get_running_loop() -> asyncio.AbstractEventLoop | None:
    """
    Get the running loop safely.

    Returns
    -------
    `asyncio.AbstractEventLoop | None`
        The running loop. None if faced RuntimeError.
    """
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return None
