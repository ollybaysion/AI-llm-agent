from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field

class NodeHistory(BaseModel):
    node: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    status: Literal["OK", "ERROR"] = "OK"
    detail: Optional[Dict[str, Any]] = None

class ErrorItem(BaseModel):
    code: str
    message: str
    node: Optional[str] = None

class TraceState(BaseModel):
    node_history: List[NodeHistory] = Field(default_factory=list)
    errors: List[ErrorItem] = Field(default_factory=list)

class ProgressEvent(BaseModel):
    ts: datetime
    type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
