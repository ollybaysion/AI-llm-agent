from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field

class RecommendLlmRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    jobId: str
    userId: str
    requestedAt: datetime
    query: str
    attributes: Dict[str, Any] = Field(default_factory=dict)

class RecommendLlmResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    jobId: str
    messageId: str
    createdAt: datetime
    payload: Any
