from __future__ import annotations

from langgraph.graph import StateGraph, END

from ..state.agent_state import AgentState
from ..nodes import (
    n1_parse_intent_and_constraints,
    n4_make_plan_steps,
    n5_retrieve_candidates,
    n6_rank_and_select,
    n7_compose_answer,
)
from ..graph.routes import route_after_parse
from ..ports.llm import LlmClient
from ..adapters.out import InternalScoreHttpClient

def build_graph(llm: LlmClient):
    g = StateGraph(AgentState)

    score_client = InternalScoreHttpClient()

    g.add_node(
        "parse_intent_and_constraints",
        lambda state: n1_parse_intent_and_constraints(state, llm),
    )
    g.add_node(
        "make_plan_steps",
        lambda state: n4_make_plan_steps(state, llm),
    )
    g.add_node(
        "retrieve_candidates",
        lambda state: n5_retrieve_candidates(state, llm),
    )
    g.add_node(
        "rank_and_select",
        lambda state: n6_rank_and_select(state, score_client),
    )
    g.add_node(
        "compose_answer",
        lambda state: n7_compose_answer(state, llm),
    )

    g.set_entry_point("parse_intent_and_constraints")

    g.add_conditional_edges(
        "parse_intent_and_constraints",
        route_after_parse,
        {
            "make_plan_steps": "make_plan_steps",
        },
    )

    g.add_edge("make_plan_steps", "retrieve_candidates")
    g.add_edge("retrieve_candidates", "rank_and_select")
    g.add_edge("rank_and_select", "compose_answer")
    g.add_edge("compose_answer", END)

    return g.compile()