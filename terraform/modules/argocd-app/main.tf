/**
 * ArgoCD Application Module
 *
 * Deploys ArgoCD Application CRD for guessme.
 */

terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
  }
}

resource "kubernetes_manifest" "app" {
  manifest = yamldecode(file("${path.module}/guessme-app.yaml"))
}
