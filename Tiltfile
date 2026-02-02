# Tiltfile for Guessme local K8s development

# Backend image with live update (no rebuild for .py changes)
docker_build(
    'guessme-backend',
    context='backend',
    dockerfile='backend/Dockerfile',
    live_update=[
        # Sync source code changes (no rebuild needed)
        sync('backend/src', '/app/src'),

        # Restart Ray Serve when Python files change
        run(
            'pkill -HUP -f "serve run" || true',
            trigger=['backend/src/**/*.py']
        ),
    ],
    # Only rebuild when these change
    only=[
        'src/',
        'pyproject.toml',
        'uv.lock',
    ],
)

# Apply K8s manifests
k8s_yaml(kustomize('k8s'))

# Port forward backend to localhost:8000
k8s_resource(
    'guessme-backend',
    port_forwards=['8000:8000'],
    labels=['backend'],
)

# Frontend (optional - can run separately with pnpm dev)
# local_resource(
#     'frontend',
#     serve_cmd='cd frontend && pnpm dev',
#     labels=['frontend'],
# )
