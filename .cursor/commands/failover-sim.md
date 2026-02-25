---
name: failover-sim
description: Simulate and validate failover and disaster recovery readiness for all data stores and services.
---

# Failover Simulation

Validate disaster recovery readiness by auditing backup, replication, and failover configurations.

## Steps

1. **Inventory data stores** — List all databases, caches, queues, and object stores in the system.

2. **Audit backup coverage** — For each data store:
   - Invoke skill: `resilience-backups` for backup strategy patterns
   - Verify automated backups exist (full + incremental)
   - Check backup location (must be cross-region)
   - Check last successful backup and restore test date

3. **Audit replication** — For each critical data store:
   - Verify replication mode matches criticality (sync for zero-loss, async for speed)
   - Check replica lag
   - Verify failover mechanism (automatic vs manual)

4. **Assess recovery targets**:
   - Invoke skill: `storage-tiers` for tiering assessment
   - Verify RPO/RTO defined for each store
   - Compare actual recovery capability against targets

5. **Design failover drill** — Propose a failover test plan:
   - Invoke skill: `incident-analysis` for chaos experiment structure

6. **Report gaps** — Identify missing backups, untested recovery, and undefined RPO/RTO.

## Output Format

```markdown
## Failover Readiness Assessment

### Data Store Inventory
| Store | Type | Backup | Replication | RPO Target | RPO Actual | RTO Target | RTO Actual |
|-------|------|--------|-------------|-----------|-----------|-----------|-----------|

### Gaps
1. **[CRITICAL]** [Missing backup or failover]
2. **[HIGH]** [Untested recovery]

### Proposed Failover Drill
- [Scenario, method, expected result, abort conditions]
```
