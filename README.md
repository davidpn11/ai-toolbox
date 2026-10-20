# AI Toolbox

A portable library of reusable AI agents and skills. This repo contains no application code — it exists solely to store agent definitions and skill modules that can be copied — or installed — into any project.

## How to Use

Two install paths, depending on what you're pulling in:

- **Skills** (`.agents/skills/`) — installable with the [`skills` CLI](https://github.com/vercel-labs/skills) (`npx skills add`), which works across 75+ AI coding tools. This includes both the domain-knowledge skills (react-tailwind, elysia-api, ...) and a Skill-format version of every agent persona below, so tools that don't support Claude Code-style subagents still get the same expertise.
- **Subagents** (`.agents/agents/`) — Claude Code-native subagent definitions (isolated context window, restricted tool access, dedicated model). These aren't part of the Skills ecosystem, so they're copied by hand — see [Copy everything](#copy-everything) below.

Either way, agents/skills read the **target project's** `AGENTS.md` for workspace conventions, not this repo's.

## Install with `npx skills add`

```bash
# Pull every skill (personas + domain knowledge) into the current project
npx skills add davidpn11/ai-toolbox --agent claude-code

# Cherry-pick one or more
npx skills add davidpn11/ai-toolbox --skill fe-engineer --skill react-tailwind --agent claude-code

# See what's available without installing
npx skills add davidpn11/ai-toolbox --list
```

Swap `--agent claude-code` for any other supported target (`cursor`, `codex`, `windsurf`, etc.) — the CLI installs into that tool's own skills directory. Omit `--agent` and it will prompt.

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

`.agents/skills/` — every entry here is `npx skills add`-installable.

**Agent-persona skills** (Skill-format twin of each subagent above, for tools without subagent support):

| Skill | Companion subagent |
|-------|---------------------|
| `architect` | `architect` |
| `planner` | `planner` |
| `fe-engineer` | `fe-engineer` |
| `ui-engineer` | `ui-engineer` |
| `be-js-engineer` | `be-js-engineer` |
| `be-rust-engineer` | `be-rust-engineer` |
| `quality-engineer` | `quality-engineer` |
| `security-engineer` | `security-engineer` |

**Domain-knowledge skills** — reusable reference material, used by the agents above:

| Skill | Used By |
|-------|---------|
| `react-tailwind` | fe-engineer, ui-engineer |
| `elysia-api` | be-js-engineer |
| `playwright-testing` | quality-engineer |
| `owasp-security` | security-engineer |
| `monorepo` | fe-engineer, be-js-engineer, architect |

**Workflow skills** — reusable engineering workflows, independent of the persona agents. Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) and [cursor/plugins](https://github.com/cursor/plugins) (both MIT, see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)); the survey behind them is in [docs/research/](docs/research/skills-survey-mattpocock-cursor-pstack.md).

| Skill | What it does | Invoked by |
|-------|--------------|------------|
| `grilling` | Interview the user in rounds until nothing is silently assumed; facts found by the agent, decisions put to the user | user or model |
| `grill-with-docs` | `grilling` plus `domain-modeling`: the interview writes `CONTEXT.md` and ADRs as it goes | user |
| `domain-modeling` | Glossary and ADR discipline (`CONTEXT.md`, `docs/adr/`), with the three-gate ADR rule | model |
| `research` | Background agent, primary sources only, cited Markdown under `docs/research/` with confidence tiers | model |
| `prototype` | Throwaway code that answers one design question: shareable HTML logic demo, or structurally different UI variants behind `?variant=` | model |
| `codebase-design` | Deep-module vocabulary (module, interface, seam, adapter, depth, locality), red flags, design-it-twice, rationale template | model |
| `architecture-review` | Scan for deepening opportunities, visual before/after report, then grill through the chosen candidate | user |
| `code-review` | Parallel reviewers per axis (Standards, Spec, optional Quality and Blast radius), then lead judgment into Act on / Consider / Noted / Dismissed | model |
| `resolve-merge-conflicts` | Resolve by intent from commits, PRs, and issues; never `--abort`; checks green before commit | model |
| `unslop` | Numbered list of AI-writing tells to remove from prose, plus a code-slop section | model |
| `figma-design` | Figma MCP server workflow in both directions: design to code with Code Connect and tokens, code and prototypes back to the canvas | model |

`code-review` shares its name with Claude Code's built-in `/code-review`. Installing it into a project shadows the built-in one; rename the directory if you want both.

## Installation

### `npx skills add` (recommended for skills)

See [Install with `npx skills add`](#install-with-npx-skills-add) above. This installs from `.agents/skills/` — both the persona skills and the domain-knowledge skills — into the target project's own skills directory, in the format that project's tool expects.

### Copy everything (only way to get native Claude Code subagents)

```bash
cp -r ai-toolbox/.agents /path/to/your-project/
cp ai-toolbox/AGENTS.md /path/to/your-project/  # optional — adapt for your project
```

### Cherry-pick individual agents or skills

```bash
# Single subagent
cp ai-toolbox/.agents/agents/fe-engineer.md /path/to/your-project/.agents/agents/

# Single skill (works for both persona and domain-knowledge skills)
cp -r ai-toolbox/.agents/skills/react-tailwind /path/to/your-project/.agents/skills/
```

After copying or installing, edit the target project's `AGENTS.md` to declare its own stack, coding standards, and conventions. The agents/skills read that file at runtime.

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
.agents/
├── agents/                # 8 Claude Code subagents (copy-only, not npx-installable)
│   ├── architect.md
│   ├── planner.md
│   ├── fe-engineer.md
│   ├── ui-engineer.md
│   ├── be-js-engineer.md
│   ├── be-rust-engineer.md
│   ├── quality-engineer.md
│   └── security-engineer.md
└── skills/                # npx skills add-installable — personas + knowledge
    ├── architect/         SKILL.md
    ├── planner/           SKILL.md
    ├── fe-engineer/       SKILL.md
    ├── ui-engineer/       SKILL.md
    ├── be-js-engineer/    SKILL.md
    ├── be-rust-engineer/  SKILL.md
    ├── quality-engineer/  SKILL.md
    ├── security-engineer/ SKILL.md
    ├── react-tailwind/    SKILL.md
    ├── elysia-api/        SKILL.md
    ├── playwright-testing/SKILL.md
    ├── owasp-security/    SKILL.md
    ├── monorepo/          SKILL.md
    ├── grilling/          SKILL.md
    ├── grill-with-docs/   SKILL.md
    ├── domain-modeling/   SKILL.md, CONTEXT-FORMAT.md, ADR-FORMAT.md
    ├── research/          SKILL.md
    ├── prototype/         SKILL.md, LOGIC.md, UI.md
    ├── codebase-design/   SKILL.md, DEEPENING.md, DESIGN-IT-TWICE.md, DESIGN-RED-FLAGS.md, RATIONALE.md
    ├── architecture-review/ SKILL.md, HTML-REPORT.md
    ├── code-review/       SKILL.md, references/
    ├── resolve-merge-conflicts/ SKILL.md
    ├── unslop/            SKILL.md
    └── figma-design/      SKILL.md
AGENTS.md                  # Delegation protocol & agent catalog
THIRD_PARTY_NOTICES.md     # MIT notices for adapted skills
docs/research/             # Research notes written by the research skill
```

## Delegation Protocol

See [AGENTS.md](AGENTS.md) for the full delegation protocol, plan schema, task lifecycle, and execution rules.
