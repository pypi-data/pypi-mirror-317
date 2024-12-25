"""
Reference: https://developers.notion.com/reference/block
"""

from __future__ import annotations
from uuid import UUID
from datetime import datetime
from typing import Union, Optional, Literal, List, Annotated

from pydantic_api.base import BaseModel
from pydantic import Field, HttpUrl, PositiveInt

from ..user import PartialUser
from .rich_text import RichTextObject
from ..parent import PageParentObject, BlockParentObject, DatabaseParentObject
from ..common import (
    IconObject,
    ColorLiteral,
    CodeLanguageLiteral,
)
from ..file import FileObject, _BaseFileObject, _FileExternal, _FileUploaded


BlockTypeLiteral = Literal[
    "bookmark",
    "breadcrumb",
    "bulleted_list_item",
    "callout",
    "child_database",
    "child_page",
    "column",
    "column_list",
    "divider",
    "embed",
    "equation",
    "file",
    "heading_1",
    "heading_2",
    "heading_3",
    "image",
    "link_preview",
    "link_to_page",
    "numbered_list_item",
    "paragraph",
    "pdf",
    "quote",
    "synced_block",
    "table",
    "table_of_contents",
    "table_row",
    "template",
    "to_do",
    "toggle",
    "unsupported",
    "video",
]
"""Reference: https://developers.notion.com/reference/block#keys"""

ParentOfBlock = Union[
    PageParentObject,
    BlockParentObject,
    DatabaseParentObject,
]
"""Databases can be parented by pages, blocks, or by the whole workspace. Reference: https://developers.notion.com/reference/block#parent"""


class BaseBlock(BaseModel):
    """Reference: https://developers.notion.com/reference/block#keys"""

    object: Literal["block"] = "block"
    id: UUID
    parent: ParentOfBlock
    type: BlockTypeLiteral
    created_time: datetime
    created_by: PartialUser
    last_edited_time: datetime
    last_edited_by: PartialUser
    archived: bool
    in_trash: bool
    has_children: bool


class EmptyBlockData(BaseModel):
    pass


# bookmark: Refer to https://developers.notion.com/reference/block#bookmark
class BookMarkBlockData(BaseModel):
    caption: List[RichTextObject] = Field(
        default_factory=list, description="The caption for the bookmark."
    )
    url: str = Field(..., description="The link for the bookmark")


class BookmarkBlock(BaseBlock):
    type: Literal["bookmark"] = "bookmark"
    bookmark: BookMarkBlockData = Field(
        ...,
        description="Bookmark block object",
    )


# breadcrumb: Refer to https://developers.notion.com/reference/block#breadcrumb
class BreadcrumbBlock(BaseBlock):
    type: Literal["breadcrumb"] = "breadcrumb"
    breakdcrumb: EmptyBlockData = Field(
        default_factory=EmptyBlockData,
    )


# bulleted_list_item: Refer to https://developers.notion.com/reference/block#bulleted_list_item
class BulletedListItemBlockData(BaseModel):
    rich_text: List[RichTextObject] = Field(
        default_factory=list, description="The content of the bulleted list item."
    )
    color: ColorLiteral
    children: List[BlockObject] = Field(
        default_factory=list,
        description="The nested child blocks (if any) of the bulleted_list_item block.",
    )


class BulletedListItem(BaseModel):
    type: Literal["bulleted_list_item"] = "bulleted_list_item"
    bulleted_list_item: BulletedListItemBlockData = Field(
        ...,
        description="Bulleted list item block object",
    )


# callout: Refer to https://developers.notion.com/reference/block#callout
class CalloutBlockData(BaseModel):
    rich_text: List[RichTextObject] = Field(
        default_factory=list, description="The content of the callout."
    )
    icon: Optional[IconObject] = Field(None)
    color: ColorLiteral


class CalloutBlock(BaseBlock):
    type: Literal["callout"] = "callout"
    callout: CalloutBlockData


# child_database: Refer to https://developers.notion.com/reference/block#child_database
class ChildDatabaseBlockData(BaseModel):
    title: str = Field(..., description="The plain text title of the database.")


class ChildDatabaseBlock(BaseBlock):
    """
    Note:

    📘 Creating and updating child_database blocks

    To create or update child_database type blocks, use the Create a database and the Update a database endpoints, specifying the ID of the parent page in the parent body param.
    """

    type: Literal["child_database"] = "child_database"
    child_database: ChildDatabaseBlockData


# child_page: Refer to https://developers.notion.com/reference/block#child_page
class ChildPageBlockData(BaseModel):
    title: str = Field(..., description="The plain text title of the page.")


