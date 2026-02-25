# Deployment Safety Rules

## Release Strategy (CRITICAL)

- Production deploys use canary or blue-green (never big-bang)
- Automated rollback on health check failure
- Rollback plan documented before every release
- Feature flags wrap new behavior (toggle off without redeploy)

## Backward Compatibility (CRITICAL)

Safe changes (no coordination):
- Add new optional field with default
- Add new endpoint or event type
- Widen validation

Breaking changes (require migration plan):
- Remove or rename field/endpoint
- Change field type or semantics
- Tighten validation

NEVER ship breaking changes without:
- Major version bump
- Deprecation notice (minimum 90 days)
- Migration guide for consumers

## Multi-Service Releases

- Deploy consumers before producers
- Consumers handle old AND new formats during transition
- Never require simultaneous deployment of multiple services

## Database Migrations

- Migrations MUST be backward-compatible
- Never drop column and deploy code in same release
- Additive changes first, removal in separate later release
- Migrations tested in staging before production

## Semantic Versioning

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)
- Version bump required for every release

## Reference

See skills: `deployment-strategies`, `env-compat-extend`, `staff-principles` for comprehensive patterns.
