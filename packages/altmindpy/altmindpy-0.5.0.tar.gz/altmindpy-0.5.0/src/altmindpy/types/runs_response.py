# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .run_response import RunResponse

__all__ = ["RunsResponse"]


class RunsResponse(BaseModel):
    count: int

    data: List[RunResponse]

    object: Optional[Literal["list"]] = None
