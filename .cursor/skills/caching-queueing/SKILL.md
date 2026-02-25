---
name: caching-queueing
description: Caching hierarchies, invalidation strategies, and message queue patterns. Use when implementing caches, choosing queue systems, handling backpressure, or designing async processing pipelines.
---

# Caching & Queueing Strategies

Cache the right things at the right level. Queue work to smooth load and decouple systems.

## When to Activate

- Adding or reviewing cache implementations
- Choosing between cache invalidation strategies
- Designing message queue or async processing systems
- Handling backpressure or overload protection
- Optimizing read-heavy or write-heavy workloads

## Caching

### Cache Hierarchy

Access from fastest to slowest:

| Layer | Latency | Capacity | Use Case |
|-------|---------|----------|----------|
| CPU cache (L1/L2/L3) | 1-10ns | KB-MB | Compiler/runtime managed |
| In-process (LRU map) | 10-100ns | MB | Hot data, per-instance |
| Distributed (Redis) | 0.5-2ms | GB | Shared across instances |
| CDN | 10-50ms | TB | Static assets, API responses |
| Database query cache | 1-10ms | GB | Repeated identical queries |

### Invalidation Strategies

| Strategy | Consistency | Complexity | Best For |
|----------|------------|------------|----------|
| TTL expiry | Eventual | Low | Data that can be stale briefly |
| Write-through | Strong | Medium | Critical data, low write volume |
| Write-behind | Eventual | High | High write volume, latency-sensitive |
| Cache-aside | Eventual | Low | General purpose, read-heavy |
| Event-driven | Near-real-time | Medium | Multi-service, event-sourced |

### Cache-Aside Pattern
```go
func getUser(ctx context.Context, id string) (*User, error) {
    // Check cache first
    if cached, err := cache.Get(ctx, "user:"+id); err == nil {
        return cached.(*User), nil
    }

    // Cache miss — load from database
    user, err := db.GetUser(ctx, id)
    if err != nil {
        return nil, err
    }

    // Populate cache with TTL
    cache.Set(ctx, "user:"+id, user, 5*time.Minute)
    return user, nil
}
```

### Preventing Cache Stampede
When a popular key expires, many requests hit the database simultaneously:
```go
// ✅ Use singleflight to coalesce concurrent requests
var group singleflight.Group

func getUser(ctx context.Context, id string) (*User, error) {
    if cached, err := cache.Get(ctx, "user:"+id); err == nil {
        return cached.(*User), nil
    }

    // Only one goroutine fetches; others wait for its result
    result, err, _ := group.Do("user:"+id, func() (interface{}, error) {
        user, err := db.GetUser(ctx, id)
        if err != nil {
            return nil, err
        }
        cache.Set(ctx, "user:"+id, user, 5*time.Minute)
        return user, nil
    })
    if err != nil {
        return nil, err
    }
    return result.(*User), nil
}
```

### Cache Key Design
```
// Pattern: {entity}:{id}:{version_or_variant}
"user:12345"
"user:12345:profile"
"search:query_hash:page_1"
"config:feature_flags:v3"
```

Rules:
- Keys are descriptive and namespaced
- Include version for schema changes
- Hash complex inputs (query params, filters)
- Set TTL on every key — no immortal cache entries

## Queueing

### Queue Selection Guide

| System | Best For | Throughput | Ordering |
|--------|----------|-----------|----------|
| Redis Streams | Simple queues, low-medium volume | Medium | Per-stream |
| Kafka | High-volume event streaming | Very high | Per-partition |
| NATS | Low-latency pub/sub | High | Per-subject |
| RabbitMQ | Complex routing, RPC patterns | Medium | Per-queue |
| SQS | Managed, serverless workloads | Medium | Best-effort |

### Backpressure Handling

Never let producers overwhelm consumers:

```go
// ✅ Bounded queue with rejection
func enqueue(ctx context.Context, queue chan<- Job, job Job) error {
    select {
    case queue <- job:
        return nil
    case <-ctx.Done():
        return ctx.Err()
    default:
        return ErrQueueFull // reject, don't block
    }
}
```

### Dead Letter Queue (DLQ)

Messages that fail repeatedly go to a DLQ for investigation:
```go
func processMessage(ctx context.Context, msg Message) error {
    if msg.RetryCount >= maxRetries {
        return dlq.Send(ctx, msg) // move to dead letter queue
    }

    if err := handle(ctx, msg); err != nil {
        msg.RetryCount++
        return queue.Requeue(ctx, msg, backoffDelay(msg.RetryCount))
    }
    return nil
}
```

### Consumer Patterns

**Competing consumers**: Multiple consumers share a queue for parallel processing.
**Partitioned consumers**: Each consumer owns a partition for ordering guarantees.
**Fan-out**: Each consumer gets a copy of every message.

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| Cache without TTL | Stale data forever | Always set TTL |
| Cache everything | Memory exhaustion | Cache hot data only, set max size |
| Delete-then-cache | Race condition window | Use cache-aside or write-through |
| Unbounded queue | OOM under load | Bounded queue + backpressure |
| No DLQ | Poison messages block processing | Always configure DLQ |
| Retry without backoff | Thundering herd on recovery | Exponential backoff with jitter |

## Verification Checklist

- [ ] Every cache entry has a TTL
- [ ] Cache max size is configured
- [ ] Cache stampede protection in place (singleflight or locking)
- [ ] Queue consumers are idempotent
- [ ] Dead letter queue configured
- [ ] Backpressure handled (reject or rate-limit, never block indefinitely)
- [ ] Cache key naming is consistent and namespaced

---

**Remember**: A cache that can't be invalidated is a bug factory. A queue without backpressure is a time bomb. Design both for the failure case, not just the happy path.
