---
name: advanced-concurrency
description: Advanced concurrency models, threading strategies, and parallel programming patterns. Use when working with goroutines, threads, async/await, worker pools, or any shared-state coordination.
---

# Advanced Concurrency Patterns

Concurrency is about structure; parallelism is about execution. Get the structure right, and safe parallelism follows.

## When to Activate

- Writing concurrent or parallel code
- Designing worker pools or task pipelines
- Coordinating shared state across goroutines/threads
- Debugging race conditions or deadlocks
- Choosing between concurrency models

## Core Principles

### 1. Share Nothing When Possible

The safest concurrent code shares no mutable state. Prefer:
1. Independent copies per goroutine/thread
2. Message passing (channels, queues)
3. Immutable shared data
4. Synchronized mutable data (last resort)

### 2. Concurrency Models

Choose the right model for the problem:

| Model | Best For | Trade-off |
|-------|----------|-----------|
| CSP (channels) | Pipeline stages, fan-out/fan-in | Channel management complexity |
| Actor model | Independent stateful entities | Message routing, mailbox overflow |
| Fork-join | CPU-bound parallel computation | Thread overhead for small tasks |
| Async/await | I/O-bound concurrent operations | Colored function problem |
| Worker pool | Bounded parallel task execution | Pool sizing, backpressure |

### 3. Design for Cancellation

Every concurrent operation must be cancellable:
```go
// ✅ Context-aware concurrency
func processItems(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)
    for _, item := range items {
        item := item
        g.Go(func() error {
            select {
            case <-ctx.Done():
                return ctx.Err()
            default:
                return process(ctx, item)
            }
        })
    }
    return g.Wait()
}
```

## Patterns

### Fan-Out / Fan-In
Distribute work across workers, collect results:
```go
func fanOutFanIn(ctx context.Context, items []Item, workers int) []Result {
    jobs := make(chan Item, len(items))
    results := make(chan Result, len(items))

    // Start workers
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for item := range jobs {
                results <- process(ctx, item)
            }
        }()
    }

    // Send jobs
    for _, item := range items {
        jobs <- item
    }
    close(jobs)

    // Collect results
    go func() {
        wg.Wait()
        close(results)
    }()

    var out []Result
    for r := range results {
        out = append(out, r)
    }
    return out
}
```

### Rate-Limited Worker Pool
Bound concurrency to prevent resource exhaustion:
```go
func rateLimitedPool(ctx context.Context, items []Item, maxConcurrent int) {
    sem := make(chan struct{}, maxConcurrent)
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)
        sem <- struct{}{} // acquire slot
        go func(it Item) {
            defer wg.Done()
            defer func() { <-sem }() // release slot
            process(ctx, it)
        }(item)
    }
    wg.Wait()
}
```

### Pipeline
Chain stages with channels:
```go
func pipeline(ctx context.Context, input <-chan Raw) <-chan Result {
    validated := validate(ctx, input)
    enriched := enrich(ctx, validated)
    return transform(ctx, enriched)
}
```

## Avoiding Common Bugs

### Race Conditions
```go
// ❌ Data race: shared counter without sync
var count int
for i := 0; i < 100; i++ {
    go func() { count++ }()
}

// ✅ Atomic operation
var count atomic.Int64
for i := 0; i < 100; i++ {
    go func() { count.Add(1) }()
}
```

### Deadlocks
```go
// ❌ Deadlock: inconsistent lock ordering
// Goroutine 1: Lock(A) → Lock(B)
// Goroutine 2: Lock(B) → Lock(A)

// ✅ Always acquire locks in consistent order
// Goroutine 1: Lock(A) → Lock(B)
// Goroutine 2: Lock(A) → Lock(B)
```

### Goroutine Leaks
```go
// ❌ Leaked goroutine: channel never read
ch := make(chan int)
go func() {
    ch <- expensiveComputation() // blocks forever if nobody reads
}()
// forgot to read from ch

// ✅ Use context for cancellation
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()
go func() {
    select {
    case ch <- expensiveComputation():
    case <-ctx.Done():
        return // clean exit
    }
}()
```

### False Sharing
```go
// ❌ Adjacent fields modified by different goroutines (same cache line)
type Counters struct {
    A int64
    B int64
}

// ✅ Pad to separate cache lines
type Counters struct {
    A int64
    _ [56]byte // padding to 64-byte cache line
    B int64
}
```

## Retry with Backoff and Jitter

Always use jitter to prevent thundering herd:
```go
func retryWithBackoff(ctx context.Context, fn func() error, maxRetries int) error {
    for attempt := 0; attempt <= maxRetries; attempt++ {
        if err := fn(); err == nil {
            return nil
        }
        if attempt == maxRetries {
            return fmt.Errorf("max retries exceeded")
        }
        // Exponential backoff with full jitter
        base := time.Duration(1<<uint(attempt)) * 100 * time.Millisecond
        jitter := time.Duration(rand.Int63n(int64(base)))
        select {
        case <-time.After(jitter):
        case <-ctx.Done():
            return ctx.Err()
        }
    }
    return nil
}
```

## Verification Checklist

- [ ] All shared mutable state is synchronized
- [ ] No goroutine/thread spawned without cancellation path
- [ ] Channel operations have timeout or context
- [ ] Lock ordering is consistent across all code paths
- [ ] Worker pools are bounded (not unbounded goroutine spawning)
- [ ] `go test -race` passes
- [ ] Resources are cleaned up on cancellation

---

**Remember**: If you have to choose between concurrent code that's clever and concurrent code that's obviously correct, always choose obviously correct.
