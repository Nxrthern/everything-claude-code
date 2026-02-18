---
name: platform-engineering
description: Infrastructure as code, deployment strategies, cloud cost optimization, and developer platform patterns. Use when designing infrastructure, CI/CD pipelines, or internal developer tooling.
---

# Platform Engineering

Build the platform that lets teams ship fast, fail safely, and spend wisely.

## When to Activate

- Designing infrastructure as code
- Building or reviewing CI/CD pipelines
- Optimizing cloud costs and resource usage
- Setting up developer environments
- Implementing deployment strategies

## Infrastructure as Code

### Principles
- **All infrastructure in version control** — no ClickOps
- **Idempotent applies** — running twice produces same result
- **Environment parity** — dev ≈ staging ≈ production
- **Modular composition** — reusable modules, not copy-paste
- **Drift detection** — alert when reality diverges from code

### IaC Tool Selection

| Tool | Best For | State Management |
|------|----------|-----------------|
| Terraform/OpenTofu | Multi-cloud, mature ecosystem | Remote state (S3, GCS) |
| Pulumi | Developers who prefer real languages | Managed or self-hosted |
| Helm | Kubernetes app packaging | Tiller/release history |
| Kustomize | K8s config overlay | None (gitops) |
| CDK | AWS-native, TypeScript teams | CloudFormation |

### Module Structure
```
infrastructure/
├── modules/
│   ├── networking/     # VPC, subnets, security groups
│   ├── compute/        # ECS, EKS, Lambda
│   ├── database/       # RDS, ElastiCache
│   └── monitoring/     # CloudWatch, Datadog
├── environments/
│   ├── dev/
│   ├── staging/
│   └── production/
└── shared/             # DNS, IAM, shared resources
```

## Deployment Strategies

| Strategy | Risk | Rollback Speed | Complexity |
|----------|------|----------------|------------|
| Rolling update | Medium | Slow (re-deploy) | Low |
| Blue-green | Low | Fast (switch) | Medium |
| Canary | Lowest | Fast (route shift) | High |
| Feature flags | Lowest | Instant (toggle) | Medium |

### Canary Deployment Flow
```
1. Deploy canary (5% traffic)
2. Monitor for 10 minutes:
   - Error rate < baseline + 0.1%
   - Latency p99 < baseline + 20%
   - No new error signatures
3. If healthy: promote to 25% → 50% → 100%
4. If unhealthy: automatic rollback to previous version
```

### Progressive Delivery Checklist
- [ ] Health check endpoint defined
- [ ] Metrics emitted for canary comparison
- [ ] Automated rollback on health check failure
- [ ] Deploy completes in < 15 minutes
- [ ] Zero-downtime guaranteed

## Container Standards

### Dockerfile Best Practices
```dockerfile
# Multi-stage build
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /server ./cmd/server

# Minimal runtime image
FROM gcr.io/distroless/static-debian12
COPY --from=builder /server /server
USER nonroot:nonroot
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD ["/server", "healthcheck"]
ENTRYPOINT ["/server"]
```

Rules:
- Multi-stage builds (separate build and runtime)
- Non-root user for runtime
- Specific image tags, never `latest`
- Health check in Dockerfile
- `.dockerignore` for minimal build context
- Pin base image digests for reproducibility

### Resource Limits
Every container must define:
```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

## Cost Optimization

### Right-Sizing Strategy
```
1. Collect 2 weeks of utilization data
2. Identify instances with < 20% avg CPU or < 40% avg memory
3. Downsize to next smaller instance type
4. Monitor for 1 week
5. Repeat quarterly
```

### Cost Reduction Playbook

| Strategy | Savings | Effort | Risk |
|----------|---------|--------|------|
| Right-size instances | 30-50% | Low | Low |
| Spot/preemptible for stateless | 60-80% | Medium | Medium |
| Reserved instances for baseline | 30-40% | Low | Commitment |
| Scale-to-zero for dev/staging | 40-70% | Medium | Startup latency |
| Storage tiering | 40-60% | Medium | Access latency |
| Delete orphan resources | 5-15% | Low | None |

### Cost Monitoring
- Tag all resources by team, service, and environment
- Set budget alerts at 80% and 100% thresholds
- Review cost anomalies weekly
- Attribute costs to teams for accountability

## Developer Experience

### Local Development
- One-command environment setup (`make dev` or `docker compose up`)
- Seed data for local databases
- Mock external dependencies
- Fast feedback loop (< 5 second build)

### CI/CD Pipeline Performance
- Cache dependencies between runs
- Parallelize independent stages
- Use incremental builds
- Target: PR feedback in < 10 minutes

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| Manual production changes | Drift, unreproducible | Everything as code |
| `latest` tags in production | Non-reproducible deploys | Pin specific versions |
| No resource limits | Noisy neighbor, OOM kills | Set requests and limits |
| Shared dev database | Data corruption, conflicts | Database per developer |
| Monolith CI pipeline | Slow feedback, blast radius | Per-service pipelines |

---

**Remember**: The best platform is invisible. Developers should think about their product, not their infrastructure. If they're fighting the platform, the platform has failed.
