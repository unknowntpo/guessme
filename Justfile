# Guessme - Root Development Commands

# Default: show available commands
default:
    @just --list

# === K8s / Tilt ===

# Start Tilt (local K8s development)
tilt:
    tilt up

# Start Tilt in headless mode (no browser)
tilt-headless:
    tilt up --stream

# Stop Tilt and clean up
tilt-down:
    tilt down

# Check K8s resources
k8s-status:
    kubectl get all -n guessme

# Port forward backend manually (if not using Tilt)
k8s-port-forward:
    kubectl port-forward -n guessme svc/guessme-backend 8000:8000

# Apply K8s manifests directly (without Tilt)
k8s-apply:
    kubectl apply -k k8s/

# Delete K8s resources
k8s-delete:
    kubectl delete -k k8s/

# === Docker ===

# Build backend image locally
docker-build:
    docker build -t guessme-backend backend/

# Run backend container locally (for testing)
docker-run:
    docker run -p 8000:8000 guessme-backend

# === Backend (delegated) ===

# Run backend commands via backend/Justfile
be *args:
    cd backend && just {{args}}

# === Frontend ===

# Start frontend dev server
fe-dev:
    cd frontend && pnpm dev

# Run frontend tests
fe-test:
    cd frontend && pnpm test

# === Full Stack ===

# Start everything for local dev (needs 3 terminals)
dev:
    @echo "Run in separate terminals:"
    @echo "  Terminal 1: just tilt          # K8s + backend"
    @echo "  Terminal 2: just fe-dev        # Frontend"
    @echo "  Terminal 3: just be mlflow     # MLflow UI"
