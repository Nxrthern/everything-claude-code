---
name: rotate-check
description: Check credential rotation status and identify stale secrets that need rotation.
---

# Rotation Check

Audit all credentials for rotation compliance and identify overdue rotations.

## Steps

1. **Inventory credentials** — List all credentials in the system:
   - Database passwords
   - API keys (internal and third-party)
   - TLS certificates
   - JWT signing keys
   - Service tokens
   - SSH keys

2. **Check rotation status**:
   - Invoke skill: `rotation-strategies` for rotation schedules
   - Determine last rotation date for each credential
   - Compare against rotation policy (30/90/180/365 days)
   - Flag overdue credentials

3. **Verify rotation mechanism**:
   - Is rotation automated or manual?
   - Does rotation support zero-downtime (dual-key)?
   - Has rotation been tested in staging?

4. **Check monitoring**:
   - Alerts configured for stale credentials?
   - Dashboard showing rotation status?

5. **Report with priority** — Overdue rotations are HIGH severity.

## Output Format

```markdown
## Rotation Status

### Credential Inventory
| Credential | Type | Last Rotated | Policy | Due Date | Status |
|-----------|------|-------------|--------|----------|--------|
| [name] | [DB/API/TLS/JWT] | [date] | [90 days] | [date] | [Current/Due/Overdue] |

### Overdue Rotations
1. **[HIGH]** [Credential name] — [X days] overdue

### Automation Status
| Credential | Automated | Dual-Key | Tested |
|-----------|-----------|----------|--------|

### Recommendations
- [Credentials to rotate immediately]
- [Automation to implement]
```
