from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ScorePlaceInput(BaseModel):
    placeId: int

class ScoreOptions(BaseModel):
    window: str = "H24"
    returnBreakdown: bool = True
    topK: int = 1

class UserContext(BaseModel):
    usetId: str
    area: str
    date: str
    startTime: str
    budgetRange: str
    transportation: str
    mood: List[str] = Field(default_factory=list)


class TimeContext(BaseModel):
    now: str

class InternalScoreRequest(BaseModel):
    userContext: UserContext
    timeContext: TimeContext
    places: List[ScorePlaceInput]
    options: ScoreOptions

class ScoredPlace(BaseModel):
    placeId: int
    totalScore: float
    breakdown: Optional[Dict[str, Any]] = None

class ScoreMeta(BaseModel):
    scoringVersion: Optional[str] = None
    cache: Optional[str] = None
    window: Optional[Any] = None

class InternalScoreResponse(BaseModel):
    scoredPlaces: List[ScoredPlace] = Field(default_factory=list)
    meta: Optional[ScoreMeta] = None


