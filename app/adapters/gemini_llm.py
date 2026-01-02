from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google import genai
from google.genai import types

from ..ports.llm import LlmClient, LlmCallOptions

class LlmError(RuntimeError):
    pass

class LlmJsonError(LlmError):
    pass

def _strip_code_fences(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        t = t.replace("```json", "").replace("```JSON", "").replace("```", "").strip()
    return t

def _extract_first_json_object(text: str) -> Dict[str, Any]:
    """
    Best-effort JSON object extractor:
    - removes code fences
    - slices from first '{' to last '}'
    """
    t = _strip_code_fences(text)

    l = t.find("{")
    r = t.rfind("}")
    if l == -1 or r == -1 or r <= l:
        raise LlmJsonError(f"Could not locate JSON object. head={t[:200]!r}")

    payload = t[l : r + 1]
    try:
        return json.loads(payload)
    except json.JSONDecodeError as e:
        raise LlmJsonError(f"JSON decode failed: {e}. head={payload[:200]!r}") from e

@dataclass(frozen=True)
class GeminiConfig:
    api_key: Optional[str] = None
    model: str = "gemini-2.0-flash"
    temperature: float = 0.2
    max_output_tokens: int = 2048

    max_retries: int = 2
    retry_backoff_sec: float = 1.0

class GeminiLlmClient(LlmClient):
    """
    google-genai 기반 LLM 어댑터.
    - generate_text: 일반 텍스트
    - generate_json: response_mime_type='application/json' + robust parse
    """

    def __init__(self, cfg: GeminiConfig):
        self.cfg = cfg

        if cfg.api_key:
            self.client = genai.Client(api_key=cfg.api_key)
        else:
            self.client = genai.Client()

    def generate_text(self, prompt: str, *, options: Optional[LlmCallOptions] = None) -> str:
        resp = self._call_generate_content(
            prompt=prompt,
            options=options,
            default_response_mime_type=None,
            default_response_schema=None,
        )
        return (resp.text or "").strip()

    def generate_json(self, prompt: str, *, options: Optional[LlmCallOptions] = None) -> Dict[str, Any]:
        resp = self._call_generate_content(
            prompt=prompt,
            options=options,
            default_response_mime_type="application/json",
            default_response_schema=None,
        )
        raw = (resp.text or "").strip()

        try:
            obj = json.loads(_strip_code_fences(raw))
            if not isinstance(obj, dict):
                raise LlmJsonError(f"Expected JSON object, got {type(obj)}")
            return obj
        except Exception:
            obj = _extract_first_json_object(raw)
            if not isinstance(obj, dict):
                raise LlmJsonError(f"Expected JSON object, got {type(obj)}")
            return obj

    def _call_generate_content(
            self,
            *,
            prompt: str,
            options: Optional[LlmCallOptions],
            default_response_mime_type: Optional[str],
            default_response_schema: Optional[Dict[str, Any]],
    ):
        last_err: Optional[Exception] = None

        for attempt in range(self.cfg.max_retries + 1):
            try:
                cfg = types.GenerateContentConfig(
                    temperature=self.cfg.temperature,
                    max_output_tokens=self.cfg.max_output_tokens,
                )

                response_mime_type = options.response_mime_type if options and options.response_mime_type is not None else default_response_mime_type
                response_schema = options.response_schema if options and options.response_schema is not None else default_response_schema

                if response_mime_type:
                    cfg.response_mime_type = response_mime_type
                if response_schema:
                    cfg.response_schema = response_schema

                if options and options.tools:
                    cfg.tools = options.tools

                return self.client.models.generate_content(
                    model=self.cfg.model,
                    contents=prompt,
                    config=cfg,
                )

            except Exception as e:
                last_err = e
                if attempt >= self.cfg.max_retries:
                    break
                time.sleep(self.cfg.retry_backoff_sec * (attempt + 1))

        raise LlmError(f"Gemini call failed after retries: {last_err}")