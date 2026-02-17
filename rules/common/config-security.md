# Configuration & Secrets Security Rules

## Secrets (CRITICAL)

NEVER:
- Hardcoded secrets in source code, config files, or comments
- Secrets in Docker images or build artifacts
- Secrets in log output or error messages
- Same credentials across environments

ALWAYS:
- Centralized vault (HashiCorp Vault, AWS SSM, or equivalent)
- Least privilege — each service only its own secrets
- Audit logging for all secret access
- Pre-commit scanning for exposed credentials

## Encryption (CRITICAL)

- All data at rest encrypted (AES-256 or equivalent)
- All data in transit encrypted (TLS 1.2+)
- Encryption keys managed via KMS/HSM (never alongside data)
- Envelope encryption for application-level secrets

## Rotation

- All credentials rotate on schedule (90 days maximum)
- Rotation is automated (not manual)
- Zero-downtime rotation (dual-key during transition)
- Rotation monitoring with alerts on stale credentials

## Configuration

- All config in version control (GitOps)
- Schema validation in CI for config changes
- Drift detection between environments
- Config changes require PR review
- Feature flags have owners and expiration dates

## Reference

See skills: `secrets-management`, `encryption-strategies`, `rotation-strategies`, `config-management` for comprehensive patterns.
