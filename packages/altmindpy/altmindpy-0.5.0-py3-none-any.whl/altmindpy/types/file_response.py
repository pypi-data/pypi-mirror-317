# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["FileResponse"]


class FileResponse(BaseModel):
    id: str

    bytes: int

    content_type: str

    created_at: int

    filename: str

    purpose: str

    object: Optional[Literal["file"]] = None
