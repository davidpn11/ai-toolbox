# AI Toolbox

A portable library of AI agent skills for the whole development lifecycle: research, planning, and implementation. It contains no application code.

The skills are built for a **planner hub**: one folder (its own git repo) where a single planner runs every feature, whether it touches one repo or several. The planner hands each task to an Orca worker (Claude or Codex) in that repo's own worktree. Repos stay independent and carry only facts, in their `AGENTS.md`; the process lives here.

## Install into the hub

Install at project level, from inside the hub, for both agents, and commit the result so every worktree of the hub has the skills:

```bash
cd /path/to/hub
npx skills add davidpn11/ai-toolbox --agent claude-code
npx skills add davidpn11/ai-toolbox --agent codex
mkdir -p .claude/agents && cp /path/to/ai-toolbox/.agents/agents/*.md .claude/agents/
git add -A && git commit -m "Install ai-toolbox"
```

Update later with `npx skills update -p`, then commit. The hub needs an `AGENTS.md` (template: `AGENTS-HUB.md` in `doc-templates`) and a `CLAUDE.md` holding `@AGENTS.md`. Add each repo with the `onboard-repo` skill.

Do not install the same skill names globally: Claude Code prefers personal skills (`~/.claude/skills`) over project skills, so a global `planner` or `grilling` would silently replace the hub's.

The CLI flattens the phase folders, so every skill refers to the others by name.

## The flow

```
/lifecycle <idea>            (in the hub)
   │
   ├─ 1. Research ── investigation · spike · research · prototype
   │
   ├─ 2. Planning ── product-research → design-research → grilling + domain-modeling
   │                 → codebase-design → spec → planner (plan.yaml)
   │
   └─ 3. Implementation ── planner → Orca workers per repo, in waves
                           → cross-family review → security wave → one PR per repo
```

Every phase writes into one feature folder in the hub, and the next phase reads it:

```
features/<slug>/
  research/*.md  investigation-*.md  spike-*.md
  product-brief.md  design-brief.md  questionnaire-*.md  rationale-*.md
  spec.md  plan.yaml
  tasks/<task_id>.md   self-contained spec file for each Orca worker
```

Because the state lives in files, `/lifecycle <slug>` resumes in a fresh session from wherever the work stopped.

## Skills

### Shared

| Skill | What it does | Invoked by |
|-------|--------------|------------|
| `lifecycle` | Conductor: detects the phase from the feature folder and runs the next skill | user |
| `delegation` | Tiers and runtimes (Claude, Codex), the subagent brief, the worker spec file, and the response contract | model |
| `doc-templates` | Feature folder layout, writing rules, and templates, including the hub and repo `AGENTS.md` | model |
| `onboard-repo` | Writes a repo's `AGENTS.md` (stack per path, verify commands, contracts) and adds it to the hub registry | user, `planner` |

### Research: find out everything the feature depends on

| Skill | What it does | Runs on |
|-------|--------------|---------|
| `research` | One question, primary sources, one cited note | forked background subagent, `sonnet` |
| `investigation` | How the current code works, why, and what a change touches | `scout` fan-out, verified by the main model |
| `spike` | Time-boxed feasibility test with a GO / NO-GO / INCONCLUSIVE verdict | main model, `runner` for measurements |
| `prototype` | Throwaway code that answers one design question | main model |

Prose passes through `unslop`, which this collection expects to be installed separately (cursor/plugins).

### Planning: decide what to build, then how

| Skill | What it does | Invoked by |
|-------|--------------|------------|
| `product-research` | Problem, users, alternatives, success signals; writes the product brief | model |
| `design-research` | Flows, screen states, prior art, accessibility; writes the design brief | model |
| `grilling` | Interview in rounds until nothing is silently assumed | model |
| `domain-modeling` | `CONTEXT.md` glossary and ADRs, written the moment a term or decision settles | model |
| `questionnaire` | A document for someone else to fill in | model |
| `codebase-design` | Deep-module vocabulary, design-it-twice, rationale pages, and an architecture review mode | model, user |
| `figma-design` | Figma MCP in both directions | model |
| `spec` | Synthesizes the feature folder into one buildable spec | model |
| `planner` | Spec to `plan.yaml`, then runs it: Orca workers per repo in waves, cross-family review, one PR per repo in merge order | user, model |

### Implementation: what the workers get

The planner pastes a specialist skill into each worker's spec file, chosen from the repo's stack.

| Skill | What it does |
|-------|--------------|
| `fe-engineer`, `ui-engineer`, `be-js-engineer`, `be-rust-engineer`, `quality-engineer`, `security-engineer` | Specialist personas, one per stack; each carries its own reference file |
| `elysia-api`, `monorepo` | Reference material added to a spec when the repo needs it |
| `branch-review` | Parallel reviewers per axis (Standards, Spec, Quality, Blast radius), then lead judgment |
| `resolve-merge-conflicts` | Resolves conflicts by intent; never aborts; checks pass before commit |

## Subagents

Read-only Claude Code helpers plus the planner entry point. Copy them to the hub's `.claude/agents/`.

| Subagent | Model | Job |
|----------|-------|-----|
| `scout` | `haiku` | Read-only fact-finding with `path:line` evidence |
| `runner` | `haiku` | Runs tests, builds and scripts; reports output; never fixes |
| `planner` | `inherit` | The hub's main session agent (`claude --agent planner`) |

Repo code is only ever edited by Orca workers, so there are no per-specialist subagents. Codex uses the same skills and no subagents.

The `research` skill forks its own background subagent through skill frontmatter (`context: fork`, `model: sonnet`). Harnesses without these keys ignore them and follow the same instructions in the skill body.

## Structure

```
.agents/
├── agents/              scout, runner, planner (copy to the hub's .claude/agents/)
└── skills/
    ├── shared/          lifecycle, delegation, doc-templates, onboard-repo
    ├── research/        research, investigation, spike, prototype
    ├── planning/        product-research, design-research, grilling, domain-modeling,
    │                    questionnaire, codebase-design, figma-design, spec, planner
    └── implementation/  the six personas, elysia-api, monorepo,
                         branch-review, resolve-merge-conflicts
research/                decisions and surveys about this repo (ADR-001, ADR-002)
THIRD_PARTY_NOTICES.md   MIT notices for adapted skills
```

Skills sit exactly at `.agents/skills/<phase>/<skill>/SKILL.md`. A phase folder must not contain a `SKILL.md` of its own: the `skills` CLI stops descending at the first one it finds. See [ADR-001](research/ADR-001-three-phase-skill-layout.md) and [ADR-002](research/ADR-002-skills-survey-mattpocock-cursor-pstack.md).

## Credits

Many workflow skills are adapted from [mattpocock/skills](https://github.com/mattpocock/skills) and [cursor/plugins](https://github.com/cursor/plugins), both MIT. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
