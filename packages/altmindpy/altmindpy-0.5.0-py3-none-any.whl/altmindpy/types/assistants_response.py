# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .assistant_response import AssistantResponse

__all__ = ["AssistantsResponse"]


class AssistantsResponse(BaseModel):
    count: int

    data: List[AssistantResponse]

    object: Optional[Literal["list"]] = None
