# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "MessageCreateParams",
    "ContentContentArray",
    "ContentContentArrayTextContent",
    "ContentContentArrayTextContentText",
    "ContentContentArrayImageFileContent",
    "ContentContentArrayImageFileContentImageFile",
    "ContentContentArrayToolContent",
    "ContentContentArrayToolContentTool",
]


class MessageCreateParams(TypedDict, total=False):
    content: Required[Union[str, Iterable[ContentContentArray]]]

    message_metadata: object

    original_role: Optional[Literal["user", "assistant", "system", "tool"]]

    role: Optional[Literal["user", "assistant", "system", "tool"]]

    thread_id: Optional[str]

    tool_calls: Optional[Iterable[object]]


class ContentContentArrayTextContentText(TypedDict, total=False):
    value: Required[str]


class ContentContentArrayTextContent(TypedDict, total=False):
    text: Required[ContentContentArrayTextContentText]

    type: Literal["text"]


class ContentContentArrayImageFileContentImageFile(TypedDict, total=False):
    file_id: Required[str]


class ContentContentArrayImageFileContent(TypedDict, total=False):
    image_file: Required[ContentContentArrayImageFileContentImageFile]

    type: Literal["image_file"]


class ContentContentArrayToolContentTool(TypedDict, total=False):
    content: Optional[object]

    name: Optional[str]

    tool_call_id: Optional[str]


class ContentContentArrayToolContent(TypedDict, total=False):
    tool: Required[ContentContentArrayToolContentTool]

    type: Literal["tool"]


ContentContentArray: TypeAlias = Union[
    ContentContentArrayTextContent, ContentContentArrayImageFileContent, ContentContentArrayToolContent
]
