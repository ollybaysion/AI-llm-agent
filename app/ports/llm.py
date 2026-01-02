from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol, List

@dataclass(frozen=True)
class LlmCallOptions:
    tools: Optional[List[Any]] = None

    response_mime_type: Optional[str] = None

    response_schema: Optional[Any] = None


class LlmClient(Protocol):
    def generate_json(self, prompt: str, *, options: Optional[LlmCallOptions] = None) -> Dict[str, Any]:
        """Return a JSON object (dict). Raises on fatal errors."""
        ...

    def generate_text(self, prompt: str, *, options: Optional[LlmCallOptions] = None) -> str:
        """Return plain text."""
        ...