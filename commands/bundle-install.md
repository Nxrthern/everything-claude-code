---
name: bundle-install
description: Install a curated bundle of related skills for a specific role or use case
---

# Bundle Installer

Install pre-curated collections of skills tailored for specific roles and projects.

## Usage

`/bundle-install <bundle-id>`

## Available Bundles

### Role-Based Bundles

- `principal-engineer` - Core + architecture + infrastructure + security + observability
- `startup-founder` - Core + business + AI/ML + frameworks + deployment
- `security-specialist` - Core + security + pentesting + compliance
- `data-engineer` - Core + databases + AI/ML + cloud-providers + workflow-automation
- `frontend-lead` - Core + frameworks (React/Next/Flutter) + testing + deployment

### Use-Case Bundles

- `core-dev` - Core development skills across languages
- `cloud-ops` - Infrastructure and operations
- `devops-pro` - CI/CD, Kubernetes, IaC

## Examples

```
/bundle-install principal-engineer
/bundle-install startup-founder
/bundle-install security-specialist
/bundle-install data-engineer
```

## Installation Flow

1. Show bundle contents
2. Ask for installation target (user-level or project-level)
3. Ask for customization options
4. Install selected skills
5. Verify installation
6. Show quick-start guide

## Bundle Contents

Each bundle includes:
- Core foundational skills
- Domain-specific skills
- Language/framework patterns
- Best practices and tools
- Testing and validation skills

## Related Commands

- `/skill-search` - Find individual skills
- `/workflow-run` - Execute a workflow using skills
