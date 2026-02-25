# Distributed Systems Rules

## Network Calls (CRITICAL)

Every external call MUST have:
1. **Timeout** — No unbounded waits, ever
2. **Retry with backoff** — Exponential backoff + jitter
3. **Circuit breaker** — Fail fast when downstream is unhealthy
4. **Context propagation** — Cancellation and tracing flow through

## Idempotency (CRITICAL)

All write operations MUST be idempotent:
- Use idempotency keys for mutations
- Design message handlers to be safely replayed
- Store processed IDs for deduplication

## Data Ownership

- Each service owns its data — no shared databases
- Cross-service data access via APIs or events, never direct DB queries
- Schema changes in one service must not break others

## Consistency

- Default to eventual consistency unless business rules require strong
- Document consistency model for every data flow
- Use sagas for distributed transactions, never two-phase commit

## Failure Handling

Every dependency failure must have a defined behavior:
- Slow dependency → timeout + fallback
- Down dependency → cached/default response
- Bad data → validation + dead letter queue
- Self failure → health check fails, traffic shifts

## Event Design

- Events are immutable facts, not commands
- Include: event_id, type, version, timestamp, source, correlation_id
- Consumers MUST be idempotent
- Dead letter queues for all consumers

## Reference

See skills: `distributed-systems`, `event-driven-architecture`, `advanced-networking` for comprehensive patterns.
