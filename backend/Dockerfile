# Multi-stage Dockerfile for Guessme backend
# Stage 1: Builder - install dependencies
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (cached layer)
RUN uv sync --frozen --no-dev --no-install-project

# Copy source code
COPY src/ src/

# Install project
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code (for live sync compatibility)
COPY --from=builder /app/src /app/src

# Copy model weights (if exists)
COPY src/guessme/model/weights/ /app/src/guessme/model/weights/

# Set PATH to use venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# Ray Serve port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run Ray Serve
CMD ["serve", "run", "--host", "0.0.0.0", "guessme.main:app"]