---
name: env-compat-extend
description: Environment isolation, backward compatibility, semantic versioning, and extensibility patterns. Use when managing dev/staging/prod environments, planning API versioning, or ensuring changes don't break consumers.
---

# Environment Isolation, Compatibility & Extensibility

Isolated environments prevent surprises. Backward compatibility preserves trust. Extensibility enables evolution.

## When to Activate

- Managing environment parity (dev/staging/prod)
- Planning API or schema versioning
- Ensuring backward compatibility in releases
- Designing extensible systems (plugins, hooks)
- Implementing deprecation workflows

## Environment Isolation

### Environment Hierarchy
```
Development  → Individual developer environments
    ↓
Integration  → Shared, auto-deployed from feature branches
    ↓
Staging      → Production-like, deployed from main branch
    ↓
Production   → Live, deployed via release pipeline
```

### Isolation Requirements

| Aspect | Requirement |
|--------|-------------|
| Data | Separate databases per environment (never share prod DB) |
| Secrets | Different credentials per environment |
| Config | Environment-specific, version-controlled |
| Network | Isolated VPCs/namespaces, no cross-env access |
| Dependencies | Same versions as production (or explicitly different) |

### Environment Parity Rules
- Staging mirrors production in infrastructure and config
- All environments use same deployment mechanism
- Data shape matches (use anonymized production data for staging)
- Feature flags consistent between staging and production (for the same features)

## Semantic Versioning

### Version Format: MAJOR.MINOR.PATCH
```
MAJOR — Breaking changes (incompatible API change)
MINOR — New features (backward compatible)
PATCH — Bug fixes (backward compatible)

Examples:
  1.0.0 → 1.0.1  (patch: bug fix)
  1.0.1 → 1.1.0  (minor: new feature, compatible)
  1.1.0 → 2.0.0  (major: breaking change)
```

### Version Rules for APIs
```
v1 → v2 transition:
1. Announce deprecation of v1 (minimum 6 months notice)
2. Deploy v2 alongside v1 (both active)
3. Migrate consumers to v2 with support
4. Monitor v1 traffic → zero
5. Remove v1 after grace period
```

## Backward Compatibility

### Safe Changes (No Version Bump Needed)
- Add new optional field (with default value)
- Add new endpoint
- Add new enum value (if consumers handle unknown)
- Add new event type
- Widen input validation (accept more)
- Add new header (optional)

### Breaking Changes (Require Major Version)
- Remove or rename field
- Change field type
- Remove endpoint
- Change required fields
- Tighten validation (reject previously valid input)
- Change authentication requirements
- Change response structure

### Compatibility Testing
```go
// ✅ Test that old clients still work with new server
func TestBackwardCompatibility(t *testing.T) {
    server := startNewVersionServer()

    // Send request in old format
    resp := sendOldFormatRequest(server, oldPayload)
    assert.Equal(t, 200, resp.StatusCode)

    // Verify response contains expected fields
    body := parseResponse(resp)
    assert.NotEmpty(t, body.ID)        // field still exists
    assert.NotEmpty(t, body.Name)      // field still exists
    // New field may or may not be present — that's OK
}
```

## Extensibility Patterns

### Open-Closed Principle
Open for extension, closed for modification:

```go
// ✅ Extensible via interface
type PaymentProcessor interface {
    Process(ctx context.Context, payment Payment) error
}

// New payment methods don't modify existing code
type StripeProcessor struct{}
type PayPalProcessor struct{}

// Registry pattern for dynamic extension
type ProcessorRegistry struct {
    processors map[string]PaymentProcessor
}

func (r *ProcessorRegistry) Register(name string, p PaymentProcessor) {
    r.processors[name] = p
}
```

### Plugin Architecture
```go
// ✅ Hook-based extensibility
type Hooks struct {
    BeforeCreate []func(ctx context.Context, entity Entity) error
    AfterCreate  []func(ctx context.Context, entity Entity) error
}

func (h *Hooks) RunBeforeCreate(ctx context.Context, e Entity) error {
    for _, hook := range h.BeforeCreate {
        if err := hook(ctx, e); err != nil {
            return err
        }
    }
    return nil
}
```

## Deprecation Workflow

```markdown
## Deprecation: [Feature/Endpoint/Field]

### Timeline
- T+0: Deprecation announced (docs, changelog, response headers)
- T+30 days: Warning logs for consumers still using deprecated path
- T+90 days: Deprecation notice in API response
- T+180 days: Feature removed (or migrated automatically)

### Communication
- Deprecation header: `Sunset: Sat, 01 Aug 2026 00:00:00 GMT`
- Migration guide published
- Direct notification to high-usage consumers
```

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| Shared database across environments | Data corruption, security | Separate DB per environment |
| Breaking change without version bump | Silent consumer failures | Semver + compatibility tests |
| Removing feature without deprecation | Surprise breakage | Sunset header + grace period |
| Hardcoded environment-specific values | Drift, misconfiguration | Environment variables + config files |
| Testing only in dev, deploying to prod | "Works on my machine" | Test in staging, mirror production |

---

**Remember**: Backward compatibility is a promise to your consumers. Breaking that promise breaks trust. If you must break compatibility, make it a major version, communicate early, and support the transition.
