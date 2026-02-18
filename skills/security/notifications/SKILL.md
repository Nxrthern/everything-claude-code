---
name: notifications
description: Alerting system design, notification routing, escalation policies, and multi-channel delivery patterns. Use when designing alerting pipelines, implementing notification systems, or configuring on-call escalation.
---

# Notification & Alerting Patterns

Good alerts wake you up for real problems. Bad alerts train you to ignore everything. Design for signal, not noise.

## When to Activate

- Designing alerting and notification systems
- Implementing multi-channel notification delivery
- Configuring on-call escalation policies
- Reducing alert fatigue
- Building user-facing notification systems

## Operational Alerting

### Alert Severity Levels

| Severity | Impact | Response | Channel | Example |
|----------|--------|----------|---------|---------|
| P1 Critical | Service down, data loss | Immediate (< 5 min) | Page + phone | Database unreachable |
| P2 High | Major feature degraded | 15 min | Page + Slack | Payment failures > 5% |
| P3 Medium | Performance degraded | 1 hour | Slack | p99 latency 3x normal |
| P4 Low | Minor issue | Next business day | Email/ticket | Dashboard slow |
| P5 Info | No action needed | None | Dashboard only | Deploy completed |

### Alert Design Rules

**Good alert**:
- Symptom-based (user impact), not cause-based
- Actionable — responder knows what to do
- Has runbook link
- Low false positive rate (< 5%)
- Fires at the right urgency level

**Bad alert**:
- CPU > 80% (so what? are users affected?)
- Any single error (noise)
- No runbook (what do I do at 3 AM?)
- Fires on every deploy (alert fatigue)

### Alert Template
```yaml
alert: HighErrorRate
expr: |
  rate(http_requests_total{status=~"5.."}[5m])
  / rate(http_requests_total[5m]) > 0.01
for: 5m
labels:
  severity: critical
  team: backend
annotations:
  summary: "Error rate > 1% for {{ $labels.service }}"
  runbook: "https://runbooks.internal/high-error-rate"
  dashboard: "https://grafana.internal/d/service-health"
  impact: "Users experiencing 5xx errors"
```

## Escalation Policies

```
Alert fires → Primary on-call (5 min to acknowledge)
    → No ack → Secondary on-call (5 min)
        → No ack → Engineering manager
            → No ack → VP Engineering

Override rules:
- P1: Skip to phone call immediately
- P2: Slack + page
- P3: Slack only (business hours)
- P4: Email/ticket only
```

### On-Call Best Practices
- Maximum 1 week rotation
- Maximum 2 pages per shift (average) — fix noisy alerts
- Handoff includes active incidents and context
- Post-shift debrief for recurring alerts
- Compensate on-call fairly

## Multi-Channel Notification Delivery

### Channel Selection

| Channel | Latency | Reliability | Use For |
|---------|---------|-------------|---------|
| Push notification | Seconds | Medium | Real-time user events |
| SMS | Seconds | High | Critical alerts, 2FA |
| Email | Minutes | High | Digests, receipts, reports |
| Slack/Teams | Seconds | Medium | Team collaboration, P3+ alerts |
| Phone call | Seconds | High | P1 critical only |
| In-app | Instant | High | Feature updates, actions needed |
| Webhook | Seconds | Medium | System-to-system integration |

### Delivery Architecture
```
Event → Notification Service → Priority Router
                                   │
                                   ├── P1: Phone + SMS + Slack + Email
                                   ├── P2: Slack + Email
                                   ├── P3: Slack (business hours) + Email
                                   └── P4: Email only

Deduplication: Unique key per event (prevent repeat sends)
Rate limiting: Max 3 notifications per user per hour (except P1)
Preferences: User opt-in per channel and category
```

### Idempotent Delivery
```go
// ✅ Prevent duplicate notifications
func sendNotification(ctx context.Context, n Notification) error {
    // Deduplicate by notification key
    sent, _ := store.IsSent(ctx, n.DeduplicationKey)
    if sent {
        return nil // already delivered
    }

    if err := deliverToChannels(ctx, n); err != nil {
        return err
    }

    store.MarkSent(ctx, n.DeduplicationKey, 24*time.Hour)
    return nil
}
```

## User Notification System

### User Preferences
```json
{
  "user_id": "usr_123",
  "preferences": {
    "order_updates": { "email": true, "push": true, "sms": false },
    "marketing":     { "email": true, "push": false, "sms": false },
    "security":      { "email": true, "push": true, "sms": true },
    "quiet_hours":   { "start": "22:00", "end": "08:00", "timezone": "Asia/Tokyo" }
  }
}
```

### Quiet Hours and Batching
- Respect user timezone for quiet hours
- Batch low-priority notifications (digest)
- Never suppress security alerts (login, password change)
- Allow snooze per notification category

## Anti-Patterns

| Anti-Pattern | Impact | Fix |
|-------------|--------|-----|
| Alert on every error | Alert fatigue, ignored pages | Alert on error rate, not count |
| No runbook on alert | Responder doesn't know what to do | Mandatory runbook link |
| Same severity for everything | True emergencies lost in noise | Tiered severity levels |
| No deduplication | Spam on repeated events | Unique key per notification |
| No user preferences | Users opt out entirely | Granular per-category control |
| Alerting without SLO context | Arbitrary thresholds | Alert on SLO burn rate |

---

**Remember**: Every unnecessary alert erodes trust in the alerting system. When everything is urgent, nothing is urgent. Be ruthless about alert quality — your on-call engineers' sleep depends on it.
