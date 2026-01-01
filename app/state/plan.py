from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field

class StepTimeHint(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None

class StepRequirements(BaseModel):
    must_have: List[str] = Field(default_factory=list)
    avoid: List[str] = Field(default_factory=list)

class StepBudgetHint(BaseModel):
    min: Optional[int] = None
    max: Optional[int] = None

class Step(BaseModel):
    step_id: str
    label: str
    category: str
    time_hint: StepTimeHint = Field(default_factory=StepTimeHint)
    requirements: StepRequirements = Field(default_factory=StepRequirements)
    budget_hint_krw: StepBudgetHint = Field(default_factory=StepBudgetHint)

class Plan(BaseModel):
    steps: List[Step] = Field(default_factory=list)
    strategy: Optional[str] = None
