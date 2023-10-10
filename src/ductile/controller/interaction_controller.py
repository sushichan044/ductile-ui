from typing import TYPE_CHECKING

from discord import CategoryChannel, ForumChannel

from .controller import ViewController

if TYPE_CHECKING:
    from discord import Interaction

    from ..view import View  # noqa: TID252


class InteractionController(ViewController):
    """InteractionController is a class that controls the view with `discord.abc.Messageable`."""

    def __init__(
        self,
        view: "View",
        *,
        interaction: "Interaction",
        timeout: float | None = 180,
        ephemeral: bool = False,
    ) -> None:
        super().__init__(view, timeout=timeout)
        self.__interaction = interaction
        self.__ephemeral = ephemeral

    async def send(self) -> None:
        """Send the view to the channel."""
        target = self.__interaction
        view_kwargs = self._process_view_for_discord("files")

        if target.is_expired():
            if target.channel is not None and not isinstance(target.channel, CategoryChannel | ForumChannel):
                self.message = await target.channel.send(**view_kwargs)
            return

        if target.response.is_done():
            self.message = await target.followup.send(**view_kwargs, ephemeral=self.__ephemeral, wait=True)
            return

        await target.response.send_message(**view_kwargs, ephemeral=self.__ephemeral)
        self.message = await target.original_response()
        return