class ChildPageBlock(BaseBlock):
    """
    Note:

    📘 Creating and updating child_page blocks

    To create or update child_page type blocks, use the Create a page and the Update page endpoints, specifying the ID of the parent page in the parent body param.
    """

    type: Literal["child_page"] = "child_page"
    child_page: ChildPageBlockData


# code: Refer to https://developers.notion.com/reference/block#code
class CodeBlockData(BaseModel):
    caption: List[RichTextObject] = Field(
        default_factory=list,
        description="The rich text in the caption of the code block.",
    )
    rich_text: List[RichTextObject] = Field(
        default_factory=list, description="The content of the code block."
    )
    language: CodeLanguageLiteral = Field(
        ..., description="The language of the code contained in the code block."
    )


class CodeBlock(BaseBlock):
    type: Literal["code"] = "code"
    code: CodeBlockData


# column: Refer to https://developers.notion.com/reference/block#column_list_and_column
class ColumnBlock(BaseBlock):
    """
    Columns are parent blocks for any block types listed in this reference except for other columns. They do not contain any information within the column property. They can only be appended to column_lists.
    """

    type: Literal["column"] = "column"
    column: EmptyBlockData = Field(
        default_factory=EmptyBlockData,
    )


# column_list: Refer to https://developers.notion.com/reference/block#column_list_and_column
class ColumnListBlock(BaseBlock):
    """
    Column lists are parent blocks for columns. They do not contain any information within the column_list property.

    When creating a column_list block via Append block children, the column_list must have at least two columns, and each column must have at least one child.

    Follow these steps to fetch the content in a column_list:

    Get the column_list ID from a query to Retrieve block children for the parent page.

    Get the column children from a query to Retrieve block children for the column_list.

    Get the content in each individual column from a query to Retrieve block children for the unique column ID.
    """

    type: Literal["column_list"] = "column_list"
    column_list: EmptyBlockData = Field(
        default_factory=EmptyBlockData,
    )


# divider: Refer to https://developers.notion.com/reference/block#divider
class DividerBlock(BaseBlock):
    type: Literal["divider"] = "divider"
    divider: EmptyBlockData = Field(
        default_factory=EmptyBlockData,
    )


# embed: Refer to https://developers.notion.com/reference/block#embed
class EmbedBlockData(BaseModel):
    url: HttpUrl = Field(..., description="The URL of the embed.")


class EmbedBlock(BaseBlock):
    """
    Note:

    🚧 Differences in embed blocks between the Notion app and the API

    The Notion app uses a 3rd-party service, iFramely, to validate and request metadata for embeds given a URL. This works well in a web app because Notion can kick off an asynchronous request for URL information, which might take seconds or longer to complete, and then update the block with the metadata in the UI after receiving a response from iFramely.

    We chose not to call iFramely when creating embed blocks in the API because the API needs to be able to return faster than the UI, and because the response from iFramely could actually cause us to change the block type. This would result in a slow and potentially confusing experience as the block in the response would not match the block sent in the request.

    The result is that embed blocks created via the API may not look exactly like their counterparts created in the Notion app.

    👍 Vimeo video links can be embedded in a Notion page via the public API using the embed block type.

    For supported video sources, see [Supported video types](https://developers.notion.com/reference/block#supported-video-types).
    """

    type: Literal["embed"] = "embed"
    embed: EmbedBlockData


# equation: Refer to https://developers.notion.com/reference/block#equation
class EquationBlockData(BaseModel):
    expression: str = Field(..., description="A KaTeX compatible string.")


class EquationBlock(BaseBlock):
    """
    Equation block objects are represented as children of paragraph blocks. They are nested within a rich text object and contain the following information within the equation property:
    """

    type: Literal["equation"] = "equation"
    equation: EquationBlockData


# file
class BaseBlockFileObject(_BaseFileObject):
    caption: List[RichTextObject] = Field(
        default_factory=list,
        description="The caption for the file block.",
    )


class ExternalBlockFileObject(_BaseFileObject):
    type: Literal["external"] = "external"
    external: _FileExternal


class UploadedBlockFileObject(_BaseFileObject):
    type: Literal["file"] = "file"
    file: _FileUploaded


BlockFileObject = Annotated[
    Union[ExternalBlockFileObject, UploadedBlockFileObject],
    Field(discriminator="type"),
]
"""FileObject + caption field"""


class FileBlock(BaseBlock):
    type: Literal["file"] = "file"
    file: BlockFileObject


# headings: Refer to https://developers.notion.com/reference/block#heading
class HeadingBlockData(BaseModel):
    rich_text: List[RichTextObject] = Field(
        default_factory=list, description="The content of the heading."
    )
    color: ColorLiteral
    is_toggleable: bool = Field(
        ...,
        description="Whether or not the heading block is a toggle heading or not. If true, then the heading block toggles and can support children. If false, then the heading block is a static heading block.",
    )


