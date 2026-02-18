#!/usr/bin/env python3
"""
Migrate ECC skills into categorized structure and merge with AAS skills.
Organizes all skills into: _core, architecture, languages, frameworks, testing, 
databases, infrastructure, security, ai-ml, business, cloud-providers, 
workflow-automation, collaboration, specialized.
"""

import os
import shutil
import json
from pathlib import Path
from typing import Dict, List, Set

# ECC repo path
ECC_SKILLS_DIR = Path("/Users/bradbowden/GolandProjects/everything-claude-code/skills")
AAS_SKILLS_DIR = Path("/Users/bradbowden/GolandProjects/antigravity-awesome-skills/skills")

# Skill categorization mapping
SKILL_CATEGORIES = {
    # Core foundational skills
    "_core": {
        "coding-standards",
        "tdd-workflow",
        "security-review",
        "verification-loop",
        "eval-harness",
        "continuous-learning",
        "continuous-learning-v2",
        "iterative-retrieval",
        "strategic-compact",
        "staff-principles",
        "configure-ecc",
    },
    
    # Architecture & system design
    "architecture": {
        "distributed-systems",
        "event-driven-architecture",
        "sharding-partitioning",
        "multi-cloud-region",
        "caching-queueing",
        "advanced-concurrency",
        "advanced-networking",
        "advanced-performance",
        "advanced-testing",
        "architecture-decision-records",
        "c4-context",
        "microservices-patterns",
    },
    
    # Languages
    "languages": {
        "golang-patterns",
        "python-patterns",
        "python-testing",
        "java-coding-standards",
        "cpp-coding-standards",
        "cpp-testing",
        "swift-actor-persistence",
        "swift-protocol-di-testing",
        "typescript-expert",
        "rust-pro",
        "java-pro",
    },
    
    # Frameworks
    "frameworks": {
        "backend-patterns",
        "frontend-patterns",
        "django-patterns",
        "django-security",
        "django-tdd",
        "django-verification",
        "springboot-patterns",
        "springboot-security",
        "springboot-tdd",
        "springboot-verification",
        "jpa-patterns",
        "react-patterns",
        "nextjs-best-practices",
        "flutter-expert",
        "laravel-expert",
        "shopify-development",
        "remotion-best-practices",
    },
    
    # Testing
    "testing": {
        "golang-testing",
        "e2e-testing",
        "webapp-testing",
    },
    
    # Databases
    "databases": {
        "postgres-patterns",
        "clickhouse-io",
        "query-optimization",
        "data-management",
        "data-redundancy-search",
        "database-migrations",
        "prisma-expert",
        "neon-postgres",
    },
    
    # Infrastructure & DevOps
    "infrastructure": {
        "platform-engineering",
        "deployment-patterns",
        "deployment-strategies",
        "docker-patterns",
        "observability",
        "incident-analysis",
        "kubernetes-architect",
        "terraform-specialist",
        "aws-serverless",
        "helm-chart-scaffolding",
    },
    
    # Security & Compliance
    "security": {
        "encryption-strategies",
        "secrets-management",
        "network-security-mesh",
        "rotation-strategies",
        "security-scan",
        "pentest-checklist",
        "ethical-hacking-methodology",
        "vulnerability-scanner",
        "threat-modeling-expert",
    },
    
    # AI/ML
    "ai-ml": {
        "cost-aware-llm-pipeline",
        "regex-vs-llm-structured-text",
        "rag-engineer",
        "prompt-engineer",
        "ai-agents-architect",
        "langchain-architecture",
        "vector-database-engineer",
    },
    
    # Business
    "business": {
        "seo-audit",
        "pricing-strategy",
        "copywriting",
        "product-manager-toolkit",
        "business-analyst",
        "startup-metrics-framework",
        "legal-advisor",
    },
    
    # Workflow Automation
    "workflow-automation": {
        "n8n-code-python",
        "n8n-node-configuration",
        "airflow-dag-patterns",
        "temporal-python-pro",
        "zapier-make-patterns",
    },
    
    # Collaboration
    "collaboration": {
        "brainstorming",
        "writing-skills",
        "postmortem-writing",
        "wiki-architect",
    },
    
    # Specialized/Niche
    "specialized": {
        "nutrient-document-processing",
        "content-hash-cache-pattern",
        "env-compat-extend",
        "api-design",
        "config-management",
        "config-servicing",
        "live-updates",
        "resilience-backups",
        "resource-optimization",
        "rotation-strategies",
        "storage-tiers",
        "notifications",
        "loki-mode",
        "unity-developer",
    },
    
    # Cloud Providers (will handle separately)
    "cloud-providers": set(),  # Will be populated from AAS
}

