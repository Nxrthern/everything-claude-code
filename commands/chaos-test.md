---
name: chaos-test
description: Design and plan chaos engineering experiments to validate system resilience.
---

# Chaos Test Design

Design chaos engineering experiments for the current system.

## Steps

1. **Map dependencies** — Identify all external dependencies (databases, caches, APIs, queues, third-party services).

2. **Enumerate failure modes** — For each dependency:
   - What happens when it's unreachable?
   - What happens when it responds slowly (10x latency)?
   - What happens when it returns errors?
   - What happens when it returns corrupt data?

3. **Review resilience patterns** — Check that each failure mode has a handler:
   - Invoke skill: `distributed-systems` for failure handling patterns
   - Verify timeouts, retries, circuit breakers, fallbacks

4. **Design experiments** — For each unprotected failure mode, design a chaos experiment:
   - Invoke skill: `advanced-testing` for chaos testing methodology

5. **Prioritize** — Rank experiments by:
   - Severity of unhandled failure (user impact)
   - Likelihood of failure occurring
   - Ease of running experiment

6. **Define safety controls** — For each experiment:
   - Abort conditions (when to stop)
   - Blast radius (what's affected)
   - Kill switch (how to stop immediately)

## Output Format

```markdown
## Chaos Test Plan: [System]

### Dependency Map
| Dependency | Type | Current Resilience |
|-----------|------|-------------------|
| [Name] | [DB/Cache/API/Queue] | [Timeout/CB/Fallback/None] |

### Experiments (Priority Order)

#### Experiment 1: [Name]
- **Hypothesis**: When [failure], the system will [expected behavior]
- **Steady state**: [Normal metrics]
- **Method**: [How to inject failure]
- **Blast radius**: [What's affected]
- **Abort condition**: [When to stop]
- **Expected result**: [What should happen]

### Gaps Found
- [Resilience patterns missing]

### Recommendations
- [Changes needed before running experiments]
```
