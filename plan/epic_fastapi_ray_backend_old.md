# Epic: FastAPI WebSocket Backend with Ray Serve

**Status:** Done

## Summary

Replace Node.js mock-server with FastAPI WebSocket server running inside Ray Serve for ML model serving.

## Architecture

```
┌─────────────┐     WebSocket      ┌──────────────────────────────────────┐
│   Frontend  │ ←───────────────→  │           Ray Serve (:8000)          │
│   (Vue 3)   │                    │  ┌─────────────┐  ┌───────────────┐  │
└─────────────┘                    │  │   FastAPI   │→ │ PredictorActor│  │
                                   │  │  Deployment │  │   (Ray)       │  │
                                   │  └─────────────┘  └───────────────┘  │
                                   └──────────────────────────────────────┘
```

## Checklist

### Phase 1: Setup & Pydantic Models (TDD)
- [x] Add dependencies: fastapi, uvicorn[standard], pydantic, ray[serve]
- [x] Create backend/ structure
- [x] Write tests for message models (12 tests)
- [x] Implement Point, Prediction, ClientMessage, ServerMessage models

### Phase 2: Ray Predictor Actor (TDD)
- [x] Write tests for predictor logic (8 tests)
- [x] Implement `@ray.remote` PredictorActor
- [x] Fake predictions (random labels for UI testing)

### Phase 3: WebSocket Handler (TDD)
- [x] Write integration tests (6 tests)
- [x] Implement /ws endpoint
- [x] Handle stroke/submit/clear messages

### Phase 4: Ray Serve Deployment
- [x] Create @serve.deployment for FastAPI
- [x] Local run: `uv run serve run backend.main:app`
- [x] Server starts on port 8000

### Phase 5: Cleanup
- [x] Remove mock-server/
- [x] Update frontend .env (VITE_WS_URL=ws://localhost:8000)
- [x] Update CLAUDE.md with new commands

## Test Summary

- **26 tests total** (12 message + 8 predictor + 6 websocket)
- All tests passing

## Files

```
backend/
├── __init__.py
├── main.py              # Ray Serve entry
├── websocket/
│   ├── __init__.py
│   ├── handler.py       # WebSocket endpoint
│   └── messages.py      # Pydantic models
├── predictor/
│   ├── __init__.py
│   └── actor.py         # Ray actor
└── tests/
    ├── __init__.py
    ├── test_messages.py
    ├── test_predictor.py
    └── test_websocket.py
```

## Commands

```bash
# Install deps
uv sync

# Run backend
uv run serve run backend.main:app

# Run tests
uv run pytest backend/tests/
```
