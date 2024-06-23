from typing import TYPE_CHECKING, Literal

from discord import Emoji, PartialEmoji, ui
from discord import SelectOption as _SelectOption
from typing_extensions import NotRequired, Required, TypedDict

from ..utils import call_any_function, is_sync_func  # noqa: TID252

if TYPE_CHECKING:
    from discord import ChannelType, Interaction

    from ..types import (  # noqa: TID252
        ChannelSelectCallback,
        ChannelSelectSyncCallback,
        MentionableSelectCallback,
        MentionableSelectSyncCallback,
        RoleSelectCallback,
        RoleSelectSyncCallback,
        SelectCallback,
        SelectSyncCallback,
        UserSelectCallback,
        UserSelectSyncCallback,
    )


class SelectStyle(TypedDict, total=False):
    """SelectStyle is a TypedDict that represents the style of a select."""

    disabled: bool
    placeholder: str | None
    row: Literal[0, 1, 2, 3, 4]


# class SelectOption(BaseModel):
#     """
#     SelectOption is a class that represents a select option.

#     This class extends the `pydantic.BaseModel` class and has validation.
#     """

#     label: str = Field(min_length=1, max_length=100)
#     value: str | None = Field(default=None, min_length=1, max_length=100)
#     description: str | None = Field(default=None, min_length=1, max_length=100)
#     emoji: str | Emoji | PartialEmoji | None = Field(default=None)
#     selected_by_default: bool = Field(default=False)

#     model_config = {"arbitrary_types_allowed": True}


class SelectOption(TypedDict):
    """SelectOption is a TypedDict that represents a select option."""

    label: Required[str]
    value: NotRequired[str | None]
    description: NotRequired[str | None]
    emoji: NotRequired[str | Emoji | PartialEmoji | None]
    default: NotRequired[bool]


class SelectConfigBase(TypedDict, total=False):
    """SelectConfigBase is a TypedDict that represents the config of a select."""

    min_values: int | None
    max_values: int | None


class SelectConfig(SelectConfigBase):
    """SelectConfig is a class that represents the config of a select."""


class ChannelSelectConfig(SelectConfigBase):
    """ChannelSelectConfig is a class that represents the config of a channel select."""

    channel_types: "list[ChannelType]"


class RoleSelectConfig(SelectConfigBase):
    """RoleSelectConfig is a class that represents the config of a role select."""


class MentionableSelectConfig(SelectConfigBase):
    """MentionableSelectConfig is a class that represents the config of a mentionable select."""


class UserSelectConfig(SelectConfigBase):
    """UserSelectConfig is a class that represents the config of a user select."""


