from __future__ import annotations

from .common import JSON_ONLY_RULES

PLAN_SCHEMA = {
    "strategy": "4STEP_DEFAULT|DINNER_ONLY|CAFE_WALK|CUSTOM",
    "steps": [
        {
            "step_id": "string",
            "label": "string",
            "category": "meal|cafe|walk|activity|bar|view|other",
            "time_hint": {"start": None, "end": None},
            "requirements": {"must_have": [], "avoid": []},
            "budget_hint_krw": {"min": None, "max": None},
        }
    ],
}

PLAN_SYSTEM = """\
너는 '데이트 코스 플래너'다.
제약조건에 맞는 코스 단계(steps)를 설계한다.
"""

def build_plan_prompt(constraints_json: str) -> str:
    return f"""\
{PLAN_SYSTEM}

{JSON_ONLY_RULES}

[제약조건 constraints JSON]
{constraints_json}

[규칙]
- 시간이 짧으면 steps를 2~3개로 줄여라.
- 일반적인 데이트는 3~4개 steps(식사/카페/산책/저녁 등)로 구성.
- step_id는 중복 금지.
- must/avoid를 requirements에 반영.
- 확신 없는 시간/예산은 null로.

[출력 JSON 스키마]
{PLAN_SCHEMA}
"""