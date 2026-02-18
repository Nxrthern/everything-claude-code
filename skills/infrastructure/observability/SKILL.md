---
name: observability
description: Monitoring, logging, metrics, and distributed tracing patterns. Use when instrumenting services, defining SLOs, designing dashboards, or building alerting systems.
---

# Observability Engineering

Observable systems answer "what is happening and why?" from their telemetry alone, without deploying new code.

## When to Activate

- Adding instrumentation to a service
- Defining SLOs, SLIs, or error budgets
- Designing dashboards or alerting rules
- Implementing distributed tracing
- Reviewing logging practices

## The Three Pillars

### 1. Metrics

Aggregated numerical measurements over time.

**RED Method** (request-driven services):
- **R**ate — Requests per second
- **E**rrors — Failed requests per second
- **D**uration — Latency distribution

**USE Method** (resources):
- **U**tilization — Percentage of resource used
- **S**aturation — Queue depth, pending work
- **E**rrors — Error count

**Naming Convention**:
```
{namespace}_{subsystem}_{name}_{unit}

# Examples
http_requests_total
http_request_duration_seconds
db_connections_active
cache_hit_ratio
queue_depth_messages
```

**Histogram Buckets** for latency:
```go
// Cover common latency ranges
buckets := []float64{0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10}
```

### 2. Logs

Structured event records for debugging.

**Rules**:
- ALWAYS structured (JSON), never free-text
- ALWAYS include: timestamp, level, service, trace_id, message
- NEVER log PII, passwords, tokens, or secrets
- Use levels correctly:
  - `DEBUG`: Developer diagnostics (not in production)
  - `INFO`: State transitions, business events
  - `WARN`: Recoverable issues, degraded operation
  - `ERROR`: Failures requiring attention
  - `FATAL`: Unrecoverable, service shutting down

**Structured Log Example**:
```go
logger.Info("order processed",
    "trace_id", ctx.TraceID(),
    "order_id", order.ID,
    "user_id", order.UserID,
    "amount", order.Total,
    "duration_ms", elapsed.Milliseconds(),
)
```

### 3. Traces

Request flow across service boundaries.

**Every trace should include**:
- Span per significant operation (HTTP call, DB query, cache lookup)
- Attributes for filtering (user ID, tenant, request type)
- Status and error details on failure spans
- Context propagation across all boundaries (HTTP headers, queue metadata)

```go
func processOrder(ctx context.Context, order Order) error {
    ctx, span := tracer.Start(ctx, "processOrder",
        trace.WithAttributes(
            attribute.String("order.id", order.ID),
            attribute.String("user.id", order.UserID),
        ),
    )
    defer span.End()

    // Downstream calls inherit trace context
    if err := validatePayment(ctx, order); err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, "payment validation failed")
        return err
    }
    return nil
}
```

## SLO Framework

### Define SLIs
Choose metrics that reflect user experience:

| Operation | SLI | Measurement |
|-----------|-----|-------------|
| API request | Latency | p99 request duration |
| API request | Availability | % of successful responses |
| Background job | Freshness | Time since last successful run |
| Data pipeline | Correctness | % of records processed without error |

### Set SLOs
```markdown
## SLO: API Availability
- **SLI**: Proportion of HTTP requests returning non-5xx status
- **Target**: 99.9% over 30-day rolling window
- **Error budget**: 0.1% = 43.2 minutes of downtime per month

## SLO: API Latency
- **SLI**: Proportion of requests completing in < 200ms
- **Target**: 99% of requests < 200ms (p99)
- **Error budget**: 1% of requests may exceed 200ms
```

### Burn Rate Alerting
Alert when consuming error budget too fast:
- 1-hour burn rate > 14.4x → page immediately (budget exhausted in 1 hour)
- 6-hour burn rate > 6x → page (budget exhausted in 6 hours)
- 3-day burn rate > 1x → ticket (on track to exhaust budget)

## Dashboard Design

### Service Health Dashboard
Every service dashboard must include:
1. Request rate (traffic)
2. Error rate (reliability)
3. Latency distribution (performance)
4. Saturation (CPU, memory, connections, queue depth)
5. SLO status and error budget remaining

### Layout Rules
- Most critical signals at top
- Time-series aligned to same time range
- Include annotations for deploys and incidents
- Link to runbooks from each panel

## Anti-Patterns

| Anti-Pattern | Impact | Fix |
|-------------|--------|-----|
| Unstructured logs | Unsearchable, no correlation | Structured JSON with trace IDs |
| Average-only metrics | Hidden tail latency | Use histograms with percentiles |
| Alert on every error | Alert fatigue, ignored pages | Alert on SLO burn rate |
| No trace propagation | Blind spots across services | Propagate context everywhere |
| Dashboard sprawl | Nobody checks 50 dashboards | One health dashboard per service |
| Monitoring infra only | No visibility into business impact | Add business metrics |

---

**Remember**: Observability is not a feature you add after launch. It's a design principle you build in from the start. If you can't see it, you can't fix it.
