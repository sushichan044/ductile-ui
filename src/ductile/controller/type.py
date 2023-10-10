from typing import TypedDict

import discord


class _ViewObjectDict(TypedDict, total=False):
    """
    ViewObjectDict is a type hint for the dictionary that is used to send a view to Discord.

    This can be passed to `discord.abc.Messageable.send` as unpacked keyword arguments.

    Accessing the keys are not recommended since the existence of the keys are not guaranteed.

    Example
    -------
    ```py
    d: ViewObjectDict = {
        "content": "Hello, world!",
        "embeds": [discord.Embed(title="Hello, world!")],
    }
    await ctx.send(**d)
    """

    content: str
    embeds: list[discord.Embed]
    view: discord.ui.View


class ViewObjectDictWithAttachment(_ViewObjectDict, total=False):
    """
    ViewObjectDictWithAttachment is a type hint for the dictionary that is used to send a view to Discord.

    This is suitable for `discord.abc.Messageable.edit()` as unpacked keyword arguments.
    """

    attachments: list[discord.File]


class ViewObjectDictWithFiles(_ViewObjectDict, total=False):
    """
    ViewObjectDictWithFiles is a type hint for the dictionary that is used to send a view to Discord.

    This is suitable for `discord.abc.Messageable.send()` as unpacked keyword arguments.
    """

    files: list[discord.File]
