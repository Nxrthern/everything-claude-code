# Data Scaling Rules

## Sharding

When data exceeds single-node capacity:
- Shard key MUST have high cardinality and even distribution
- 90%+ of queries MUST include the shard key
- Cross-shard queries documented and minimized
- Rebalancing plan documented before sharding
- Hotspot monitoring in place

## Partitioning

- Time-series data MUST use time-based partitioning
- Old partitions archived or dropped (not deleted row-by-row)
- Partition key aligns with most common query filter

## Multi-Region Data

- PII stays in compliance zone (GDPR, APPI)
- No synchronous cross-region calls in user request path
- Global data (catalog, config) replicated to all regions
- Data residency documented per data type

## Search

- Full-text search uses search engine (Elasticsearch/OpenSearch), not SQL LIKE
- Search index synced via CDC or events (not dual write)
- Database is source of truth, search engine is projection

## Deduplication

- Unique constraints on identity columns
- UPSERT for idempotent writes
- Bloom filters for high-volume probabilistic dedup

## Reference

See skills: `sharding-partitioning`, `data-redundancy-search`, `multi-cloud-region` for comprehensive patterns.
