from __future__ import annotations
from typing import Any, Dict
from .graph import run_agent
from .model import RecommendLlmRequest
from .ports import LlmClient
from .state import AgentState

def agent_call(llm_request: RecommendLlmRequest, llm: LlmClient) -> Dict[str, Any]:
    try:
        state: AgentState = run_agent(
            job_id=llm_request.jobId,
            user_query=llm_request.query,
            llm=llm
        )

        message = (state.response.final or "").strip()
        errors = [e.model_dump() for e in state.trace.errors]

        ok = bool(message) and len(errors) == 0
        if not message:
            message = "요청을 처리했지만 응답을 생성하지 못했어. 조건을 조금 더 자세히 알려줘."

        return {
            "jobId": state.job_id,
            "ok": ok,
            "message": message,
            "errors": errors,
            "trace": [h.model_dump() for h in state.trace.node_history],
            "progress": [ev.model_dump() for ev in state.progress_event],
        }

    except Exception as e:
        return {
            "jobId": llm_request.jobId,
            "ok": False,
            "message": "현재 요청이 많거나 시스템 오류가 발생했어. 잠시 후 다시 시도해줘.",
            "errors": [
                {
                    "code": "AGENT_CALL_FAILED",
                    "message": str(e),
                    "node": None,
                }
            ],
            "trace": [],
            "progress": [],
        }

