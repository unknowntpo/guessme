# Guessme - System Design

AI-powered number guessing game (MNIST-style).

## Milestone 0: Local POC with MLOps

### Epic 1: Local K8s + Ray (POC) → [epic1_local_k8s_ray_poc.md](epic1_local_k8s_ray_poc.md)
- Deploy locally with Tilt + K8s
- Ray Serve for model serving
- PyTorch CNN for MNIST
- Prove end-to-end works
- GitHub Action ready

### Epic 2: Data Versioning
- DVC setup (local remote)
- Track MNIST dataset

### Epic 3: Experiment Tracking
- MLflow integration
- Model registry

### Epic 4: Pipeline Automation
- Airflow DAG
- Auto train → deploy

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Frontend | Vue 3 + Vite |
| Backend | FastAPI + Ray Serve |
| Model | PyTorch CNN |
| Local Dev | Tilt + K8s |
| Data Versioning | DVC (local) |
| Experiment Tracking | MLflow |
| Distributed Training | Ray Train |
| Pipeline | Airflow |

## Architecture (Epic 1 - POC)

```
┌────────┐  WS   ┌─────────────┐     ┌─────────────┐
│   FE   │←────→│  Ray Serve  │────→│  CNN Model  │
│ Vue.js │      │  (FastAPI)  │     │  (predict)  │
└────────┘      └─────────────┘     └─────────────┘
         \_______ K8s + Tilt (local) _______/
```

## Architecture (Full - Epic 4)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Airflow   │────→│  Ray Train  │────→│   MLflow    │
│ (pipeline)  │     │  (train)    │     │ (tracking)  │
└─────────────┘     └──────┬──────┘     └─────────────┘
                          │
┌─────────────┐           ↓
│     DVC     │     ┌─────────────┐
│   (data)    │────→│ Model Reg   │
└─────────────┘     └──────┬──────┘
                          │ deploy
                          ↓
┌────────┐  WS   ┌─────────────┐     ┌─────────────┐
│   FE   │←────→│  Ray Serve  │────→│  CNN Model  │
│ Vue.js │      │  (FastAPI)  │     │  (predict)  │
└────────┘      └─────────────┘     └─────────────┘
```

## Testing Strategy

| Level | Scope | Framework |
|-------|-------|-----------|
| UT | Backend unit | pytest |
| UT | Frontend unit | Vitest |
| UT | Model unit | pytest |
| IT | API integration | pytest + httpx |
| IT | K8s services | pytest + k8s client |
| E2E | Full flow | Playwright |

### Per Epic Testing

**Epic 1 (POC):**
- UT: CNN model forward pass, preprocessing
- IT: Ray Serve API, WebSocket flow
- E2E: Draw → predict → display result

**Epic 2-4:**
- IT: DVC data fetch, MLflow logging, Airflow DAG triggers
