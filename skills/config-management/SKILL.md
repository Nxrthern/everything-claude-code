---
name: config-management
description: Configuration lifecycle, drift detection, GitOps, and environment-specific configuration patterns. Use when managing application configuration, preventing config drift, or implementing configuration-as-code workflows.
---

# Configuration Management

Configuration is code. Version it, validate it, review it, and deploy it with the same rigor as your application.

## When to Activate

- Setting up configuration management for a service
- Detecting or preventing configuration drift
- Implementing GitOps for config deployment
- Managing environment-specific overrides
- Designing feature flag systems

## Configuration Hierarchy

```
Priority (highest to lowest):
1. Environment variables (runtime override)
2. Config server values (etcd, Consul)
3. Environment-specific config file (config.production.yaml)
4. Base config file (config.yaml)
5. Application defaults (hardcoded in code)

Rule: Higher priority overrides lower.
Every value must exist at level 5 (default) at minimum.
```

## GitOps for Configuration

### Workflow
```
Developer → Edit config in Git → PR Review → Merge
    → CI validates schema + policy
    → CD deploys config to target environment
    → Service detects change (watch/poll)
    → Service reloads config (zero downtime)
```

### Repository Structure
```
config/
├── base/                    # Shared defaults
│   ├── config.yaml
│   └── feature-flags.yaml
├── environments/
│   ├── development/
│   │   └── config.yaml      # Dev overrides
│   ├── staging/
│   │   └── config.yaml      # Staging overrides
│   └── production/
│       └── config.yaml      # Production overrides
└── schemas/
    └── config.schema.json   # Validation schema
```

## Configuration Validation

### Schema Validation in CI
```yaml
# JSON Schema for config validation
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["server", "database"],
  "properties": {
    "server": {
      "type": "object",
      "properties": {
        "port": { "type": "integer", "minimum": 1024, "maximum": 65535 },
        "timeout_seconds": { "type": "integer", "minimum": 1, "maximum": 300 }
      },
      "required": ["port"]
    },
    "database": {
      "type": "object",
      "properties": {
        "max_connections": { "type": "integer", "minimum": 1, "maximum": 1000 }
      }
    }
  }
}
```

### Policy Validation
```yaml
# Rules that CI enforces:
- Production timeout must be >= staging timeout
- Max connections must be >= expected pod count * 2
- Feature flags must have an owner and expiration date
- No plaintext secrets in config files
```

## Drift Detection

### What Causes Drift
- Manual changes in production (ClickOps)
- Failed deployments leaving partial config
- Config server values changed without Git update
- Environment variable overrides not documented

### Detection Strategies
```
Continuous reconciliation:
1. Read desired state from Git
2. Read actual state from environment
3. Compare and alert on differences
4. Optionally auto-remediate (careful with this)

Tools: Terraform plan, ArgoCD sync status, custom diff scripts
```

### Drift Response
| Drift Type | Severity | Action |
|-----------|----------|--------|
| Config value differs from Git | HIGH | Investigate, reconcile to Git |
| Extra config not in Git | MEDIUM | Document or remove |
| Missing config from Git | CRITICAL | Deploy missing config |
| Infrastructure drift | HIGH | Terraform plan + apply |

## Live Configuration Updates

### Signal-Based Reload
```go
// ✅ Reload config on SIGHUP without restart
func watchConfig(configPath string, cfg *atomic.Value) {
    sigs := make(chan os.Signal, 1)
    signal.Notify(sigs, syscall.SIGHUP)

    for range sigs {
        newCfg, err := loadConfig(configPath)
        if err != nil {
            log.Error("config reload failed", "error", err)
            continue // keep old config
        }
        cfg.Store(newCfg)
        log.Info("config reloaded successfully")
    }
}
```

### Config Server Watch
```go
// ✅ Watch etcd/Consul for changes
func watchConfigServer(ctx context.Context, key string, cfg *atomic.Value) {
    watcher := configClient.Watch(ctx, key)
    for event := range watcher {
        newCfg, err := parseConfig(event.Value)
        if err != nil {
            log.Error("invalid config from server", "error", err)
            continue
        }
        if err := validateConfig(newCfg); err != nil {
            log.Error("config validation failed", "error", err)
            continue
        }
        cfg.Store(newCfg)
        log.Info("config updated from server", "version", event.Version)
    }
}
```

## Feature Flags as Config

```yaml
# Feature flags with metadata
feature_flags:
  new_checkout_flow:
    enabled: true
    rollout_percentage: 25
    owner: "checkout-team"
    expires: "2026-06-01"
    description: "New streamlined checkout experience"

  dark_mode:
    enabled: false
    owner: "frontend-team"
    expires: "2026-04-01"
```

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| Config in code (hardcoded) | Requires redeploy to change | Externalize to config files/env vars |
| Manual production config | Drift, no audit trail | GitOps workflow |
| No schema validation | Invalid config crashes service | Validate in CI + on load |
| No default values | Missing config = crash | Defaults for every value |
| Config without owner | Orphaned, never cleaned up | Owner + expiration on everything |

---

**Remember**: Every production incident caused by "a config change" is really caused by "a config change without validation, review, or rollback plan." Treat config with the same discipline as code.
