# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ThreadResponse"]


class ThreadResponse(BaseModel):
    id: str

    created_at: int

    object: Optional[Literal["thread"]] = None

    thread_metadata: Optional[builtins.object] = None

    title: Optional[str] = None
