---
name: config-servicing
description: Config server patterns using etcd, Consul, and similar systems. Covers live serving with watches, composable configs, inheritance, and fallback strategies. Use when implementing centralized configuration serving for distributed systems.
---

# Configuration Servicing

Serve configuration like you serve APIs — versioned, cached, observable, and with fallbacks for when the server is down.

## When to Activate

- Implementing centralized config serving (etcd, Consul, ZooKeeper)
- Designing config inheritance and composition
- Building config caching and fallback strategies
- Managing config for multi-service, multi-environment systems

## Config Server Selection

| System | Best For | Consistency | Watch Support |
|--------|----------|------------|---------------|
| etcd | Kubernetes-native, strong consistency | Raft (strong) | Yes (native) |
| Consul | Service discovery + config | Raft (strong) | Yes (blocking queries) |
| ZooKeeper | Coordination, leader election | ZAB (strong) | Yes (watches) |
| AWS AppConfig | Serverless, managed | Eventual | Yes (polling) |
| Spring Cloud Config | Java/Spring ecosystem | Git-backed | Yes (bus refresh) |

## Config Composition

### Inheritance Model
```
base.yaml          ← Default values for all environments
  └── staging.yaml  ← Overrides for staging
  └── production.yaml ← Overrides for production
      └── production-us.yaml  ← Regional overrides

Merge order: base → environment → region
Later values override earlier.
```

### Composable Config Pattern
```yaml
# base.yaml
server:
  port: 8080
  timeout_seconds: 30
database:
  max_connections: 10
  pool_timeout_seconds: 5

# production.yaml (overrides only what differs)
server:
  timeout_seconds: 10    # tighter timeout in production
database:
  max_connections: 50    # more connections in production
```

### Config Templates
```yaml
# Template with environment substitution
database:
  host: "{{.DB_HOST}}"
  port: {{.DB_PORT | default 5432}}
  name: "{{.SERVICE_NAME}}_{{.ENVIRONMENT}}"
  max_connections: {{if eq .ENVIRONMENT "production"}}50{{else}}10{{end}}
```

## Serving Patterns

### Watch-Based (Preferred)
```go
// ✅ Watch etcd for config changes
func watchConfig(ctx context.Context, client *clientv3.Client, key string) <-chan *Config {
    updates := make(chan *Config)
    go func() {
        defer close(updates)
        watchCh := client.Watch(ctx, key, clientv3.WithPrefix())
        for response := range watchCh {
            for _, event := range response.Events {
                cfg, err := parseConfig(event.Kv.Value)
                if err != nil {
                    log.Error("invalid config", "error", err)
                    continue
                }
                updates <- cfg
            }
        }
    }()
    return updates
}
```

### Poll-Based (Fallback)
```go
// ✅ Poll with interval when watches aren't available
func pollConfig(ctx context.Context, fetchFn func() (*Config, error), interval time.Duration) <-chan *Config {
    updates := make(chan *Config)
    go func() {
        defer close(updates)
        ticker := time.NewTicker(interval)
        defer ticker.Stop()

        var lastHash string
        for {
            select {
            case <-ticker.C:
                cfg, err := fetchFn()
                if err != nil {
                    log.Warn("config fetch failed", "error", err)
                    continue
                }
                hash := computeHash(cfg)
                if hash != lastHash {
                    updates <- cfg
                    lastHash = hash
                }
            case <-ctx.Done():
                return
            }
        }
    }()
    return updates
}
```

## Caching and Fallback

### Local Cache with Fallback
```go
// ✅ Config server down? Use cached version.
type ConfigClient struct {
    remote    ConfigServer
    cache     *atomic.Value  // last known good config
    cacheFile string         // persistent cache on disk
}

func (c *ConfigClient) GetConfig(ctx context.Context) *Config {
    // Try remote first
    cfg, err := c.remote.Fetch(ctx)
    if err == nil {
        c.cache.Store(cfg)
        c.saveToDisk(cfg) // persist for cold start
        return cfg
    }

    // Fallback to in-memory cache
    if cached := c.cache.Load(); cached != nil {
        log.Warn("using cached config", "error", err)
        return cached.(*Config)
    }

    // Fallback to disk cache (cold start scenario)
    if diskCfg, err := c.loadFromDisk(); err == nil {
        log.Warn("using disk-cached config")
        return diskCfg
    }

    // Last resort: application defaults
    log.Error("all config sources failed, using defaults")
    return DefaultConfig()
}
```

### Cache Strategy
```
Request flow:
1. Check in-memory cache (< 1ms)
2. If expired, fetch from config server (< 10ms)
3. If server unreachable, use stale cache + alert
4. If no cache, use disk-persisted last-known-good
5. If nothing, use hardcoded defaults + CRITICAL alert
```

## Versioning and Rollback

```
Every config change gets a version:
  config/myservice/v1  → { "timeout": 30 }
  config/myservice/v2  → { "timeout": 15 }
  config/myservice/v3  → { "timeout": 20 }

Rollback: Point to previous version
  active_version: v3 → v2 (instant rollback)

Rule: Keep last 10 versions for rollback
```

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| No fallback when server down | Service won't start | Local cache + defaults |
| Config server as SPOF | All services fail together | Cache, replicate, degrade |
| No versioning | Can't rollback bad config | Version every change |
| Poll too frequently | Unnecessary load | Watch-based or long poll intervals |
| No validation on serve | Bad config propagates | Validate before storing |

---

**Remember**: The config server is infrastructure — treat it with the same reliability standards as your database. When it's down, your services must continue with cached values, not crash.
