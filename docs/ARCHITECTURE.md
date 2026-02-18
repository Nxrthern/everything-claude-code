# Omniskill Architecture

> The ultimate AI agent knowledge base and orchestration system combining ECC's deep infrastructure with AAS's massive breadth.

## Overview

**Omniskill** is a unified, modular system for enabling AI agents (Claude, Gemini, Copilot, and others) to operate as principal engineers across any technical domain, business function, or organizational challenge.

The system has three layers:

1. **Orchestration Layer** - Agents, commands, hooks, contexts, and rules that coordinate AI behavior
2. **Knowledge Layer** - 900+ skills organized across 14 domains covering technical and non-technical expertise
3. **Meta Layer** - Bundles, workflows, catalog, and installation systems for easy access

---

## Layer 1: Orchestration Infrastructure

### Agents (Specialized AI Personas)

**31 specialized agents** for different roles and domains:

- **Core Technical**: architect, code-reviewer, security-reviewer, planner
- **Language-Specific**: go-reviewer, python-reviewer, go-build-resolver, build-error-resolver
- **Domain-Specific**: database-reviewer, query-optimizer, e2e-runner, doc-updater
- **New Domain Agents**: business-analyst, ai-ml-engineer, pentest-coordinator, cloud-architect, workflow-designer, content-strategist

Each agent:
- Has specific tools and model preferences
- Specializes in a domain or technology
- Can be delegated to via `/agent-name` mention
- Works with skills from the knowledge layer

### Commands (Quick Execution Workflows)

**42 slash commands** for quick task execution:

- **Execution**: `/build-fix`, `/go-build`, `/tdd`, `/e2e`, `/code-review`, `/plan`
- **Learning**: `/learn`, `/instinct-export`, `/instinct-import`, `/instinct-status`
- **Workflow**: `/multi-plan`, `/multi-backend`, `/multi-frontend`, `/multi-workflow`
- **New Commands**: `/workflow-run`, `/skill-search`, `/bundle-install`, `/security-pentest`, `/business-review`

### Hooks (Event-Driven Automations)

Hooks run before/after tool executions to enforce quality:

- **PreToolUse**: Block unsafe operations (dev server outside tmux, doc file spam)
- **PostToolUse**: Auto-format, check types, run linters
- **Lifecycle**: Session start/end, pre-compact, pattern extraction

### Contexts (Interaction Modes)

Switch modes to match your task:

- `dev.md` - Implementation mode (active coding, make changes, move fast)
- `research.md` - Exploration mode (read-only, understand before acting)
- `review.md` - Code review mode (severity-prioritized analysis)
- `security-audit.md` - Security assessment mode
- `business-strategy.md` - Strategic planning mode

### Rules (Enforceable Guidelines)

**Two-level rule system**:

1. **Common Rules** (always apply)
   - Coding style, git workflow, testing, security, performance
   - Data resilience, distributed systems, observability
   - Deployment safety, reliability patterns

2. **Language-Specific Rules** (opt-in)
   - TypeScript/JavaScript: immutability, Zod validation, Playwright testing
   - Python: PEP 8, black/ruff/isort formatting, pytest
   - Go: gofmt, table-driven tests, error wrapping
   - Java: naming conventions, Optional, streams, generics
   - **New**: Rust, C#/.NET, Swift, Ruby, PHP

---

## Layer 2: Knowledge System (900+ Skills)

### 14 Skill Categories

Skills are organized hierarchically by domain:

```
skills/
├── _core/              10 skills - Foundational patterns
├── architecture/       13 skills - System design, concurrency, performance
├── languages/          12 skills - Language-specific patterns and testing
├── frameworks/         16 skills - Framework-specific patterns (Django, Spring, React, etc.)
├── testing/             5 skills - Testing patterns and TDD
├── databases/          10 skills - Databases, query optimization, migrations
├── infrastructure/     10 skills - DevOps, deployment, observability, incidents
├── security/           15 skills - Security, encryption, secrets, compliance
├── ai-ml/               8 skills - RAG, prompt engineering, agents, ML pipelines
├── business/           12 skills - Pricing, marketing, product management, legal
├── cloud-providers/   120 skills - Azure, AWS, GCP services
├── workflow-automation/ 9 skills - n8n, Airflow, Temporal, Zapier
├── collaboration/      13 skills - Brainstorming, writing, documentation
└── specialized/       637 skills - Niche tools, vendors, frameworks
```

### Core Skills (_core/)

Foundational practices that apply universally:

