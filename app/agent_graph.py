from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, TypedDict

from langgraph.graph import StateGraph, END

class AgentState(TypedDict, total=False):
    request: Dict[str, Any]
    answer: Dict[str, Any]


def build_graph():
    g = StateGraph(AgentState)

    def plan(state: AgentState) -> AgentState:
        return state

    def respond(state: AgentState) -> AgentState:
        req = state.get("request", {})
        query = req.get("query") or req.get("payload", {}).get("query") or ""
        state["answer"] = {"text": f"[echo] {query}"}
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
