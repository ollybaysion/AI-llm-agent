from __future__ import annotations

from typing import Any, Dict

from pydantic import ValidationError

from ..state.agent_state import AgentState
from ..state.common import Intent
from ..state.constraints import Constraints
from ..prompts import build_parse_prompt
from ..utils import traced_node, TraceOptions
from ..ports import LlmClient

@traced_node(
    "parse_intent_and_constraints",
    options=TraceOptions(error_code="PARSE_FAILED", swallow_exceptions=True, emit_done_event=True),
)
def n1_parse_intent_and_constraints(state: AgentState, llm: LlmClient) -> Dict[str, Any]:
    """
    Returns patch:
      - intent
      - constraints
      - missing_slots
    """
    prompt = build_parse_prompt(state.user_query_raw)
    out = llm.generate_json(prompt)

    intent_raw = out.get("intent", "UNKNOWN")
    intent: Intent = intent_raw if intent_raw in ("GENERATE", "FETCH_SAVED", "MODIFY", "ALTERNATIVE", "UNKNOWN") else "UNKNOWN"

    try:
        constraints = Constraints(**(out.get("constraints") or {}))
    except ValidationError as e:
        constraints = Constraints()
        missing_slots = list(set((out.get("missing_slots") or []) + ["constraints"]))
        return {"intent": intent, "constraints": constraints, "missing_slots": missing_slots}

    missing_slots = out.get("missing_slots") or []

    return {
        "intent": intent,
        "constraints": constraints,
        "missing_slots": missing_slots,
    }
