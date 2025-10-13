# core-api-gateway

A containerized API project for secure development and production with Podman on SELinux-enabled Linux distributions.

***

## Development Setup

### Prerequisites

- Podman (`dnf install podman`) or Docker
- SELinux enabled (Fedora/RHEL/CentOS)
- Python 3.10+ (for local dev)
- OpenSSL

### First-Time Setup

```bash
# Clone project
git clone <repo-url>
cd <repo-dir>

# Relabel app directory for Podman + SELinux
sudo chcon -Rt svirt_sandbox_file_t ./app

# Generate development SSL certificates
bash generate-certs.sh
```

### Build & Run (HTTPS-enabled)

```bash
podman compose up --build
```

- Your API will be available at:
  [https://localhost:8443/](https://localhost:8443/)
- For self-signed certs, test with:
  `curl -k https://localhost:8443/health`

***

## SELinux Configuration

If you encounter "permission denied" with mounted folders:

```bash
sudo chcon -Rt svirt_sandbox_file_t ./app
```

Always use `:z` (shared) or `:Z` (exclusive) with volume mounts in your Compose YAML.

***

## HTTPS Certificates

**Do NOT commit cert.pem or key.pem to git.**

Add these lines to `.gitignore`:

```
cert.pem
key.pem
```

***

## Production Deployment

- NEVER commit production TLS certs/keys. Provision securely (mount as secrets/volumes).
- Use a reverse proxy (Nginx, Caddy, Traefik) for HTTPS on standard port 443.

***

## Troubleshooting

- **Permission Denied (SELinux):**
  ```bash
  sudo chcon -Rt svirt_sandbox_file_t ./app
  ```
- **curl: SSL certificate problem:**
  Use `-k` flag for self-signed certs:
  `curl -k https://localhost:8443/health`
- **HTTPS on nonstandard ports:**
  Specify port in URL (e.g., `https://localhost:8443`).
