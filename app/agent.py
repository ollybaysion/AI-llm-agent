from __future__ import annotations
from typing import Any, Dict
from app.agent_graph import run_agent

def agent_call(llm_request: Dict[str, Any]) -> Dict[str, Any]:
    return run_agent(llm_request)

