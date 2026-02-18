---
name: data-redundancy-search
description: Data normalization, deduplication, and search engine integration patterns. Use when reducing data redundancy, implementing full-text search, or choosing between document stores, wide-column, and relational databases.
---

# Data Redundancy & Searchability

Normalize to reduce redundancy. Denormalize to optimize reads. Index to make it searchable. Know when to use each.

## When to Activate

- Designing database schemas for new services
- Implementing full-text search or faceted search
- Choosing between relational, document, and wide-column stores
- Deduplicating data across systems
- Integrating search engines (Elasticsearch, OpenSearch)

## Normalization

### Normal Forms (Practical Guide)

| Form | Rule | Example |
|------|------|---------|
| 1NF | No repeating groups, atomic values | Split `tags: "go,rust"` → separate rows |
| 2NF | No partial dependencies | Move `user_name` out of `orders` table |
| 3NF | No transitive dependencies | Move `city, state` to `addresses` table |

### When to Normalize (OLTP)
- Transactional systems with frequent writes
- Data integrity is critical (single source of truth)
- Storage efficiency matters
- Relationships are complex and queryable

### When to Denormalize (OLAP/Read-heavy)
- Read-heavy workloads (dashboards, reports)
- Query performance > storage efficiency
- Data is append-only or rarely updated
- Materialized views for pre-computed aggregates

## Deduplication Strategies

### At Ingest
```sql
-- ✅ UPSERT: Insert or update on conflict
INSERT INTO events (id, type, data, created_at)
VALUES ($1, $2, $3, $4)
ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data;
```

### Unique Constraints
```sql
-- ✅ Database-enforced uniqueness
ALTER TABLE users ADD CONSTRAINT uq_users_email UNIQUE (email);

-- ✅ Composite uniqueness
ALTER TABLE order_items ADD CONSTRAINT uq_order_item
  UNIQUE (order_id, product_id);
```

### Probabilistic Deduplication
For high-volume streams where exact dedup is too expensive:
- **Bloom filter**: Fast "probably exists" check (Redis Bloom)
- **HyperLogLog**: Approximate distinct count
- **MinHash**: Near-duplicate detection for documents

## Search Engine Integration

### When to Use a Search Engine

| Need | Use | Not |
|------|-----|-----|
| Full-text search with relevance | Elasticsearch/OpenSearch | SQL LIKE '%term%' |
| Faceted search (filters + counts) | Elasticsearch/OpenSearch | Multiple COUNT queries |
| Autocomplete/suggest | Elasticsearch completion | Application-level filtering |
| Simple exact match | Database index | Search engine (overkill) |
| Geospatial search | Elasticsearch or PostGIS | Neither alone for complex |

### Elasticsearch/OpenSearch Patterns

```json
// Index mapping with analyzers
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "status": { "type": "keyword" },
      "created_at": { "type": "date" },
      "tags": { "type": "keyword" }
    }
  }
}
```

### Sync Strategy
Keep search index in sync with primary database:
- **Change Data Capture**: Stream DB changes to search (Debezium)
- **Dual write**: Write to both (risk of inconsistency)
- **Event-driven**: Publish events, consumer updates index
- **Periodic reindex**: Full rebuild on schedule (simplest, highest lag)

Prefer CDC or event-driven over dual write.

## Database Selection Guide

| Workload | Best Fit | Why |
|----------|----------|-----|
| Transactional, relational | PostgreSQL, MySQL | ACID, joins, constraints |
| Document-oriented, flexible schema | MongoDB | Nested documents, schema evolution |
| Wide-column, massive scale | Cassandra, ScyllaDB | Write throughput, linear scaling |
| Time-series | TimescaleDB, InfluxDB | Time-based partitioning, retention |
| Graph relationships | Neo4j, Neptune | Traversal queries |
| Key-value, low latency | Redis, DynamoDB | Sub-millisecond lookups |
| Full-text search | Elasticsearch, OpenSearch | Relevance scoring, analyzers |

## Anti-Patterns

| Anti-Pattern | Impact | Fix |
|-------------|--------|-----|
| SQL LIKE '%term%' for search | Full table scan, no relevance | Use search engine |
| Storing CSV in a column | Breaks 1NF, unqueryable | Normalize to rows |
| No unique constraints | Silent duplicates | Add constraints + UPSERT |
| Search index as source of truth | Data loss risk | DB is source, index is projection |
| Over-normalization | Too many JOINs, slow reads | Denormalize hot read paths |

## Verification Checklist

- [ ] Primary database enforces uniqueness constraints
- [ ] Deduplication strategy defined for each ingest path
- [ ] Search engine synced via CDC or events (not dual write)
- [ ] Schema normalization level matches workload (OLTP vs OLAP)
- [ ] Full-text search uses proper analyzers, not SQL LIKE

---

**Remember**: The database is for truth. The search engine is for discovery. Keep them in sync, but never confuse their roles.
