from __future__ import annotations
from typing import Any, Dict
from .graph import run_agent
from .model import RecommendLlmRequest
from .ports import LlmClient

def agent_call(llm_request: RecommendLlmRequest, llm: LlmClient) -> Dict[str, Any]:
    state = run_agent(
        job_id=llm_request.jobId,
        user_query=llm_request.query,
        llm=llm
    )
    return state.model_dump()

