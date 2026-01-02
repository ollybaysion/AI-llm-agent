from __future__ import annotations

from .common import JSON_ONLY_RULES

PARSE_SCHEMA = {
    "intent": "GENERATE|FETCH_SAVED|MODIFY|ALTERNATIVE|UNKNOWN",
    "constraints": {
        "region": {"city": None, "district": None, "near": None},
        "date": None,
        "time_window": {"start": None, "end": None},
        "budget_krw": {"min": None, "max": None},
        "party": {"type": None, "size": None},
        "transport": None,
        "pace": None,
        "preferences": {"likes": [], "dislikeds": [], "must": [], "avoid": []},
        "constraints_freeform": None,
    },
    "missing_slots": [],
}

PARSE_SYSTEM = """\
너는 '데이트 코스 추천' 시스템의 입력 파서다.
사용자 입력을 구조화해 constraints와 intent를 추출한다.
"""

def build_parse_prompt(user_query_raw: str) -> str:
    return f"""\
{PARSE_SYSTEM}

{JSON_ONLY_RULES}

[입력]
{user_query_raw}

[출력 JSON 스키마]
{PARSE_SCHEMA}
"""
