# Project AGENTS.md template

Written by `orca-project-setup` at the root of the Orca project. Facts only; `orca-planner` reads it to pick specialists, workers and verify commands, and pastes each repo's section into its workers' spec files, so keep every section short and true.

```markdown
# <project name>

Orca project for work across <repo A> and <repo B>. The repos stay independent; this folder holds the plans and worker spec files. No repo code lives here.

## How to work here

- Ask for a feature and use the `orca-planner` skill (bigger features: start with `lifecycle`). Claude and Codex both plan here, with the same skills.
- Feature documents go in `docs/features/<slug>/`, with worker spec files in `tasks/`.
- Only Orca workers edit repo code, each in its own worktree nested under this project. In-session helpers are read-only.
- One PR per repo, providers first; each PR links its siblings and states the merge order. Never merge.

## Repos

### <repo name>

- Orca repo id: `<id>`
- Path: `<absolute path>`
- What it is: <one line>

| Path | Stack | Specialist |
| --- | --- | --- |
| `<glob>` | <languages, frameworks> | <roster name from the architect skill, or none> |

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
