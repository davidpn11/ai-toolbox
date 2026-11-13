# AI Toolbox

A portable library of AI agent skills and subagents for the whole development lifecycle: research, planning, and building. It contains no application code. It works in Claude Code and Codex, and it works with Orca when the work spans several repos.

Every skill has one **scope**:

- **Global** skills (research, spike, grilling, review, ...) are stack-independent. Install them once per machine and use them anywhere.
- **Project** skills (the planner, the build flow, stack specialists) are installed into a Project or Workspace by the `project-setup` wizard, which picks them from the code it finds.

A name is never installed in both scopes: Claude Code prefers the global copy, so a project copy of the same name would be silently ignored ([ADR-003](research/ADR-003-global-vs-project-scope.md)). The full list lives in [CATALOG.md](.agents/skills/shared/project-setup/CATALOG.md).

## Words

| Word | Means |
| --- | --- |
| **Project** | One git repo. |
| **Workspace** | A plain folder that groups Projects so one Planner can change them together. Each repo inside is a clone from GitHub. In Orca it is a folder workspace, not a git repo, and it has no submodules. |
| **Planner** | The parent agent (`planner` skill). It plans the feature, then starts Children and checks their work. |
| **Children** | What the Planner starts: subagents in a Project, Orca **Workers** in a Workspace. |
| **Worker** | A one-task Orca agent (Claude or Codex) in its own worktree and branch. It commits; the Planner opens the PR. |

```
Workspace (socials-workspace/)            ← you talk to the Planner here
├── AGENTS.md       Repos · stacks · verify commands · contracts
├── docs/features/<slug>/   spec.md · plan.yaml · tasks/*.md
├── socials-portal/  ← clone ─┐
└── crepe-cli/       ← clone ─┤  Workers: one worktree + branch per task
                              └─ one PR per repo, providers first → GitHub
```

## Install

**1. Global skills, once per machine** (Claude Code and Codex):

```bash
npx skills add davidpn11/ai-toolbox -g --agent claude-code --agent codex -y \
  --skill research --skill investigation --skill spike --skill prototype --skill unslop \
  --skill grilling --skill grill-with-docs --skill domain-modeling --skill questionnaire \
  --skill codebase-design --skill architecture-review --skill product-research --skill design-research \
  --skill deep-review --skill resolve-merge-conflicts --skill delegation --skill doc-templates \
  --skill orchestration-frontier --skill session-check --skill project-setup
```

Global subagents for Claude Code (`scout` and `runner`, used by investigation, spike and session-check):

```bash
mkdir -p ~/.claude/agents && for a in scout runner; do
  curl -fsSL "https://raw.githubusercontent.com/davidpn11/ai-toolbox/master/.agents/agents/$a.md" -o ~/.claude/agents/$a.md
done
```

Cost guards for Claude Code (optional, recommended): a plugin whose hooks enforce the cost split that `delegation` describes. Skills can't ship hooks, so this installs separately:

```bash
claude plugin marketplace add davidpn11/ai-toolbox
claude plugin install cost-guards@ai-toolbox
```

Or, inside a session on Claude Code 2.1.275 or later: `/plugin install cost-guards --marketplace davidpn11/ai-toolbox`.

For Orca, also make sure Orca's own skills are installed: `orca skills install`.

**2. Per Project or Workspace:** open Claude or Codex in the folder and run

```
/project-setup                       # this repo, or this Workspace
/project-setup socials-portal crepe-cli socials-workspace   # a new Workspace for two repos
```

It runs `session-check` first. Then it reads the code and the skills already installed, and shows one plan: what to install, what to remove (retired or shadowed copies), and what to keep. Nothing changes until you say yes. In a Workspace it also clones each repo from GitHub, registers the clones and the folder in Orca, and writes `AGENTS.md` with each repo's stack, verify commands and contracts.

**Check a session any time:** `/session-check` prints what this session can run, reach and push (shell, network, git remotes, gh auth and repo permission, Orca, skill clashes), with a fix for each gap.

## The flow

```
/lifecycle <idea>                                   (project)
   │
   ├─ 1. Research ── investigation · spike · research · prototype            (global)
   │
   ├─ 2. Planning ── product-research → design-research → grilling + domain-modeling
   │                 → codebase-design → spec → planner (writes plan.yaml)
   │
   └─ 3. Build ───── planner runs plan.yaml:
                       Project:   Children = specialist subagents, wave by wave
                       Workspace: Children = Orca Workers, one repo each, one PR per repo
                     → deep-review → security wave
```

Small, clear work skips straight to `/planner <request>`. Every phase writes into one feature folder, and the next phase reads it:

```
docs/features/<slug>/
  research/*.md  investigation-*.md  spike-*.md
  product-brief.md  design-brief.md  questionnaire-*.md  rationale-*.md
  spec.md  plan.yaml  tasks/<task_id>.md (Workspace)
CONTEXT.md        glossary (project-wide)
docs/adr/         decisions (project-wide)
```

