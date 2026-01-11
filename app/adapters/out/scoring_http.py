from __future__ import annotations

import os
from typing import Optional

import httpx

from ...dto.scoring import InternalScoreResponse, InternalScoreRequest
from ...ports.scoring import ScoreClient

class InternalScoreHttpClient(ScoreClient):
    def __init__(
            self,
            base_url: Optional[str] = None,
            timeout_s: float = 3.0,
    ):
        self.base_url = (base_url or os.getenv("INTERNAL_API_BASE_URL", "http://localhost:8080")).rstrip("/")
        self.timeout_s = timeout_s

        def score(self, req: InternalScoreRequest) -> InternalScoreResponse:
            url = f"{self.base_url}/internal/score"
            with httpx.Client(timeout=self.timeout_s) as client:
                r = client.post(url, json=req.model_dump())
                r.raise_for_status()
                return InternalScoreResponse.model_validate(r.json())

