# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["AssistantCreateParams"]


class AssistantCreateParams(TypedDict, total=False):
    model: Required[str]

    assistant_metadata: object

    description: Optional[str]

    instructions: Optional[str]

    name: Optional[str]

    tools: Iterable[Optional[object]]
