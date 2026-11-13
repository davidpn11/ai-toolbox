# ADR-003: Global vs project scope, one planner

Status: accepted, 2026-11-12

## Context

Skills from this repo ended up in three places with no rule: some global, every skill copied into each Orca project, and older copies (plus mattpocock and cursor versions of the same names) in individual repos. Claude Code prefers a global skill over a project skill of the same name, so a stale copy in one place silently wins over the current one in another.

The build side had three overlapping skills. `planner` wrote `plan.yaml`, `architect` ran it through subagents, and `orca-planner` ran it through Orca Workers. The user calls the parent agent the Planner, so "architect" was a second name for the same role.

## Decision

1. **Every skill has exactly one scope**, recorded in `.agents/skills/shared/project-setup/CATALOG.md`:
   - *global*: stack-independent thinking, research, review and workflow tools, installed once per machine;
   - *project*: the build pipeline (`planner`, `lifecycle`, `spec`) and the stack personas and references, installed into a Project or Workspace by `project-setup`.
2. **One `planner`** plans and then runs the plan. Children are subagents in a Project (`RUN-PROJECT.md`) and Orca Workers in a Workspace (`RUN-WORKSPACE.md`). `architect` and `orca-planner` are retired.
3. **`code-review` is renamed `deep-review`**, so a global install does not hide Claude Code's built-in `/code-review`.
4. **`project-setup` replaces `orca-project-setup`.** It handles a single repo and a multi-repo Workspace, reads what is already installed, and removes retired names.
5. **Vocabulary**, used in every skill: Project = one repo; Workspace = a plain folder grouping Projects (an Orca folder workspace, not a git repo, no submodules); Worker = a one-task agent in its own worktree; Children = the Workers or subagents a Planner starts.

## Consequences

- A project install never includes a global name, and `project-setup` flags project copies of global names as clashes.
- A global skill may name a project skill as the next step (`spec`, `planner`), but must still work in a folder that lacks it.
- Repos set up before this ADR keep `architect`/`orca-planner`/`code-review` until `project-setup` is run on them.
