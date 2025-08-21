from typing import Any, Dict
import json

def safe_json_parse(text: str) -> Dict[str, Any]:
    # 모델이 코드블록을 붙이는 흔한 케이스 보정
    cleaned = text.strip().strip('`')
    if cleaned.startswith('json'):
        cleaned = cleaned[4:].strip()
    try:
        return json.loads(cleaned)
    except Exception as e:
        # 마지막 보호: 중괄호 앞뒤 잡스러운 텍스트 제거 시도
        first = cleaned.find('{')
        last = cleaned.rfind('}')
        if first != -1 and last != -1:
            return json.loads(cleaned[first:last+1])
        raise e