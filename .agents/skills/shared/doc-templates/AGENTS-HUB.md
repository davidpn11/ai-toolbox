# Hub AGENTS.md template

`AGENTS.md` at the root of the hub: the one folder where the `planner` runs every feature, across one repo or several. Pair it with a `CLAUDE.md` holding the single line `@AGENTS.md`, because Claude Code reads `CLAUDE.md`, not `AGENTS.md`.

```markdown
# <hub name>

Planner hub. Every feature starts here, whether it touches one repo or several. Repos stay independent; this folder holds the plans, the worker spec files and the registry that ties them together. No repo code lives here.

## How to work here

- Start a feature with the `lifecycle` skill; plan and build with the `planner` skill. Claude and Codex both plan here, with the same skills.
- Each feature lives in `features/<slug>/` (layout in the `doc-templates` skill): spec, `plan.yaml`, and `tasks/<task_id>.md` worker spec files.
- Only Orca workers edit repo code, each in its own worktree of its repo (`orca orchestration worker-start --worktree new-top-level --repo id:<id>`). In-session subagents are read-only.
- One PR per repo, providers first. Each PR links this hub's feature folder and its sibling PRs and states the merge order. The planner never merges.
- A repo joins the registry through the `onboard-repo` skill, which also writes its `AGENTS.md`.

## Repo registry

| Repo | Orca repo id | Path | Stack | Owns | Provides | Consumes |
| --- | --- | --- | --- | --- | --- | --- |
| <name> | `<id from orca repo list --json>` | `<absolute path>` | <one line> | <what it is the source of truth for> | <contracts other repos use> | <contracts it uses> |

## Skills

Installed at project level from ai-toolbox and committed, so every worktree of this hub has them. Update with `npx skills update -p`, then commit.
```
