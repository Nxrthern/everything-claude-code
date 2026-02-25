---
name: multi-cloud-region
description: Multi-region and multi-cloud architecture patterns. Use when designing globally distributed systems, optimizing for regional latency, ensuring data residency compliance, or planning cross-region disaster recovery.
---

# Multi-Cloud & Multi-Region Architecture

Design for regional independence. Communicate across regions as little as possible, and never synchronously in the critical path.

## When to Activate

- Designing globally distributed systems
- Optimizing latency for geographically dispersed users
- Ensuring data residency compliance (GDPR, data sovereignty)
- Planning cross-region disaster recovery
- Evaluating multi-cloud strategies

## Multi-Region Patterns

### Active-Active (All Regions Serving)
```
Users → DNS (geo-routing) → Nearest Region
                              ├── Region A (full stack)
                              ├── Region B (full stack)
                              └── Region C (full stack)

Inter-region: Async replication for data consistency
```

**When to use**: Global user base, latency-sensitive, high availability required.
**Trade-off**: Conflict resolution needed, eventual consistency between regions.

### Active-Passive (Primary + DR)
```
Users → Region A (primary, serves all traffic)
          └── Async replication → Region B (standby, no traffic)

Failover: DNS switch to Region B on Region A failure
```

**When to use**: Cost-sensitive, compliance requires DR, not latency-sensitive.
**Trade-off**: Failover delay (DNS propagation), Region B resources underutilized.

### Follow-the-Sun
```
Peak hours:   Route to local region
Off-peak:     Route to cheapest region or scale down

Region A: Active 06:00-18:00 local
Region B: Active 06:00-18:00 local (12h offset)
```

**When to use**: Cost optimization for time-zone-dependent traffic.

## Data Residency and Compliance

### Zone Sharding
Partition data by regulatory zone:
```
EU users     → eu-west-1 (GDPR compliance)
US users     → us-east-1 (SOX compliance)
APAC users   → ap-northeast-1 (APPI compliance)
```

Rules:
- User data stays in compliance zone
- Cross-zone queries routed to correct zone
- Metadata (non-PII) can be global
- Audit trail for any cross-zone data access

### Global vs Regional Data
| Data Type | Scope | Replication |
|-----------|-------|-------------|
| User PII | Regional (compliance zone) | No cross-region |
| Product catalog | Global | Replicate everywhere |
| Session data | Regional | No cross-region |
| Config/feature flags | Global | Replicate everywhere |
| Analytics (aggregated) | Global | Replicate from regional |

## Latency Optimization

### Proximity Routing
- DNS-based: Route53 latency routing, CloudFlare geo
- Anycast: Single IP, network routes to nearest PoP
- CDN: Cache static content at edge locations
- Edge compute: Run logic at edge (CloudFlare Workers, Lambda@Edge)

### Cross-Region Communication Rules
- **NEVER** synchronous calls across regions in user request path
- **PREFER** async replication for data sync between regions
- **CACHE** remote data locally with TTL for read-heavy access
- **BATCH** cross-region operations to reduce round-trip overhead
- **MEASURE** inter-region latency (typically 50-200ms depending on distance)

## Multi-Cloud Considerations

### When Multi-Cloud Makes Sense
- Regulatory requirement for vendor diversity
- Best-of-breed services from different providers
- Negotiating leverage on pricing
- Avoiding vendor lock-in for critical components

### When It Doesn't
- Small team without deep expertise in multiple clouds
- Tightly integrated stack (e.g., all-in on AWS services)
- Complexity cost outweighs vendor-risk mitigation

### Multi-Cloud Abstraction Layers
| Layer | Use Agnostic Tool | Not |
|-------|-------------------|-----|
| Infrastructure | Terraform/Pulumi | Cloud-specific CLI |
| Containers | Kubernetes | ECS, Cloud Run alone |
| Secrets | HashiCorp Vault | AWS SSM alone |
| Monitoring | Datadog, Grafana | CloudWatch alone |
| Storage | S3-compatible API | Provider-specific API |

## Anti-Patterns

| Anti-Pattern | Impact | Fix |
|-------------|--------|-----|
| Synchronous cross-region calls | 100-200ms added latency | Async replication, local cache |
| Global database, single region | Single point of failure | Regional replicas or multi-master |
| No data residency plan | Compliance violation | Zone shard PII data |
| Tight coupling to one cloud | Vendor lock-in | Abstract with agnostic tools |
| Same failover region as primary | Both fail in regional outage | Use geographically distant DR |

---

**Remember**: Multi-region is a trade-off between latency, consistency, and cost. Start with a clear answer to "what happens when a region goes down?" and design backward from there.
