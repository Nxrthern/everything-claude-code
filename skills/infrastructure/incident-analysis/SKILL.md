---
name: incident-analysis
description: Incident response, root cause analysis, and postmortem best practices. Use when responding to production incidents, writing postmortems, building runbooks, or designing incident management processes.
---

# Incident Analysis & Response

Incidents are learning opportunities. Respond fast, investigate thoroughly, and build systems that prevent recurrence.

## When to Activate

- Responding to a production incident
- Writing a postmortem after an outage
- Building runbooks for operational procedures
- Designing incident management processes
- Analyzing failure patterns across incidents

## Incident Response Framework

### Severity Classification

| Severity | User Impact | Response | Example |
|----------|------------|----------|---------|
| SEV1 | Total service outage | Immediate, all-hands | Database down, 100% error rate |
| SEV2 | Major feature broken | 15 min response | Payment processing failing |
| SEV3 | Degraded performance | 1 hour response | p99 latency 5x normal |
| SEV4 | Minor issue, workaround exists | Next business day | Dashboard slow to load |

### Response Roles

- **Incident Commander**: Coordinates response, makes decisions
- **Technical Lead**: Drives investigation and remediation
- **Communications Lead**: Updates stakeholders and status page
- **Scribe**: Records timeline and decisions in real-time

### Response Workflow

```
1. DETECT    → Alert fires or user report
2. TRIAGE    → Classify severity, assign roles
3. MITIGATE  → Stop the bleeding (rollback, failover, scale)
4. DIAGNOSE  → Find root cause from telemetry
5. RESOLVE   → Apply fix, verify recovery
6. FOLLOWUP  → Postmortem within 48 hours
```

**Key principle**: Mitigate first, diagnose second. Restore service before understanding why it broke.

## Root Cause Analysis

### The Five Whys

Dig past symptoms to systemic causes:
```
Why did the service go down?
→ The database ran out of connections.

Why did it run out of connections?
→ A new feature opened connections without closing them.

Why weren't connections closed?
→ The code path didn't use defer/finally for cleanup.

Why wasn't this caught?
→ No integration test for connection lifecycle.

Why was there no test?
→ Testing guidelines don't cover resource cleanup patterns.

Root cause: Missing testing standards for resource lifecycle management.
Action: Add resource cleanup to testing requirements and code review checklist.
```

### Contributing Factor Analysis

Root cause is rarely singular. Identify:
- **Trigger**: What initiated the incident (deploy, traffic spike, dependency failure)
- **Condition**: What made the system vulnerable (missing timeout, no circuit breaker)
- **Detection gap**: Why wasn't it caught earlier (no alert, alert fatigue, missing metric)
- **Recovery gap**: What slowed recovery (no runbook, unclear ownership, manual process)

## Postmortem Template

```markdown
# Incident Postmortem: [Title]

**Date**: [YYYY-MM-DD]
**Duration**: [Start time] → [End time] ([total duration])
**Severity**: [SEV1-4]
**Author**: [Name]
**Status**: [Draft | Review | Final]

## Summary
[2-3 sentences: What happened, who was affected, how was it resolved]

## Impact
- Users affected: [number or percentage]
- Duration of impact: [time]
- Revenue impact: [if applicable]
- Data loss: [if applicable]

## Timeline (all times UTC)
| Time | Event |
|------|-------|
| HH:MM | [First sign of trouble] |
| HH:MM | [Alert fired] |
| HH:MM | [Investigation began] |
| HH:MM | [Root cause identified] |
| HH:MM | [Mitigation applied] |
| HH:MM | [Service fully recovered] |

## Root Cause
[Technical explanation — blameless, focus on systems not people]

## Contributing Factors
1. [Factor that made the system vulnerable]
2. [Factor that delayed detection]
3. [Factor that slowed recovery]

## What Went Well
- [Effective response actions]
- [Systems that worked as designed]

## What Went Wrong
- [Systems or processes that failed]
- [Gaps in tooling or documentation]

## Action Items
| Action | Owner | Priority | Due Date | Status |
|--------|-------|----------|----------|--------|
| [Preventive fix] | [Who] | P0 | [When] | Open |
| [Detection improvement] | [Who] | P1 | [When] | Open |
| [Process improvement] | [Who] | P2 | [When] | Open |

## Lessons Learned
[Key takeaways for the broader organization]
```

## Runbook Template

```markdown
# Runbook: [Alert or Scenario Name]

## Overview
[What this alert means and typical causes]

## Severity
[How urgent is this?]

## Diagnosis Steps
1. Check [specific dashboard/metric]
2. Verify [component health]
3. Look for [common causes]

## Mitigation Steps
1. [Immediate action to reduce impact]
2. [Temporary fix or workaround]

## Resolution Steps
1. [Permanent fix procedure]
2. [Verification steps]

## Escalation
- [When to escalate]
- [Who to contact]

## Related
- Dashboard: [link]
- Previous incidents: [links]
```

## Incident Pattern Recognition

Track recurring themes across incidents:

| Pattern | Frequency | Systemic Fix |
|---------|-----------|-------------|
| Deploy-related outage | Weekly | Canary deploys, automated rollback |
| Dependency timeout cascade | Monthly | Circuit breakers, timeout tuning |
| Capacity exhaustion | Quarterly | Auto-scaling, capacity planning |
| Configuration error | Monthly | Config validation in CI, feature flags |
| Data migration issue | Per migration | Migration runbook, dry-run in staging |

## Blameless Culture Principles

- Focus on systems and processes, not individuals
- "How did the system allow this?" not "Who caused this?"
- Assume everyone acted with best intentions and available information
- The goal is learning and improvement, not punishment
- Share postmortems widely — transparency builds trust

---

**Remember**: Every incident is a gift — it reveals something about your system you didn't know. The only wasted incident is one you don't learn from.
