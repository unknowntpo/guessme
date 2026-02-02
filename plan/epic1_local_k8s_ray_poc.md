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

### Phase 1: PyTorch CNN Model (TDD) ✅
- [x] UT: Model forward pass (28x28 → 10 classes)
- [x] UT: Preprocessing (canvas → tensor)
- [x] Implement simple CNN (Conv → Pool → FC)
- [x] Train on MNIST, save weights (99.27% accuracy)

### Phase 2: Ray Serve Integration (TDD) ✅
- [x] UT: Model loading, inference
- [x] IT: Ray Serve /predict endpoint
- [x] Update predictor actor to use real model

### Phase 3: MLflow + DVC ✅
- [x] DVC init, track model weights
- [x] MLflow SQLite backend for training
- [x] MLflow tracing for inference
- [x] CI: Download weights from GitHub Release
- [x] Preprocessing pipeline (dilate, center, blur)

### Phase 4: K8s + Tilt Setup
- [ ] Dockerfile for backend
- [ ] K8s manifests (deployment, service)
- [ ] Tiltfile for hot reload
- [ ] Local registry setup

### Phase 5: Frontend Adapt
- [x] REST-based game mode
- [x] CORS middleware
- [ ] Update canvas to 28x28 grid style
- [ ] E2E: Full draw → predict flow

### Phase 6: CI/CD ✅
- [x] GitHub Action: UT + IT
- [x] Download weights from GitHub Release
- [ ] GitHub Action: Build container

### Phase 7: K8s + Tilt Setup (Future)
- [ ] Dockerfile for backend
- [ ] K8s manifests (deployment, service)
- [ ] Tiltfile for hot reload
- [ ] Local registry setup

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

## TODO (Future)

- [ ] **Ray Train + MLflow integration**: Use Ray Train for distributed training with MLflow tracking. Reference: `/Users/unknowntpo/repo/unknowntpo/ml_playground`
