# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["UserCreateParams"]


class UserCreateParams(TypedDict, total=False):
    email: Required[str]

    password: Required[str]

    full_name: Optional[str]

    is_active: bool

    is_superuser: bool
