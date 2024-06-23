from typing import TYPE_CHECKING

from typing_extensions import TypedDict

if TYPE_CHECKING:
    from discord import Embed, File, ui


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
    embeds: "list[Embed]"
    view: "ui.View"


class ViewObjectDictWithAttachment(_ViewObjectDict, total=False):
    attachments: "list[File]"


class ViewObjectDictWithFiles(_ViewObjectDict, total=False):
    files: "list[File]"
