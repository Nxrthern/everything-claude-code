---
name: storage-tiers
description: Hot/warm/cold storage strategies, cost-performance trade-offs, and data migration policies. Use when designing storage architectures, optimizing storage costs, or implementing data lifecycle policies.
---

# Storage Tiering Strategies

Store data where the math works — fast and expensive for hot data, slow and cheap for cold. Automate the migration between.

## When to Activate

- Designing storage architecture for new systems
- Optimizing storage costs for large datasets
- Implementing data lifecycle and migration policies
- Choosing between storage classes (SSD, HDD, object, archive)
- Planning retention and archival strategies

## Storage Tiers

| Tier | Latency | Cost | Access Pattern | Example |
|------|---------|------|---------------|---------|
| Hot | < 10ms | $$$ | Frequent read/write | SSD, in-memory (Redis) |
| Warm | 10-100ms | $$ | Occasional read, rare write | Standard S3, HDD |
| Cold | 100ms-hours | $ | Rare read, no write | S3 Infrequent Access, GCS Nearline |
| Archive | Hours-days | ¢ | Near-never read | Glacier, GCS Archive |

## Tiering by Data Type

| Data Type | Hot | Warm | Cold | Delete |
|-----------|-----|------|------|--------|
| Active user data | While active | 90 days inactive | 1 year | Per policy/request |
| Transaction records | 30 days | 1 year | 7 years | After compliance period |
| Application logs | 7 days | 30 days | 1 year | After retention |
| Raw analytics events | 7 days | 30 days (aggregate) | Raw → cold at 90 days | Aggregated survives |
| Media/uploads | While referenced | 90 days unreferenced | 1 year | After grace period |
| Backups | Latest 7 days | 30 days | 1 year | Rolling window |

## Automatic Tiering

### S3 Lifecycle Policy
```json
{
  "Rules": [
    {
      "ID": "TierDownRule",
      "Status": "Enabled",
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER" }
      ],
      "Expiration": { "Days": 365 }
    }
  ]
}
```

### Intelligent Tiering
Use when access patterns are unpredictable:
- S3 Intelligent-Tiering monitors access and moves automatically
- No retrieval fees, small monitoring fee
- Good default for uncertain workloads

## Database Tiering

### Table Partitioning for Tiering
```sql
-- Hot: Current month on fast storage
-- Cold: Older partitions on cheaper storage

CREATE TABLE events (
    id BIGSERIAL,
    data JSONB,
    created_at TIMESTAMPTZ
) PARTITION BY RANGE (created_at);

-- Current month: fast tablespace
CREATE TABLE events_current PARTITION OF events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01')
    TABLESPACE fast_ssd;

-- Old data: slow tablespace
CREATE TABLE events_2026_01 PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01')
    TABLESPACE slow_hdd;
```

### Read Replicas for Tiering
- Primary: Handles writes and hot reads
- Read replica: Serves analytics and reporting queries
- Delayed replica: Serves historical queries and point-in-time lookups

## Cost Optimization Decisions

### Decision Framework
```
Is this data accessed daily?
  Yes → Hot tier
  No  → Is it accessed weekly?
    Yes → Warm tier
    No  → Is it needed for compliance?
      Yes → Cold tier with defined retention
      No  → Can it be deleted?
        Yes → Delete with grace period
        No  → Archive tier
```

### Cost Comparison (Typical Cloud)
```
Hot (SSD/S3 Standard):     $0.023/GB/month
Warm (S3 IA):              $0.0125/GB/month  (46% savings)
Cold (Glacier Instant):    $0.004/GB/month   (83% savings)
Archive (Glacier Deep):    $0.00099/GB/month (96% savings)

Example: 10TB dataset
  All hot:     $230/month
  Tiered:      $45/month (80% savings)
```

## Migration Patterns

### Online Migration (Zero Downtime)
```
1. Create new storage tier
2. Set up replication/sync from hot to warm
3. Verify data consistency
4. Update read path to check both tiers
5. Stop writing to old tier for migrated data
6. Clean up old tier after verification
```

### Bulk Migration
```
1. Snapshot hot data
2. Copy snapshot to cold tier (background job)
3. Verify integrity (checksums)
4. Update metadata to point to cold location
5. Delete from hot tier after grace period
```

## Anti-Patterns

| Anti-Pattern | Waste | Fix |
|-------------|-------|-----|
| Everything on hot storage | 80%+ cost wasted | Tier by access pattern |
| No lifecycle policy | Storage grows unbounded | Automate with rules |
| Manual migration | Error-prone, forgotten | Automate with lifecycle policies |
| Archive without index | Can't find archived data | Maintain metadata catalog |
| No retrieval cost estimate | Surprise bills on restore | Calculate before archiving |

---

**Remember**: Storage costs are a slow leak — small per-GB, massive at scale. The best time to set up tiering is when you design the system. The second best time is now.