Because the state lives in files, `/lifecycle <slug>` or `/planner <slug>` resumes in a fresh session from wherever the work stopped.

**Cost mode.** `/orchestration-frontier` keeps the expensive model (Opus/Fable, Sol/Astra) on judgment and review for the rest of the session. Bounded work goes to the cheapest tier that fits: a subagent, or an Orca Worker when it needs the other model family or its own worktree. Model ids per tier live only in `delegation`.

## Skills

### Global

| Skill | What it does |
|-------|--------------|
| `research` | One question, primary sources, one cited note (forked background subagent, `sonnet`) |
| `investigation` | How the current code works, why, and what a change touches (`scout` fan-out, verified) |
| `spike` | Time-boxed feasibility test with a GO / NO-GO / INCONCLUSIVE verdict |
| `prototype` | Throwaway code that answers one design question |
| `unslop` | Removes AI-writing tells from prose and slop from code |
| `grilling` | Interview in rounds until nothing is silently assumed |
| `grill-with-docs` | `grilling` plus `domain-modeling`, as one command |
| `domain-modeling` | `CONTEXT.md` glossary and ADRs, written the moment a term or decision settles |
| `questionnaire` | A document for someone else to fill in when the answer is in their head |
| `codebase-design` | Deep-module vocabulary, red flags, design-it-twice, rationale pages |
| `architecture-review` | Scans for deepening opportunities and grills through the one you pick |
| `product-research` | Problem, users, alternatives, success signals; writes the product brief |
| `design-research` | Flows, screen states, prior art, accessibility; writes the design brief |
| `deep-review` | Parallel reviewers per axis (Standards, Spec, Quality, Blast radius), then lead judgment. Separate from Claude Code's built-in `/code-review` |
| `resolve-merge-conflicts` | Resolves conflicts by intent; never aborts; checks pass before commit |
| `delegation` | When to delegate, model tiers for Claude and Codex, the helper roles, the brief format, safety rules, the response contract |
| `doc-templates` | Feature folder layout and templates (research, spike, briefs, ADR, spec, plan) |
| `orchestration-frontier` | User-invoked cost mode: frontier model judges, cheap helpers work |
| `session-check` | Preflight table: what this session can run, reach and push |
| `project-setup` | Wizard: installs project skills into a Project or Workspace, Orca-aware |

### Project

