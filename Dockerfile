
# 베이스 이미지
FROM python:3.13-slim

# 작업 디렉토리 설정
WORKDIR /app

# uv 설치
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 의존성 파일 먼저 복사 (캐시 활용)
COPY pyproject.toml .
COPY uv.lock .

# 의존성 설치
RUN uv sync --frozen --no-dev

# 소스코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 실행 명령
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
