---
name: staff-review
description: Holistic staff-engineer-level review covering architecture, performance, reliability, observability, and security.
---

# Staff-Level Review

Perform a comprehensive staff-engineer review of the current codebase or recent changes.

## Steps

1. **Gather context** — Read `git diff` for recent changes, identify affected services and data flows.

2. **Architecture review** — Evaluate service boundaries, data ownership, coupling, and communication patterns.
   - Invoke skill: `distributed-systems` for multi-service patterns
   - Invoke skill: `staff-principles` for trade-off analysis

3. **Performance review** — Identify hot paths, N+1 queries, unbounded allocations, and missing caches.
   - Invoke skill: `advanced-performance` for profiling guidance
   - Invoke skill: `caching-queueing` for cache strategy

4. **Concurrency review** — Check shared state, synchronization, cancellation, and resource lifecycle.
   - Invoke skill: `advanced-concurrency` for patterns

5. **Reliability review** — Verify timeouts, retries, circuit breakers, graceful degradation, and health checks.
   - Invoke skill: `incident-analysis` for failure mode analysis

6. **Observability review** — Verify metrics, structured logging, tracing, and SLOs.
   - Invoke skill: `observability` for instrumentation standards

7. **Security review** — Check input validation, auth, secrets, and OWASP patterns.
   - Invoke skill: `security-review` for security checklist

8. **Report findings** — Use severity levels (CRITICAL/HIGH/MEDIUM/LOW). Include specific file locations, root cause, and fix recommendation for each finding.

## Output Format

```markdown
## Staff Review: [Scope]

### Summary
[1-2 sentence overview of the review scope and overall assessment]

### Architecture: [PASS/CONCERNS/FAIL]
- [Findings]

### Performance: [PASS/CONCERNS/FAIL]
- [Findings]

### Concurrency: [PASS/CONCERNS/FAIL]
- [Findings]

### Reliability: [PASS/CONCERNS/FAIL]
- [Findings]

### Observability: [PASS/CONCERNS/FAIL]
- [Findings]

### Security: [PASS/CONCERNS/FAIL]
- [Findings]

### Action Items
1. [CRITICAL] ...
2. [HIGH] ...
3. [MEDIUM] ...
```
