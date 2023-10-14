from collections.abc import Awaitable, Callable
from typing import TypeAlias

import discord
from discord.app_commands import AppCommandChannel, AppCommandThread

__all__ = [
    "InteractionCallback",
    "SelectCallback",
    "ChannelSelectCallback",
    "RoleSelectCallback",
    "MentionableSelectCallback",
    "UserSelectCallback",
    "ModalCallback",
]

# InteractionCallback
InteractionCallback: TypeAlias = Callable[[discord.Interaction], Awaitable[None]]
InteractionSyncCallback: TypeAlias = Callable[[discord.Interaction], None]

# SelectCallback
SelectCallback: TypeAlias = Callable[[discord.Interaction, list[str]], Awaitable[None]]
SelectSyncCallback: TypeAlias = Callable[[discord.Interaction, list[str]], None]

ChannelSelectCallback: TypeAlias = Callable[
    [discord.Interaction, list[AppCommandChannel | AppCommandThread]],
    Awaitable[None],
]
ChannelSelectSyncCallback: TypeAlias = Callable[
    [discord.Interaction, list[AppCommandChannel | AppCommandThread]],
    None,
]

RoleSelectCallback: TypeAlias = Callable[
    [discord.Interaction, list[discord.Role]],
    Awaitable[None],
]
RoleSelectSyncCallback: TypeAlias = Callable[
    [discord.Interaction, list[discord.Role]],
    None,
]

MentionableSelectCallback: TypeAlias = Callable[
    [discord.Interaction, list[discord.Role | discord.Member | discord.User]],
    Awaitable[None],
]
MentionableSelectSyncCallback: TypeAlias = Callable[
    [discord.Interaction, list[discord.Role | discord.Member | discord.User]],
    None,
]

UserSelectCallback: TypeAlias = Callable[[discord.Interaction, list[discord.User | discord.Member]], Awaitable[None]]
UserSelectSyncCallback: TypeAlias = Callable[[discord.Interaction, list[discord.User | discord.Member]], None]


# ModalCallback
ModalCallback: TypeAlias = Callable[[discord.Interaction, dict[str, str]], Awaitable[None]]
ModalSyncCallback: TypeAlias = Callable[[discord.Interaction, dict[str, str]], None]
