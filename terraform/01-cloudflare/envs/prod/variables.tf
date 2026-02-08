variable "kubeconfig_path" {
  description = "Path to kubeconfig file for homelab cluster"
  type        = string
  default     = "~/.kube/config-morefine"
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token (Zone:DNS:Edit + Tunnel permissions)"
  type        = string
  sensitive   = true
}

variable "cloudflare_account_id" {
  description = "Cloudflare Account ID"
  type        = string
}

variable "cloudflare_zone_id" {
  description = "Cloudflare Zone ID for unknowntpo.com"
  type        = string
}

variable "access_allowed_emails" {
  description = "Emails allowed to access Zero Trust protected apps"
  type        = list(string)
  sensitive   = true
}
