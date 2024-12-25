# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Token"]


class Token(BaseModel):
    access_token: str

    token_type: Optional[str] = None
