# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Guessme is an AI-powered draw guessing game where users draw on a canvas, and an ML model recognizes their drawings.

## Development Commands

```bash
# Install dependencies (uses uv)
uv sync

# Run the application
uv run python main.py

# Run tests
uv run pytest

# Run a single test
uv run pytest path/to/test.py::test_function

# Lint and format
uv run ruff check .
uv run ruff format .
```

## Tech Stack

- Python 3.12+
- uv for package management
- pytest for testing
- ruff for linting/formatting