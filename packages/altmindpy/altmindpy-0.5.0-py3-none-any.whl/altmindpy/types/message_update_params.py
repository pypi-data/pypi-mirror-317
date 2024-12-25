# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "MessageUpdateParams",
    "Content",
    "ContentTextContent",
    "ContentTextContentText",
    "ContentImageFileContent",
    "ContentImageFileContentImageFile",
    "ContentToolContent",
    "ContentToolContentTool",
]


class MessageUpdateParams(TypedDict, total=False):
    content: Optional[Iterable[Content]]

    message_metadata: Optional[object]

    role: Optional[Literal["user", "assistant", "system", "tool"]]

    tool_calls: Optional[Iterable[object]]


class ContentTextContentText(TypedDict, total=False):
    value: Required[str]


class ContentTextContent(TypedDict, total=False):
    text: Required[ContentTextContentText]

    type: Literal["text"]


class ContentImageFileContentImageFile(TypedDict, total=False):
    file_id: Required[str]


class ContentImageFileContent(TypedDict, total=False):
    image_file: Required[ContentImageFileContentImageFile]

    type: Literal["image_file"]


class ContentToolContentTool(TypedDict, total=False):
    content: Optional[object]

    name: Optional[str]

    tool_call_id: Optional[str]


class ContentToolContent(TypedDict, total=False):
    tool: Required[ContentToolContentTool]

    type: Literal["tool"]


Content: TypeAlias = Union[ContentTextContent, ContentImageFileContent, ContentToolContent]
