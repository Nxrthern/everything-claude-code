---
name: event-driven-architecture
description: Event-driven system design including pub/sub, event sourcing, sagas, and streaming patterns. Use when designing loosely coupled systems, async workflows, or distributed transaction coordination.
---

# Event-Driven Architecture

Events represent facts that have happened. Build systems around facts, not commands.

## When to Activate

- Designing loosely coupled multi-service systems
- Implementing async workflows or notifications
- Coordinating distributed transactions
- Building event sourcing or CQRS systems
- Designing data pipelines or streaming architectures

## Core Concepts

### Event Types

| Type | Purpose | Example |
|------|---------|---------|
| Domain event | Something happened in the business | `OrderPlaced`, `UserRegistered` |
| Integration event | Cross-service notification | `PaymentCompleted`, `InventoryReserved` |
| Command event | Request for action | `ProcessPayment`, `SendEmail` |
| Change data capture | Database change stream | `users.row.updated` |

### Event Design

A well-designed event:
```json
{
  "event_id": "evt_abc123",
  "event_type": "order.placed",
  "version": 1,
  "timestamp": "2026-01-15T10:30:00Z",
  "source": "order-service",
  "correlation_id": "req_xyz789",
  "data": {
    "order_id": "ord_456",
    "user_id": "usr_789",
    "total_amount": 99.99,
    "currency": "USD"
  }
}
```

Rules:
- Immutable — events are facts, never modified
- Self-contained — consumer doesn't need to call back for context
- Versioned — schema changes don't break consumers
- Identified — unique ID for deduplication

## Delivery Guarantees

| Guarantee | Mechanism | Cost |
|-----------|-----------|------|
| At-most-once | Fire and forget | Simplest, may lose events |
| At-least-once | Ack after processing, retry on failure | Duplicates possible, consumer must be idempotent |
| Exactly-once | Idempotency key + transactional processing | Most complex, highest consistency |

### Idempotent Consumer Pattern
```go
func handleEvent(ctx context.Context, event Event) error {
    // Check if already processed
    processed, err := store.IsProcessed(ctx, event.ID)
    if err != nil {
        return err
    }
    if processed {
        return nil // safe to skip
    }

    // Process within transaction
    tx, err := db.Begin(ctx)
    if err != nil {
        return err
    }
    defer tx.Rollback()

    if err := processEvent(ctx, tx, event); err != nil {
        return err
    }

    // Mark as processed in same transaction
    if err := store.MarkProcessed(ctx, tx, event.ID); err != nil {
        return err
    }

    return tx.Commit()
}
```

## Saga Pattern

Coordinate multi-service workflows without distributed transactions:

### Choreography (Event-driven)
Each service reacts to events and emits next event:
```
OrderService: OrderPlaced →
PaymentService: PaymentProcessed →
InventoryService: InventoryReserved →
ShippingService: ShipmentScheduled
```

Compensation on failure:
```
ShippingService: ShipmentFailed →
InventoryService: InventoryReleased →
PaymentService: PaymentRefunded →
OrderService: OrderCancelled
```

### Orchestration (Coordinator)
Central orchestrator controls the flow:
```go
func (s *OrderSaga) Execute(ctx context.Context, order Order) error {
    // Step 1: Reserve payment
    if err := s.paymentSvc.Reserve(ctx, order); err != nil {
        return err
    }

    // Step 2: Reserve inventory
    if err := s.inventorySvc.Reserve(ctx, order); err != nil {
        s.paymentSvc.Release(ctx, order) // compensate
        return err
    }

    // Step 3: Confirm
    if err := s.paymentSvc.Confirm(ctx, order); err != nil {
        s.inventorySvc.Release(ctx, order) // compensate
        s.paymentSvc.Release(ctx, order)   // compensate
        return err
    }

    return nil
}
```

## Event Sourcing

Store state as a sequence of events, not a snapshot:

```go
// Events are the source of truth
type AccountEvent interface{}

type AccountOpened struct {
    AccountID string
    OwnerID   string
    OpenedAt  time.Time
}

type MoneyDeposited struct {
    AccountID string
    Amount    decimal.Decimal
    At        time.Time
}

// Rebuild state from events
func rebuildAccount(events []AccountEvent) Account {
    var account Account
    for _, event := range events {
        account = account.Apply(event)
    }
    return account
}
```

Benefits: Full audit trail, temporal queries, replay capability.
Trade-offs: Storage cost, projection complexity, eventual consistency.

## CQRS (Command Query Responsibility Segregation)

Separate write model from read model:
- **Write side**: Processes commands, validates, stores events
- **Read side**: Subscribes to events, builds optimized read projections

Use when read and write patterns differ significantly (e.g., complex writes, simple reads or vice versa).

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| Events as commands | Tight coupling through events | Events are facts, not instructions |
| Fat events with entire entity | Bandwidth, coupling | Include only changed fields + IDs |
| No schema versioning | Breaking consumers on changes | Version events, use compatible evolution |
| No dead letter queue | Poison messages block pipeline | Always configure DLQ |
| Synchronous event processing | Defeats the purpose | Process asynchronously |
| No correlation ID | Impossible to trace flows | Include correlation ID in every event |

## Verification Checklist

- [ ] Events are immutable and versioned
- [ ] Consumers are idempotent
- [ ] Dead letter queues configured for all consumers
- [ ] Correlation IDs flow through entire event chain
- [ ] Compensating actions defined for each saga step
- [ ] Schema evolution strategy documented
- [ ] Monitoring on consumer lag, DLQ depth, processing latency

---

**Remember**: Events are facts about what happened, not instructions about what to do. Design your events to be useful to consumers you haven't imagined yet.
