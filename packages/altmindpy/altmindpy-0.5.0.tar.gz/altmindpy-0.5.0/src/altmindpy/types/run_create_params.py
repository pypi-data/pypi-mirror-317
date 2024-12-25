# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["RunCreateParams"]


class RunCreateParams(TypedDict, total=False):
    assistant_id: Required[Optional[str]]

    thread_id: Required[Optional[str]]

    stream: bool

    additional_instructions: Optional[str]

    instructions: Optional[str]

    model: Optional[str]

    run_metadata: object

    tool_choice: Optional[object]

    tools: Iterable[Optional[object]]

    type: Literal["default", "analysis", "execution"]
