# Query Performance Rules

## Indexing (CRITICAL)

- Every column in WHERE, JOIN, or ORDER BY on large tables MUST have an index (or justified absence)
- Composite indexes follow ESR order: Equality, Sort, Range
- No unused indexes — they slow writes for zero benefit

## Query Patterns (CRITICAL)

NEVER:
- `SELECT *` in application code — specify columns
- Queries inside loops (N+1) — batch or JOIN
- Unbounded queries without LIMIT — paginate everything
- Functions on indexed columns in WHERE — use range instead
- Leading wildcards (`LIKE '%term'`) — use full-text index

ALWAYS:
- Use parameterized queries (never string concatenation)
- Review EXPLAIN plan for new or changed queries
- Use connection pooling for all database access
- Set statement timeout to prevent runaway queries

## Pagination

All list queries MUST be paginated:
- Prefer cursor-based pagination (WHERE id > ? LIMIT N)
- Offset pagination only for small datasets
- Always return total count or has_next indicator

## Reference

See skills: `query-optimization`, `data-redundancy-search` for comprehensive patterns.
