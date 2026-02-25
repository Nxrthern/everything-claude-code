---
name: secrets-audit
description: Scan codebase for exposed secrets, audit vault coverage, and check credential rotation compliance.
---

# Secrets Audit

Comprehensive scan for exposed credentials, vault coverage gaps, and rotation compliance.

## Steps

1. **Scan for exposed secrets** — Search codebase for hardcoded credentials:
   - Invoke skill: `secrets-management` for detection patterns
   - Search for API keys, passwords, private keys, tokens
   - Check config files, environment defaults, Docker files, comments

2. **Audit vault coverage**:
   - List all credentials used by the system
   - Verify each is stored in centralized vault
   - Check access policies (least privilege)
   - Verify audit logging enabled

3. **Check encryption coverage**:
   - Invoke skill: `encryption-strategies` for standards
   - Verify data at rest encrypted
   - Verify data in transit encrypted (TLS)
   - Check key management (KMS/HSM)

4. **Check rotation compliance**:
   - Invoke skill: `rotation-strategies` for rotation patterns
   - List credentials and last rotation date
   - Flag any older than policy allows (typically 90 days)
   - Verify zero-downtime rotation support

5. **Report with severity** — CRITICAL for any exposed secret.

## Output Format

```markdown
## Secrets Audit

### Exposed Secrets
| Location | Type | Severity |
|----------|------|----------|
| [file:line] | [type] | CRITICAL |

### Vault Coverage
- Secrets in vault: [X/Y]
- Missing: [list]

### Rotation Compliance
| Credential | Last Rotated | Policy | Status |
|-----------|-------------|--------|--------|

### Encryption Coverage
- At rest: [Complete/Partial/None]
- In transit: [TLS version]

### Action Items
1. [CRITICAL] Rotate and remove exposed secrets
2. [HIGH] Migrate missing secrets to vault
```
