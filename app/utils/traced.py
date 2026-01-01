from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Protocol, TypeVar, cast

from .trace import (
    trace_node_start,
    trace_node_end_ok,
    trace_node_end_error,
    trace_node_done_event,
)

class HasTrace(Protocol):
    trace: Any
    progress_event: Any

TState = TypeVar("TState", bound=HasTrace)
NodeFn = Callable[[TState], Dict[str, Any]]

@dataclass(frozen=True)
class TraceOptions:
    emit_done_event: bool = True
    swallow_exceptions: bool = True
    error_code: str = "NODE_FAILED"

def traced_node(
        node_name: str,
        *,
        options: TraceOptions = TraceOptions(),
        start_detail: Optional[Dict[str, Any]] = None,
        done_summary: Optional[str] = None,
) -> Callable[[NodeFn[TState]], NodeFn[TState]]:
    def decorator(fn: NodeFn[TState]) -> NodeFn[TState]:
        def wrapper(state: TState, *args: Any, **kwargs: Any) -> Dict[str, Any]:
            trace_node_start(state, node_name, detail=start_detail)
            try:
                patch = fn(state, *args, **kwargs)
                if patch is None:
                    patch = {}
                if not isinstance(patch, dict):
                    raise TypeError(f"Node must return dict patch, got: {type(patch)}")

                trace_node_end_ok(state, node_name, detail={"patch_keys": list(patch.keys())})
                if options.emit_done_event:
                    trace_node_done_event(
                        state,
                        node_name,
                        summary=done_summary or f"{node_name} done",
                        payload={"patch_keys": list(patch.keys())},
                    )
                return patch

            except Exception as e:
                trace_node_end_error(
                    state,
                    node_name,
                    options.error_code,
                    message=str(e),
                    detail={"exception": type(e).__name__},
                )
                if options.emit_done_event:
                    trace_node_done_event(
                        state,
                        node_name,
                        summary=f"{node_name} failed",
                        payload={"error": options.error_code, "message": str(e)},
                    )

                if options.swallow_exceptions:
                    return {}
                raise

        return cast(NodeFn, wrapper)
    return decorator

