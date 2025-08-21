import os
from typing import Optional
from langchain_core.language_models import BaseChatModel

def _need(pkg: str, hint: str):
    try:
        return __import__(pkg, fromlist=["*"])
    except ImportError as e:
        raise ImportError(f"Optional provider not installed: {pkg}. {hint}") from e

def make_llm(provider: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: Optional[float] = None) -> BaseChatModel:
    p = (provider or os.getenv("PROVIDER", "openai")).lower()
    model = model_name or os.getenv("MODEL_NAME", "gpt-4o-mini")
    temp = float(os.getenv("TEMPERATURE", "0.2")) if temperature is None else temperature

    if p == "openai":
        from langchain_openai import ChatOpenAI   # 설치됨
        return ChatOpenAI(model=model, temperature=temp)

    if p == "gemini":
        mod = _need("langchain_google_genai",
                    "pip install langchain-google-genai && set GOOGLE_API_KEY")
        return mod.ChatGoogleGenerativeAI(model=model, temperature=temp)

    if p == "anthropic":
        mod = _need("langchain_anthropic",
                    "pip install langchain-anthropic && set ANTHROPIC_API_KEY")
        return mod.ChatAnthropic(model=model, temperature=temp)

    if p == "perplexity":
        mod = _need("langchain_community.chat_models",
                    "pip install langchain-community && set PERPLEXITY_API_KEY")
        return mod.ChatPerplexity(model=model, temperature=temp)

    raise ValueError(f"Unsupported PROVIDER: {p}")

def provider_supports_images(provider: Optional[str] = None) -> bool:
    p = (provider or os.getenv("PROVIDER", "openai")).lower()
    return p in {"openai", "gemini"}