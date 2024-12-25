# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["ThreadCreateParams"]


class ThreadCreateParams(TypedDict, total=False):
    thread_metadata: object

    title: Optional[str]
