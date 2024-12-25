# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["UserUpdateParams"]


class UserUpdateParams(TypedDict, total=False):
    email: Optional[str]

    full_name: Optional[str]

    is_active: bool

    is_superuser: bool

    password: Optional[str]
