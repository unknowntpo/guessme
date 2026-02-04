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

# Install wget (required by KubeRay readiness probes) and curl (for health checks)
RUN apt-get update && apt-get install -y --no-install-recommends wget curl && rm -rf /var/lib/apt/lists/*

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

# Symlink ray binary so KubeRay's `bash -c "ray start ..."` can find it
RUN ln -sf /app/.venv/bin/ray /usr/local/bin/ray

# Ray ports: GCS, Dashboard, Serve
EXPOSE 6379 8265 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Ray head mode — RayService manages serve deployments
CMD ["ray", "start", "--head", "--block", "--dashboard-host=0.0.0.0"]