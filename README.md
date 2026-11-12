# AI Toolbox

A portable library of AI agent skills and subagents for the whole development lifecycle: research, planning, and implementation. It contains no application code. Install the skills into any project with `npx skills add`, and copy the subagents if you use Claude Code.

Skills read the **target project's** `AGENTS.md` for its stack and conventions.

## Install

```bash
# Every skill
npx skills add davidpn11/ai-toolbox --agent claude-code

# A few
npx skills add davidpn11/ai-toolbox --skill lifecycle --skill research --agent claude-code

# See what's available
npx skills add davidpn11/ai-toolbox --list
```

Swap `--agent claude-code` for any supported target (`cursor`, `codex`, `windsurf`, ...). The CLI installs into that tool's own skills directory and flattens the phase folders, so every skill refers to the others by name.

Claude Code subagents are not part of the skills ecosystem. Copy them by hand:

```bash
mkdir -p /path/to/project/.claude/agents
cp ai-toolbox/.agents/agents/*.md /path/to/project/.claude/agents/
```

Each subagent preloads skills by name, so install the skills too.

## Work across repos with Orca

When a change in one repo needs changes in another, install one skill globally, once:

```bash
npx skills add davidpn11/ai-toolbox --skill orca-project-setup -g --agent claude-code --agent codex
```

Then, in Claude or Codex anywhere, say `/orca-project-setup <repo A> <repo B>`. It creates an Orca folder workspace grouping the repos, installs every skill in this collection into it for both agents, and writes one `AGENTS.md` describing each repo (stack, verify commands, contracts). The repos are not touched. Open the project in Orca and ask for the feature: the `orca-planner` skill plans it, runs each task as an Orca worker (Claude or Codex) in that repo's own worktree, has the diffs reviewed by the other model family, and opens one PR per repo in merge order.

| Skill | What it does | Invoked by |
|-------|--------------|------------|
| `orca-project-setup` | Creates the Orca project for a set of repos, installs the skills, describes the repos | user (install globally) |
| `orca-planner` | Plans with `planner`, builds through Orca workers per repo, one PR per repo | user, `lifecycle` |

Keep the other skills out of your global install: Claude Code prefers a global skill over a project skill with the same name, so a global `planner` would replace the project's copy. The setup skill checks for clashes.

## The flow

```
/lifecycle <idea>
   │
   ├─ 1. Research ── investigation · spike · research · prototype
   │                 (what exists, what works, what the docs say)
   │
   ├─ 2. Planning ── product-research → design-research → grilling + domain-modeling
   │                 → codebase-design → spec → planner
   │                 (questionnaire and prototype when a question can't be asked here)
   │
   └─ 3. Implementation ── architect → specialists in waves → code-review → security wave
```

Every phase writes into one feature folder, and the next phase reads it:

```
docs/features/<slug>/
  research/*.md  investigation-*.md  spike-*.md
  product-brief.md  design-brief.md  questionnaire-*.md  rationale-*.md
  spec.md  plan.yaml
CONTEXT.md        glossary (project-wide)
docs/adr/         decisions (project-wide)
```

Because the state lives in files, `/lifecycle <slug>` resumes in a fresh session from wherever the work stopped.

## Skills

### Shared

| Skill | What it does | Invoked by |
|-------|--------------|------------|
| `lifecycle` | Conductor: detects the phase from the feature folder and runs the next skill | user |
| `delegation` | Model tiers (fast, standard, deep), the subagent brief format, and the response contract | model |
| `doc-templates` | Feature folder layout, writing rules (provenance, confidence tiers, gaps), and templates for research, investigation, spike, briefs, questionnaire, ADR, rationale, spec, and plan | model |

### Research: find out everything the feature depends on

| Skill | What it does | Runs on |
|-------|--------------|---------|
| `research` | One question, primary sources, one cited note | forked background subagent, `sonnet` |
| `investigation` | How the current code works, why, and what a change touches | `scout` fan-out on `haiku`, verified by the main model |
| `spike` | Time-boxed feasibility test with a GO / NO-GO / INCONCLUSIVE verdict | main model, `runner` for measurements |
| `prototype` | Throwaway code that answers one design question (logic demo, UI variants, or a script) | main model |
| `unslop` | Removes AI-writing tells from prose and slop from code; every document passes through it | main model |

`unslop` feeds `research`, which feeds `investigation` and `spike`.