def migrate_ecc_skills():
    """Migrate ECC skills from flat structure to categorized structure."""
    print("Starting ECC skill migration...")
    
    for category, skill_names in SKILL_CATEGORIES.items():
        if category == "cloud-providers":
            continue
            
        target_dir = ECC_SKILLS_DIR / category
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for skill_name in skill_names:
            source = ECC_SKILLS_DIR / skill_name
            dest = target_dir / skill_name
            
            if source.exists() and not dest.exists():
                print(f"  Moving {skill_name} -> {category}/")
                shutil.move(str(source), str(dest))
            elif dest.exists():
                print(f"  {skill_name} already in {category}/")
            elif not source.exists():
                print(f"  WARNING: {skill_name} not found in ECC")

def migrate_aas_skills():
    """Migrate AAS skills into categorized structure."""
    print("\nStarting AAS skill migration...")
    
    if not AAS_SKILLS_DIR.exists():
        print(f"  WARNING: AAS skills dir not found at {AAS_SKILLS_DIR}")
        return
    
    # Azure skills go to cloud-providers/azure
    azure_pattern = "azure-"
    aws_pattern = "aws-"
    gcp_pattern = "gcp-"
    
    # Other AAS category patterns
    aas_to_category = {
        # AI/ML
        ("rag-", "prompt-", "llm-", "langgraph", "langchain", "vector-"): "ai-ml",
        
        # Business
        ("seo-", "pricing-", "copywriting", "marketing-", "startup-", "business-", "legal-"): "business",
        
        # Workflow automation
        ("n8n-", "airflow-", "temporal-", "zapier-", "inngest", "trigger-"): "workflow-automation",
        
        # Collaboration & Writing
        ("brainstorming", "writing-", "postmortem-", "wiki-", "documentation-"): "collaboration",
        
        # Frameworks
        ("flutter-", "react-", "nextjs-", "laravel-", "shopify-", "remotion-", "unity-"): "frameworks",
        
        # Specialized
        ("loki-", "remotion-"): "specialized",
    }
    
    aas_skills = [d for d in AAS_SKILLS_DIR.iterdir() if d.is_dir()]
    
    for skill_dir in sorted(aas_skills)[:50]:  # Start with first 50 for testing
        skill_name = skill_dir.name
        
        # Skip if already in ECC
        if any(skill_name in names for names in SKILL_CATEGORIES.values() if isinstance(names, set)):
            continue
        
        # Determine category
        category = "specialized"
        
        if skill_name.startswith("azure-"):
            category = "cloud-providers/azure"
        elif skill_name.startswith("aws-"):
            category = "cloud-providers/aws"
        elif skill_name.startswith("gcp-"):
            category = "cloud-providers/gcp"
        else:
            for patterns, cat in aas_to_category.items():
                if any(skill_name.startswith(p) for p in patterns):
                    category = cat
                    break
        
        target_dir = ECC_SKILLS_DIR / category
        target_dir.mkdir(parents=True, exist_ok=True)
        
        dest = target_dir / skill_name
        if not dest.exists():
            print(f"  Copying {skill_name} -> {category}/")
            shutil.copytree(str(skill_dir), str(dest), dirs_exist_ok=False)

def handle_overlapping_skills():
    """Handle 11 overlapping skills - merge or keep best version."""
    print("\nHandling overlapping skills...")
    
    overlapping = [
        "python-patterns",
        "secrets-management", 
        "tdd-workflow",
        "cc-skill-backend-patterns",
        "cc-skill-clickhouse-io",
        "cc-skill-coding-standards",
        "cc-skill-continuous-learning",
        "cc-skill-frontend-patterns",
        "cc-skill-project-guidelines-example",
        "cc-skill-security-review",
        "cc-skill-strategic-compact",
    ]
    
    print(f"  Found {len(overlapping)} overlapping skills")
    for skill in overlapping:
        print(f"    - {skill}")

if __name__ == "__main__":
    migrate_ecc_skills()
    migrate_aas_skills()
    handle_overlapping_skills()
    print("\nMigration complete!")
