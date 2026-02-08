variable "tunnel_name" {
  description = "Name of the Cloudflare Tunnel"
  type        = string
}

variable "account_id" {
  description = "Cloudflare Account ID"
  type        = string
}

variable "zone_id" {
  description = "Cloudflare Zone ID"
  type        = string
}

variable "domain" {
  description = "Base domain (e.g., unknowntpo.com)"
  type        = string
}

variable "ingress_rules" {
  description = "List of ingress routes for the tunnel"
  type = list(object({
    subdomain   = string
    service_url = string
  }))
}

variable "k8s_namespace" {
  description = "Kubernetes namespace for the secret"
  type        = string
  default     = "guessme"
}

variable "k8s_secret_name" {
  description = "Name of the K8s secret to create"
  type        = string
  default     = "cloudflared-credentials"
}
