from __future__ import annotations

import json
from .common import JSON_ONLY_RULES

CANDIDATE_SCHEMA = {
    "candidates": [
        {
            "place_id": "string (can be empty, will be overwritten)",
            "name": "string",
            "category": "string",
            "location": {"lat": None, "lng": None, "address": None},
            "price_level": None,
            "open_hours": None,
            "tags": [],
            "source": "maps",
            "score": {"total": 0.0, "breakdown": {}},
            "notes": None,
        }
    ]
}

CANDIDATES_SYSTEM = """\
너는 '데이트 코스 장소 후보 수집기'다.
주어진 step 요구사항에 맞는 실제 장소 후보를 수집한다.
수집을 위해 사용할 수 있는 도구 목록은 다음과 같다.
1. Google Maps
"""

def build_candidate_prompt(constraint_json: str, step_json: str, k: int = 10) -> str:
    return f"""\
{CANDIDATES_SYSTEM}

{JSON_ONLY_RULES}

[제약조건 constraints JSON]
{constraint_json}

[현재 step JSON]
{step_json}

[규칙]
- Google Maps를 활용해 실제 존재하는 장소를 찾는다.
- 후보는 {k}개 내외.
- 이번 버전에서는 "브레이크타입/예약" 정보는 수집하지 않는다.
- 불확실하거나 당장 얻기 어려운 정보(open_hours, price_level, lat/lng 등)는 null로 둬도 된다.
- source는 무조건 "maps".
- place_id는 빈 문자열로 둬도 된다(서버에서 생성/치환한다).
- tags는 step의 requirements.must_have를 참고해서 적당히 넣되, 모르면 []로.
- 설명을 길게 쓰지 말고 JSON만 출력.

[출력 JSON 스키마]
{CANDIDATE_SCHEMA}
"""