from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ..utils.time import now_utc
from .common import Intent, Channel
from .constraints import Constraints
from .plan import Plan
from .places import PlaceCandidate, SelectedCourse
from .response import ResponseState, PersistState
from .trace import TraceState, ProgressEvent

class ClassifyingQuestion(BaseModel):
    id: str
    question: str
    choices: Optional[List[str]] = None

class AgentState(BaseModel):
    job_id: str
    user_id: Optional[str] = None
    user_query_raw: str
    channel: Channel = "api"
    requested_at: Any = Field(default_factory=now_utc)
    locale: str = "ko-KR"
    timezone: str = "Asia/Seoul"

    intent: Intent = "UNKNOWN"
    constraints: Constraints = Field(default_factory=Constraints)
    missing_slot: List[str] = Field(default_factory=list)

    clarifying_question: List[ClassifyingQuestion] = Field(default_factory=list)
    user_answers: Dict[str, Any] = Field(default_factory=dict)

    plan: Plan = Field(default_factory=Plan)

    candidates_by_step: Dict[str, List[PlaceCandidate]] = Field(default_factory=dict)
    selected_course: SelectedCourse = Field(default_factory=SelectedCourse)

    response: ResponseState = Field(default_factory=ResponseState)
    persist: PersistState = Field(default_factory=PersistState)

    trace: TraceState = Field(default_factory=TraceState)
    progress_event: List[ProgressEvent] = Field(default_factory=list)

    model_config = {
        "extra": "forbid",
    }