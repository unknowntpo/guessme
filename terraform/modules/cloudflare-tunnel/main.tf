/**
 * Cloudflare Tunnel Module
 *
 * Creates:
 * - Cloudflare Tunnel
 * - DNS CNAME records (one per ingress route)
 * - K8s secret with tunnel credentials
 *
 * Supports multiple ingress routes on a single tunnel.
 */

terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

# Generate tunnel secret
resource "random_id" "tunnel_secret" {
  byte_length = 35
}

# Create Cloudflare Tunnel
resource "cloudflare_zero_trust_tunnel_cloudflared" "this" {
  account_id = var.account_id
  name       = var.tunnel_name
  secret     = random_id.tunnel_secret.b64_std
}

# Configure tunnel ingress rules (multiple routes)
resource "cloudflare_zero_trust_tunnel_cloudflared_config" "this" {
  account_id = var.account_id
  tunnel_id  = cloudflare_zero_trust_tunnel_cloudflared.this.id

  config {
    dynamic "ingress_rule" {
      for_each = var.ingress_rules
      content {
        hostname = "${ingress_rule.value.subdomain}.${var.domain}"
        service  = ingress_rule.value.service_url
      }
    }

    # Catch-all rule (required)
    ingress_rule {
      service = "http_status:404"
    }
  }
}

# DNS CNAME records (one per ingress route)
resource "cloudflare_record" "tunnel_cname" {
  for_each = { for r in var.ingress_rules : r.subdomain => r }

  zone_id = var.zone_id
  name    = each.value.subdomain
  content = "${cloudflare_zero_trust_tunnel_cloudflared.this.id}.cfargotunnel.com"
  type    = "CNAME"
  proxied = true
  ttl     = 1

  comment = "Managed by Terraform - ${var.tunnel_name}"
}

# Create K8s secret with tunnel credentials
resource "kubernetes_secret" "cloudflared_credentials" {
  metadata {
    name      = var.k8s_secret_name
    namespace = var.k8s_namespace
  }

  data = {
    "credentials.json" = jsonencode({
      AccountTag   = var.account_id
      TunnelID     = cloudflare_zero_trust_tunnel_cloudflared.this.id
      TunnelName   = cloudflare_zero_trust_tunnel_cloudflared.this.name
      TunnelSecret = random_id.tunnel_secret.b64_std
    })
    "token" = cloudflare_zero_trust_tunnel_cloudflared.this.tunnel_token
  }

  type = "Opaque"
}
