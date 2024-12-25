# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .message_response import MessageResponse

__all__ = ["MessagesResponse"]


class MessagesResponse(BaseModel):
    count: int

    data: List[MessageResponse]

    object: Optional[Literal["list"]] = None
