# Network & Service Mesh Rules

## Encryption (CRITICAL)

- TLS 1.2+ required for ALL communication (prefer TLS 1.3)
- mTLS between all services in production
- No plaintext communication across network boundaries

## API Gateway

- All external traffic routes through API gateway
- Authentication and rate limiting at gateway level
- Gateway is thin — no business logic

## Service Communication

ALWAYS:
- Connection pooling for all outbound connections
- Health checks on all upstream dependencies
- Compression for payloads > 1KB
- Explicit timeouts on every network call

NEVER:
- Flat network without network policies
- Direct database access from external services
- Unencrypted service-to-service communication

## Load Balancing

- Health-check-aware load balancing
- Liveness AND readiness probes on every service
- Graceful shutdown with connection draining

## Zero Trust

- Network policies restrict service-to-service communication
- Each service can only reach dependencies it needs
- All access authenticated and authorized at service boundary

## Reference

See skills: `network-security-mesh`, `advanced-networking` for comprehensive patterns.
