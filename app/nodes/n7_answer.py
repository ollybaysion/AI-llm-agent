from __future__ import annotations

from typing import Any, Dict

from ..state.agent_state import AgentState
from ..prompts import build_answer_prompt
from ..utils import traced_node, TraceOptions
from ..ports import LlmClient

@traced_node(
    "compose_answer",
    options=TraceOptions(error_code="ANSWER_FAILED", swallow_exceptions=False, emit_done_event=True),
)
def n7_compose_answer(state: AgentState, llm:LlmClient) -> Dict[str, Any]:
    """
    Returns patch:
      - response.final
    """
    prompt = build_answer_prompt(
        state.constraints.model_dump_json(ensure_ascii=False),
        state.plan.model_dump_json(ensure_ascii=False),
        state.selected_course.model_dump_json(ensure_ascii=False),
    )
    text = llm.generate_text(prompt)

    return {"response": {"format": "markdown", "final": text}}
