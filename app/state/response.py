from __future__ import annotations

from typing import Optional
from pydantic import BaseModel

from .common import ResponseFormat

class ResponseState(BaseModel):
    format: ResponseFormat = "markdown"
    draft: Optional[str] = None
    final: Optional[str] = None

class PersistState(BaseModel):
    should_save: bool = False
    cache_key: Optional[str] = None
    saved_course_id: Optional[str] = None