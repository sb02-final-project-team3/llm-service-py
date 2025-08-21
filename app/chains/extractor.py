from typing import Dict, Any
import json
from langchain_core.runnables import Runnable
from .providers import make_llm, provider_supports_images
from .prompts import vision_prompt
from app.models.schemas import VisionOut

TYPE_ENUM = "TOP|BOTTOM|OUTER|DRESS|SHOES|ACCESSORY|ETC"

def build_vision_chain(model_override: str | None = None) -> Runnable:
    llm = make_llm(model_name=model_override)
    # Pydantic 구조화 출력 (LangChain이 JSON 파싱/검증)
    structured_llm = llm.with_structured_output(VisionOut)
    return vision_prompt | structured_llm

async def run_vision(payload: Dict[str, Any], model_override: str | None = None) -> Dict[str, Any]:
    options = payload.get("optionsByDef") or {}
    def_list = ", ".join(payload.get("definitionNames", [])[:50]) or ", ".join(options.keys()) or "색상, 사이즈, 재질, 핏, 길이"
    options_json = json.dumps(options, ensure_ascii=False)
    schema_hint = '{"name":"string|null","type":"string|null","attributes":[{"definitionName":"string","value":"string|null"}]}'

    inputs = {
        "schema_hint": schema_hint,
        "type_enum": TYPE_ENUM,
        "def_list": def_list,
        "options_json": options_json,
        "locale": payload.get("locale", "ko-KR"),
        "title": payload.get("title") or "",
        "description": payload.get("description") or "",
        "image_url": payload.get("imageUrl") or "",
    }

    chain = build_vision_chain(model_override=model_override)
    # (멀티모달) 모델이 이미지를 직접 받을 수 있다면 메시지에 이미지 첨부 (OpenAI/Gemini 일부 모델)
    # 여기선 프롬프트에 imageUrl을 텍스트로 제공하고, 추후 provider별 확장을 providers.py에서 처리

    result: VisionOut = await chain.ainvoke(inputs)
    return result.model_dump()