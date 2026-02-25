---
name: traffic-audit
description: Audit network security, service mesh configuration, load balancing, and API gateway setup.
---

# Traffic Audit

Review network security posture, service mesh configuration, and traffic routing for the system.

## Steps

1. **Map traffic flow** — Identify all north-south (external) and east-west (internal) communication paths.

2. **Audit encryption**:
   - Invoke skill: `network-security-mesh` for zero-trust patterns
   - Verify TLS on all external endpoints
   - Verify mTLS between internal services
   - Check TLS version (must be 1.2+, prefer 1.3)

3. **Audit API gateway** — For external-facing services:
   - Authentication configured
   - Rate limiting enabled
   - Request validation in place
   - No business logic in gateway

4. **Audit load balancing**:
   - Health checks configured on all upstreams
   - Liveness and readiness probes defined
   - Graceful shutdown with connection draining

5. **Audit network policies**:
   - Invoke skill: `encryption-strategies` for encryption coverage
   - Services can only reach their dependencies (least privilege)
   - No flat network without policies

6. **Report findings** with severity and fix recommendations.

## Output Format

```markdown
## Traffic Audit

### Communication Map
| Source | Destination | Protocol | Encrypted | Authenticated |
|--------|-------------|----------|-----------|---------------|

### Findings
1. **[CRITICAL/HIGH/MEDIUM]** [Issue]
   - **Risk**: [What could go wrong]
   - **Fix**: [Specific recommendation]

### Network Policy Coverage
- Services with policies: [X/Y]
- Services without: [list]
```
