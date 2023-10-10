from typing import TYPE_CHECKING

from .controller import ViewController

if TYPE_CHECKING:
    import discord

    from ..view import View  # noqa: TID252


class MessageableController(ViewController):
    def __init__(self, view: "View", *, messageable: "discord.abc.Messageable", timeout: float | None = 180) -> None:
        super().__init__(view, timeout=timeout)
        self.__messageable = messageable

    async def send(self) -> None:
        target = self.__messageable
        view_kwargs = self._process_view_for_discord("files")

        self.message = await target.send(**view_kwargs)
