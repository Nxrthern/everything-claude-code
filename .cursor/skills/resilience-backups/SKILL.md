---
name: resilience-backups
description: Backup strategies, failover mechanisms, data replication, and disaster recovery patterns. Use when designing backup systems, planning failover, or implementing data replication for high availability.
---

# Resilience & Backup Strategies

A backup you haven't tested is a wish. A failover you haven't rehearsed is a gamble. Test both regularly.

## When to Activate

- Designing backup and restore strategies
- Implementing database replication and failover
- Planning disaster recovery procedures
- Setting RPO/RTO targets for data stores
- Configuring automated backup scheduling

## Backup Strategy

### Three Layers of Protection

| Layer | What | Frequency | Retention |
|-------|------|-----------|-----------|
| Full backup | Complete database dump | Weekly | 4 weeks |
| Incremental backup | Changes since last full | Daily | 2 weeks |
| Point-in-time recovery | WAL/binlog streaming | Continuous | 7 days |

### Backup Best Practices

```markdown
## Backup Checklist
- [ ] Automated (no manual steps)
- [ ] Encrypted at rest and in transit
- [ ] Stored in different region than primary
- [ ] Stored in different cloud account (ransomware protection)
- [ ] Retention policy enforced automatically
- [ ] Restore tested monthly to staging
- [ ] Backup success/failure monitored and alerted
- [ ] Restore time documented and verified
```

### PostgreSQL Example
```bash
# Full backup (pg_dump)
pg_dump -Fc -h $DB_HOST -U $DB_USER $DB_NAME > backup_$(date +%Y%m%d).dump

# Point-in-time recovery setup (WAL archiving)
# postgresql.conf
archive_mode = on
archive_command = 'aws s3 cp %p s3://backups/wal/%f'

# Restore to specific point in time
recovery_target_time = '2026-01-15 14:30:00'
```

## Replication Modes

| Mode | Data Loss | Latency Impact | Use Case |
|------|-----------|----------------|----------|
| Synchronous | Zero | Higher write latency | Financial data, auth |
| Semi-synchronous | Near-zero | Moderate | Important business data |
| Asynchronous | Possible (seconds) | None | Analytics, logs |
| Delayed replica | Minutes behind | None | Protection against bad writes |

### Failover Patterns

**Automatic failover** (preferred):
```
Health check detects primary failure
    → Promote replica to primary (< 30 seconds)
    → Update DNS/connection string
    → Notify operations team
    → Old primary becomes replica after recovery
```

**Manual failover** (for complex cases):
```
Operator detects issue
    → Verify primary is truly failed (avoid split-brain)
    → Promote designated replica
    → Redirect traffic
    → Verify data consistency
```

### Split-Brain Prevention
When both nodes think they're primary:
- Use fencing (STONITH) to shut down old primary
- Quorum-based decisions (odd number of voters)
- Lease-based leadership with short TTL

## Data Aggregation and Materialized Views

Reduce query load on live data:
```sql
-- Materialized view for dashboard
CREATE MATERIALIZED VIEW daily_order_summary AS
SELECT
    DATE(created_at) AS date,
    tenant_id,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount
FROM orders
GROUP BY DATE(created_at), tenant_id;

-- Refresh on schedule (not on every query)
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_order_summary;
```

## Data Rotation and Archival

### Partition-Based Rotation
```sql
-- Time-based partitioning for automatic rotation
CREATE TABLE events (
    id BIGSERIAL,
    data JSONB,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

-- Monthly partitions
CREATE TABLE events_2026_01 PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

-- Drop old partitions (instant, no vacuum needed)
DROP TABLE events_2025_01;
```

### TTL-Based Cleanup
```sql
-- Automated cleanup job
DELETE FROM sessions
WHERE expires_at < NOW() - INTERVAL '7 days';

-- For large tables, batch delete to avoid lock contention
DELETE FROM events
WHERE id IN (
    SELECT id FROM events
    WHERE created_at < NOW() - INTERVAL '90 days'
    LIMIT 10000
);
```

## Disaster Recovery Tiers

| Tier | RTO | RPO | Strategy | Cost |
|------|-----|-----|----------|------|
| Tier 1 | Minutes | Zero | Multi-AZ sync replication | $$$ |
| Tier 2 | < 1 hour | < 5 min | Cross-region async + PITR | $$ |
| Tier 3 | < 4 hours | < 1 hour | Daily backups + restore | $ |
| Tier 4 | < 24 hours | < 24 hours | Weekly backups | $ |

## Verification Checklist

- [ ] Every data store has automated backups
- [ ] Backups are encrypted and stored cross-region
- [ ] Restore procedure documented and tested monthly
- [ ] RPO/RTO defined for each data store
- [ ] Replication mode matches data criticality
- [ ] Failover tested in staging quarterly
- [ ] Backup monitoring with alerting on failure
- [ ] Data rotation/archival automated

---

**Remember**: Disaster recovery is not optional — it's the difference between "we lost a few seconds of data" and "we lost the company." Test your restores more often than you hope to use them.
