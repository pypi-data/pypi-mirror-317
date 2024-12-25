# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .file_response import FileResponse

__all__ = ["FilesResponse"]


class FilesResponse(BaseModel):
    count: int

    data: List[FileResponse]

    object: Optional[Literal["list"]] = None