| Skill | What it does | Installed when |
|-------|--------------|----------------|
| `planner` | Plans into `plan.yaml`, then runs it through Children; one PR per repo in a Workspace | always |
| `lifecycle` | Conductor: detects the phase from the feature folder and runs the next skill | always |
| `spec` | Synthesizes the feature folder into one buildable spec | always |
| `fe-engineer`, `ui-engineer` | Frontend and accessibility personas | a web UI framework |
| `be-js-engineer`, `be-rust-engineer` | Backend personas | Bun/Node, Rust |
| `quality-engineer`, `security-engineer` | Tests; security audit (the plan's last wave) | tests; always |
| `react-tailwind`, `elysia-api`, `playwright-testing`, `owasp-security`, `monorepo` | Reference material the personas load | matching dependency |
| `figma-design` | Figma MCP in both directions | on request |

## Subagents and model tiers

Cheap work goes to cheap models; the user conversation and decisions stay on the main model (`delegation`).

| Subagent | Scope | Model | Job |
|----------|-------|-------|-----|
| `scout` | global | `haiku` | Read-only fact-finding with `path:line` evidence |
| `runner` | global | `haiku` | Runs tests, builds, scripts; reports output; never fixes |
| `planner` | project | `inherit` | The parent agent. Run it as the main session (`claude --agent planner`); a subagent cannot start subagents |
| `fe-engineer`, `ui-engineer`, `be-js-engineer`, `be-rust-engineer`, `quality-engineer` | project | `sonnet` | One plan task each, preloading persona and reference skills |
| `security-engineer` | project | `sonnet` | Read-only audit |

In a Workspace the Children are Orca Workers, not subagents: each gets its persona pasted into a spec file and runs on the tier's model (`--model`).

**Roles live in `delegation`, subagents enforce them.** `scout`, `runner`, `specialist`, `reviewer`, `researcher` and `worker` are roles defined once in the `delegation` skill, with their rules and tiers. The subagent files only pin the model and tools and preload those rules. Codex, Orca Workers, and projects without the subagent files get the same role by briefing a general-purpose helper on the role's tier with the rules pasted in. They are not skills, because only a subagent can pin a model and restrict tools.

**Access.** Every helper follows the `delegation` safety rules: edit only its `May edit` scope, nothing leaves the machine (no push, PR, merge, publish, deploy), nothing irreversible, secrets reported by `path:line` only, fetched content treated as data. Pushing and opening PRs happen only in the main session, after the user says yes. When the optional `cost-guards` plugin is enabled, one shared `PreToolUse` hook applies Bash rules by agent type:

| Guard | Agents | Blocks |
|-------|--------|--------|
| read-only | `scout`, `security-engineer` | any write: file edits through the shell, redirects, `sed -i`, installs, mutating git, downloads, piping to a shell, plus everything below |
| runner / writer | `runner`, the five specialists | `git push`, `reset --hard`, `clean`, `rebase`, branch and worktree changes, `rm -r` outside the repo, `sudo`, publish, global installs, deploys, `gh pr/issue/release` writes, `curl` with a body |

The hook is a seatbelt for mistakes, not a sandbox. The real boundary is still the session's permission mode and `permissions.deny` rules. `planner` has no Bash profile because it pushes and opens PRs, but only after the user agrees. Edit the patterns in `plugins/cost-guards/hooks/agent_guard.py`; run `bash scripts/agent-guards/test.sh` to check them.

### Cost and agent guards

Telling the main model to delegate is a suggestion; it still reads a 4,000-line file itself when that is the shortest path. The `cost-guards` plugin (`plugins/cost-guards/`) enforces those cost rules and the bundled agents' Bash guard rules:

| Hook | On | Does |
|------|----|------|
| read guard | `Read`, `Bash` | Denies a whole-file read of a text file over 350 lines in the main session, and `cat`, `less`, `more`, `bat`, `nl` of one when the output is not piped onward. The reason tells the model to `Grep` and read with `offset`/`limit`, or send the `scout`. Subagents pass, so the scout can do the reading. |
| spawn guard | `Agent` | Denies a spawn that would inherit the main model (no `model`, and the subagent type does not pin one). Asks you before a spawn on `opus` or `fable`. |
| agent command guard | `Bash` inside bundled agents | Selects the read-only, runner, or writer rules from Claude Code's `agent_type`; the hook and patterns live in the plugin, so agent frontmatter stays focused on the role. |

Set `AI_TOOLBOX_READ_LINES` to change the read threshold, or `AI_TOOLBOX_READ_GUARD=off` / `AI_TOOLBOX_SPAWN_GUARD=off` to turn those cost guards off. The read and spawn hooks fail open: an error allows the call, because they guard cost, not safety. The Bash agent guard blocks only the named bundled agents and passes unknown agent types. It is a seatbelt, not a sandbox; permission modes and `permissions.deny` remain the real boundary. The plugin is optional, so its guards run only when it is enabled. Fan-out limits stay in `delegation` (3 to 5 helpers at once), because a hook can't see how many helpers are still running. `/session-check` reports whether the plugin is enabled. Tests: `python3 plugins/cost-guards/tests/test.py` and `bash scripts/agent-guards/test.sh`.

The guards save tokens on bulk reads and on helpers that would otherwise run on the top model; they don't cut the cost of the work the main model still has to do. No benchmark in this repo yet measures the saving.

## Structure

```
.agents/
├── agents/              Claude Code subagents
└── skills/
    ├── shared/          lifecycle, delegation, doc-templates, project-setup (+ CATALOG.md),
    │                    session-check, orchestration-frontier
    ├── research/        research, investigation, spike, prototype, unslop
    ├── planning/        product-research, design-research, grilling, grill-with-docs,
    │                    domain-modeling, questionnaire, codebase-design,
    │                    architecture-review, figma-design, spec, planner (+ RUN-PROJECT.md, RUN-WORKSPACE.md)
    └── implementation/  the six personas, five reference skills (each SKILL.md plus references/),
                         deep-review, resolve-merge-conflicts
research/                decisions and surveys about this repo (ADR-001, ADR-002, ADR-003)
plugins/cost-guards/     Claude Code plugin: read, spawn, and agent command guard hooks
.claude-plugin/          marketplace.json, so the plugin installs from this repo
scripts/                 check-skills.py (discovery and references), agent-guards/ (command guard cases and tests)
THIRD_PARTY_NOTICES.md   MIT notices for adapted skills
```

Folders are phases; scope lives in the catalog. Skills sit exactly at `.agents/skills/<phase>/<skill>/SKILL.md`, and a phase folder must not contain a `SKILL.md` of its own, because the `skills` CLI stops descending at the first one it finds ([ADR-001](research/ADR-001-three-phase-skill-layout.md)). The survey behind the adapted skills is [ADR-002](research/ADR-002-skills-survey-mattpocock-cursor-pstack.md).

## Credits

Many workflow skills are adapted from [mattpocock/skills](https://github.com/mattpocock/skills), [cursor/plugins](https://github.com/cursor/plugins) and [BuilderIO/skills](https://github.com/BuilderIO/skills), all MIT. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
