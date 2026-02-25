---
name: sharding-partitioning
description: Data sharding strategies, partitioning schemes, consistent hashing, and rebalancing patterns. Use when designing for horizontal data scaling, choosing shard keys, or planning data distribution across nodes.
---

# Sharding & Partitioning

Shard for scale. Partition for performance. Choose the key wisely — it's the hardest thing to change later.

## When to Activate

- Data volume exceeds single-node capacity
- Write throughput requires horizontal distribution
- Designing shard key selection for new systems
- Planning data rebalancing or resharding
- Optimizing query routing in sharded systems

## Sharding vs Partitioning

| Concept | Definition | Scope |
|---------|-----------|-------|
| Partitioning | Dividing a table into segments within one database | Single node |
| Sharding | Distributing data across multiple databases/nodes | Multiple nodes |

Both reduce the amount of data any single query must scan.

## Shard Key Selection

The shard key is the single most important decision in a sharded system:

### Good Shard Key Properties
- **High cardinality**: Millions of distinct values (avoids hotspots)
- **Even distribution**: Data spread uniformly across shards
- **Query-aligned**: Most queries include the shard key (avoid scatter-gather)
- **Immutable**: Key value doesn't change (avoids cross-shard migration)

### Common Shard Key Patterns

| Key | Good For | Risk |
|-----|----------|------|
| `tenant_id` | Multi-tenant SaaS | Large tenants create hotspots |
| `user_id` | User-centric apps | Celebrity users create hotspots |
| `hash(entity_id)` | Even distribution | No range queries |
| `region` | Geo-partitioning | Uneven population distribution |
| `(tenant_id, date)` | Composite: locality + time range | Complexity |

### Shard Key Anti-Patterns
- **Auto-increment ID**: All writes go to the last shard (sequential hotspot)
- **Timestamp alone**: All writes go to the current time shard
- **Low-cardinality field**: Country code (200 values for millions of shards)
- **Frequently updated field**: Forces cross-shard migration

## Sharding Strategies

### Hash-Based Sharding
```
shard_number = hash(shard_key) % total_shards

Pros: Even distribution
Cons: Adding shards requires rehashing ALL data
```

### Consistent Hashing
```
Nodes and keys hashed onto same ring (0 to 2^32)
Key → first node clockwise on ring

Pros: Adding/removing node moves only ~1/N of keys
Cons: Potential for uneven distribution
Fix:  Virtual nodes (100-200 vnodes per physical node)
```

### Range-Based Sharding
```
Shard 1: A-F
Shard 2: G-M
Shard 3: N-S
Shard 4: T-Z

Pros: Range queries stay on one shard
Cons: Uneven distribution (some ranges have more data)
Fix:  Dynamic range splitting when shard gets too large
```

### Directory-Based Sharding
```
Lookup table: key → shard mapping
  user_123 → shard_2
  user_456 → shard_1

Pros: Maximum flexibility, any mapping
Cons: Lookup table is SPOF, bottleneck
Fix:  Cache lookup table, replicate it
```

## Partition Strategies (Within a Database)

### Time-Based Partitioning
```sql
CREATE TABLE events (
    id BIGSERIAL,
    data JSONB,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_01 PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE events_2026_02 PARTITION OF events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
```

Benefits:
- Drop old partitions instantly (vs slow DELETE)
- Queries with time range only scan relevant partitions
- Different storage tiers per partition (hot/cold)

### List Partitioning
```sql
CREATE TABLE orders (
    id BIGSERIAL,
    region TEXT,
    data JSONB
) PARTITION BY LIST (region);

CREATE TABLE orders_us PARTITION OF orders FOR VALUES IN ('us-east', 'us-west');
CREATE TABLE orders_eu PARTITION OF orders FOR VALUES IN ('eu-west', 'eu-central');
CREATE TABLE orders_apac PARTITION OF orders FOR VALUES IN ('ap-northeast', 'ap-southeast');
```

## Cross-Shard Query Patterns

When queries span multiple shards:
- **Fan-out/gather**: Send query to all shards, merge results (expensive)
- **Global secondary index**: Maintain cross-shard index (consistency cost)
- **Denormalized lookup table**: Pre-computed cross-shard data (staleness)

Rule: Design so 90%+ of queries hit a single shard.

## Rebalancing

### Online Resharding (Zero Downtime)
```
1. Create new shard topology
2. Start dual-writing to old and new shards
3. Backfill historical data to new shards (background)
4. Verify data consistency (checksums)
5. Switch reads to new shard topology
6. Stop writes to old shards
7. Decommission old topology after verification
```

### Hotspot Mitigation
```
Detection: Monitor per-shard CPU, IOPS, queue depth
Mitigation:
  - Salt shard key: append random suffix to spread writes
  - Split hot shard: subdivide into 2-4 smaller shards
  - Write buffer: aggregate writes in memory, flush in batches
  - Cache hot reads: reduce read load on hot shard
```

## Verification Checklist

- [ ] Shard key has high cardinality and even distribution
- [ ] 90%+ of queries include the shard key
- [ ] Rebalancing plan documented for growth
- [ ] Cross-shard query patterns identified and minimized
- [ ] Hotspot monitoring in place
- [ ] Backup strategy covers all shards

---

**Remember**: Sharding solves scale problems but creates coordination problems. Every cross-shard operation is a distributed systems challenge. Choose your shard key to minimize those challenges.
