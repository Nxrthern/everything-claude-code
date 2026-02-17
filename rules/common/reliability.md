# Reliability Rules

## Resilience Patterns (CRITICAL)

Every service MUST implement:
1. **Timeouts** — On every external call, no exceptions
2. **Health checks** — Liveness and readiness probes
3. **Graceful shutdown** — Drain in-flight requests before exit

## Retry Strategy

ALWAYS:
- Exponential backoff with jitter
- Maximum retry count (3-5 attempts)
- Only retry transient failures (5xx, timeout), not permanent (4xx)
- Idempotent operations only

NEVER:
- Retry without backoff (thundering herd)
- Retry non-idempotent operations without idempotency key
- Retry indefinitely (use circuit breaker)

## Circuit Breakers

Required on any dependency that has failed in the past:
- **Closed**: Normal operation
- **Open**: Fail fast, return fallback
- **Half-open**: Probe with single request

## Graceful Degradation

When a dependency fails, the service MUST:
- Continue serving with reduced functionality (not crash)
- Return cached/default responses where possible
- Clearly indicate degraded state in health checks
- Log the degradation with appropriate severity

## Capacity

- Load test at 2x expected peak
- Auto-scaling configured for stateless services
- Resource limits set on all containers
- Connection pool sizes explicitly configured

## Deployment Safety

- Canary or blue-green deployment for production
- Automated rollback on health check failure
- Feature flags for risky changes
- No deployment during known high-traffic periods without approval

## Incident Readiness

- Runbooks for every alerting rule
- Severity classification documented
- Escalation paths defined
- Postmortem within 48 hours of SEV1/SEV2

## Reference

See skills: `incident-analysis`, `advanced-testing` (chaos testing), `platform-engineering` for comprehensive patterns.