1. **coding-standards** - Immutability, error handling, code organization
2. **tdd-workflow** - 80%+ coverage, unit/integration/E2E tests
3. **security-review** - Authentication, input validation, secrets, API security
4. **verification-loop** - Build, type check, lint, test, security gates
5. **eval-harness** - Eval-driven development framework
6. **continuous-learning** & **continuous-learning-v2** - Extract patterns from sessions
7. **iterative-retrieval** - Solve subagent context problem
8. **strategic-compact** - Manual context compaction at logical intervals
9. **staff-principles** - Senior engineer leadership patterns

### Architecture Skills

Deep technical foundations:

- `distributed-systems` - Consensus, partitioning, replication, consistency
- `event-driven-architecture` - Pub/sub, event sourcing, sagas, streaming
- `sharding-partitioning` - Data sharding, consistent hashing
- `multi-cloud-region` - Global distribution, latency optimization, disaster recovery
- `caching-queueing` - Cache hierarchies, message queues, patterns
- `advanced-concurrency` - Threading, goroutines, async/await, worker pools
- `advanced-performance` - Profiling, optimization, benchmarking, tail latency
- `advanced-testing` - Property-based tests, chaos engineering, fuzzing

### Language Skills

Language-specific patterns and best practices:

**Supported Languages**: TypeScript, Python, Go, Java, C++, Rust, C#/.NET, Swift, Ruby, PHP

Each language has:
- **Pattern Skill** - Idioms, conventions, best practices
- **Testing Skill** - Framework patterns, TDD, coverage
- **Security/Style Rules** - Language-specific guidelines

### Framework Skills

Production patterns for specific frameworks:

**Backend**: Django, Django-REST, Spring Boot, FastAPI, Express, Laravel, ASP.NET Core
**Frontend**: React, Next.js, Vue, Angular, Flutter, React Native
**Specialized**: Remotion (video), Shopify, Unity, Godot

### Business Skills

Non-technical domains for business and strategy:

- `pricing-strategy` - Pricing models, willingness-to-pay, packaging
- `product-manager-toolkit` - Roadmapping, user stories, OKRs
- `startup-metrics-framework` - CAC, LTV, churn, unit economics
- `seo-audit` - Keyword research, content optimization, technical SEO
- `copywriting` - Persuasive copy, headlines, landing pages
- `legal-advisor` - Contracts, compliance, corporate governance

### Cloud Provider Skills (122 total)

**Azure** (100+ skills):
- AI Services: Form Recognizer, Content Safety, AI Projects, Vision, Transcription
- Storage: Blob, Data Lake, File Share, Queue, Cosmos
- Services: Functions, Service Bus, Event Hub, Event Grid, Key Vault
- Management: Application Insights, Monitor, Configuration, Identity

**AWS** (10+ skills):
- Serverless, Lambda, DynamoDB, S3, Penetration testing

**GCP** (5+ skills):
- Cloud Run, Functions, Storage, BigQuery

---

## Layer 3: Meta & Access Systems

### Bundle System

Pre-curated skill collections by role:

- **principal-engineer** - Core + architecture + infrastructure + security + observability
- **startup-founder** - Core + business + AI/ML + frameworks + deployment
- **security-specialist** - Core + security + pentesting + compliance
- **data-engineer** - Core + databases + AI/ML + cloud + workflows
- **frontend-lead** - Core + frameworks + testing + performance
- **core-dev** - Languages + coding + testing
- **cloud-ops** - Infrastructure + Kubernetes + Terraform
- **devops-pro** - CI/CD, IaC, orchestration, monitoring

Each bundle installs exactly what you need - no bloat.

### Workflow System

Step-by-step execution guides for complex goals:

- **ship-saas-mvp** - Plan → Build backend → Build frontend → Test → Ship
- **security-audit-web-app** - Scope → Authenticate → Validate input → Protect secrets → Report
- **data-pipeline-build** - Define → Design → Implement → Optimize → Deploy
- **ml-model-training** - Problem definition → Data prep → Train → Evaluate → Deploy
- **cloud-migration** - Assess → Design → Build → Migrate → Optimize

Each workflow:
- Recommends specific skills for each step
- Provides context and best practices
- Guides you through execution
- Tracks completion

### Catalog & Discovery

**Search via `/skill-search`**:

- Keyword search: `react patterns`, `kubernetes`
- Category search: `category:ai-ml`, `category:security`
- Role search: `role:principal-engineer`, `role:startup-founder`

**Installation via `/bundle-install`**:

