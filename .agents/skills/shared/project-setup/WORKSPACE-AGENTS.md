# Workspace AGENTS.md template

Written by `project-setup` at the root of a Workspace. Facts only: the `planner` reads it to pick specialists, Workers and verify commands, and pastes each repo's section into its Workers' spec files, so keep every section short and true. The **Repos** heading is what tells the planner it is in a Workspace.

```markdown
# <project name>

Orca Workspace for work across <repo A> and <repo B>. Each repo is a clone from GitHub inside this folder; this folder itself is not a git repo. It holds the plans and Worker spec files.

## How to work here

- Ask for a feature with `/planner <feature>` (bigger features: `/lifecycle <idea>`). Claude and Codex both plan here, with the same skills.
- Feature documents go in `docs/features/<slug>/`, with worker spec files in `tasks/`.
- Only Orca Workers edit repo code, each in its own worktree and branch, as a Child of this Workspace. In-session helpers are read-only. Never edit the clones directly.
- Before planning, `git pull` in each clone so Workers branch from the merged base.
- One PR per repo, providers first; each PR links its siblings and states the merge order. Never merge.

## Repos

### <repo name>

- Orca repo id: `<id>`
- Path: `<workspace>/<repo>` (clone of `github.com/<owner>/<repo>`, base branch `<main>`)
- What it is: <one line>

| Path | Stack | Specialist |
| --- | --- | --- |
| `<glob>` | <languages, frameworks> | <roster name from the planner skill, or none> |

Package manager: <...>. Monorepo: <no | yes, tool>.

Verify commands (run from the repo root, in order):

| Check | Command | Result at setup |
| --- | --- | --- |
| Install | `<command>` | <passed / failed: reason / not run: reason> |
| Typecheck / lint | `<command>` | |
| Tests | `<command>` | |
| Build | `<command>` | |

Conventions: <only what a newcomer would get wrong>.
Do not touch: `<generated or vendored paths>`.

### <next repo>

<same shape>

## Contracts

| Contract | Defined in | Provided by | Consumed by |
| --- | --- | --- | --- |
| <API, schema, package export, CLI flags, file format> | `<repo>:<path>` | <repo> | <repo> |

A change to a contract goes first and alone, in the provider repo.
```