class Heading1Block(BaseBlock):
    type: Literal["heading_1"] = "heading_1"
    heading_1: HeadingBlockData


class Heading2Block(BaseBlock):
    type: Literal["heading_2"] = "heading_2"
    heading_2: HeadingBlockData


class Heading3Block(BaseBlock):
    type: Literal["heading_3"] = "heading_3"
    heading_3: HeadingBlockData


HeadingBlock = Annotated[
    Union[Heading1Block, Heading2Block, Heading3Block],
    Field(discriminator="type"),
]


class HeadingBlockFactory:
    @classmethod
    def new(
        cls,
        rich_text: List[RichTextObject],
        color: ColorLiteral | None = None,
        is_toggleable: bool = False,
        heading_type: Literal["heading_1", "heading_2", "heading_3"] = "heading_1",
    ):
        pass


# image: Refer to https://developers.notion.com/reference/block#image
ImageBlockData = FileObject


class ImageBlock(BaseBlock):
    type: Literal["image"] = "image"
    image: ImageBlockData


# link_preview: Refer to https://developers.notion.com/reference/block#link_preview
class LinkPreviewBlockData(BaseModel):
    url: HttpUrl = Field(..., description="The URL of the link preview.")


class LinkPreviewBlock(BaseBlock):
    """
    🚧 The link_preview block can only be returned as part of a response. The API does not support creating or appending link_preview blocks.
    """

    type: Literal["link_preview"] = "link_preview"
    link_preview: LinkPreviewBlockData


# mention: Refer to https://developers.notion.com/reference/block#mention
# mention is not an independent block, it is nested in the rich text object in the paragraph block, so just use MentionObject


# numbered_list_item: Refer to https://developers.notion.com/reference/block#numbered_list_item
class NumberedListItemBlockData(BaseModel):
    rich_text: List[RichTextObject] = Field(
        default_factory=list, description="The content of the numbered list item."
    )
    color: ColorLiteral
    children: List[BlockObject] = Field(
        default_factory=list,
        description="The nested child blocks (if any) of the numbered_list_item block.",
    )


class NumberedListItem(BaseModel):
    type: Literal["numbered_list_item"] = "numbered_list_item"
    numbered_list_item: NumberedListItemBlockData = Field(
        ...,
        description="Numbered list item block object",
    )


# paragraph: Refer to https://developers.notion.com/reference/block
class ParagraphBlockData(BaseModel):
    rich_text: List[RichTextObject] = Field(
        default_factory=list, description="The content of the paragraph."
    )
    color: ColorLiteral
    children: List[BlockObject] = Field(
        default_factory=list,
        description="The nested child blocks (if any) of the paragraph block.",
    )


class ParagraphBlock(BaseBlock):
    type: Literal["paragraph"] = "paragraph"
    paragraph: ParagraphBlockData


# pdf: Refer to https://developers.notion.com/reference/block#pdf
class PdfBlock(BaseBlock):
    type: Literal["pdf"] = "pdf"
    pdf: BlockFileObject


# quote: Refer to https://developers.notion.com/reference/block#quote
class QuoteBlockData(BaseModel):
    rich_text: List[RichTextObject] = Field(
        default_factory=list, description="The content of the quote."
    )
    color: ColorLiteral
    children: List[BlockObject] = Field(
        default_factory=list,
        description="The nested child blocks (if any) of the quote block.",
    )


class QuoteBlock(BaseBlock):
    type: Literal["quote"] = "quote"
    quote: QuoteBlockData


# synced_block: Refer to https://developers.notion.com/reference/block#synced-block
class OriginalSyncedBlockData(BaseModel):
    synced_from: Literal[None] = None
    children: List[BlockObject] = Field(
        default_factory=list,
        description="The nested child blocks (if any) of the synced block.",
    )


class BaseSyncedBlock(BaseBlock):
    type: Literal["synced_block"] = "synced_block"


class OriginalSyncedBlock(BaseSyncedBlock):
    synced_block: OriginalSyncedBlockData


class BlockReference(BaseModel):
    block_id: str


class DuplicateSyncedBlockData(BaseModel):
    synced_from: BlockReference


class DupliateSyncedBlock(BaseSyncedBlock):
    synced_block: DuplicateSyncedBlockData


SyncedBlock = Union[OriginalSyncedBlock, DupliateSyncedBlock]


# table: Refer to https://developers.notion.com/reference/block#table
class TableBlockData(BaseModel):
    table_width: PositiveInt = Field(
        ...,
        description="The number of columns in the table. Note that table_width can only be set when the table is first created.",
    )
    has_column_header: bool = Field(
        ...,
        description="Whether the table has a column header. If true, then the first row in the table appears visually distinct from the other rows.",
    )
    has_row_header: bool = Field(
        ...,
        description="Whether the table has a header row. If true, then the first column in the table appears visually distinct from the other columns.",
    )


