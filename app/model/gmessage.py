from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.generics import GenericModel

T = TypeVar("T")

class GMessage(GenericModel, Generic[T]):
    model_config = ConfigDict(extra="forbid")

    gId: str
    gDestination: str
    key: Optional[str] = None
    createdAt: datetime
    headers: Dict[str, str]
    payload: T