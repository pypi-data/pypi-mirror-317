# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .thread_response import ThreadResponse

__all__ = ["ThreadsResponse"]


class ThreadsResponse(BaseModel):
    count: int

    data: List[ThreadResponse]

    object: Optional[Literal["list"]] = None
