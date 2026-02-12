FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY src/ src/

RUN uv sync --frozen --no-dev

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

RUN mkdir -p /app/src/guessme/model/weights && \
    apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -fsSL -o /app/src/guessme/model/weights/mnist_cnn.pt \
      https://github.com/unknowntpo/guessme/releases/download/model-v0.1.0/mnist_cnn.pt && \
    apt-get purge -y curl && rm -rf /var/lib/apt/lists/*

ENV PATH="/app/.venv/bin:$PATH" PYTHONPATH="/app/src"

EXPOSE 8000

CMD ["uvicorn", "guessme.main:app", "--host", "0.0.0.0", "--port", "8000"]
