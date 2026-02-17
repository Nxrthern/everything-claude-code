---
name: secrets-management
description: Centralized vault management, credential lifecycle, least privilege access, and secrets auditing. Use when managing API keys, passwords, certificates, or any sensitive credentials across environments.
---

# Secrets Management

A secret in source code is not a secret. A secret without rotation is a liability. A secret without audit is a blind spot.

## When to Activate

- Setting up secrets management for a project
- Reviewing code for hardcoded credentials
- Implementing credential rotation
- Auditing secrets access and permissions
- Migrating from env vars to a vault

## Secrets Hierarchy

```
Priority order for secrets:
1. Vault (HashiCorp Vault, AWS SSM, GCP Secret Manager)
2. Kubernetes secrets (encrypted at rest)
3. CI/CD secret variables (GitHub Actions, GitLab CI)
4. Environment variables (runtime only, never committed)

NEVER:
- Source code (including comments)
- Config files in version control
- Docker images or build artifacts
- Log output or error messages
- Chat messages or documentation
```

## Vault Architecture

### Centralized Vault Pattern
```
Application → Vault Client → Vault Server → Backend (encrypted storage)
                  │
                  ├── Authenticate (token, Kubernetes SA, IAM role)
                  ├── Authorize (policy check)
                  ├── Retrieve secret
                  └── Audit log entry
```

### Access Policies
```hcl
# Vault policy: user-service can only read its own secrets
path "secret/data/user-service/*" {
  capabilities = ["read"]
}

# Deny access to other services' secrets
path "secret/data/payment-service/*" {
  capabilities = ["deny"]
}
```

### Dynamic Secrets
Generate short-lived credentials on demand:
```
Request → Vault generates temporary DB credentials
       → Credentials valid for 1 hour
       → Auto-revoked after TTL
       → No long-lived credentials to rotate
```

## Secret Types and Handling

| Type | Rotation Period | Storage | Example |
|------|----------------|---------|---------|
| API keys | 90 days | Vault | Third-party service keys |
| Database credentials | 30 days (or dynamic) | Vault | PostgreSQL passwords |
| TLS certificates | 90 days (auto via ACME) | Cert manager | Service mTLS certs |
| Signing keys | 1 year | HSM/KMS | JWT signing keys |
| Service tokens | 24 hours (or dynamic) | Vault | Inter-service auth |
| User passwords | User-driven | Hashed in DB | Never stored in plaintext |

## Detection and Prevention

### Pre-Commit Scanning
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    hooks:
      - id: gitleaks
```

### Patterns to Detect
```
# High-confidence patterns
AKIA[0-9A-Z]{16}                    # AWS access key
ghp_[A-Za-z0-9]{36}                 # GitHub personal token
sk-[A-Za-z0-9]{48}                  # OpenAI API key
-----BEGIN (RSA )?PRIVATE KEY-----  # Private key
xoxb-[0-9]{10,}-[A-Za-z0-9]{24}    # Slack bot token
```

### Emergency Response (Secret Leak)
```
1. IMMEDIATE: Revoke the leaked credential
2. Rotate: Generate new credential
3. Deploy: Update all consumers with new credential
4. Audit: Check access logs for unauthorized use
5. Investigate: How was it leaked? Fix the process
6. Monitor: Watch for abuse of old credential
```

## Application Integration

### Go Example
```go
// ✅ Fetch secret from vault at startup
func loadDBCredentials(ctx context.Context) (*DBConfig, error) {
    client, err := vault.NewClient(vault.DefaultConfig())
    if err != nil {
        return nil, fmt.Errorf("vault client: %w", err)
    }

    secret, err := client.KVv2("secret").Get(ctx, "db/user-service")
    if err != nil {
        return nil, fmt.Errorf("vault read: %w", err)
    }

    return &DBConfig{
        Host:     secret.Data["host"].(string),
        Password: secret.Data["password"].(string),
    }, nil
}
```

### Kubernetes Integration
```yaml
# Mount vault secret as environment variable
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: user-service
  containers:
    - name: app
      env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: user-service-db
              key: password
```

## Audit Requirements

Every secret access must be logged:
```json
{
  "timestamp": "2026-01-15T10:30:00Z",
  "action": "secret.read",
  "path": "secret/data/user-service/db",
  "identity": "kubernetes/user-service-sa",
  "source_ip": "10.0.1.50",
  "success": true
}
```

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| Secrets in Git | Permanent exposure | Vault + pre-commit scanning |
| Shared credentials across envs | Blast radius | Unique per environment |
| Long-lived credentials | Stale, wider exposure window | Dynamic secrets or short TTL |
| No audit logging | Invisible breach | Enable vault audit backend |
| Manual rotation | Forgotten, inconsistent | Automate rotation |

---

**Remember**: Treat every credential as if it's already been compromised. The question isn't whether it will leak — it's how quickly you can detect and rotate when it does.
