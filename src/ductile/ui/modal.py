from typing import TYPE_CHECKING, Literal, TypedDict

from discord import TextStyle, ui

if TYPE_CHECKING:
    from discord import Interaction

    from ..types import ModalCallback  # noqa: TID252


class TextInputStyle(TypedDict, total=False):
    """TextInputStyle is a TypedDict that represents the style of a text input."""

    field: Literal["short", "long"]
    placeholder: str | None
    default: str | None
    row: Literal[0, 1, 2, 3, 4]


class TextInputConfig(TypedDict, total=False):
    """TextInputConfig is a TypedDict that represents the config of a text input."""

    required: bool
    min_length: int | None
    max_length: int | None


class TextInput(ui.TextInput):
    """
    TextInput is a class that represents a text input.

    This class has compatibility with the `discord.ui.TextInput` class.

    """

    def __init__(
        self,
        label: str,
        /,
        *,
        style: TextInputStyle,
        config: TextInputConfig,
        custom_id: str | None = None,
    ) -> None:
        __d = {
            "label": label,
            "style": TextStyle[style.get("field", "short")],
            "placeholder": style.get("placeholder", None),
            "default": style.get("default", None),
            "required": config.get("required", False),
            "row": style.get("row", None),
            "min_length": config.get("min_length", None),
            "max_length": config.get("max_length", None),
        }
        if custom_id:
            __d["custom_id"] = custom_id
        super().__init__(**__d)


class Modal(ui.Modal):
    """
    Modal is a class that represents a modal.

    This class has compatibility with the `discord.ui.Modal` class.
    """

    def __init__(  # noqa: PLR0913
        self,
        *,
        title: str,
        inputs: list[TextInput],
        timeout: float | None = None,
        custom_id: str | None = None,
        on_submit: "ModalCallback | None" = None,
    ) -> None:
        __d = {
            "title": title,
            "timeout": timeout,
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_submit
        self.__inputs = inputs
        super().__init__(**__d)
        for _in in self.__inputs:
            self.add_item(_in)

    async def on_submit(self, interaction: "Interaction") -> None:  # noqa: D102
        if self.__callback_fn:
            await self.__callback_fn(interaction, {i.label: i.value for i in self.__inputs})
