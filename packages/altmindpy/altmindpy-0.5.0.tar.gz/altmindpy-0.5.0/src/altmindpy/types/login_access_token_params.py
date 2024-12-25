# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["LoginAccessTokenParams"]


class LoginAccessTokenParams(TypedDict, total=False):
    password: Required[str]

    username: Required[str]

    client_id: Optional[str]

    client_secret: Optional[str]

    grant_type: Optional[str]

    scope: str
