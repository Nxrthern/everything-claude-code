---
name: distributed-systems
description: Distributed system design patterns including consensus, partitioning, replication, and consistency models. Use when building multi-node systems, choosing data partitioning strategies, or reasoning about CAP trade-offs.
---

# Distributed Systems Patterns

Distributed systems fail in ways that monoliths can't. Design for the failures you know, and observe the ones you don't.

## When to Activate

- Designing systems that span multiple nodes or services
- Choosing consistency vs availability trade-offs
- Implementing data partitioning or replication
- Designing for network partitions and partial failures
- Evaluating distributed consensus requirements

## Fundamental Trade-offs

### CAP Theorem

You can have at most two of three during a network partition:
- **Consistency**: Every read receives the most recent write
- **Availability**: Every request receives a response
- **Partition tolerance**: System operates despite network splits

In practice, partitions happen — so you choose between CP and AP:
- **CP**: Reject requests during partition (databases, financial systems)
- **AP**: Serve potentially stale data during partition (caches, search indexes)

### PACELC Extension

When no partition (E), choose between Latency and Consistency:
- **PA/EL**: Available during partition, low latency otherwise (Cassandra, DynamoDB)
- **PC/EC**: Consistent always, higher latency (traditional RDBMS)
- **PA/EC**: Available during partition, consistent otherwise (most practical systems)

## Data Partitioning

### Strategies

| Strategy | Distribution | Range Queries | Reshuffling |
|----------|-------------|---------------|-------------|
| Hash-based | Even | Poor | Full reshuffle on node change |
| Range-based | Variable | Excellent | Move ranges only |
| Consistent hashing | Even | Poor | Minimal reshuffle |
| Directory-based | Configurable | Configurable | Lookup overhead |

### Consistent Hashing
Minimizes data movement when nodes join/leave:
- Hash both keys and nodes onto the same ring
- Keys map to next clockwise node
- Virtual nodes for better balance (100-200 vnodes per physical node)
- Only ~1/N of keys move when a node changes

### Hot Partition Detection
Signs of a hot partition:
- One node at high CPU while others are idle
- Uneven queue depths across partitions
- Latency percentiles differ significantly between partitions

Mitigation:
- Add salt to partition key for popular entities
- Split hot partitions into sub-partitions
- Cache hot partition data

## Replication

### Models

| Model | Writes | Read Scaling | Consistency | Failover |
|-------|--------|-------------|-------------|----------|
| Leader-follower | Single leader | Yes (followers) | Strong from leader | Promote follower |
| Multi-leader | Multiple | Yes | Conflict resolution needed | Automatic |
| Leaderless | Any node | Yes | Quorum-tunable | No single point |

### Quorum Reads/Writes
```
N = total replicas
W = write quorum
R = read quorum

Strong consistency when: W + R > N

Common configurations:
- N=3, W=2, R=2 (strong consistency, tolerates 1 failure)
- N=3, W=3, R=1 (fast reads, slow writes)
- N=3, W=1, R=3 (fast writes, slow reads)
```

## Consensus Patterns

### When You Need Consensus
- Leader election
- Distributed locking
- Sequence/ID generation
- Atomic broadcast (total order)

### When You Don't
- Eventual consistency is acceptable
- CRDTs can resolve conflicts
- Idempotent operations with at-least-once delivery

## Distributed Data Structures

| Structure | Use Case | Distributed Version |
|-----------|----------|-------------------|
| Hash map | Key-value lookup | Consistent-hashed distributed KV |
| Queue | Task distribution | Kafka partitions, SQS |
| Counter | Aggregation | CRDT G-Counter |
| Set | Membership | CRDT OR-Set, Bloom filter |
| Lock | Mutual exclusion | Redlock, ZooKeeper lock |

### Bloom Filters
Probabilistic membership test — "probably yes" or "definitely no":
- Use for: Cache existence checks, duplicate detection, spam filtering
- Space efficient: ~10 bits per element for 1% false positive rate
- Cannot remove elements (use counting Bloom filters instead)

## Failure Handling

### Partial Failure Strategies
```
If downstream is slow → timeout + circuit breaker
If downstream is down → fallback response + retry queue
If data is stale → serve stale + async refresh
If network partitions → degrade to local data + reconcile later
If leader fails → elect new leader + replay uncommitted
```

### Vector Clocks
Track causality across distributed nodes:
- Each node maintains a logical clock
- Compare clocks to detect concurrent writes
- Resolve conflicts with application logic or last-writer-wins

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| Shared database between services | Coupling, single point of failure | Service-owned data stores |
| Distributed transactions (2PC) | Blocking, coordinator failure | Saga pattern |
| Assuming clock synchronization | Data corruption, split brain | Logical clocks, NTP with bounds |
| No partition handling | System hangs on network issues | Timeouts, circuit breakers, fallbacks |
| Ignoring data locality | Cross-region latency | Partition data by access pattern |

---

**Remember**: A distributed system is one where a computer you didn't even know existed can cause your program to fail. Design every interaction assuming the network will betray you.
