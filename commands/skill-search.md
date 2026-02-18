---
name: skill-search
description: Search and discover skills from the catalog by keyword, category, or role
---

# Skill Search

Search the 900+ skill catalog to find the right tool for your task.

## Usage

`/skill-search <query>`

`/skill-search category:<category>`

`/skill-search role:<role>`

## Search Examples

```
/skill-search react patterns
/skill-search category:security
/skill-search role:backend-engineer
/skill-search kubernetes
```

## Query Types

### Keyword Search
Search across skill names and descriptions:

```
/skill-search "prompt engineering"
/skill-search "kubernetes"
```

### Category Search
Find skills in specific categories:

```
/skill-search category:ai-ml
/skill-search category:cloud-providers
/skill-search category:frameworks
```

### Role-Based Search
Find bundles for specific roles:

```
/skill-search role:principal-engineer
/skill-search role:startup-founder
/skill-search role:security-specialist
```

## Result Format

Returns:
- Skill name and description
- Category and tags
- Quick reference to documentation
- Installation command

## Related Commands

- `/bundle-install` - Install a collection of related skills
- `/workflow-run` - Execute a multi-step workflow
