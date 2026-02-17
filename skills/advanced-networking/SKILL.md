---
name: advanced-networking
description: Network protocol optimization, connection management, and low-latency communication patterns. Use when designing APIs, managing connections, or optimizing network I/O for distributed systems.
---

# Advanced Networking

Every network call is an opportunity for failure, latency, and resource consumption. Minimize, batch, and protect every one.

## When to Activate

- Designing inter-service communication
- Optimizing API call patterns or payload sizes
- Implementing connection pooling or management
- Choosing between protocols (HTTP, gRPC, WebSocket)
- Debugging network latency or timeout issues

## Protocol Selection

| Protocol | Latency | Throughput | Use Case |
|----------|---------|-----------|----------|
| gRPC | Low | High | Service-to-service, streaming |
| HTTP/2 | Low-Medium | High | APIs, multiplexed connections |
| HTTP/3 (QUIC) | Low | High | Mobile, lossy networks |
| WebSocket | Very Low | Medium | Real-time bidirectional |
| TCP raw | Lowest | Highest | Custom protocols, max performance |
| UDP | Lowest | Highest | Metrics, logs, fire-and-forget |

### When to Use gRPC Over REST
- Internal service-to-service communication
- Streaming (server, client, or bidirectional)
- Strong typing with protobuf contracts
- Need for low latency and high throughput

### When to Use REST Over gRPC
- Public-facing APIs
- Browser clients without gRPC-Web
- Simple CRUD operations
- Team familiarity

## Connection Management

### Connection Pooling
Every external service must use connection pooling:

```go
// ✅ HTTP connection pool
client := &http.Client{
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        MaxConnsPerHost:     20,
        IdleConnTimeout:     90 * time.Second,
        TLSHandshakeTimeout: 10 * time.Second,
    },
    Timeout: 30 * time.Second,
}

// ✅ Database connection pool
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(10)
db.SetConnMaxLifetime(5 * time.Minute)
db.SetConnMaxIdleTime(1 * time.Minute)
```

### Connection Pool Sizing
```
Optimal pool size = (core_count * 2) + effective_spindle_count

For I/O-bound services: pool_size ≈ connections_needed_at_peak * 1.5
For CPU-bound services: pool_size ≈ num_CPUs + 1
```

Rules:
- Set max pool size (never unbounded)
- Set idle timeout (reclaim unused connections)
- Set max lifetime (prevent stale connections)
- Monitor pool exhaustion

## Request Optimization

### Batching
```go
// ❌ Individual requests
for _, id := range ids {
    result, _ := client.Get(ctx, "/api/items/"+id)
    results = append(results, result)
}

// ✅ Batch request
results, _ := client.Post(ctx, "/api/items/batch", BatchRequest{IDs: ids})
```

### Compression
```go
// ✅ Enable compression for payloads > 1KB
transport := &http.Transport{
    DisableCompression: false, // enable gzip
}

// For gRPC
grpc.WithDefaultCallOptions(grpc.UseCompressor("gzip"))
```

### Payload Optimization
- Send only needed fields (field masks, GraphQL)
- Use efficient serialization (protobuf > JSON > XML)
- Compress large payloads (gzip, zstd)
- Paginate list responses

## Timeout Strategy

Every network call needs a timeout. Layer timeouts from outer to inner:

```go
// ✅ Layered timeouts
// Overall request timeout
ctx, cancel := context.WithTimeout(ctx, 10*time.Second)
defer cancel()

// Connection timeout (subset of request timeout)
dialer := &net.Dialer{Timeout: 2 * time.Second}

// TLS handshake timeout
transport := &http.Transport{
    TLSHandshakeTimeout: 3 * time.Second,
    ResponseHeaderTimeout: 5 * time.Second,
}
```

Rules:
- Connection timeout < Request timeout
- Downstream timeout < Upstream timeout (leave room for retries)
- Always propagate context cancellation

## DNS and Service Discovery

- Cache DNS lookups (but respect TTL)
- Use connection pooling to amortize DNS cost
- Health-check-aware load balancing
- Circuit break unhealthy endpoints

## Anti-Patterns

| Anti-Pattern | Impact | Fix |
|-------------|--------|-----|
| No connection pooling | Connection overhead per request | Pool and reuse connections |
| No timeout | Hung connections, thread exhaustion | Timeout every external call |
| Unbounded connections | File descriptor exhaustion | Set max connections |
| No compression | Wasted bandwidth | Compress payloads > 1KB |
| Chatty protocols | Latency from round-trips | Batch, pipeline, or multiplex |
| Ignoring DNS TTL | Stale endpoints | Respect TTL, periodic refresh |
| Retry without circuit breaker | Amplify failures | Circuit break + backoff |

## Verification Checklist

- [ ] All external calls have explicit timeouts
- [ ] Connection pools configured with max size and idle timeout
- [ ] Large payloads compressed
- [ ] Batch APIs used where available
- [ ] Circuit breaker on unreliable dependencies
- [ ] Health checks for all downstream services
- [ ] Metrics on connection pool utilization

---

**Remember**: The network is not reliable, not fast, and not free. Every call you can eliminate, batch, or cache is a win for latency, cost, and reliability.
