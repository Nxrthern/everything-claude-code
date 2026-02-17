# Data Resilience Rules

## Backups (CRITICAL)

Every data store MUST have:
- Automated backups (full weekly + incremental daily minimum)
- Point-in-time recovery enabled for databases
- Backups stored in a different region than primary
- Backup success monitored and alerted on failure
- Restore tested monthly in staging

## Failover

- RPO and RTO defined for every data store
- Critical data (payments, auth): synchronous replication, RPO = 0
- Failover mechanism tested quarterly
- Split-brain prevention in place (fencing or quorum)

## Data Lifecycle

- Retention policy defined for every data type
- Automated archival from hot → warm → cold → delete
- Grace period before permanent deletion
- Audit trail for data lifecycle transitions

## Storage

- Data tiered by access frequency (hot/warm/cold/archive)
- Lifecycle policies automated (not manual migration)
- Storage costs monitored monthly by service/team

## Reference

See skills: `resilience-backups`, `storage-tiers`, `data-management` for comprehensive patterns.
