# Repo AGENTS.md template

`AGENTS.md` at the root of each repo the hub works on. Written and refreshed by `onboard-repo`. It holds **facts only**: no process, no planner instructions. The `planner` reads it to pick specialists and verify commands, and pastes its sections into every worker spec file, so keep each section short and true.

```markdown
# <repo name>

<One paragraph: what this repo is, who uses it, what it does not do.>

## Stack

| Path | Stack | Specialist |
| --- | --- | --- |
| `<glob, e.g. src/**>` | <languages, frameworks, runtime> | <a roster name from the planner skill, or none> |

Package manager: <bun | npm | pnpm | cargo | ...>. Monorepo: <no | yes, tool>.

## Verify commands

Run from the repo root, in this order. A task is done only when these pass.

| Check | Command |
| --- | --- |
| Install | `<command>` |
| Typecheck / lint | `<command>` |
| Unit tests | `<command>` |
| Build | `<command>` |
| End-to-end | `<command, or none>` |

## Contracts

What other repos or tasks depend on. A change to any of these goes first and alone in a plan.

| Contract | Path | Provides to / consumes from |
| --- | --- | --- |
| <API, schema, file format, CLI flags, package export> | `<path>` | <repo names, or external> |

## Conventions

- <Only what a newcomer would get wrong: naming, error handling, where tests live, generated files not to edit.>

## Do not touch

- `<paths that are generated, vendored, or owned elsewhere>`
```

Rules:

- Every command in "Verify commands" was run once by `onboard-repo` and passed, or is marked `(not run: <reason>)`.
- The Specialist column uses only names from the `planner` skill's roster; a stack it does not cover gets `none`.
- No project history, no roadmap, no TODOs. Those live in the hub's feature folders.
