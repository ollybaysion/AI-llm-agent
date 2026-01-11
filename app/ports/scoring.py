from __future__ import annotations

from typing import Protocol

from ..dto.scoring import InternalScoreRequest, InternalScoreResponse

class ScoreClient(Protocol):
    def score(self, req: InternalScoreRequest) -> InternalScoreResponse:
        ...