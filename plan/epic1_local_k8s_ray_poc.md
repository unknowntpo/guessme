# Epic 1: Local K8s + Ray POC

**Status:** In Progress

## Summary

Deploy MNIST CNN model with Ray Serve on local K8s (Tilt). Prove e2e: draw digit → predict → display.

## Architecture

```
┌────────┐  WS   ┌─────────────────────────────────────────┐
│   FE   │←────→│              K8s (local)                │
│ Vue.js │      │  ┌─────────────┐     ┌──────────────┐   │
└────────┘      │  │  Ray Serve  │────→│  CNN Model   │   │
                │  │  (FastAPI)  │     │  (PyTorch)   │   │
                │  └─────────────┘     └──────────────┘   │
                └─────────────────────────────────────────┘
                         ↑ Tilt (hot reload)
```

## Checklist

### Phase 1: PyTorch CNN Model (TDD)
- [x] UT: Model forward pass (28x28 → 10 classes)
- [x] UT: Preprocessing (canvas → tensor)
- [x] Implement simple CNN (Conv → Pool → FC)
- [ ] Train on MNIST, save weights

### Phase 2: Ray Serve Integration (TDD)
- [ ] UT: Model loading, inference
- [ ] IT: Ray Serve /predict endpoint
- [ ] Update predictor actor to use real model

### Phase 3: K8s + Tilt Setup
- [ ] Dockerfile for backend
- [ ] K8s manifests (deployment, service)
- [ ] Tiltfile for hot reload
- [ ] Local registry setup

### Phase 4: Frontend Adapt
- [ ] Update canvas to 28x28 grid style
- [ ] IT: WebSocket with K8s backend
- [ ] E2E: Full draw → predict flow

### Phase 5: CI/CD
- [ ] GitHub Action: UT + IT
- [ ] GitHub Action: Build container
- [ ] (Optional) K8s IT in CI

## Test Summary

| Level | Test | Framework |
|-------|------|-----------|
| UT | CNN forward pass | pytest |
| UT | Preprocessing | pytest |
| UT | Frontend components | Vitest |
| IT | Ray Serve API | pytest + httpx |
| IT | WebSocket flow | pytest |
| E2E | Draw → predict | Playwright |

## Files (New/Modified)

```
backend/
├── model/
│   ├── __init__.py
│   ├── cnn.py           # PyTorch CNN
│   ├── preprocess.py    # Image preprocessing
│   └── weights/         # Saved model weights
├── predictor/
│   └── actor.py         # Update to use real model
└── tests/
    ├── test_cnn.py
    └── test_preprocess.py

k8s/
├── deployment.yaml
├── service.yaml
└── kustomization.yaml

Dockerfile
Tiltfile

.github/workflows/
└── ci.yaml              # Update for new tests
```

## Commands

```bash
# Train model (one-time)
uv run python -m backend.model.train

# Run tests
uv run pytest backend/tests/

# Local K8s (requires Tilt + K8s cluster)
tilt up

# E2E tests
cd frontend && pnpm test:e2e
```

## Dependencies

```
# pyproject.toml additions
torch
torchvision
```

## Notes

- Reuse existing FastAPI + Ray Serve from old epic
- CNN: 2 conv layers + 2 FC layers (simple)
- Canvas sends 28x28 grayscale image data
