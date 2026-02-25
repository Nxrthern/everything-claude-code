---
name: rotation-strategies
description: Automated credential, key, and certificate rotation with zero-downtime dual-key support. Use when implementing rotation policies, managing certificate lifecycles, or designing systems that handle credential changes gracefully.
---

# Rotation Strategies

Every credential has a shelf life. Automate rotation so you never have to remember, and design for dual-key so you never have downtime.

## When to Activate

- Implementing automated credential rotation
- Designing certificate lifecycle management
- Setting up rotation policies for secrets
- Building systems that handle credential rollover gracefully
- Auditing credential age and rotation compliance

## Rotation Principles

### 1. Automate Everything
Manual rotation is forgotten rotation. Automate via:
- Vault auto-rotation policies
- Cloud provider rotation lambdas
- ACME protocol for TLS certificates
- Cron jobs with validation

### 2. Dual-Key During Transition
Both old and new credentials must work simultaneously:
```
Timeline:
  T+0:  Generate new credential
  T+0:  Both old AND new are valid
  T+1h: Deploy new credential to all consumers
  T+2h: Verify all consumers use new credential
  T+4h: Revoke old credential (grace period)
```

### 3. Test Rotation in Staging First
Every rotation procedure must be tested in a non-production environment before being enabled in production.

## Credential Rotation Schedules

| Credential Type | Rotation Period | Method | Zero-Downtime |
|----------------|----------------|--------|---------------|
| Database passwords | 30 days | Vault dynamic secrets (preferred) | Yes (dual-user) |
| API keys | 90 days | Generate new, deprecate old | Yes (grace period) |
| TLS certificates | 90 days | ACME auto-renewal | Yes (cert manager) |
| JWT signing keys | 6 months | JWKS rotation | Yes (key ID in token) |
| SSH keys | 6 months | Generate, deploy, revoke | Yes (authorized_keys) |
| Encryption keys | 1 year | KMS key version rotation | Yes (envelope encryption) |
| Service tokens | 24 hours | Vault dynamic (short TTL) | Yes (auto-refresh) |

## Rotation Patterns

### Database Credential Rotation
```
1. Create new DB user (user_v2) with same permissions
2. Update vault/config with new credentials
3. Rolling restart consumers (or live config reload)
4. Monitor: all connections using user_v2
5. Drop old DB user (user_v1)
```

### JWT Signing Key Rotation (JWKS)
```
JWKS endpoint serves multiple keys with key IDs:
{
  "keys": [
    { "kid": "key-2026-02", "kty": "RSA", ... },  // current
    { "kid": "key-2025-11", "kty": "RSA", ... }   // previous (still valid)
  ]
}

Rotation:
1. Generate new key, add to JWKS
2. New tokens signed with new key ID
3. Old tokens validated using old key ID (until expiry)
4. Remove old key from JWKS after max token lifetime
```

### TLS Certificate Rotation
```
ACME auto-renewal (Let's Encrypt / cert-manager):
1. Certificate expires in 30 days → renewal triggered
2. New certificate issued
3. Server reloads certificate (no restart)
4. Old certificate naturally expires

Kubernetes cert-manager handles this automatically:
  - Watches certificate expiry
  - Renews before expiry
  - Updates Kubernetes secret
  - Triggers pod config reload
```

### API Key Rotation
```go
// ✅ Support multiple valid keys during transition
func validateAPIKey(ctx context.Context, key string) bool {
    validKeys := vault.GetCurrentKeys(ctx, "api-keys/service-x")
    for _, valid := range validKeys {
        if subtle.ConstantTimeCompare([]byte(key), []byte(valid)) == 1 {
            return true
        }
    }
    return false
}
```

## Monitoring Rotation Health

### Key Metrics
```yaml
# Alert on stale credentials
- alert: CredentialNotRotated
  expr: (time() - credential_last_rotated_timestamp) > 90 * 86400
  labels:
    severity: warning
  annotations:
    summary: "Credential {{ $labels.name }} not rotated in 90+ days"
```

### Rotation Dashboard
| Credential | Last Rotated | Policy | Next Due | Status |
|-----------|-------------|--------|----------|--------|
| DB password | 2026-01-20 | 30 days | 2026-02-19 | Due soon |
| API key | 2025-12-01 | 90 days | 2026-03-01 | Current |
| TLS cert | 2026-02-01 | 90 days | 2026-05-01 | Current |

## Emergency Rotation

When a credential is compromised:
```
1. IMMEDIATELY: Revoke compromised credential
2. Generate new credential in vault
3. Deploy to all consumers (emergency push)
4. Verify all consumers healthy
5. Audit: check for unauthorized access during exposure
6. Postmortem: how was it compromised?
```

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| Manual rotation | Forgotten, inconsistent | Automate with vault/cron |
| Hard cutover (no dual-key) | Downtime during rotation | Grace period with both valid |
| Same credential across envs | Rotation in one breaks all | Unique per environment |
| No rotation monitoring | Stale credentials unnoticed | Alert on age threshold |
| Rotation without testing | Production outage on rotate | Test in staging first |

---

**Remember**: The best rotation is the one nobody notices. Automate it, test it, monitor it, and design your systems to handle credential changes as a normal operation, not an emergency.
