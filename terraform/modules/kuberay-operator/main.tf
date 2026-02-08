/**
 * KubeRay Operator Module
 *
 * Installs KubeRay operator via Helm for RayService CRD support.
 */

terraform {
  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.10"
    }
  }
}

resource "helm_release" "kuberay_operator" {
  name             = "kuberay-operator"
  repository       = "https://ray-project.github.io/kuberay-helm/"
  chart            = "kuberay-operator"
  version          = var.chart_version
  namespace        = "kuberay-system"
  create_namespace = true

  values = [
    yamlencode({
      resources = {
        requests = {
          cpu    = "100m"
          memory = "128Mi"
        }
        limits = {
          cpu    = "500m"
          memory = "256Mi"
        }
      }
    })
  ]
}

variable "chart_version" {
  description = "KubeRay operator Helm chart version"
  type        = string
  default     = "1.3.2"
}
