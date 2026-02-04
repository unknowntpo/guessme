# Tiltfile for Guessme local K8s development with KubeRay

# KubeRay operator (manages RayService CRD)
load('ext://helm_resource', 'helm_resource', 'helm_repo')
helm_repo('kuberay', 'https://ray-project.github.io/kuberay-helm/')
helm_resource(
    'kuberay-operator',
    'kuberay/kuberay-operator',
    flags=['--version=1.3.2'],
    labels=['infra'],
)

# Backend image
docker_build(
    'guessme-backend',
    context='backend',
    dockerfile='backend/Dockerfile',
    live_update=[
        sync('backend/src', '/app/src'),
    ],
    only=['src/', 'pyproject.toml', 'uv.lock'],
)

# Tell Tilt where to find image refs in RayService CRD
k8s_image_json_path(
    '{.spec.rayClusterConfig.headGroupSpec.template.spec.containers[*].image}',
    api_version='ray.io/v1',
    kind='RayService',
)

# Apply K8s manifests (RayService)
k8s_yaml(kustomize('k8s'))

# RayService is now auto-detected as workload via k8s_image_json_path
# extra_pod_selectors discovers pods created by KubeRay operator
k8s_resource(
    'guessme',
    extra_pod_selectors=[{'ray.io/node-type': 'head'}],
    port_forwards=[
        '8000:8000',  # Ray Serve
        '8265:8265',  # Ray Dashboard
    ],
    labels=['backend'],
    links=[
        link('http://localhost:8000/docs', 'API Docs'),
        link('http://localhost:8000/health', 'Health'),
        link('http://localhost:8265', 'Ray Dashboard'),
    ],
    resource_deps=['kuberay-operator'],
)

# Frontend: Vite dev server (port 5173)
local_resource(
    'frontend',
    serve_cmd='cd frontend && pnpm dev',
    labels=['frontend'],
    links=[link('http://localhost:5173', 'Frontend UI')],
    deps=['frontend/src', 'frontend/package.json'],
)

# MLflow: Experiment tracking UI (port 5001)
local_resource(
    'mlflow',
    serve_cmd='cd backend && uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5001',
    labels=['observability'],
    links=[link('http://localhost:5001', 'MLflow UI')],
)
