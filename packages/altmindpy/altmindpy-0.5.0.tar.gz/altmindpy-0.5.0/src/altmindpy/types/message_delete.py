# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["MessageDelete"]


class MessageDelete(BaseModel):
    id: str

    deleted: Optional[bool] = None

    object: Optional[Literal["message.deleted"]] = None
