# Observability Rules

## Instrumentation (CRITICAL)

Every service MUST emit:
1. **Metrics** — Request rate, error rate, latency (RED method)
2. **Structured logs** — JSON format with correlation IDs
3. **Traces** — Span per significant operation, context propagated

## Logging Standards

ALWAYS:
- Structured format (JSON)
- Include: timestamp, level, service, trace_id, message
- Use correct severity (DEBUG/INFO/WARN/ERROR/FATAL)

NEVER:
- Log PII, passwords, tokens, or secrets
- Use unstructured string concatenation
- Log at ERROR for expected conditions (use WARN)

## Metrics Standards

Naming convention: `{service}_{subsystem}_{name}_{unit}`

Required metrics per service:
- `http_request_duration_seconds` (histogram)
- `http_requests_total` (counter, by status code)
- `http_request_errors_total` (counter)
- Resource saturation (connections, memory, CPU)

## SLOs

Every user-facing service MUST define:
- **SLI**: Metric that measures user experience
- **SLO**: Target percentage over rolling window
- **Error budget**: Acceptable failure allowance

## Alerting

Good alerts are:
- **Actionable** — Someone can do something
- **Symptom-based** — Alert on user impact, not causes
- **Documented** — Links to runbook and dashboard
- **Low noise** — Less than 5% false positive rate

Bad alerts are:
- CPU > 80% (without user impact correlation)
- Any single error occurrence
- No runbook attached

## Reference

See skills: `observability`, `incident-analysis` for comprehensive patterns.
