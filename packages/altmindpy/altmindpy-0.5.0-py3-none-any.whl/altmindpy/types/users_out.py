# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .shared.user_out import UserOut

__all__ = ["UsersOut"]


class UsersOut(BaseModel):
    count: int

    data: List[UserOut]
