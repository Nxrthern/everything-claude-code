---
name: network-security-mesh
description: API gateways, service mesh, mTLS, load balancing, and zero-trust networking patterns. Use when designing service-to-service communication, implementing security at the network layer, or choosing load balancing strategies.
---

# Network Security & Service Mesh

North-south traffic gets a gateway. East-west traffic gets a mesh. Everything gets mutual TLS.

## When to Activate

- Designing API gateway configuration
- Implementing service mesh (Istio, Linkerd)
- Configuring load balancing strategies
- Implementing zero-trust networking
- Securing service-to-service communication

## Traffic Patterns

### North-South (External → Internal)
```
Client → API Gateway → Service
         │
         ├── Authentication (JWT, API key)
         ├── Rate limiting
         ├── Request validation
         ├── TLS termination
         └── Routing
```

**Tools**: Kong, Envoy, AWS API Gateway, Traefik

### East-West (Service → Service)
```
Service A → Sidecar Proxy → Sidecar Proxy → Service B
            │                │
            ├── mTLS         ├── mTLS
            ├── Retry        ├── Circuit breaker
            ├── Tracing      ├── Load balancing
            └── Metrics      └── Authorization
```

**Tools**: Istio, Linkerd, Consul Connect

## API Gateway Patterns

### Gateway Responsibilities
| Function | Why | Example |
|----------|-----|---------|
| Authentication | Centralized auth check | Validate JWT, API key |
| Rate limiting | Protect backends | 100 req/min per API key |
| Request routing | Decouple clients from services | `/api/v2/users` → user-service |
| Request/response transform | API versioning, format conversion | Snake_case ↔ camelCase |
| Caching | Reduce backend load | Cache GET responses by key |
| Circuit breaking | Protect from cascade | Open circuit on 50% errors |

### Gateway Anti-Patterns
- Business logic in the gateway (keep it thin)
- Single gateway for all traffic (separate by domain)
- No health checks on upstream services
- Gateway as single point of failure (deploy redundantly)

## Service Mesh

### When You Need a Mesh
- 10+ microservices communicating
- Need consistent mTLS across all services
- Want centralized traffic policy (retries, timeouts)
- Need distributed tracing without code changes
- Require fine-grained authorization (service-to-service)

### When You Don't
- Monolith or < 5 services
- Team lacks Kubernetes/mesh expertise
- Latency budget can't afford sidecar overhead (~1-2ms per hop)
- Simple retry/timeout needs (handle in client library)

### Mesh Configuration Example (Istio)
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: user-service
spec:
  hosts:
    - user-service
  http:
    - route:
        - destination:
            host: user-service
            subset: v2
          weight: 90
        - destination:
            host: user-service
            subset: v1
          weight: 10
      retries:
        attempts: 3
        retryOn: 5xx,reset,connect-failure
      timeout: 10s
```

## Zero-Trust Networking

### Principles
1. **Never trust, always verify** — Every request is authenticated
2. **Least privilege** — Services can only reach what they need
3. **Assume breach** — Design as if the network is compromised
4. **Encrypt everything** — mTLS between all services

### Implementation
```yaml
# Network policy: user-service can only talk to db and cache
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: user-service-egress
spec:
  podSelector:
    matchLabels:
      app: user-service
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - port: 5432
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - port: 6379
```

## Load Balancing

### Algorithms

| Algorithm | Best For | Trade-off |
|-----------|----------|-----------|
| Round-robin | Equal instances, simple | Ignores instance health/load |
| Least connections | Varying request complexity | Slight overhead to track |
| Weighted round-robin | Heterogeneous instances | Manual weight management |
| Consistent hash | Session affinity, caching | Uneven on skewed keys |
| Random with 2 choices | Simple + effective | Good balance with low overhead |

### Health Checking
```yaml
# Kubernetes probes
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /readyz
    port: 8080
  periodSeconds: 5
  failureThreshold: 2
```

- **Liveness**: Is the process alive? (restart if not)
- **Readiness**: Can it serve traffic? (remove from LB if not)
- **Startup**: Is it done initializing? (don't check liveness until ready)

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| No mTLS between services | Data exposed in transit | Enable mesh mTLS or manual TLS |
| Flat network, no policies | Lateral movement on breach | Network policies + zero trust |
| Gateway as business logic | Coupling, complexity | Keep gateway thin |
| No health checks on LB | Traffic to dead instances | Liveness + readiness probes |
| Single load balancer | SPOF | Redundant LB with failover |

---

**Remember**: The network is hostile territory. Encrypt everything, authenticate every connection, and authorize every request. Zero trust isn't paranoia — it's engineering discipline.
