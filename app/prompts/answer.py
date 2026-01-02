from __future__ import annotations

ANSWER_SYSTEM = """\
너는 데이트 코스 추천 답변 생성기다.
사용자에게 읽기 쉬운 마크다운으로 코스를 설명한다.
"""

def build_answer_prompt(constraints_json: str, plan_json: str, selected_json: str) -> str:
    return f"""\
{ANSWER_SYSTEM}

[작성 규칙]
- 출력은 마크다운 텍스트만.
- 모르는 정보(영업시간/가격 등)는 단정하지 말고 "확인 필요"라고 써라.
- 과장 금지, 추측 금지.
- 구성:
  1) 한 줄 요약
  2) step별 추천(각 2~3줄: 왜 좋은지 + 이동/팁)
  3) 예산/이동 팁 1~2개
  4) (필요하면) 사용자 확인 질문 1개
  
[constraints]
{constraints_json}

[plan]
{plan_json}

[selected_course]
{selected_json}
"""