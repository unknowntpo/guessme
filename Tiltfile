# Tiltfile for Guessme local K8s development

# Backend image
docker_build(
    'ghcr.io/unknowntpo/guessme/backend',
    context='backend',
    dockerfile='backend/Dockerfile',
    live_update=[
        sync('backend/src', '/app/src'),
    ],
    only=['src/', 'pyproject.toml', 'uv.lock'],
)

# Apply K8s manifests
k8s_yaml(kustomize('k8s'))

k8s_resource(
    'guessme-backend',
    port_forwards=['8000:8000'],
    labels=['backend'],
    links=[
        link('http://localhost:8000/docs', 'API Docs'),
        link('http://localhost:8000/health', 'Health'),
    ],
)

# Frontend: Vite dev server (port 5173)
local_resource(
    'frontend',
    serve_cmd='cd frontend && pnpm dev',
    labels=['frontend'],
    links=[link('http://localhost:5173', 'Frontend UI')],
    deps=['frontend/src', 'frontend/package.json'],
)
