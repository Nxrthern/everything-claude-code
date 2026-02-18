---
name: query-optimization
description: Database query performance, indexing strategies, and query plan analysis. Use when writing SQL, designing indexes, investigating slow queries, or reviewing data access patterns.
---

# Query Optimization

Every query tells a story. Read the execution plan to understand what the database is actually doing, not what you asked it to do.

## When to Activate

- Writing or reviewing SQL queries
- Designing database indexes
- Investigating slow queries or timeouts
- Reviewing ORM-generated queries
- Planning schema for query patterns

## Indexing Strategies

### Index Types and Use Cases

| Index Type | Best For | Example |
|-----------|----------|---------|
| B-tree | Equality, range, sorting, prefix LIKE | `WHERE created_at > '2026-01-01'` |
| Hash | Equality only (exact match) | `WHERE id = 'abc123'` |
| GIN | Full-text, JSONB, arrays | `WHERE tags @> '{"go"}'` |
| GiST | Geospatial, range types | `WHERE location <@ box '...'` |
| Partial | Filtered subsets | `WHERE status = 'active'` (only index active rows) |
| Covering | Index-only scans | Include all selected columns in index |

### Composite Index Rules

Column order matters — follow the ESR rule:
1. **E**quality columns first (`WHERE status = 'active'`)
2. **S**ort columns next (`ORDER BY created_at`)
3. **R**ange columns last (`WHERE created_at > '2026-01-01'`)

```sql
-- Query: WHERE tenant_id = ? AND status = 'active' ORDER BY created_at DESC
-- ✅ Good index: (tenant_id, status, created_at DESC)
-- ❌ Bad index:  (created_at, tenant_id, status)
```

### When NOT to Index

- Columns with very low cardinality (boolean, status with 2-3 values) on small tables
- Tables with heavy write, light read patterns (indexes slow writes)
- Columns rarely used in WHERE, JOIN, or ORDER BY
- Temporary or staging tables

## Query Anti-Patterns

### N+1 Queries (CRITICAL)
```sql
-- ❌ N+1: One query per user's orders
for user_id in user_ids:
    SELECT * FROM orders WHERE user_id = ?

-- ✅ Batch: Single query for all
SELECT * FROM orders WHERE user_id IN (?, ?, ?, ...)

-- ✅ Join: Single query with relationship
SELECT u.name, o.total
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.id IN (?, ?, ?)
```

### SELECT * (HIGH)
```sql
-- ❌ Fetches all columns, prevents index-only scans
SELECT * FROM users WHERE tenant_id = ?

-- ✅ Fetch only needed columns
SELECT id, name, email FROM users WHERE tenant_id = ?
```

### Unbounded Queries (HIGH)
```sql
-- ❌ Returns entire table
SELECT * FROM events WHERE type = 'click'

-- ✅ Paginated with cursor
SELECT id, data FROM events
WHERE type = 'click' AND id > ?
ORDER BY id
LIMIT 100
```

### Implicit Type Casts (MEDIUM)
```sql
-- ❌ String compared to integer — index not used
SELECT * FROM users WHERE phone = 1234567890

-- ✅ Correct type
SELECT * FROM users WHERE phone = '1234567890'
```

### Functions on Indexed Columns (HIGH)
```sql
-- ❌ Index on created_at not used
SELECT * FROM orders WHERE DATE(created_at) = '2026-01-15'

-- ✅ Range query uses index
SELECT * FROM orders
WHERE created_at >= '2026-01-15' AND created_at < '2026-01-16'
```

## Reading Query Plans

### PostgreSQL EXPLAIN
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id)
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.tenant_id = 'abc'
GROUP BY u.name;
```

### Plan Node Guide
| Node | Meaning | Good/Bad |
|------|---------|----------|
| Seq Scan | Full table scan | Bad on large tables |
| Index Scan | B-tree lookup + heap fetch | Good |
| Index Only Scan | Answered from index alone | Best |
| Bitmap Index Scan | Index filter → heap | Good for many matching rows |
| Hash Join | Build hash, probe | Good for equality joins |
| Merge Join | Both sorted, merge | Good for large sorted sets |
| Nested Loop | Row-by-row | Good if outer is small |

### What to Look For
- **Seq Scan on large table** → Missing index
- **Estimated vs actual rows** far apart → Stale statistics, run ANALYZE
- **High buffers** → Large working set, may need more memory
- **Sort node** → Missing index for ORDER BY

## Connection and Query Hygiene

- Always use connection pooling (PgBouncer, HikariCP)
- Set statement timeout to prevent runaway queries
- Use prepared statements for repeated queries
- Close cursors and result sets promptly
- Monitor active connections vs pool size

## Verification Checklist

- [ ] Every WHERE clause column has an index (or justified absence)
- [ ] No N+1 query patterns in application code
- [ ] No `SELECT *` in production queries
- [ ] All list queries paginated with LIMIT
- [ ] Query plans reviewed for new or changed queries
- [ ] Connection pooling configured
- [ ] Statement timeout set

---

**Remember**: The database is smarter than you think — but only if you give it the right indexes and statistics. Let the planner do its job, then verify with EXPLAIN that it made the right choice.
