from typing import Annotated, TypeAlias

from annotated_types import Le, Len
from discord import File
from pydantic import BaseModel, Field

from .embed import SafeEmbed

MessageContent: TypeAlias = Annotated[str, Le(2000)]
MessageEmbeds: TypeAlias = Annotated[list[SafeEmbed], Len(max_length=10)]
MessageFiles: TypeAlias = Annotated[list[File], Len(max_length=10)]


class SafeMessage(BaseModel):
    """Message with validation."""

    content: MessageContent | None = Field(default=None)
    embeds: MessageEmbeds | None = Field(default=None)
    files: MessageFiles | None = Field(default=None)
