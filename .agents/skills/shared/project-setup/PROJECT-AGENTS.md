# Project AGENTS.md template

Written by `project-setup` at the root of a single repo, or merged into the `AGENTS.md` already there (keep the existing sections; add only what is missing). Facts only: the `planner` reads it to pick specialists and verify commands.

```markdown
# <repo name>

<one line: what it is, for whom>

## How to work here

- Build features with `/planner <feature>` (bigger ones: `/lifecycle <idea>`). Feature documents go in `docs/features/<slug>/`.
- Work on a branch; finish with a PR. Never merge from an agent.

## Stack

| Path | Stack | Specialist |
| --- | --- | --- |
| `<glob>` | <languages, frameworks> | <roster name from the planner skill, or none> |

Package manager: <...>. Monorepo: <no | yes, tool>.

## Verify

Run from the repo root, in order:

| Check | Command | Result at setup |
| --- | --- | --- |
| Install | `<command>` | <passed / failed: reason / not run: reason> |
| Typecheck / lint | `<command>` | |
| Tests | `<command>` | |
| Build | `<command>` | |

## Conventions

<only what a newcomer would get wrong>

Do not touch: `<generated or vendored paths>`.
```
