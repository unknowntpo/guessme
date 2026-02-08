/**
 * Cloudflared Deployment Module
 *
 * Deploys cloudflared connector as a K8s Deployment
 * to connect the Cloudflare Tunnel to the cluster.
 */

terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
  }
}

resource "kubernetes_deployment" "cloudflared" {
  metadata {
    name      = "cloudflared"
    namespace = var.namespace

    labels = {
      app = "cloudflared"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "cloudflared"
      }
    }

    template {
      metadata {
        labels = {
          app = "cloudflared"
        }
      }

      spec {
        container {
          name  = "cloudflared"
          image = "cloudflare/cloudflared:latest"

          args = [
            "tunnel",
            "--no-autoupdate",
            "run",
            "--token",
            "$(TUNNEL_TOKEN)",
          ]

          env {
            name = "TUNNEL_TOKEN"
            value_from {
              secret_key_ref {
                name = var.secret_name
                key  = "token"
              }
            }
          }

          resources {
            requests = {
              cpu    = "50m"
              memory = "64Mi"
            }
            limits = {
              cpu    = "200m"
              memory = "128Mi"
            }
          }
        }
      }
    }
  }
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "guessme"
}

variable "secret_name" {
  description = "Name of the K8s secret with tunnel credentials"
  type        = string
  default     = "cloudflared-credentials"
}
