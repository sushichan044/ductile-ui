from typing import Annotated, TypeAlias

from annotated_types import Le, Len
from discord import Colour
from pydantic import AwareDatetime, BaseModel, Field, HttpUrl

from .url import AttachmentUrl

EmbedTitle: TypeAlias = Annotated[str, Le(256)]
EmbedDescription: TypeAlias = Annotated[str, Le(4096)]
EmbedUrl: TypeAlias = HttpUrl
EmbedTimestamp: TypeAlias = AwareDatetime
EmbedColor: TypeAlias = int | Colour

EmbedFooterText: TypeAlias = Annotated[str, Le(2048)]
EmbedFooterIconUrl: TypeAlias = HttpUrl | AttachmentUrl


class EmbedFooter(BaseModel):
    """Embed footer with validation."""

    text: EmbedFooterText | None = Field(default=None)
    icon_url: EmbedFooterIconUrl | None = Field(default=None)


EmbedAuthorName: TypeAlias = Annotated[str, Le(256)]
EmbedAuthorUrl: TypeAlias = HttpUrl
EmbedAuthorIconUrl: TypeAlias = HttpUrl | AttachmentUrl


class SafeEmbedAuthor(BaseModel):
    """Embed author with validation."""

    name: EmbedAuthorName
    url: EmbedAuthorUrl | None = Field(default=None)
    icon_url: EmbedAuthorIconUrl | None = Field(default=None)


EmbedFieldTitle: TypeAlias = Annotated[str, Le(256)]
EmbedFieldValue: TypeAlias = Annotated[str, Le(1024)]
EmbedFieldInline: TypeAlias = bool


class SafeEmbedField(BaseModel):
    """Embed field with validation."""

    name: EmbedFieldTitle
    value: EmbedFieldValue
    inline: EmbedFieldInline = Field(default=False)


EmbedFields: TypeAlias = Annotated[list[SafeEmbedField], Len(max_length=25)]


class SafeEmbed(BaseModel):
    """Embed with validation."""

    title: EmbedTitle | None = Field(default=None)
    description: EmbedDescription | None = Field(default=None)
    url: EmbedUrl | None = Field(default=None)
    timestamp: EmbedTimestamp | None = Field(default=None)
    color: EmbedColor | None = Field(default=None)

    author: SafeEmbedAuthor | None = Field(default=None)
    footer: EmbedFooter | None = Field(default=None)
    fields: EmbedFields | None = Field(default=None)

    image: HttpUrl | AttachmentUrl | None = Field(default=None)
    thumbnail: AttachmentUrl | HttpUrl | None = Field(default=None)
