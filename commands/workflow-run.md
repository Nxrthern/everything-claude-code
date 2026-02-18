---
name: workflow-run
description: Execute a step-by-step workflow from the curated workflows catalog
---

# Workflow Runner

Run pre-built workflows to accomplish complex multi-step goals.

## Usage

`/workflow-run <workflow-id>`

## Available Workflows

- `ship-saas-mvp` - End-to-end SaaS MVP development
- `security-audit-web-app` - Security assessment for web applications
- `data-pipeline-build` - Build and optimize data ETL pipelines
- `cloud-migration` - Migrate on-premise systems to cloud
- `ml-model-training` - Train and evaluate ML models

## Examples

```
/workflow-run ship-saas-mvp
/workflow-run security-audit-web-app
/workflow-run data-pipeline-build
```

## How It Works

1. Selects workflow from `data/workflows.json`
2. Loads recommended skills for each step
3. Guides through step-by-step execution
4. Provides context and best practices
5. Tracks completion and milestones

Each workflow is fully defined in `data/workflows.json` with:
- Step titles and goals
- Recommended skills for each step
- Success criteria
- Common pitfalls

## Related Commands

- `/skill-search` - Find individual skills
- `/bundle-install` - Install a skill bundle
