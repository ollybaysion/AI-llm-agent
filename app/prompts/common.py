from __future__ import annotations

import json
from typing import Any, Dict

JSON_ONLY_RULES = """\
[출력 규칙]
- 출력은 반드시 JSON만. 코드블록(````), 설명, 여분 텍스트 절대 금지.
- 모든 키는 스키마에 맞춰 포함. 값이 없으면 null 또는 [].
- 확실하지 않으면 추측하지 말고 null.
- 문자열은 한국어로(단, enum 값은 스키마 그대로).
"""

def json_dumps_ko(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))