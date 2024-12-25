# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import TypedDict

__all__ = ["AssistantUpdateParams"]


class AssistantUpdateParams(TypedDict, total=False):
    assistant_metadata: Optional[object]

    description: Optional[str]

    instructions: Optional[str]

    model: Optional[str]

    name: Optional[str]

    tools: Optional[Iterable[Optional[object]]]
