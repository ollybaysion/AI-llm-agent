from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..state.agent_state import AgentState
from ..state.places import PlaceCandidate, SelectedCourse
from ..state.places import Score as CandidateScore
from ..utils import traced_node, TraceOptions
from ..utils.time import now_utc
from ..utils.place_id import stable_long_place_id
from ..ports.scoring import ScoreClient
from ..dto.scoring import (
    InternalScoreRequest,
    UserContext,
    TimeContext,
    ScoreOptions,
    ScorePlaceInput,
)

def _safe_get(obj: Any, *names: str, default: Any = None) -> Any:
    for n in names:
        if hasattr(obj, n):
            v = getattr(obj, n)
            if v is not None:
                return v

    return default

def _to_user_context(state: AgentState) -> UserContext:

    c = state.constraints

    user_id = state.user_id or "anonymous"
    area = str(_safe_get(c, "area", "region", default="") or "")
    date = str(_safe_get(c, "date", default="2026-01-11") or "2026-01-11")
    start_time = str(_safe_get(c, "startTime", "start_time", default="18:00") or "18:00")
    budget = str(_safe_get(c, "budgetRange", "budget_range", default="MID") or "MID")
    trans =str(_safe_get(c, "transportation", default="WALK") or "WALK")
    mood = list(_safe_get(c, "mood", default=[]) or [])

    return UserContext(
        userId=user_id,
        area=area,
        date=date,
        startTime=start_time,
        budgetRange=budget,
        transportation=trans,
        mood=mood,
    )

def _pick_best(cands: List[PlaceCandidate]) -> Optional[PlaceCandidate]:
    if not cands:
        return None
    return max(cands, key=lambda x: float(x.score.total or 0.0))

@traced_node(
    "rank_and_select",
    options=TraceOptions(error_code="SCORE_FAILED", swallow_exceptions=True, emit_done_event=True),
)
def n6_rank_and_select(state: AgentState, score_client: ScoreClient) -> Dict[str, Any]:
    user_ctx = _to_user_context(state)
    now_iso = now_utc().replace(tzinfo=None).isoformat(timespec="seconds")
    options = ScoreOptions(window="H24", returnBreakdown=True, topK=1)

    selected_by_step: Dict[str, PlaceCandidate] = {}

    for step in (state.plan.steps or []):
        step_id = step.step_id
        cands = list(state.candidates_by_step.get(step_id) or [])

        if not cands:
            continue

        id_to_cand: Dict[int, PlaceCandidate] = {}
        places: List[ScorePlaceInput] = []
        for cand in cands:
            pid_long = stable_long_place_id(cand.place_id)
            id_to_cand[pid_long] = cand
            places.append(ScorePlaceInput(placeId=pid_long))

        req = InternalScoreRequest(
            userContext=user_ctx,
            timeContext=TimeContext(now=now_iso),
            places=places,
            options=options,
        )

        resp = score_client.score(req)
        print(resp)

        for sp in (resp.scoredPlaces or []):
            cand = id_to_cand.get(sp.placeId)
            if not cand:
                continue
            cand.score = CandidateScore(
                total=float(sp.totalScore),
                breakdown=dict(sp.breakdown or {}),
            )

        best = _pick_best(cands)
        if best:
            selected_by_step[step_id] = best

    return {
        "selected_course": SelectedCourse(
            selected_by_step=selected_by_step,
            route_summary=None,
        )
    }
