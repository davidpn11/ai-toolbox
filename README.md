# AI Toolbox

A portable library of reusable AI agents and skills. This repo contains no application code — it exists solely to store agent definitions and skill modules that can be copied into any project.

## How to Use

Copy the `.claude/agents/` and `.claude/skills/` directories (or individual files) into your target project. Agents read the **target project's** `AGENTS.md` for workspace conventions, not this repo's.

## Available Agents

| Agent | Role | Tools | Invocation |
|-------|------|-------|------------|
| `architect` | Orchestrator — delegates all work, never implements directly | Read-only + agent delegation | User-invocable, primary entry point |
| `planner` | Context enricher — asks questions, creates plan.yaml with DAG of tasks | Read-only | Subagent of architect |
| `fe-engineer` | Frontend implementation — React 19, TS, Tailwind v4, Next.js/Vite | Full edit | Subagent |
| `ui-engineer` | Web quality — accessibility (WCAG 2.1 AA), SEO, Core Web Vitals | Full edit | Subagent |
| `be-js-engineer` | Backend JS — TypeScript + Bun.js APIs | Full edit | Subagent |
| `be-rust-engineer` | Backend Rust — Axum/Actix APIs and scripts | Full edit | Subagent |
| `quality-engineer` | Testing — Vitest unit tests, Playwright e2e | Full edit | Subagent |
| `security-engineer` | Security audit — OWASP Top 10, secrets, vulnerabilities | Read-only (never modifies code) | Subagent |

## Skills

Reusable knowledge modules shared across agents:

| Skill | Used By |
|-------|---------|
| `react-tailwind` | fe-engineer, ui-engineer |
| `bun-api` | be-js-engineer |
| `playwright-testing` | quality-engineer |
| `owasp-security` | security-engineer |
| `monorepo` | fe-engineer, be-js-engineer, architect |

## Installation

### Copy everything

```bash
cp -r ai-toolbox/.claude /path/to/your-project/
cp ai-toolbox/AGENTS.md /path/to/your-project/  # optional — adapt for your project
```

### Cherry-pick individual agents or skills

```bash
# Single agent
cp ai-toolbox/.claude/agents/fe-engineer.md /path/to/your-project/.claude/agents/

# Single skill
cp -r ai-toolbox/.claude/skills/react-tailwind /path/to/your-project/.claude/skills/
```

After copying, edit the target project's `AGENTS.md` to declare its own stack, coding standards, and conventions. The agents will read that file at runtime.

## Architecture

The **architect** agent orchestrates all work. It never implements directly — instead it delegates to specialized agents through a plan-based workflow:

```
User Request
    │
    ▼
┌──────────┐     ┌──────────┐
│ architect │────▶│ planner  │  ← asks questions, creates plan.yaml
└──────────┘     └──────────┘
    │
    ▼ (delegates per plan)
┌────────────────────────────────────────────────┐
│  fe-engineer  │  be-js-engineer   │  ui-engineer│
│  be-rust-engineer   │  quality-engineer         │
└────────────────────────────────────────────────┘
    │
    ▼ (final review)
┌───────────────────┐
│ security-engineer │  ← read-only audit
└───────────────────┘
```

## Structure

```
.claude/
├── agents/          # 8 specialized agents
│   ├── architect.md
│   ├── planner.md
│   ├── fe-engineer.md
│   ├── ui-engineer.md
│   ├── be-js-engineer.md
│   ├── be-rust-engineer.md
│   ├── quality-engineer.md
│   └── security-engineer.md
└── skills/          # Reusable knowledge modules
    ├── react-tailwind/
    ├── bun-api/
    ├── playwright-testing/
    ├── owasp-security/
    └── monorepo/
AGENTS.md            # Delegation protocol & agent catalog
```

## Delegation Protocol

See [AGENTS.md](AGENTS.md) for the full delegation protocol, plan schema, task lifecycle, and execution rules.
