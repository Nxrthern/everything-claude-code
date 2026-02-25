---
name: staff-principles
description: Staff engineer leadership principles including business impact alignment, technical decision-making, evolutionary architecture, and cross-team influence. Use when making architectural decisions, evaluating trade-offs, or aligning technical work with business outcomes.
---

# Staff Engineer Principles

Staff engineers bridge technology and business. They make systems better, teams more effective, and decisions that compound over time.

## When to Activate

- Making architectural decisions with long-term implications
- Evaluating trade-offs between competing approaches
- Aligning technical work with business outcomes
- Planning migrations or evolutionary architecture changes
- Writing RFCs, ADRs, or technical strategy documents
- Mentoring teams on technical decision-making

## Core Principles

### 1. Business Impact First

Every technical decision should trace to business value:

```
Technical Decision → User Impact → Business Outcome

Examples:
- "Reduce p99 latency 500ms → 100ms" → "Users complete checkout 15% more often" → "$X revenue increase"
- "Migrate to event-driven" → "Features ship 2x faster" → "Faster time to market"
- "Add circuit breakers" → "Partial outage instead of total" → "99.95% availability vs 99.5%"
```

When proposing technical work, always articulate:
- **What** changes technically
- **Why** it matters to users/business
- **How much** effort vs expected return
- **When** the investment pays off

### 2. Reversibility Drives Decision Speed

| Decision Type | Speed | Example |
|--------------|-------|---------|
| Easily reversible | Decide fast, iterate | Library choice, API field name |
| Reversible with effort | Decide in days, prototype | Database index strategy, cache layer |
| Difficult to reverse | Decide carefully, RFC | Primary database, service boundary |
| Irreversible | Full consensus required | Data deletion, public API contract |

Spend decision time proportional to reversibility cost.

### 3. Simplicity is a Feature

Complexity is a silent tax on every future change:
- Prefer boring technology that the team knows
- Choose the simplest solution that meets requirements
- Add complexity only when measured need demands it
- Remove complexity as aggressively as you add features

### 4. Invariants Over Implementation

Define what must always be true, regardless of implementation:
```markdown
System Invariants:
- Every write operation is idempotent
- No user can access another user's data
- Balances never go negative
- Events are processed in causal order per entity
```

Invariants survive refactors. Implementation details don't.

## Evolutionary Architecture

### Strangler Fig Pattern
Migrate incrementally, not all at once:
```
Phase 1: Route 100% to old system, shadow to new (validate)
Phase 2: Route 10% to new system (canary)
Phase 3: Route 50/50 (parallel run)
Phase 4: Route 100% to new system
Phase 5: Decommission old system
```

### Backward Compatibility
Changes that don't break consumers:
- **Add** new fields (optional, with defaults)
- **Add** new endpoints or events
- **Add** new enum values (if consumers handle unknown)

Changes that break consumers (require migration):
- Remove or rename fields
- Change field types or semantics
- Remove endpoints or events
- Change validation rules to be stricter

### Migration Strategy
```markdown
## Migration: [From] → [To]

### Why
[Business justification]

### Approach
[Strangler fig / parallel run / big bang]

### Success Criteria
[How we know migration is complete]

### Rollback Plan
[How we revert if things go wrong]

### Timeline
- Week 1-2: [Phase]
- Week 3-4: [Phase]
- Week 5: [Validation and cutover]
```

## Technical Decision-Making

### RFC Template
```markdown
# RFC: [Title]

## Problem
[What problem are we solving? Why now?]

## Proposal
[What do we want to do?]

## Alternatives Considered
### Option A: [Name]
- Pros: [List]
- Cons: [List]
- Effort: [T-shirt size]

### Option B: [Name]
- Pros: [List]
- Cons: [List]
- Effort: [T-shirt size]

## Recommendation
[Which option and why]

## Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| [Risk] | [H/M/L] | [H/M/L] | [Plan] |

## Success Metrics
[How we measure success]

## Open Questions
[Unresolved items]
```

### Decision Criteria Hierarchy
When multiple options exist, evaluate in order:
1. **Correctness**: Does it solve the actual problem?
2. **Simplicity**: Is it the simplest correct solution?
3. **Operability**: Can we run and debug it in production?
4. **Performance**: Does it meet latency/throughput requirements?
5. **Cost**: Is the total cost (build + operate + maintain) reasonable?
6. **Extensibility**: Does it accommodate likely future needs?

## Technical Debt Management

### Debt Classification
| Type | Example | When to Pay |
|------|---------|-------------|
| Deliberate-prudent | "Ship now, refactor next sprint" | As scheduled |
| Deliberate-reckless | "We don't have time for tests" | Immediately |
| Inadvertent-prudent | "Now we know a better approach" | When area is next touched |
| Inadvertent-reckless | "What's a design pattern?" | Prioritize training |

### Debt Reduction Strategy
- Track debt as first-class work items
- Allocate 15-20% of each sprint to debt reduction
- Pay debt in the area you're already working in
- Measure: deployment frequency, change failure rate, time to recover

## Influence Without Authority

Staff engineers lead through influence, not title:
- **Write things down**: RFCs, ADRs, docs > verbal arguments
- **Show, don't tell**: Prototype > presentation
- **Build consensus gradually**: 1:1s before group meetings
- **Make the right thing easy**: Tooling, templates, examples
- **Measure and share results**: Data > opinions

---

**Remember**: The best technical decisions are the ones that make future decisions easier. Optimize for the long game — team velocity, system sustainability, and compounding returns.
