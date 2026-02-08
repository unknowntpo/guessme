/**
 * 01-cloudflare: Cloudflare Tunnel Layer
 *
 * Creates Cloudflare Tunnel exposing:
 * - guessme.unknowntpo.com       -> Ray Serve API
 * - argocd-homelab.unknowntpo.com -> ArgoCD UI
 *
 * Prerequisites:
 * - 00-k8s-apps layer applied
 * - Cloudflare API token with Zone:DNS:Edit + Tunnel permissions
 *
 * Usage:
 *   export TF_VAR_cloudflare_api_token="<your-token>"
 *   terraform init
 *   terraform plan
 *   terraform apply
 */

# Single tunnel with multiple ingress routes
module "cloudflare_tunnel" {
  source = "../../../modules/cloudflare-tunnel"

  tunnel_name = "homelab-prod-tunnel"
  account_id  = var.cloudflare_account_id
  zone_id     = var.cloudflare_zone_id
  domain      = "unknowntpo.com"

  ingress_rules = [
    {
      subdomain   = "guessme"
      service_url = "http://guessme-serve-svc.guessme.svc.cluster.local:8000"
    },
    {
      subdomain     = "argocd-homelab"
      service_url   = "https://argocd-server.argocd.svc.cluster.local:443"
      no_tls_verify = true
    },
  ]

  k8s_namespace   = "guessme"
  k8s_secret_name = "cloudflared-credentials"
}

# Cloudflared connector: runs in-cluster to connect tunnel
module "cloudflared_deployment" {
  source = "../../../modules/cloudflared-deployment"

  namespace   = "guessme"
  secret_name = "cloudflared-credentials"

  depends_on = [module.cloudflare_tunnel]
}
