from __future__ import annotations

from typing import Any, Dict

from pydantic import ValidationError

from ..state.agent_state import AgentState
from ..state.plan import Plan, Step
from ..prompts import build_plan_prompt
from ..utils import traced_node, TraceOptions
from ..ports import LlmClient

@traced_node(
    "make_plan_steps",
    options=TraceOptions(error_code="PLAN_FAILED", swallow_exceptions=True, emit_done_event=True),
)
def n4_make_plan_steps(state: AgentState, llm: LlmClient) -> Dict[str, Any]:
    """
    Returns patch:
      - plan
    """

    constraints_json = state.constraints.model_dump_json(ensure_ascii=False)
    prompt = build_plan_prompt(constraints_json)
    out = llm.generate_json(prompt)

    try:
        plan = Plan(strategy=out.get("strategy"), steps=[Step(**s) for s in (out.get("steps") or [])])
    except ValidationError:
        return {"plan": Plan(strategy="CUSTOM", steps=[])}

    ids = [s.step_id for s in plan.steps]
    if len(ids) != len(set(ids)):
        seen = set()
        dedup_steps = []
        for step in plan.steps:
            if step.step_id in seen:
                continue
            seen.add(step.step_id)
            dedup_steps.append(step)
        plan.steps = dedup_steps

    return {"plan": plan}
