from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field

class Score(BaseModel):
    total: float = 0.0
    breakdown: Dict[str, float] = Field(default_factory=dict)

class PlaceLocation(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None
    address: Optional[str] = None

class PlaceCandidate(BaseModel):
    place_id: str
    name: str
    category: str
    location: PlaceLocation = Field(defalt_factory=PlaceLocation)
    price_level: Optional[Any] = None
    open_hours: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    source: Literal["db", "cache", "maps", "llm_suggested"] = "llm_suggested"
    score: Score = Field(default_factory=Score)
    notes: Optional[str] = None

class RouteSummary(BaseModel):
    total_distance_km: Optional[float] = None
    total_time_min: Optional[int] = None

class SelectedCourse(BaseModel):
    selected_by_step: Dict[str, PlaceCandidate] = Field(default_factory=dict)
    route_summary: Optional[RouteSummary] = None
