# app/routers/extract.py
from fastapi import APIRouter, HTTPException, Header
from app.models.schemas import VisionRequest, VisionOut
from app.chains.extractor import run_vision

router = APIRouter()

@router.post("/vision/analyze", response_model=VisionOut)
async def analyze_vision(req: VisionRequest,
    x_model_name: str | None = Header(default=None),
    x_provider: str | None = Header(default=None)):
    try:
        # provider 전환은 providers.py에서 ENV로 처리하되, 헤더로도 허용하려면 os.environ 갱신 로직 추가 가능
        result = await run_vision(req.model_dump(), model_override=x_model_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM_CALL_FAILED: {e}")
