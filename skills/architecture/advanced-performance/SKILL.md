---
name: advanced-performance
description: Advanced performance profiling, optimization, and benchmarking. Use when analyzing hot paths, reducing tail latency, profiling CPU/memory, or establishing performance budgets.
---

# Advanced Performance Engineering

Systematic performance optimization grounded in measurement. Profile first, optimize second, benchmark always.

## When to Activate

- Analyzing or optimizing hot paths
- Investigating latency spikes or tail latency
- Profiling CPU, memory, or I/O usage
- Setting or enforcing performance budgets
- Reviewing code in latency-sensitive paths
- Preparing for load testing or capacity planning

## Core Principles

### 1. Measure Before Optimizing

Never optimize without a profile. Intuition about bottlenecks is wrong more often than it's right.

```
Workflow:
1. Define the metric (latency, throughput, memory)
2. Establish baseline with profiling
3. Identify the bottleneck from data
4. Apply targeted fix
5. Benchmark before and after
6. Check for regressions in other dimensions
```

### 2. Optimize the Right Level

Impact ranking — address in order:

| Level | Example | Typical Gain |
|-------|---------|-------------|
| Architecture | Eliminate unnecessary service call | 10-100x |
| Algorithm | O(n²) → O(n log n) | 10-1000x |
| Data structure | Map lookup vs linear scan | 10-100x |
| I/O pattern | Batch N+1 into single query | 5-50x |
| Memory | Pool allocations, reduce GC pressure | 2-10x |
| Micro | Loop unroll, branch prediction | 1.1-2x |

### 3. Percentiles Over Averages

Averages hide outliers. Always measure:
- **p50**: Median experience
- **p95**: Bad experience
- **p99**: Worst realistic experience
- **p99.9**: Tail that triggers alerts

## Profiling Techniques

### CPU Profiling

Identify where time is spent:

**Go**
```go
import "runtime/pprof"

f, _ := os.Create("cpu.prof")
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()
// ... code to profile ...
```

**Python**
```python
import cProfile
import pstats

with cProfile.Profile() as pr:
    # ... code to profile ...
    stats = pstats.Stats(pr)
    stats.sort_stats("cumulative")
    stats.print_stats(20)
```

### Memory Profiling

Identify allocation hotspots:

**Go**
```go
import "runtime/pprof"

f, _ := os.Create("mem.prof")
pprof.WriteHeapProfile(f)
```

**Python**
```python
import tracemalloc

tracemalloc.start()
# ... code to profile ...
snapshot = tracemalloc.take_snapshot()
top = snapshot.statistics("lineno")
for stat in top[:10]:
    print(stat)
```

### Flamegraph Analysis

Reading a flamegraph:
1. Width = time spent (wider = more time)
2. Read bottom-up (callers → callees)
3. Look for wide plateaus (the actual bottleneck)
4. Ignore narrow spikes (noise)

## Common Optimization Patterns

### Reduce Allocations
```go
// ❌ Allocates on every call
func process(items []Item) []Result {
    results := make([]Result, 0)
    for _, item := range items {
        results = append(results, transform(item))
    }
    return results
}

// ✅ Pre-allocate with known capacity
func process(items []Item) []Result {
    results := make([]Result, 0, len(items))
    for _, item := range items {
        results = append(results, transform(item))
    }
    return results
}
```

### Batch I/O Operations
```go
// ❌ N+1 queries
for _, id := range userIDs {
    user, _ := db.GetUser(ctx, id)
    users = append(users, user)
}

// ✅ Single batch query
users, _ := db.GetUsersByIDs(ctx, userIDs)
```

### Connection Pooling
```go
// ✅ Reuse connections
pool := &http.Client{
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        IdleConnTimeout:     90 * time.Second,
    },
}
```

### Lazy Evaluation
```go
// ❌ Compute everything upfront
func getReport() Report {
    summary := computeSummary()      // expensive
    details := computeDetails()      // expensive
    charts := renderCharts()         // expensive
    return Report{summary, details, charts}
}

// ✅ Compute on demand
func getReport() Report {
    return Report{
        Summary: func() Summary { return computeSummary() },
        Details: func() Details { return computeDetails() },
        Charts:  func() Charts { return renderCharts() },
    }
}
```

## Performance Budget Template

```markdown
## Service: [Name]

### Latency Budgets
| Endpoint | p50 | p95 | p99 |
|----------|-----|-----|-----|
| GET /api/items | 20ms | 50ms | 100ms |
| POST /api/items | 50ms | 100ms | 200ms |

### Resource Budgets
| Resource | Budget | Current |
|----------|--------|---------|
| Memory per instance | 512MB | [measure] |
| CPU per request | 10ms | [measure] |
| DB queries per request | 3 max | [measure] |
| Allocations per request | < 1KB | [measure] |

### Regression Gates
- CI fails if p95 latency regresses > 10%
- CI fails if memory usage regresses > 20%
- CI fails if allocation count increases > 50%
```

## Anti-Patterns

| Anti-Pattern | Impact | Fix |
|-------------|--------|-----|
| Optimize without profiling | Wasted effort on non-bottlenecks | Always profile first |
| N+1 queries | Linear DB roundtrips | Batch or join |
| Unbounded caches | OOM under load | Set max size + TTL |
| String concatenation in loops | O(n²) allocation | Use string builder |
| Regex compilation in loops | Redundant work | Compile once, reuse |
| Synchronous I/O in hot path | Thread starvation | Async or pool |
| Logging in hot path | I/O per operation | Sample or buffer |

---

**Remember**: The fastest code is code that doesn't run. Eliminate unnecessary work before optimizing necessary work.
