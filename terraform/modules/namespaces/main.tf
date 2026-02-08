/**
 * Namespaces Module
 *
 * Creates application namespaces for guessme.
 */

terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
  }
}

resource "kubernetes_namespace" "app" {
  metadata {
    name = var.namespace

    labels = {
      app         = var.namespace
      "managed-by" = "terraform"
    }
  }
}

variable "namespace" {
  description = "Application namespace"
  type        = string
  default     = "guessme"
}

output "namespace" {
  value = kubernetes_namespace.app.metadata[0].name
}
