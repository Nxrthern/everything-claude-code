---
name: deployment-strategies
description: Blue-green, canary, rolling, and feature flag deployment patterns for zero-downtime releases. Use when planning release strategies, implementing progressive delivery, or designing rollback mechanisms.
---

# Deployment Strategies

Every deployment is a controlled experiment. The question isn't "will it work?" but "how fast can we know if it doesn't, and how fast can we undo it?"

## When to Activate

- Planning a production release strategy
- Implementing blue-green or canary deployments
- Setting up feature flags for progressive delivery
- Designing rollback mechanisms
- Coordinating multi-service releases

## Strategy Comparison

| Strategy | Risk | Rollback Speed | Resource Cost | Complexity |
|----------|------|----------------|---------------|------------|
| Rolling update | Medium | Slow (re-deploy) | Low | Low |
| Blue-green | Low | Instant (switch) | 2x during deploy | Medium |
| Canary | Lowest | Fast (route shift) | +5-10% | High |
| Feature flag | Lowest | Instant (toggle) | None extra | Medium |
| Shadow/dark launch | None (no user impact) | N/A | 2x traffic | High |

## Blue-Green Deployment

Two identical environments; switch traffic atomically:

```
Before deploy:
  [Load Balancer] ──→ [Green: v1.0] ← serving traffic
                      [Blue:  idle]

During deploy:
  [Load Balancer] ──→ [Green: v1.0] ← still serving
                      [Blue:  v1.1] ← deploying, testing

After switch:
  [Load Balancer] ──→ [Blue:  v1.1] ← serving traffic
                      [Green: v1.0] ← standby for rollback

Rollback:
  [Load Balancer] ──→ [Green: v1.0] ← instant switch back
```

### When to Use
- Database schema is backward compatible
- Need instant rollback capability
- Can afford 2x compute during transition

## Canary Deployment

Route a small percentage of traffic to new version:

```
Phase 1:  [95% → v1.0]  [5% → v1.1]   Monitor 10 min
Phase 2:  [75% → v1.0]  [25% → v1.1]  Monitor 10 min
Phase 3:  [50% → v1.0]  [50% → v1.1]  Monitor 10 min
Phase 4:  [0%  → v1.0]  [100% → v1.1] Full rollout
```

### Canary Health Criteria
```yaml
# Auto-promote when ALL conditions met for 10 minutes:
promotion_criteria:
  error_rate: < baseline + 0.1%
  latency_p99: < baseline * 1.2
  saturation: < 80%
  custom_metric: < threshold

# Auto-rollback when ANY condition met:
rollback_criteria:
  error_rate: > baseline + 1%
  latency_p99: > baseline * 2
  health_check: failing
```

## Feature Flags

Decouple deployment from release:

```go
// Deploy code anytime; release to users when ready
func handleRequest(ctx context.Context, req Request) Response {
    if featureflags.IsEnabled(ctx, "new-checkout-flow", req.UserID) {
        return newCheckoutFlow(ctx, req)
    }
    return existingCheckoutFlow(ctx, req)
}
```

### Flag Lifecycle
```
Created → Testing (internal) → Canary (% rollout) → GA (100%) → Cleanup (remove flag)
```

### Flag Hygiene
- Every flag has an owner and expiration date
- Remove flags within 30 days of reaching 100%
- Never nest flags more than 2 levels deep
- Default to "off" for new features
- Audit stale flags monthly

## A/B Testing

Feature flags + metrics for data-driven decisions:
```
Hypothesis: "New checkout reduces cart abandonment"
  Control (A): existing flow    → 50% of users
  Variant (B): new flow         → 50% of users
  Metric: completion rate
  Duration: 2 weeks minimum
  Sample size: statistically significant (calculate upfront)
```

## Multi-Service Release Coordination

When services have dependencies:
```
Step 1: Deploy consumers (handle old AND new format)
Step 2: Verify consumers healthy
Step 3: Deploy producers (send new format)
Step 4: Verify integration healthy
Step 5: (Later) Remove old format handling from consumers
```

**Rule**: Never require simultaneous deployment of multiple services. Always maintain backward compatibility during transition.

## Database Migration Safety

```
Safe migration pattern:
1. Add new column (nullable or with default)     ← deploy schema
2. Backfill existing rows                          ← background job
3. Deploy code that reads/writes new column        ← code deploy
4. Verify all systems use new column
5. (Later) Remove old column                       ← separate deploy
```

**Never**: Drop column and deploy code in same release.

## Rollback Decision Matrix

| Signal | Action | Timeline |
|--------|--------|----------|
| Error rate > 2x baseline | Auto-rollback | Immediate |
| Latency p99 > 3x baseline | Auto-rollback | Immediate |
| Customer reports | Investigate, manual rollback if confirmed | < 15 min |
| Metric regression | Flag toggle or canary halt | < 5 min |
| Data corruption | Emergency rollback + incident response | Immediate |

## Verification Checklist

- [ ] Rollback plan documented and tested
- [ ] Feature flag wraps new behavior
- [ ] Health check updated for new functionality
- [ ] Monitoring covers new code paths
- [ ] Database migration is backward-compatible
- [ ] Canary criteria defined (promote and rollback)
- [ ] Multi-service release ordering documented

---

**Remember**: The goal of deployment is not to ship code — it's to deliver value to users safely. A fast rollback is worth more than a fast deploy.
