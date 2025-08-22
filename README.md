# LLM Service (Python) — FastAPI + LangChain + LangSmith

목적: Spring Boot에서 HTTP로 호출하는 **LLM 전용 파이썬 마이크로서비스**의 최소 뼈대.
- 프레임워크: FastAPI
- LLM: LangChain (OpenAI 기본, 다른 공급자로 확장 가능)
- 관측성: LangSmith(선택)

## 1) 로컬 실행

1) 가상환경 & 설치
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2) 환경변수(.env) 작성
   - `.env.example` 복사하여 `.env` 생성, 키 채우기

3) 실행
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
   ```

4) 테스트
   ```bash
   curl -X POST http://localhost:8000/v1/extract/clothing          -H "Content-Type: application/json"          -d '{"url":"https://example.com/item/123","rawHtml":null,"optionsByDef":{"색상":["블루","블랙"]},"locale":"ko-KR"}'
   ```

5) 모델 스위칭(AB 테스트)
   ```bash
   curl -X POST http://localhost:8000/v1/extract/clothing          -H "Content-Type: application/json"          -H "X-Model-Name: gpt-4o-mini"          -d '{"url":"https://example.com/item/123"}'
   ```

## 2) Docker 빌드 & 실행
```bash
docker build -t llm-service-py:local .
docker run --rm -p 8000:8000 --env-file .env llm-service-py:local
```



## 3) Spring 연동 요약
- `POST http://llm-service-internal:8000/v1/extract/clothing` 호출
- DTO는 README 상단 설명과 동일하게 구성
- (옵션) 헤더 `X-Model-Name`으로 모델 전환

## 4) 확장 포인트
- `app/chains/providers.py`: OpenAI 외 Anthropic, Azure OpenAI 등 어댑터 추가
- `app/chains/prompts.py`: 프롬프트 버전 관리
- `app/chains/extractor.py`: 파이프라인(프롬프트→LLM→파서) 조립
- `app/chains/parsers.py`: JSON 파서/스키마 검증 강화 (pydantic-jsonschema 추천)
- `app/core/config.py`: SSM/Secrets Manager 연동으로 비밀정보 주입
- `app/core/logging.py`: 구조화 로깅 & 추적ID

## 5) 헬스체크
- `GET /health` : 200, 버전/프로바이더/모델 표시
