---
name: data-management
description: Data quality, validation, integrity, and lifecycle management. Use when designing data pipelines, enforcing data contracts, auditing data quality, or managing data retention and cleanup.
---

# Data Management

Good data is correct, complete, consistent, and timely. Bad data propagates faster than good data can fix it.

## When to Activate

- Designing data ingestion or ETL pipelines
- Enforcing data contracts between services
- Auditing data quality and completeness
- Implementing data retention and archival policies
- Cleaning up duplicate or orphaned records

## Data Quality Dimensions

| Dimension | Definition | Measure |
|-----------|-----------|---------|
| Accuracy | Data reflects reality | Error rate on spot checks |
| Completeness | Required fields populated | NULL rate on mandatory columns |
| Consistency | Same fact, same value everywhere | Cross-system comparison |
| Timeliness | Data available when needed | Ingestion lag |
| Uniqueness | No unintended duplicates | Duplicate rate per entity |
| Validity | Data conforms to schema/rules | Validation failure rate |

## Validation Layers

### Layer 1: Schema Validation (at ingress)
```go
// ✅ Validate structure before processing
type OrderEvent struct {
    OrderID   string    `json:"order_id" validate:"required,uuid"`
    UserID    string    `json:"user_id" validate:"required"`
    Amount    float64   `json:"amount" validate:"required,gt=0"`
    Currency  string    `json:"currency" validate:"required,len=3"`
    CreatedAt time.Time `json:"created_at" validate:"required"`
}
```

### Layer 2: Business Rule Validation
```go
// ✅ Enforce business invariants
func validateOrder(order OrderEvent) error {
    if order.Amount > 100000 {
        return fmt.Errorf("order exceeds maximum: %.2f", order.Amount)
    }
    if order.CreatedAt.After(time.Now()) {
        return fmt.Errorf("order timestamp in future: %v", order.CreatedAt)
    }
    return nil
}
```

### Layer 3: Database Constraints (last line of defense)
```sql
ALTER TABLE orders ADD CONSTRAINT chk_amount CHECK (amount > 0);
ALTER TABLE orders ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE orders ADD CONSTRAINT uq_order_id UNIQUE (order_id);
```

## Idempotent Operations

Every data mutation must be safe to retry:

```sql
-- ✅ UPSERT: Idempotent insert
INSERT INTO user_profiles (user_id, name, updated_at)
VALUES ($1, $2, NOW())
ON CONFLICT (user_id) DO UPDATE
SET name = EXCLUDED.name, updated_at = EXCLUDED.updated_at;
```

```go
// ✅ Idempotent processing with dedup key
func processEvent(ctx context.Context, event Event) error {
    already, _ := store.IsProcessed(ctx, event.ID)
    if already {
        return nil // safe to skip
    }
    // process and mark as processed in one transaction
    return store.ProcessAndMark(ctx, event)
}
```

## Data Lifecycle Management

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Ingest  │ →  │ Validate │ →  │  Store   │ →  │ Archive  │ →  │  Delete  │
│          │    │ & Clean  │    │  (Hot)   │    │  (Cold)  │    │ (Expire) │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### Retention Policy Template
```markdown
| Data Type | Hot Period | Warm Period | Cold Period | Delete After |
|-----------|-----------|-------------|-------------|-------------|
| User data | Active use | 90 days inactive | 1 year | Per GDPR request |
| Transactions | 30 days | 1 year | 7 years | After retention |
| Logs | 7 days | 30 days | 1 year | After retention |
| Analytics | 30 days raw | Aggregated 1 year | — | Raw deleted |
| Audit trail | 1 year | 3 years | 7 years | Per compliance |
```

## Data Auditing

### Periodic Health Checks
```sql
-- Check for orphaned records
SELECT o.id FROM orders o
LEFT JOIN users u ON o.user_id = u.id
WHERE u.id IS NULL;

-- Check for duplicates
SELECT email, COUNT(*) FROM users
GROUP BY email HAVING COUNT(*) > 1;

-- Check for NULL required fields
SELECT COUNT(*) FROM orders WHERE amount IS NULL OR user_id IS NULL;
```

### Audit Trail Pattern
```sql
CREATE TABLE audit_log (
    id          BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id   VARCHAR(100) NOT NULL,
    action      VARCHAR(20) NOT NULL,  -- INSERT, UPDATE, DELETE
    old_value   JSONB,
    new_value   JSONB,
    changed_by  VARCHAR(100) NOT NULL,
    changed_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| No validation at ingress | Bad data propagates | Validate schema + rules at boundary |
| Trust upstream data | Garbage in, garbage out | Validate everything, trust nothing |
| No retention policy | Storage grows unbounded | Define and automate lifecycle |
| Soft delete without cleanup | Table bloat | Archive and hard-delete on schedule |
| No audit trail | Can't explain data changes | Log every mutation with who/when/what |

---

**Remember**: Data quality is not a feature — it's a foundation. Every system built on bad data inherits its problems. Validate at the boundary, constrain in the database, and audit continuously.
