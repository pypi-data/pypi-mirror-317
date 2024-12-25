# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["UserPasswordParams"]


class UserPasswordParams(TypedDict, total=False):
    current_password: Required[str]

    new_password: Required[str]
