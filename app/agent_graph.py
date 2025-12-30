from __future__ import annotations

from typing import Any, Dict, TypedDict
from langgraph.graph import StateGraph, END

from app.llm_gemini_sdk import generate_text

class AgentState(TypedDict, total=False):
    request: Dict[str, Any]
    answer: Dict[str, Any]


def build_graph():
    g = StateGraph(AgentState)

    def plan(state: AgentState) -> AgentState:
        return state

    def respond(state: AgentState) -> AgentState:
        req = state.get("request", {})
        query = req.get("query", "")

        attrs = req.get("attributes") or {}
        prompt = (
            "너는 데이트 코스 추천 도우미야. \n"
            f"사용자 요청: {query}\n"
            f"추가 조건(attributes): {attrs}\n"
            "짧고 실용적으로 추천해줘."
        )

        text = generate_text(prompt)
        state["answer"] = {"text": text}
        return state

    g.add_node("plan", plan)
    g.add_node("respond", respond)

    g.set_entry_point("plan")
    g.add_edge("plan", "respond")
    g.add_edge("respond", END)

    return g.compile()

GRAPH = build_graph()

def run_agent(request_dict: Dict[str, Any]) -> Dict[str, Any]:
    out = GRAPH.invoke({"request": request_dict})
    return out.get("answer", {})
