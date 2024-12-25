# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["RunResponse"]


class RunResponse(BaseModel):
    id: str

    assistant_id: Optional[str] = None

    created_at: int

    required_action: Optional[object] = None

    status: Literal["queued", "in_progress", "completed", "requires_action", "expired", "cancelled", "failed"]

    thread_id: Optional[str] = None

    timeline: Optional[Dict[str, int]] = None

    usage: Optional[Dict[str, int]] = None

    additional_instructions: Optional[str] = None

    instructions: Optional[str] = None

    model: Optional[str] = None

    object: Optional[Literal["run"]] = None

    run_metadata: Optional[builtins.object] = None

    tool_choice: Optional[builtins.object] = None

    tools: Optional[List[Optional[builtins.object]]] = None

    type: Optional[Literal["default", "analysis", "execution"]] = None