class TableBlock(BaseBlock):
    type: Literal["table"] = "table"
    table: TableBlockData


# table_row: Refer to https://developers.notion.com/reference/block#table_rows
class TableRowBlockData(BaseModel):
    cells: List[RichTextObject] = Field(
        default_factory=list,
        description="The cells in the table row.",
    )


class TableRowBlock(BaseBlock):
    type: Literal["table_row"] = "table_row"
    table_row: TableRowBlockData


# table_of_contents: Refer to https://developers.notion.com/reference/block#table_of_contents
class TableOfContentsBlockData(BaseModel):
    color: ColorLiteral


class TableOfContentsBlock(BaseBlock):
    type: Literal["table_of_contents"] = "table_of_contents"
    table_of_contents: TableOfContentsBlockData


# template: Refer to https://developers.notion.com/reference/block#template
class TemplateBlockData(BaseModel):
    rich_text: List[RichTextObject] = Field(
        default_factory=list, description="The content of the template."
    )
    children: List[BlockObject] = Field(
        default_factory=list,
        description="The nested child blocks (if any) of the template block.",
    )


class TemplateBlock(BaseBlock):
    """
    ❗️ Deprecation Notice

    As of March 27, 2023 creation of template blocks will no longer be supported.
    """

    type: Literal["template"] = "template"
    template: TemplateBlockData


# to_do: Refer to https://developers.notion.com/reference/block#to_do
class TodoBlockData(BaseModel):
    rich_text: List[RichTextObject] = Field(
        default_factory=list, description="The rich text displayed in the To do block."
    )
    checked: Optional[bool] = Field(None, description="Whether the To do is checked.")
    color: ColorLiteral
    children: List[BlockObject] = Field(
        default_factory=list,
        description="The nested child blocks (if any) of the to_do block.",
    )


class TodoBlock(BaseModel):
    type: Literal["to_do"] = "to-do"
    to_do: TodoBlockData


# toggle-blocks: Refer to https://developers.notion.com/reference/block
class ToggleBlockData(BaseModel):
    rich_text: List[RichTextObject] = Field(
        default_factory=list, description="The content of the toggle."
    )
    color: ColorLiteral
    children: List[BlockObject] = Field(
        default_factory=list,
        description="The nested child blocks (if any) of the toggle block.",
    )


class ToggleBlock(BaseBlock):
    type: Literal["toggle"] = "toggle"
    toggle: ToggleBlockData


# video: Refer to https://developers.notion.com/reference/block#video
class VideoBlock(BaseBlock):
    """
    📘 Vimeo video links are not currently supported by the video block type. However, they can be embedded in Notion pages using the embed block type. See Embed for more information.
    """

    type: Literal["video"] = "video"
    video: BlockFileObject


# Union Type
BlockObject = Union[
    BookmarkBlock,
    BreadcrumbBlock,
    BulletedListItem,
    CalloutBlock,
    ChildDatabaseBlock,
    ChildPageBlock,
    CodeBlock,
    ColumnBlock,
    ColumnListBlock,
    DividerBlock,
    EmbedBlock,
    EquationBlock,
    FileBlock,
    Heading1Block,
    Heading2Block,
    Heading3Block,
    ImageBlock,
    LinkPreviewBlock,
    NumberedListItem,
    ParagraphBlock,
    PdfBlock,
    QuoteBlock,
    SyncedBlock,
    TableBlock,
    TableRowBlock,
    TableOfContentsBlock,
    TemplateBlock,
    TodoBlock,
    ToggleBlock,
    VideoBlock,
]

__all__ = [
    "BlockObject",
    "BookmarkBlock",
    "BreadcrumbBlock",
    "BulletedListItem",
    "CalloutBlock",
    "ChildDatabaseBlock",
    "ChildPageBlock",
    "CodeBlock",
    "ColumnBlock",
    "ColumnListBlock",
    "DividerBlock",
    "EmbedBlock",
    "EquationBlock",
    "FileBlock",
    "Heading1Block",
    "Heading2Block",
    "Heading3Block",
    "ImageBlock",
    "LinkPreviewBlock",
    "NumberedListItem",
    "ParagraphBlock",
    "PdfBlock",
    "QuoteBlock",
    "SyncedBlock",
    "TableBlock",
    "TableRowBlock",
    "TableOfContentsBlock",
    "TemplateBlock",
    "TodoBlock",
    "ToggleBlock",
    "VideoBlock",
    "BlockTypeLiteral",
    "ParentOfBlock",
]
