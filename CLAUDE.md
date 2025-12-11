# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Guessme is an AI-powered draw guessing game where users draw on a canvas, and an ML model recognizes their drawings.

## Development Commands

```bash
# Install dependencies (uses uv)
uv sync

# Run backend (Ray Serve on port 8000)
serve run backend.main:app

# Run frontend (Vite dev server)
cd frontend && pnpm dev

# Run backend tests
uv run pytest backend/tests/

# Run frontend tests
cd frontend && pnpm test

# Lint and format
uv run ruff check .
uv run ruff format .
```

## Tech Stack

### Backend
- Python 3.12+
- FastAPI + WebSocket
- Ray Serve for deployment
- uv for package management
- pytest for testing
- ruff for linting/formatting

### Frontend
- Vue 3 + Vite + TypeScript
- Tailwind CSS
- Vitest for testing
- pnpm for package management