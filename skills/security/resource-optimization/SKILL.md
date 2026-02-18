---
name: resource-optimization
description: Memory, CPU, cloud cost, and token efficiency optimization. Use when reducing resource consumption, right-sizing infrastructure, or optimizing for operational cost.
---

# Resource Optimization

Every resource has a cost — compute, memory, network, storage, and engineering time. Optimize the most expensive constraint first.

## When to Activate

- Reducing memory or CPU consumption
- Right-sizing cloud infrastructure
- Optimizing storage costs and data lifecycle
- Reducing API/token costs for LLM usage
- Improving build and CI/CD resource efficiency

## Memory Optimization

### Reduce Allocations

```go
// ❌ Allocates new slice per call
func getNames(users []User) []string {
    var names []string
    for _, u := range users {
        names = append(names, u.Name)
    }
    return names
}

// ✅ Pre-allocate with known capacity
func getNames(users []User) []string {
    names := make([]string, 0, len(users))
    for _, u := range users {
        names = append(names, u.Name)
    }
    return names
}
```

### Object Pooling
Reuse expensive objects instead of creating/destroying:
```go
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

func processRequest(data []byte) []byte {
    buf := bufferPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufferPool.Put(buf)
    }()
    // use buf...
    return buf.Bytes()
}
```

### Memory Budget Guidelines

| Component | Budget | Action if Exceeded |
|-----------|--------|--------------------|
| Per-request allocation | < 1KB | Profile allocations |
| In-memory cache | < 25% of container memory | Set max size + eviction |
| Working set | < 60% of container memory | Scale or optimize |
| Container memory limit | 2x average usage | Monitor and tune |

## CPU Optimization

### Reduce Computation

Priority order:
1. **Eliminate**: Don't compute what isn't needed
2. **Cache**: Don't recompute what hasn't changed
3. **Batch**: Amortize fixed overhead across items
4. **Parallelize**: Use available cores for independent work
5. **Optimize**: Improve the algorithm/implementation

### CPU Budget Guidelines

| Metric | Target | Tool |
|--------|--------|------|
| Handler CPU per request | < 10ms | CPU profiler |
| Idle CPU | < 10% | Monitoring |
| Peak CPU | < 70% (headroom) | Load testing |
| GC pause | < 1ms p99 | GC metrics |

## Cloud Cost Optimization

### Compute Costs

```markdown
## Right-Sizing Checklist
- [ ] Average CPU utilization > 20% (otherwise downsize)
- [ ] Average memory utilization > 40% (otherwise downsize)
- [ ] Spot instances for stateless, fault-tolerant workloads
- [ ] Reserved instances for steady-state baseline load
- [ ] Auto-scaling configured (scale down, not just up)
- [ ] Dev/staging environments scale to zero outside business hours
```

### Storage Costs

```markdown
## Storage Tiering
- Hot: Frequently accessed (< 30 days) → SSD/standard
- Warm: Occasional access (30-90 days) → Infrequent access tier
- Cold: Rare access (90+ days) → Glacier/Archive
- Delete: Expired data → Lifecycle policy auto-delete

## Data Lifecycle Policy
- Logs: 30 days hot, 90 days warm, 1 year cold, delete
- Backups: 7 days hot, 30 days warm, 1 year cold
- User data: Hot while active, warm after 90 days inactive
- Analytics: Aggregate after 30 days, raw → cold after 90
```

### Network Costs

- Minimize cross-region traffic (co-locate services)
- Use CDN for static assets
- Compress responses > 1KB
- Batch API calls to reduce request overhead
- Use VPC endpoints instead of public internet for cloud services

## Token and API Cost Optimization

For LLM and external API usage:

### Prompt Optimization
- Cache common prompt templates
- Use smaller models for simpler tasks
- Batch related requests when possible
- Truncate context to relevant portions
- Use structured output to reduce response tokens

### API Call Reduction
```go
// ❌ Separate calls
result1 := api.GetUser(id)
result2 := api.GetUserPrefs(id)
result3 := api.GetUserHistory(id)

// ✅ Batch or combined endpoint
result := api.GetUserFull(id) // single call
```

## Build and CI Optimization

### Build Speed
| Strategy | Improvement | Effort |
|----------|------------|--------|
| Dependency caching | 30-60% faster | Low |
| Parallel test execution | 40-70% faster | Low |
| Incremental builds | 50-80% faster | Medium |
| Build artifact caching | 30-50% faster | Low |
| Smaller Docker base images | 20-40% faster push/pull | Low |

### CI Cost Reduction
- Cache Docker layers between builds
- Skip unchanged service builds in monorepo
- Use smaller CI runners for lint/format steps
- Auto-cancel superseded PR builds
- Run expensive tests only on merge, not every push

## Monitoring Resource Usage

### Key Metrics to Track

```markdown
## Resource Dashboard
- CPU utilization (avg, p95, peak) per service
- Memory utilization (RSS, heap, GC) per service
- Network I/O (bytes in/out, connection count)
- Disk I/O (read/write IOPS, latency)
- Cloud spend (daily, by service, by team)
- API/token costs (daily, by use case)
```

### Alerting Thresholds
- CPU sustained > 70% for 5 min → scale up or optimize
- Memory > 80% of limit → risk of OOM
- Disk > 85% → risk of write failures
- Monthly cost > 120% of budget → investigate anomaly

## Anti-Patterns

| Anti-Pattern | Waste | Fix |
|-------------|-------|-----|
| Over-provisioned instances | 40-60% spend wasted | Right-size quarterly |
| Always-on dev environments | 70% of hours unused | Scale to zero off-hours |
| Uncompressed transfers | Bandwidth cost | Compress > 1KB |
| Immortal data | Storage grows forever | Lifecycle policies |
| Over-logging | Storage + processing cost | Log sampling, appropriate levels |

---

**Remember**: The cheapest resource is the one you don't use. Eliminate waste before optimizing usage. Small savings per request compound into large savings at scale.
