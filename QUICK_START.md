# Omniskill Quick Start Guide

Welcome to the ultimate AI agent knowledge base! Here's how to get started in 5 minutes.

## 🚀 Installation (Choose One)

### Via NPX (Easiest)
```bash
npx omniskill bundle-install principal-engineer
```

### Via Git Clone
```bash
git clone https://github.com/yourusername/omniskill.git ~/.agent/omniskill
cd ~/.agent/omniskill
npm install
```

### In Claude Code
Run: `/plugin install omniskill`

### In Cursor IDE
Already available in `.cursor/` directory

---

## 📚 Find Your Role

### For Startup Founders
```
/bundle-install startup-founder
```
Includes: Business strategy, AI/ML, frameworks, deployment

### For Principal Engineers
```
/bundle-install principal-engineer
```
Includes: Architecture, infrastructure, security, observability

### For Security Specialists
```
/bundle-install security-specialist
```
Includes: Security, pentesting, compliance

### For Data Engineers
```
/bundle-install data-engineer
```
Includes: Databases, AI/ML, pipelines, cloud

### For Frontend Leads
```
/bundle-install frontend-lead
```
Includes: React, Next.js, testing, performance

---

## 🔍 Search Skills

Find exactly what you need:

```bash
/skill-search "react patterns"          # Search by keyword
/skill-search category:ai-ml            # Search by category
/skill-search role:principal-engineer   # Search by role
/skill-search "kubernetes"              # Free text search
```

### Popular Searches
- `tdd workflow` - Test-driven development
- `security-review` - Security best practices
- `postgres-patterns` - Database patterns
- `distributed-systems` - System design
- `langchain-architecture` - LLM applications

---

## 🎯 Execute Workflows

Step-by-step guidance for complex goals:

### Ship a SaaS MVP
```bash
/workflow-run ship-saas-mvp
```
Steps: Plan → Build backend → Build frontend → Test → Ship

### Conduct Security Audit
```bash
/workflow-run security-audit-web-app
```
Steps: Scope → Authenticate → Validate input → Protect secrets → Report

### Build Data Pipeline
```bash
/workflow-run data-pipeline-build
```
Steps: Define → Design → Implement → Optimize → Deploy

### Train ML Model
```bash
/workflow-run ml-model-training
```
Steps: Problem def → Data prep → Train → Evaluate → Deploy

### Migrate to Cloud
```bash
/workflow-run cloud-migration
```
Steps: Assess → Design → Build → Migrate → Optimize

---

## 🤖 Delegate to Agents

Mention specialized agents in your chat:

```
@architect              # System design decisions
@security-reviewer      # Security audit and hardening
@ai-ml-engineer        # LLM and ML applications
@business-analyst      # Market analysis and strategy
@cloud-architect       # Infrastructure and cloud design
@workflow-designer     # Automation and orchestration
@code-reviewer         # Code quality and best practices
@database-reviewer     # Database optimization
@performance-engineer  # Performance profiling
```

**Example:**
```
@architect: Design a scalable system for real-time analytics

@security-reviewer: Audit this authentication implementation

@ai-ml-engineer: Build a RAG system for our docs
```

---

## 📖 Skills by Domain

### Core Foundations
- `coding-standards` - Code organization and quality
- `tdd-workflow` - Test-driven development
- `security-review` - Security best practices
- `verification-loop` - Quality gates and testing

### System Architecture
- `distributed-systems` - Consensus, replication, consistency
- `event-driven-architecture` - Pub/sub, event sourcing
- `sharding-partitioning` - Data distribution
- `advanced-performance` - Profiling and optimization

### Languages (10+)
- TypeScript, Python, Go, Java, Rust, C#, Swift, Ruby, PHP, C++

### Frameworks
- Django, Spring Boot, React, Next.js, FastAPI, Express, Laravel, Flutter

### Business
- `pricing-strategy` - Pricing models
- `product-manager-toolkit` - Roadmapping and OKRs
- `startup-metrics-framework` - CAC, LTV, unit economics
- `seo-audit` - SEO optimization

### Infrastructure
- `platform-engineering` - Infrastructure design
- `deployment-strategies` - Blue-green, canary, rolling
- `observability` - Monitoring, logging, tracing
- `incident-analysis` - Post-mortem practices

### AI/ML
- `rag-engineer` - Retrieval-augmented generation
- `prompt-engineer` - Prompt optimization
- `ai-agents-architect` - Multi-agent systems
- `vector-database-engineer` - Embedding and search

---

## 💡 Common Workflows

### Development
```
1. /skill-search <technology>           # Find patterns
2. @architect                            # Design check
3. /tdd                                  # Test-first development
4. /code-review                          # Quality review
5. /verify                               # Final verification
```

### Deployment
```
1. /workflow-run deployment-strategies   # Choose strategy
2. @platform-engineer                    # Infra review
3. /observability                        # Set up monitoring
4. @reliability-engineer                 # Resilience check
5. Deploy with confidence!
```

### Security
```
1. /security-pentest <scope>             # Run full assessment
2. @threat-modeling-expert              # Threat analysis
3. /code-review                          # Code security
4. /security-scan                        # Vulnerability scan
5. @security-reviewer                    # Final audit
```

---

## 📚 Documentation

### Full Documentation
- `README.md` - Complete feature overview
- `ARCHITECTURE.md` - System architecture and design
- `MERGE_COMPLETE.md` - Detailed merge summary
- `EXECUTION_REPORT.txt` - Execution details

### Guides
- `docs/SKILL_ANATOMY.md` - How skills work
- `docs/BUNDLES.md` - Available bundles
- `docs/WORKFLOWS.md` - Workflow details

### Data Files
- `data/bundles.json` - All role-based bundles
- `data/workflows.json` - All workflows
- `data/catalog.json` - Complete skill catalog

---

## ❓ FAQ

**Q: How do I use this in my existing project?**
A: Install the role-based bundle for your situation, then mention agents like `@architect` or `@security-reviewer` in your chat.

**Q: Can I create custom skills?**
A: Yes! Use `project-guidelines-example` as a template to create project-specific skills.

**Q: What if I need to extend rules?**
A: Create additional rule files in `rules/` for your team or project-specific standards.

**Q: Can I use this with other AI agents?**
A: Yes! Works with Claude, Gemini, Copilot, and others.

**Q: Is there a cost?**
A: No! Omniskill is open source and free.

---

## 🚀 Next Steps

1. **Install your bundle**: `/bundle-install <your-role>`
2. **Explore skills**: `/skill-search <topic>`
3. **Run a workflow**: `/workflow-run <workflow-id>`
4. **Mention an agent**: `@architect` or `@security-reviewer`
5. **Learn**: `/learn` to extract patterns into new skills

---

## 📞 Support

- **Documentation**: See `README.md` and `docs/`
- **Issues**: GitHub issues
- **Discussions**: GitHub discussions
- **Contributing**: See `CONTRIBUTING.md`

---

## 🎉 You're Ready!

Install your first bundle:
```
/bundle-install startup-founder
```

Then explore your new AI principal engineer!

