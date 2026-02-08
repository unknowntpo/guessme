/**
 * 00-k8s-apps: Kubernetes Resources Layer
 *
 * Deploys to existing homelab k8s cluster:
 * - KubeRay operator (for RayService CRD)
 * - Application namespace
 * - ArgoCD Application (points to k8s/ in this repo)
 *
 * Prerequisites:
 * - k8s cluster accessible via kubeconfig
 * - ArgoCD already installed
 *
 * Usage:
 *   terraform init
 *   terraform plan
 *   terraform apply
 */

# KubeRay operator (required for RayService CRD)
module "kuberay_operator" {
  source = "../../../modules/kuberay-operator"
}

# Application namespace
module "namespaces" {
  source    = "../../../modules/namespaces"
  namespace = "guessme"
}

# ArgoCD Application (syncs k8s/ directory from this repo)
module "argocd_app" {
  source = "../../../modules/argocd-app"

  depends_on = [module.kuberay_operator, module.namespaces]
}
