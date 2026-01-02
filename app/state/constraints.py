from __future__ import annotations

from typing import List, Optional, Literal
from pydantic import BaseModel, Field

from .common import Transport, Pace

class Region(BaseModel):
    city: Optional[str] = None
    district: Optional[str] = None
    near: Optional[str] = None

class TimeWindow(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None

class BudgetKRW(BaseModel):
    min: Optional[int] = None
    max: Optional[int] = None

class Party(BaseModel):
    type: Optional[Literal["couple", "friends", "family", "solo"]] = None
    size: Optional[int] = None

class Preferences(BaseModel):
    likes: List[str] = Field(default_factory=list)
    dislikes: List[str] = Field(default_factory=list)
    must: List[str] = Field(default_factory=list)
    avoid: List[str] = Field(default_factory=list)

class Constraints(BaseModel):
    region: Region = Field(default_factory=Region)
    date: Optional[str] = None
    time_window: TimeWindow = Field(default_factory=TimeWindow)
    budget_krw: BudgetKRW = Field(default_factory=BudgetKRW)
    party: Party = Field(default_factory=Party)
    transport: Optional[Transport] = None
    pace: Optional[Pace] = None
    preference: Preferences = Field(default_factory=Preferences)
    constraints_freeform: Optional[str] = None