### Planning: decide what to build, then how

| Skill | What it does | Invoked by |
|-------|--------------|------------|
| `product-research` | Problem, users, alternatives, competitors, success signals, through parallel research; writes the product brief | model |
| `design-research` | Flows, every screen state, prior-art patterns, design-system fit, accessibility; writes the design brief | model |
| `grilling` | Interview in rounds until nothing is silently assumed; facts found by agents, decisions put to the user | model |
| `grill-with-docs` | `grilling` plus `domain-modeling`, as one command | user |
| `domain-modeling` | `CONTEXT.md` glossary and ADRs, written the moment a term or decision settles | model |
| `questionnaire` | A document for someone else to fill in when the answer is in their head | model |
| `codebase-design` | Deep-module vocabulary, red flags, design-it-twice, rationale pages | model |
| `architecture-review` | Scans for deepening opportunities and grills through the one you pick | user |
| `figma-design` | Figma MCP in both directions: design to code, code and prototypes to canvas | model |
| `spec` | Synthesizes the feature folder into one buildable spec | model |
| `planner` | Spec to `plan.yaml`: vertical slices, single-specialist tasks, waves, contracts, tiers | model |

### Implementation: build it

| Skill | What it does |
|-------|--------------|
| `architect` | Executes `plan.yaml` wave by wave through the specialists, then code review and a security wave |
| `fe-engineer`, `ui-engineer`, `be-js-engineer`, `be-rust-engineer`, `quality-engineer`, `security-engineer` | Specialist personas, one per domain |
| `react-tailwind`, `elysia-api`, `playwright-testing`, `owasp-security`, `monorepo` | Reference material the personas load |
| `code-review` | Parallel reviewers per axis (Standards, Spec, Quality, Blast radius), then lead judgment |
| `resolve-merge-conflicts` | Resolves conflicts by intent; never aborts; checks pass before commit |

`code-review` shares its name with Claude Code's built-in `/code-review`. Installing it shadows the built-in one; rename the directory if you want both.

## Subagents and model tiers

Cheap work goes to cheap models; the user conversation and decisions stay on the main model. The `delegation` skill holds the rules; these Claude Code subagents put them into practice:

| Subagent | Model | Job |
|----------|-------|-----|
| `scout` | `haiku` | Read-only fact-finding: files, call sites, history, with `path:line` evidence |
| `runner` | `haiku` | Runs tests, builds, benchmarks, scripts; reports output; never fixes |
| `fe-engineer`, `ui-engineer`, `be-js-engineer`, `be-rust-engineer`, `quality-engineer` | `sonnet` | One plan task each, preloading the persona and reference skills |
| `security-engineer` | `sonnet` | Read-only audit |
| `architect` | `inherit` | Orchestrator. Run it as the main session agent (`claude --agent architect`); a subagent cannot spawn subagents |

The `research` skill forks its own background subagent on `sonnet` through skill frontmatter (`context: fork`, `model: sonnet`), so calling it once per question fans out research in parallel. Harnesses without these keys ignore them and follow the same instructions in the skill body.

## Structure

```
.agents/
├── agents/              Claude Code subagents (copy to .claude/agents/)
└── skills/
    ├── shared/          lifecycle, delegation, doc-templates
    ├── research/        research, investigation, spike, prototype, unslop
    ├── planning/        product-research, design-research, grilling, grill-with-docs,
    │                    domain-modeling, questionnaire, codebase-design,
    │                    architecture-review, figma-design, spec, planner
    └── implementation/  architect, the six personas, five reference skills,
                         code-review, resolve-merge-conflicts
research/                decisions and surveys about this repo (ADR-001, ADR-002)
THIRD_PARTY_NOTICES.md   MIT notices for adapted skills
```

Skills sit exactly at `.agents/skills/<phase>/<skill>/SKILL.md`. A phase folder must not contain a `SKILL.md` of its own: the `skills` CLI stops descending at the first one it finds. See [ADR-001](research/ADR-001-three-phase-skill-layout.md) for this layout and [ADR-002](research/ADR-002-skills-survey-mattpocock-cursor-pstack.md) for the survey behind the adapted skills.

## Credits

Many workflow skills are adapted from [mattpocock/skills](https://github.com/mattpocock/skills) and [cursor/plugins](https://github.com/cursor/plugins), both MIT. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
