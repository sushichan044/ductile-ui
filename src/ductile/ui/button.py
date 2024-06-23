from typing import TYPE_CHECKING, Literal

from discord import ButtonStyle as _ButtonStyle
from discord import ui
from typing_extensions import NotRequired, Required, TypedDict

from ..utils import call_any_function, is_sync_func  # noqa: TID252

if TYPE_CHECKING:
    from discord import Emoji, Interaction, PartialEmoji

    from ..types import InteractionCallback, InteractionSyncCallback  # noqa: TID252


class ButtonStyle(TypedDict):
    """ButtonStyle is a TypedDict that represents the style of a button."""

    color: Required[Literal["blurple", "grey", "green", "red"]]
    disabled: NotRequired[bool]
    emoji: NotRequired["str | Emoji | PartialEmoji | None"]
    row: NotRequired[Literal[0, 1, 2, 3, 4]]


class Button(ui.Button):
    """
    Button is a class that represents a button.

    This class has compatibility with the `discord.ui.Button` class.
    """

    def __init__(
        self,
        label: str | None = None,
        /,
        *,
        style: ButtonStyle,
        custom_id: str | None = None,
        on_click: "InteractionCallback | InteractionSyncCallback | None" = None,
    ) -> None:
        __style = _ButtonStyle[style.get("color", "grey")]
        __disabled = style.get("disabled", False)
        __emoji = style.get("emoji", None)
        __row = style.get("row", None)
        self.__callback_fn = on_click
        super().__init__(
            style=__style,
            disabled=__disabled,
            emoji=__emoji,
            row=__row,
            label=label,
            custom_id=custom_id,
        )

    async def callback(self, interaction: "Interaction") -> None:
        if self.__callback_fn is None:
            await interaction.response.defer()
            return

        if is_sync_func(self.__callback_fn):
            await interaction.response.defer()

        await call_any_function(self.__callback_fn, interaction)


class LinkButton(ui.Button):
    """
    LinkButton is a class that represents a link button.

    This class has compatibility with the `discord.ui.Button` class.
    """

    def __init__(self, label: str | None = None, /, *, url: str, custom_id: str | None = None) -> None:
        super().__init__(
            style=_ButtonStyle.link,
            url=url,
            label=label,
            custom_id=custom_id,
        )

    async def callback(self, interaction: "Interaction") -> None:
        pass
