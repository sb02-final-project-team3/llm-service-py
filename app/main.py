import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings, get_settings
from app.routers.extract import router as extract_router

logging.basicConfig(
    level=logging.DEBUG,  # DEBUG 레벨부터 출력
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("llm-service")

settings: Settings = get_settings()

app = FastAPI(title="LLM Service (Python)", version="0.1.0")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error at {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LangSmith tracing
if settings.langsmith_tracing:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    if settings.langsmith_api_key:
        os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
    if settings.langsmith_project:
        os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project

@app.get("/health")
def health():
    logger.info("Health check requested")
    return {
        "status": "ok",
        "provider": settings.provider,
        "model": settings.model_name,
        "temperature": settings.temperature,
        "version": "0.1.0",
    }

app.include_router(extract_router, prefix="/v1")

logger.info("LLM Service initialized")
