from typing import Annotated, TypeAlias

from pydantic import AnyUrl, UrlConstraints

AttachmentUrl: TypeAlias = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["attachment"])]
