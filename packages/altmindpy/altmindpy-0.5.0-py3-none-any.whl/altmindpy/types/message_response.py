# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "MessageResponse",
    "Content",
    "ContentTextContent",
    "ContentTextContentText",
    "ContentImageFileContent",
    "ContentImageFileContentImageFile",
    "ContentToolContent",
    "ContentToolContentTool",
]


class ContentTextContentText(BaseModel):
    value: str


class ContentTextContent(BaseModel):
    text: ContentTextContentText

    type: Optional[Literal["text"]] = None


class ContentImageFileContentImageFile(BaseModel):
    file_id: str


class ContentImageFileContent(BaseModel):
    image_file: ContentImageFileContentImageFile

    type: Optional[Literal["image_file"]] = None


class ContentToolContentTool(BaseModel):
    content: Optional[object] = None

    name: Optional[str] = None

    tool_call_id: Optional[str] = None


class ContentToolContent(BaseModel):
    tool: ContentToolContentTool

    type: Optional[Literal["tool"]] = None


Content: TypeAlias = Union[ContentTextContent, ContentImageFileContent, ContentToolContent]


class MessageResponse(BaseModel):
    id: str

    content: List[Content]

    created_at: int

    original_role: Optional[Literal["user", "assistant", "system", "tool"]] = None

    message_metadata: Optional[object] = None

    object: Optional[Literal["message"]] = None

    role: Optional[Literal["user", "assistant", "system", "tool"]] = None

    thread_id: Optional[str] = None

    tool_calls: Optional[List[builtins.object]] = None
