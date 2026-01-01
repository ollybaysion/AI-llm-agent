from __future__ import annotations

from typing import Optional

from ..state.agent_state import AgentState
from ..graph.graph import build_graph
from ..ports.llm import LlmClient

def run_agent(
        *,
        job_id: str,
        user_query: str,
        llm: LlmClient,
        user_id: Optional[str] = None,
) -> AgentState:
    graph = build_graph(llm)

    init_state = AgentState(
        job_id=job_id,
        user_id=user_id,
        user_query_raw=user_query,
    )

    final_state: AgentState = graph.invoke(init_state)
    return final_state