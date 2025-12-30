from __future__ import annotations

import os
from google import genai

_client = None

def get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client()
    return _client

def generate_text(prompt: str) -> str:
    client = get_client()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    resp = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return resp.text or ""