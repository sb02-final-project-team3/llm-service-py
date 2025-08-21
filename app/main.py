import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings, get_settings
from app.routers.extract import router as extract_router

settings: Settings = get_settings()

app = FastAPI(title="LLM Service (Python)", version="0.1.0")

# CORS (필요 시 조정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LangSmith tracing (옵션)
if settings.langsmith_tracing:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    if settings.langsmith_api_key:
        os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
    if settings.langsmith_project:
        os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project

@app.get("/health")
def health():
    return {
        "status": "ok",
        "provider": settings.provider,
        "model": settings.model_name,
        "temperature": settings.temperature,
        "version": "0.1.0",
    }

app.include_router(extract_router, prefix="/v1")