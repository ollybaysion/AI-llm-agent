from typing import Any, Dict

def agent_call(llm_request: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: LangGraph/LLM 호출 자리
    payload = llm_request.get("payload")
    return {"text": f"echo: {payload}"}

