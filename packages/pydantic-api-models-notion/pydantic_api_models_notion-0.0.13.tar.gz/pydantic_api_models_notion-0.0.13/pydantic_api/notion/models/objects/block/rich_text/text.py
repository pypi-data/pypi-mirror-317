from typing import Literal, Optional

from pydantic import Field

from pydantic_api.base import BaseModel
from .base import BaseRichTextObject


class TextObject(BaseModel):
    """Text object type."""

    content: str
    link: Optional[dict] = Field(None, description="Link object or null")


class TextRichTextObject(BaseRichTextObject):
    """Rich Text type: Text."""

    type: Literal["text"] = "text"
    text: TextObject

    @classmethod
    def new(cls, content: str, link: Optional[dict] = None):
        return cls(text=TextObject(content=content, link=link))


__all__ = [
    "TextObject",
    "TextRichTextObject",
]
