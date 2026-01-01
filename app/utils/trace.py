from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from ..state.agent_state import AgentState
from ..state.trace import NodeHistory, ErrorItem, ProgressEvent

def trace_node_start(state: AgentState, node: str, detail: Optional[Dict[str, Any]] = None) -> None:
    state.trace.node_histoy.append(
        NodeHistory(
            node=node,
            started_at=datetime.utcnow(),
            ended_at=None,
            status="OK",
            detail=detail,
        )
    )

def trace_node_end_ok(state: AgentState, node: str, detail: Optional[Dict[str, Any]] = None) -> None:
    entry = _find_last_open_entry(state, node)
    if entry is None:
        state.trace.node_history.append(
            NodeHistory(
                node=node,
                started_at=datetime.utcnow(),
                ended_at=datetime.utcnow(),
                status="OK",
                detail=detail or {"warning": "end_ok_without_start"},
            )
        )
        return

    entry.ended_at = datetime.utcnow()
    entry.status = "OK"
    if detail is not None:
        entry.detail = detail


def trace_node_end_error(
        state: AgentState,
        node: str,
        code: str,
        message: str,
        detail: Optional[Dict[str, Any]] = None,
) -> None:
    state.trace.errors.append(ErrorItem(code=code, message=message, node=node))

    entry = _find_last_open_entry(state, node)
    if entry is None:
        state.trace.node_history.append(
            NodeHistory(
                node=node,
                started_at=datetime.utcnow(),
                ended_at=datetime.utcnow(),
                status="ERROR",
                detail=detail or {"code": code, "message": message, "warning": "end_error_without_start"},
            )
        )
        return

    entry.ended_at = datetime.utcnow()
    entry.status = "ERROR"
    entry.detail = detail or {"code": code, "message": message}


def trace_event(state: AgentState, event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
    state.progress_events.append(
        ProgressEvent(
            ts=datetime.utcnow(),
            type=event_type,
            payload=payload or {},
        )
    )

def trace_node_done_event(
        state: AgentState,
        node: str,
        summary: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
) -> None:
    p = {"node": node}
    if summary:
        p["summary"] = summary
    if payload:
        p.update(payload)
    trace_event(state, "NODE_DONE", p)

def trace_final_event(state: AgentState, payload: Optional[Dict[str, Any]] = None) -> None:
    trace_event(state, "FINAL", payload or {})

def _find_last_open_entry(state: AgentState, node: str) -> Optional[NodeHistory]:
    for entry in reversed(state.trace.node_history):
        if entry.node == node and entry.ended_at is None:
            return entry
    return None
