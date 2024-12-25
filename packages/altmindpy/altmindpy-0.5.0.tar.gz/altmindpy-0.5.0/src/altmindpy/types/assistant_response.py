# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AssistantResponse"]


class AssistantResponse(BaseModel):
    id: str

    created_at: int

    model: str

    assistant_metadata: Optional[object] = None

    description: Optional[str] = None

    instructions: Optional[str] = None

    name: Optional[str] = None

    object: Optional[Literal["assistant"]] = None

    tools: Optional[List[Optional[builtins.object]]] = None
