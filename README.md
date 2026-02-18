# Omniskill

> The ultimate AI agent knowledge base empowering principal engineers to operate across any technical domain, business function, or organizational challenge.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills: 900+](https://img.shields.io/badge/Skills-900%2B-blue)](./skills/)
[![Agents: 31](https://img.shields.io/badge/Agents-31-green)](./agents/)
[![Commands: 42](https://img.shields.io/badge/Commands-42-purple)](./commands/)
[![Bundles: 8](https://img.shields.io/badge/Bundles-8-orange)](./data/bundles.json)

## What is Omniskill?

Omniskill is a unified, modular knowledge and orchestration system that turns any AI agent (Claude, Gemini, Copilot, etc.) into a principal engineer capable of:

- **Deep Technical Excellence** - From distributed systems to secure DevOps, from TDD to ML pipelines
- **Business Acumen** - Market analysis, pricing strategy, product roadmapping, startup metrics
- **Multi-Domain Expertise** - 900+ skills spanning 14 domains
- **Autonomous Execution** - 31 specialized agents and 42 commands for hands-off task completion
- **Intelligent Guidance** - 5 end-to-end workflows for complex goals

### Three Unified Layers

```
┌─────────────────────────────────────────────────────────────┐
│ Meta Layer: Bundles, Workflows, Catalog, Discovery          │
├─────────────────────────────────────────────────────────────┤
│ Knowledge Layer: 900+ Skills (14 domains, 4+ languages)     │
├─────────────────────────────────────────────────────────────┤
│ Orchestration: Agents (31), Commands (42), Hooks, Rules     │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Install Your Role Bundle

```bash
# For a SaaS startup founder
/bundle-install startup-founder

# For a principal engineer
/bundle-install principal-engineer

# For a data engineer
/bundle-install data-engineer

# For a security specialist
/bundle-install security-specialist
```

### 2. Discover Skills

```bash
/skill-search "react patterns"
/skill-search category:ai-ml
/skill-search role:principal-engineer
```

### 3. Execute Workflows

```bash
/workflow-run ship-saas-mvp
/workflow-run security-audit-web-app
/workflow-run data-pipeline-build
```

### 4. Delegate to Agents

In your chat, mention specialized agents:

- `@architect` - System design and scalability decisions
- `@security-reviewer` - Security vulnerabilities and best practices
- `@ai-ml-engineer` - RAG, prompt optimization, multi-agent systems
- `@business-analyst` - Market analysis and business strategy
- `@cloud-architect` - Infrastructure-as-code and cloud design
- `@workflow-designer` - Automation and orchestration workflows

### 5. Learn and Improve

```bash
/learn                          # Extract patterns from this session
/instinct-status               # View learned instincts
/instinct-export               # Export patterns
```

---

## Capabilities

### 900+ Skills Across 14 Domains

| Domain | Skills | Purpose |
|--------|--------|---------|
| **_core** | 10 | Foundational patterns: TDD, security, verification |
| **architecture** | 13 | Distributed systems, concurrency, event-driven |
| **languages** | 12 | TypeScript, Python, Go, Java, Rust, C#, Swift, Ruby, PHP |
| **frameworks** | 16 | Django, Spring Boot, React, Next.js, Flutter, etc. |
| **testing** | 5 | Unit, integration, E2E, chaos, property-based |
| **databases** | 10 | PostgreSQL, ClickHouse, query optimization, migrations |
| **infrastructure** | 10 | DevOps, deployment, observability, incidents |
| **security** | 15 | Encryption, secrets, compliance, pentesting |
| **ai-ml** | 8 | RAG, prompts, agents, ML pipelines |
| **business** | 12 | Pricing, marketing, product, legal, startup metrics |
| **cloud-providers** | 120 | Azure (100+), AWS (10+), GCP (5+) |
| **workflow-automation** | 9 | n8n, Airflow, Temporal, Zapier |
| **collaboration** | 13 | Brainstorming, writing, documentation, team |
| **specialized** | 637 | Niche tools, vendors, frameworks |

### 31 Specialized Agents

**Core Technical**: architect, code-reviewer, security-reviewer, planner, database-reviewer, query-optimizer, e2e-runner
**Language-Specific**: go-reviewer, python-reviewer, go-build-resolver, build-error-resolver
**DevOps**: platform-engineer, observability-engineer, reliability-engineer, performance-engineer
**Domain**: business-analyst, ai-ml-engineer, pentest-coordinator, cloud-architect, workflow-designer, content-strategist

### 42 Quick Commands

`/plan` `/tdd` `/code-review` `/build-fix` `/go-build` `/security-scan` `/go-test` `/e2e` `/perf-audit` `/refactor-clean` `/skill-search` `/bundle-install` `/workflow-run` `/security-pentest` `/business-review` ... and 27 more.

### 8 Role-Based Bundles

- **principal-engineer** - Core + architecture + infrastructure + security + observability
- **startup-founder** - Core + business + AI/ML + frameworks + deployment
- **security-specialist** - Security focused with pentesting and compliance
- **data-engineer** - Databases, ML, pipelines, cloud data services
- **frontend-lead** - React, Next.js, testing, performance, accessibility
- **cloud-ops** - Kubernetes, Terraform, deployment, observability
- **devops-pro** - CI/CD, IaC, containers, monitoring
- **core-dev** - Languages, coding standards, testing

### 5 End-to-End Workflows

1. **Ship a SaaS MVP** - Plan → Build backend → Build frontend → Test → Ship
2. **Security Audit for Web App** - Scope → Authenticate → Validate input → Protect secrets → Report
3. **Build Data ETL Pipelines** - Define → Design → Implement → Optimize → Deploy
4. **Train ML Models** - Problem def → Data prep → Train → Evaluate → Deploy
5. **Migrate to Cloud** - Assess → Design → Build → Migrate → Optimize

---

## Directory Structure

```
omniskill/
├── agents/                    # 31 specialized AI personas
├── commands/                  # 42 quick-execution workflows
├── contexts/                  # dev, research, review, security-audit, business-strategy
├── hooks/                     # Event-driven code quality automations
├── rules/                     # Language-specific guidelines (10 languages)
│   ├── common/               # Language-agnostic principles
│   ├── typescript/           # TypeScript/JavaScript
│   ├── python/               # Python
│   ├── golang/               # Go
│   ├── java/                 # Java
│   ├── cpp/                  # C++
│   ├── rust/                 # Rust
│   ├── dotnet/               # C#/.NET
│   ├── swift/                # Swift
│   ├── ruby/                 # Ruby
│   └── php/                  # PHP
│
├── skills/                    # 900+ skills in 14 categories
│   ├── _core/                # 10 foundational skills
│   ├── architecture/         # 13 system design skills
│   ├── languages/            # 12 language patterns
│   ├── frameworks/           # 16 framework patterns
│   ├── testing/              # 5 testing skills
│   ├── databases/            # 10 data skills
│   ├── infrastructure/       # 10 DevOps skills
│   ├── security/             # 15 security skills
│   ├── ai-ml/                # 8 AI/ML skills
│   ├── business/             # 12 business skills
│   ├── cloud-providers/      # 120 cloud skills
│   ├── workflow-automation/  # 9 automation skills
│   ├── collaboration/        # 13 team skills
│   └── specialized/          # 637 specialized skills
│
├── data/                      # Metadata and discovery
│   ├── bundles.json          # 8 role-based bundles
│   ├── workflows.json        # 5 end-to-end workflows
│   ├── catalog.json          # Full skill catalog
│   ├── skills_index.json     # Searchable index
│   └── aliases.json          # Skill name aliases
│
├── scripts/                   # Build and installation tools
├── .cursor/                   # Cursor IDE support
├── .claude-plugin/            # Claude Code plugin manifest
├── .opencode/                 # OpenCode plugin support
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md        # Full system architecture
│   ├── SKILL_ANATOMY.md       # How skills are structured
│   ├── BUNDLES.md             # Bundle descriptions
│   ├── WORKFLOWS.md           # Workflow guides
│   └── translations/          # i18n docs
│
└── README.md
```

---

## Installation

### Option 1: NPX (Recommended)

```bash
npx omniskill bundle-install startup-founder
```

### Option 2: Manual Clone + Setup

```bash
git clone https://github.com/your-org/omniskill.git
cd omniskill
npm install
npm run install-to-claude-code
```

### Option 3: Cursor IDE

1. Install the Omniskill plugin from Cursor's plugin marketplace
2. Skills are automatically available in `.cursor/skills/`

### Option 4: As a Git Submodule

```bash
git submodule add https://github.com/your-org/omniskill.git .agents/omniskill
```

---

## Supported Platforms

Works with:

- **Claude** (via Claude Code plugin)
- **Cursor IDE** (via `.cursor/` adapter)
- **Gemini** (via Gemini CLI)
- **GitHub Copilot** (via VS Code integration)
- **OpenCode** (via OpenCode plugin)
- **Codex CLI**
- **AdaL CLI**

---

## Core Concepts

### Skills

Self-contained knowledge units combining documentation, patterns, and best practices.

Structure:
```
skills/frameworks/react-patterns/
├── SKILL.md              # Main documentation
├── examples/             # Usage examples
├── scripts/              # Helper scripts
├── templates/            # Code templates
└── references/           # Detailed docs
```

### Agents

Specialized AI personas with specific tools and expertise.

Usage:
```
@architect              # System design decisions
@security-reviewer      # Security audit and hardening
@ai-ml-engineer        # LLM and ML applications
```

### Commands

Quick-execution slash commands for common workflows.

Usage:
```
/tdd                    # Test-driven development
/code-review           # Code quality review
/security-scan         # Security vulnerabilities
```

### Bundles

Curated collections of related skills for specific roles.

Download what you need:
```
/bundle-install principal-engineer
/bundle-install startup-founder
```

### Workflows

Step-by-step guides for complex multi-domain goals.

Execute workflows:
```
/workflow-run ship-saas-mvp
/workflow-run security-audit-web-app
```

---

## Usage Examples

### Example 1: Build a Secure SaaS MVP

```
User: I want to build a SaaS app for project management

Claude: Let me run the SaaS MVP workflow
/workflow-run ship-saas-mvp

Step 1: Plan the scope
  Recommended skills: @brainstorming, @product-manager-toolkit
  
Step 2: Build backend and API
  Recommended skills: @backend-patterns, @postgres-patterns
  @architect: Here's a recommended architecture...
  
Step 3: Build frontend
  Recommended skills: @react-patterns, @nextjs-best-practices
  
Step 4: Test and validate
  Recommended skills: @tdd-workflow, @e2e-testing
  /test                 # Run tests
  
Step 5: Ship safely
  Recommended skills: @deployment-strategies, @observability
  /verify               # Run verification loop
```

### Example 2: Conduct a Security Audit

```
/security-pentest web-app

@pentest-coordinator orchestrates comprehensive assessment:
  1. Reconnaissance - map attack surface
  2. Threat modeling - identify high-risk areas
  3. Exploitation - test vulnerabilities
  4. Reporting - create remediation roadmap

Results: 15 issues found, 3 critical, 8 high
Recommendations: Address critical issues within 48 hours
```

### Example 3: Launch a Data Pipeline

```
/workflow-run data-pipeline-build

Step 1: Define data requirements
  What are your data sources? PostgreSQL, CSV, S3?
  
Step 2: Design pipeline architecture
  @cloud-architect recommends Airflow on Kubernetes
  
Step 3: Implement transformations
  @data-engineer provides schema and transformation logic
  
Step 4: Optimize performance
  Bottleneck identified: query takes 45 minutes
  Optimization: Add indexes, parallelize, use caching
  
Step 5: Deploy and monitor
  Pipeline deployed. SLA: <60 minutes. Current: 8 minutes.
```

---

## Customization

### Create Project-Specific Skills

```markdown
---
name: mycompany-patterns
description: Company-specific coding standards and architecture
---

# MyCompany Development Patterns

## Our Stack
- TypeScript + Next.js (frontend)
- Go (backend)
- PostgreSQL (data)
- Kubernetes (orchestration)

## Key Principles
1. Security first - all data encrypted at rest and in transit
2. Observability always - all services emit metrics
3. Test-driven - minimum 80% coverage
4. Progressive - feature flags for safe deployments
```

### Add Company Rules

```markdown
---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

# MyCompany TypeScript Standards

All API responses must follow this format:

\`\`\`typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: { code: string; message: string };
  timestamp: ISO8601;
}
\`\`\`
```

---

## Performance & Optimization

### Token Optimization

- Strategic context compaction at logical intervals
- Model selection based on task complexity
- Extended thinking for high-stakes decisions

### Continuous Learning

Extract reusable patterns from sessions:

```
/learn                          # Extract patterns
/instinct-status               # View learned instincts
/instinct-export               # Export as skills
```

---

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Follow existing skill/agent/command structure
4. Test thoroughly
5. Submit a pull request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

---

## License

MIT License - See [LICENSE](./LICENSE) for details.

---

## Acknowledgments

Omniskill merges two powerful projects:

- **Everything Claude Code** (25 agents, 37 commands, deep infrastructure)
- **Antigravity Awesome Skills** (864 skills, massive breadth)

This creates the most comprehensive AI agent knowledge base for principal engineers.

---

## Quick Links

- **Documentation**: [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- **Skill Gallery**: [skills/](./skills/)
- **Available Agents**: [agents/](./agents/)
- **Commands**: [commands/](./commands/)
- **Bundles**: [data/bundles.json](./data/bundles.json)
- **Workflows**: [data/workflows.json](./data/workflows.json)
- **Rules**: [rules/](./rules/)

---

## Getting Help

- **Skill Search**: `/skill-search <keyword>`
- **Bundle Discovery**: `/bundle-install --help`
- **Workflow Guide**: `/workflow-run --help`
- **Documentation**: Check [docs/](./docs/)
- **Issues**: GitHub Issues

---

**🚀 Ready to level up? Install your first bundle today!**

```
/bundle-install principal-engineer
```
