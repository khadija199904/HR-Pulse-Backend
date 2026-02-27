FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app


ENV UV_PROJECT_ENVIRONMENT="/usr/local"
ENV UV_COMPILE_BYTECODE=1


COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev


COPY . .

CMD ["sh", "-c", "sleep 5 && uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload"] 