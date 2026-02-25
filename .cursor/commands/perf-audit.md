---
name: perf-audit
description: Performance audit — profile, benchmark, and identify optimization opportunities in the codebase.
---

# Performance Audit

Systematic performance analysis of the codebase or recent changes.

## Steps

1. **Identify scope** — Which service, endpoint, or code path to audit? Focus on user-facing hot paths first.

2. **Check for common anti-patterns**:
   - N+1 queries (database calls inside loops)
   - Unbounded allocations (growing slices/lists without capacity)
   - Missing connection pools
   - Synchronous I/O in hot paths
   - Regex or reflection in tight loops
   - String concatenation in loops
   - Unbounded caches (no max size or TTL)

3. **Review data access patterns**:
   - Invoke skill: `caching-queueing` for cache opportunities
   - Invoke skill: `advanced-networking` for connection management
   - Check for missing indexes on queried columns
   - Check for over-fetching (SELECT * when few fields needed)

4. **Review concurrency patterns**:
   - Invoke skill: `advanced-concurrency` for parallel execution opportunities
   - Check for unnecessary serialization of independent work
   - Verify worker pool sizing

5. **Recommend profiling** — Suggest specific profiling commands for the language:
   - Invoke skill: `advanced-performance` for profiling techniques

6. **Propose performance budget** — Define targets for key metrics.

## Output Format

```markdown
## Performance Audit: [Scope]

### Current State
- [Known metrics or estimates]

### Findings
1. **[CRITICAL/HIGH/MEDIUM]** [Anti-pattern or bottleneck]
   - **Location**: [File:line]
   - **Impact**: [Estimated improvement]
   - **Fix**: [Specific recommendation]

### Profiling Recommendations
- [Commands to run for deeper analysis]

### Proposed Performance Budget
| Metric | Target |
|--------|--------|
| [Metric] | [Value] |
```