class Select(ui.Select):
    """
    Select is a class that represents a select.

    This class has compatibility with the `discord.ui.Select` class.
    """

    def __init__(  # noqa: PLR0913
        self,
        *,
        config: SelectConfig,
        style: SelectStyle,
        options: list[SelectOption],
        custom_id: str | None = None,
        on_select: "SelectCallback | SelectSyncCallback | None" = None,
    ) -> None:
        __disabled = style.get("disabled", False)
        __placeholder = style.get("placeholder", None)
        __row = style.get("row", None)
        __d = {
            "disabled": __disabled,
            "placeholder": __placeholder,
            "row": __row,
            "min_values": config.get("min_values", None),
            "max_values": config.get("max_values", None),
            "options": [
                _SelectOption(
                    label=(_label := option.get("label", "")),
                    value=option.get("value", None) or _label,
                    description=option.get("description", None),
                    emoji=option.get("emoji", None),
                    default=option.get("default", False),
                )
                for option in options
            ],
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_select
        super().__init__(**__d)

    async def callback(self, interaction: "Interaction") -> None:
        if self.__callback_fn is None:
            await interaction.response.defer()
            return

        if is_sync_func(self.__callback_fn):
            await interaction.response.defer()

        await call_any_function(self.__callback_fn, interaction, self.values)


class ChannelSelect(ui.ChannelSelect):
    """
    ChannelSelect is a class that represents a channel select.

    This class has compatibility with the `discord.ui.ChannelSelect` class.
    """

    def __init__(
        self,
        *,
        config: ChannelSelectConfig,
        style: SelectStyle,
        custom_id: str | None = None,
        on_select: "ChannelSelectCallback| ChannelSelectSyncCallback | None" = None,
    ) -> None:
        __disabled = style.get("disabled", False)
        __placeholder = style.get("placeholder", None)
        __row = style.get("row", None)
        __d = {
            "disabled": __disabled,
            "placeholder": __placeholder,
            "row": __row,
            "min_values": config.get("min_values", None),
            "max_values": config.get("max_values", None),
            "channel_types": config["channel_types"],
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_select
        super().__init__(**__d)

    async def callback(self, interaction: "Interaction") -> None:
        if self.__callback_fn is None:
            await interaction.response.defer()
            return

        if is_sync_func(self.__callback_fn):
            await interaction.response.defer()

        await call_any_function(self.__callback_fn, interaction, self.values)


class RoleSelect(ui.RoleSelect):
    """
    RoleSelect is a class that represents a role select.

    This class has compatibility with the `discord.ui.RoleSelect` class.
    """

    def __init__(
        self,
        *,
        config: RoleSelectConfig,
        style: SelectStyle,
        custom_id: str | None = None,
        on_select: "RoleSelectCallback | RoleSelectSyncCallback | None" = None,
    ) -> None:
        __disabled = style.get("disabled", False)
        __placeholder = style.get("placeholder", None)
        __row = style.get("row", None)
        __d = {
            "disabled": __disabled,
            "placeholder": __placeholder,
            "row": __row,
            "min_values": config.get("min_values", None),
            "max_values": config.get("max_values", None),
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_select
        super().__init__(**__d)

    async def callback(self, interaction: "Interaction") -> None:
        if self.__callback_fn is None:
            await interaction.response.defer()
            return

        if is_sync_func(self.__callback_fn):
            await interaction.response.defer()

        await call_any_function(self.__callback_fn, interaction, self.values)


class MentionableSelect(ui.MentionableSelect):
    """
    MentionableSelect is a class that represents a mentionable select.

    This class has compatibility with the `discord.ui.MentionableSelect` class.

    """

    def __init__(
        self,
        *,
        config: MentionableSelectConfig,
        style: SelectStyle,
        custom_id: str | None = None,
        on_select: "MentionableSelectCallback | MentionableSelectSyncCallback | None" = None,
    ) -> None:
        __disabled = style.get("disabled", False)
        __placeholder = style.get("placeholder", None)
        __row = style.get("row", None)
        __d = {
            "disabled": __disabled,
            "placeholder": __placeholder,
            "row": __row,
            "min_values": config.get("min_values", None),
            "max_values": config.get("max_values", None),
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_select
        super().__init__(**__d)

    async def callback(self, interaction: "Interaction") -> None:
        if self.__callback_fn is None:
            await interaction.response.defer()
            return

        if is_sync_func(self.__callback_fn):
            await interaction.response.defer()

        await call_any_function(self.__callback_fn, interaction, self.values)


class UserSelect(ui.UserSelect):
    """
    UserSelect is a class that represents a user select.

    This class has compatibility with the `discord.ui.UserSelect` class.
    """

    def __init__(
        self,
        *,
        config: UserSelectConfig,
        style: SelectStyle,
        custom_id: str | None = None,
        on_select: "UserSelectCallback | UserSelectSyncCallback | None" = None,
    ) -> None:
        __disabled = style.get("disabled", False)
        __placeholder = style.get("placeholder", None)
        __row = style.get("row", None)
        __d = {
            "disabled": __disabled,
            "placeholder": __placeholder,
            "row": __row,
            "min_values": config.get("min_values", None),
            "max_values": config.get("max_values", None),
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_select
        super().__init__(**__d)

    async def callback(self, interaction: "Interaction") -> None:
        if self.__callback_fn is None:
            await interaction.response.defer()
            return

        if is_sync_func(self.__callback_fn):
            await interaction.response.defer()

        await call_any_function(self.__callback_fn, interaction, self.values)
