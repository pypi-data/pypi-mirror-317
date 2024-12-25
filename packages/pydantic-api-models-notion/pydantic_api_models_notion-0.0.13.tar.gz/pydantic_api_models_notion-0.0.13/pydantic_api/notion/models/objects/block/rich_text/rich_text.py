from typing import Annotated, Union

from pydantic import Field

from .text import TextRichTextObject
from .mention import MentionRichTextObject
from .equation import EquationRichTextObject

RichTextObject = Annotated[
    Union[TextRichTextObject, MentionRichTextObject, EquationRichTextObject],
    Field(discriminator="type"),
]


# Factory class for Devlopers
class RichTextObjectFactory:
    @classmethod
    def new_text(cls, content: str, link: dict = None):
        return TextRichTextObject.new(content=content, link=link)

    @classmethod
    def new_equation(cls, expression: str):
        return EquationRichTextObject.new(expression=expression)

    @classmethod
    def new_mention(cls):
        raise NotImplementedError(
            f"Factory method for Mention object is not implemented yet."
        )


__all__ = [
    "RichTextObject",
    "RichTextObjectFactory",
]
