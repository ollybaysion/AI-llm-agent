from __future__ import annotations

from typing import Any, Dict, List
import hashlib

from pydantic import ValidationError
from google.genai import types

from ..state.agent_state import AgentState
from ..state.plan import Step
from ..state.places import PlaceCandidate, PlaceLocation, Score
from ..prompts.retrieve import build_candidate_prompt
from ..utils import traced_node, TraceOptions
from ..ports import LlmClient
from ..ports.llm import LlmCallOptions

def _stable_place_id(*, name: str, address: str | None, lat: float | None, lng: float | None) -> str:
    base = f"maps|{name.strip()}|{(address or '').strip()}|{lat or ''}|{lng or ''}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()

def _normalize_candidate_dict(item: Dict[str, Any]) -> Dict[str, Any]:
    loc = item.get("location") or {}
    score = item.get("score") or {}

    item["location"] = {
        "lat": loc.get("lat"),
        "lng": loc.get("lng"),
        "address": loc.get("address"),
    }

    item["score"] = {
        "total": float(score.get("total") or 0.0),
        "breakdown": dict(score.get("breakdown") or {}),
    }

    item["source"] = "maps"

    item["place_id"] = str(item.get("place_id") or "")

    item["tags"] = list(item.get("tags") or [])

    item.setdefault("price_level", None)
    item.setdefault("open_hours", None)
    item.setdefault("notes", None)

    item["name"] = str(item.get("name") or "").strip()
    item["category"] = str(item.get("category") or "").strip()

    return item


def _to_place_candidate(item: Dict[str, Any]) -> PlaceCandidate:
    loc = item["location"]
    score = item["score"]

    return PlaceCandidate(
        place_id=item["place_id"],
        name=item["name"],
        category=item["category"] or "other",
        location=PlaceLocation(lat=loc.get("lat"), lng=loc.get("lng"), address=loc.get("address")),
        price_level=item.get("price_level"),
        open_hours=item.get("open_hours"),
        tags=item.get("tags") or [],
        source="maps",
        score=Score(total=score.get("total", 0.0), breakdown=score.get("breakdown", {})),
        notes=item.get("notes"),
    )

def _dedup(cands: List[PlaceCandidate]) -> List[PlaceCandidate]:
    seen = set()
    out: List[PlaceCandidate] = []
    for c in cands:
        key = (c.name.lower(), (c.location.address or "").lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


def _enrich_tags_from_step(step: Step, cands: List[PlaceCandidate]) -> None:
    must = step.requirements.must_have
    if not must:
        return
    for c in cands:
        for t in must:
            if t and t not in c.tags:
                c.tags.append(t)


@traced_node(
    "retrieve_candidates",
    options=TraceOptions(error_code="CANDIDATES_FAILED", swallow_exceptions=True, emit_done_event=True),
)
def n5_retrieve_candidates(state: AgentState, llm: LlmClient) -> Dict[str, Any]:
    maps_options = LlmCallOptions(
        tools=[types.Tool(google_maps=types.GoogleMaps(enable_widget=True))]
    )

    constraints_json = state.constraints.model_dump_json(ensure_ascii=False)
    k = 10

    candidate_by_step: Dict[str, List[PlaceCandidate]] = {}

    for step in (state.plan.steps or []):
        step_json = step.model_dump_json(ensure_ascii=False)
        prompt = build_candidate_prompt(constraints_json, step_json, k=k)

        out = llm.generate_json(prompt, options=maps_options)
        raw_list = (out or {}).get("candidates") or []

        cands: List[PlaceCandidate] = []
        try:
            for item in raw_list:
                if not isinstance(item, dict):
                    continue
                item = _normalize_candidate_dict(item)
                if not item["name"]:
                    continue

                cand = _to_place_candidate(item)

                cand.place_id = _stable_place_id(
                    name=cand.name,
                    address=cand.location.address,
                    lat=cand.location.lat,
                    lng=cand.location.lng,
                )

                cands.append(cand)

        except ValidationError:
            cands = []

        cands = _dedup(cands)
        _enrich_tags_from_step(step, cands)
        candidate_by_step[step.step_id] = cands[:k]

        print(step)
        print(len(cands))
        print(cands[0])

    for step in (state.plan.steps or []):
        candidate_by_step.setdefault(step.step_id, [])

    return {"candidates_by_step": candidate_by_step}
