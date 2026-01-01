from __future__ import annotations

from typing import Any, Dict, Protocol

class LlmClient(Protocol):
    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """Return a JSON object (dict). Raises on fatal errors."""
        ...

    def generate_text(self, prompt: str) -> str:
        """Return plain text."""
        ...