- Install entire bundles for a role
- Select individual skills
- Choose user-level (all projects) or project-level (this project) installation
- Automatic dependency resolution

### Installation & Platform Support

**Supported Platforms**:
- Claude Code (via plugin)
- Cursor IDE (via `.cursor/` adapter)
- Gemini CLI
- Codex CLI
- GitHub Copilot
- OpenCode
- AdaL CLI

**Installation Options**:
- User-level: `~/.agent/skills/` (all projects)
- Project-level: `./.agent/skills/` (this project)
- Via NPX: `npx omniskill bundle-install principal-engineer`

---

## Design Principles

### 1. Modularity
Each skill, agent, command, rule is independent and self-contained. Mix and match as needed.

### 2. Universal Compatibility
Works across any AI agent LLM, IDE, terminal, and operating system.

### 3. Generic by Default, Specific by Opt-in
- Common rules apply universally
- Language/framework rules are opt-in
- Specialized skills don't force adoption

### 4. Knowledge Over Configuration
Skills encode knowledge (how-to, patterns, best practices), not just configuration.

### 5. Continuous Learning
Extract reusable patterns from sessions and evolve them into skills, commands, and agents.

---

## Typical Workflow

### 1. Identify Your Role
Find yourself in the bundle list:
- Building a SaaS? → `startup-founder` bundle
- Leading frontend? → `frontend-lead` bundle
- Engineering security? → `security-specialist` bundle

### 2. Install Your Bundle
```
/bundle-install startup-founder
```

### 3. Explore & Learn
```
/skill-search "react patterns"
/workflow-run ship-saas-mvp
```

### 4. Execute with AI Agents
- For architecture: Mention `@architect` agent
- For security: Mention `@security-reviewer` agent
- For business: Mention `@business-analyst` agent
- For coding: Code normally, hooks enforce quality

### 5. Extract & Improve
As you learn patterns, use `/learn` command to extract them into reusable skills.

---

## Advanced Customization

### Create Project-Specific Skills

Use `project-guidelines-example` as a template to create skills for your org:

```markdown
---
name: mycompany-patterns
description: Company-specific coding patterns and conventions
---

# MyCompany Development Patterns

## Our Stack
- TypeScript + Next.js (frontend)
- Go (backend services)
- PostgreSQL (data)

## Key Principles
1. Security first
2. Observability always
3. Test-driven development
4. Progressive enhancement

## Custom Conventions
- All services are containerized
- All data is encrypted at rest and in transit
- All APIs require authentication
```

### Extend Rules

Add company-specific rules:

```markdown
---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

# MyCompany TypeScript Standards

> Extends common/coding-style.md with company conventions.

## API Response Format

All API responses use this format:

\`\`\`typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: { code: string; message: string };
  timestamp: ISO8601;
}
\`\`\`
```

### Create Domain-Specific Agents

For your company's unique needs, create agents in `.agent/agents/`:

```markdown
---
name: mycompany-reviewer
description: Review code for MyCompany standards and security
---

Your role is to ensure all code meets MyCompany standards...
```

---

## Statistics

- **Skills**: 900+ (61 ECC core + 846 AAS + merged overlaps)
- **Agents**: 31 (25 ECC + 6 new)
- **Commands**: 42 (37 ECC + 5 new)
- **Rules**: 30 rule files (common + 9 language-specific)
- **Bundles**: 8 role-based curations
- **Workflows**: 5 step-by-step guides
- **Supported Languages**: 10+ (TS, Python, Go, Java, C++, Rust, C#, Swift, Ruby, PHP)
- **Supported Frameworks**: 20+ (Django, Spring Boot, React, Next.js, Flutter, etc.)
- **Cloud Providers**: 3 (Azure, AWS, GCP)

---

## Next Steps

1. **Install**: `/bundle-install` your role-based bundle
2. **Explore**: `/skill-search` for specific skills
3. **Execute**: Use `/workflow-run` for guided multi-step tasks
4. **Delegate**: Mention agents like `@architect`, `@security-reviewer`, `@ai-ml-engineer`
5. **Learn**: Use `/learn` to extract patterns into skills
6. **Customize**: Add company-specific skills, rules, and agents

---

## References

- **Skills Anatomy**: See `docs/SKILL_ANATOMY.md` for skill structure
- **Bundles**: See `data/bundles.json` for all curated collections
- **Workflows**: See `data/workflows.json` for step-by-step guides
- **Rules**: See `rules/` directory for language-specific guidelines
- **Agents**: See `agents/` directory for available specialists
- **Commands**: See `commands/` directory for quick execution workflows
