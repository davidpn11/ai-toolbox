# Skill catalog

The one list of every ai-toolbox skill and where it belongs. `project-setup` reads it to choose what to install; the README mirrors it.

**The rule** ([ADR-003](https://github.com/davidpn11/ai-toolbox/blob/master/research/ADR-003-global-vs-project-scope.md)): a skill name is either global or project, never both. Claude Code prefers a global skill over a project skill of the same name, so a name installed in both places silently runs the global copy.

- **global**: useful in any folder, independent of stack. Installed once per machine with `-g`, for Claude and Codex.
- **project**: tied to a stack or to building through a plan. Installed into a Project or Workspace by `project-setup`, from the signals below.

## Global

| Skill | What for |
| --- | --- |
| `research` | One question, primary sources, one cited note |
| `investigation` | How the current code works, why, and what a change touches |
| `spike` | Time-boxed feasibility test, GO / NO-GO verdict |
| `prototype` | Throwaway code that answers one design question |
| `unslop` | Strip AI tells from prose and slop from code |
| `grilling` | Interview until nothing is silently assumed |
| `grill-with-docs` | `grilling` + `domain-modeling` in one command |
| `domain-modeling` | `CONTEXT.md` glossary and ADRs |
| `questionnaire` | A document for someone else to fill in |
| `codebase-design` | Deep-module vocabulary, design-it-twice, rationale pages |
| `architecture-review` | Find deepening opportunities, grill the one you pick |
| `product-research` | Problem, users, alternatives; writes the product brief |
| `design-research` | Flows, screen states, prior art; writes the design brief |
| `deep-review` | Parallel review axes (Standards, Spec, Quality, Blast radius) + lead judgment |
| `resolve-merge-conflicts` | Resolve conflicts by intent; checks pass before commit |
| `delegation` | When to delegate, model tiers (Claude and Codex), helper roles, brief format, safety rules, response contract |
| `doc-templates` | Feature folder layout and document templates |
| `orchestration-frontier` | User-invoked: expensive model judges, cheap helpers work |
| `session-check` | Preflight: what this session can run, reach and push |
| `project-setup` | This wizard |

Global subagents (Claude Code, `~/.claude/agents/`): `scout`, `runner`.

Not from ai-toolbox but expected globally: Orca's bundled `orca-cli` and `orchestration` (`orca skills install`).

## Project

`Install when` is checked against the target's files. In a Workspace, check every repo and install the union.

| Skill | Install when | Subagent to copy |
| --- | --- | --- |
| `planner` | always | `planner` |
| `lifecycle` | always | |
| `spec` | always | |
| `fe-engineer` | `react`, `vue`, `svelte`, `next` or `vite` in any `package.json` | `fe-engineer` |
| `ui-engineer` | same as `fe-engineer` (web UI ships) | `ui-engineer` |
| `react-tailwind` | `react` and `tailwindcss` in a `package.json` | |
| `be-js-engineer` | `bun.lock`, `elysia`, `express`, `hono`, `fastify`, or a `package.json` with no UI framework | `be-js-engineer` |
| `elysia-api` | `elysia` in a `package.json` | |
| `be-rust-engineer` | a `Cargo.toml` | `be-rust-engineer` |
| `quality-engineer` | any test runner or test folder (`vitest`, `jest`, `bun test`, `@playwright/test`, `tests/`, `e2e/`) | `quality-engineer` |
| `playwright-testing` | `@playwright/test` or `playwright.config.*` | |
| `security-engineer` | always for code repos (the plan's last wave) | `security-engineer` |
| `owasp-security` | with `security-engineer` | |
| `monorepo` | `turbo.json`, or `workspaces` in the root `package.json` | |
| `figma-design` | the user asks, or a Figma MCP server is configured | |

A stack with no row gets no specialist; the planner then briefs a general-purpose subagent or Worker with the repo's own conventions from `AGENTS.md`.

## Retired names

Remove these from any Project or Workspace that still has them; they were replaced.

| Old | Now |
| --- | --- |
| `architect` (skill, `.claude/agents/architect.md`, or a prefixed copy such as `claude-architect.md`) | `planner` |
| `orca-planner` | `planner` (Workspace mode) |
| `code-review` (ai-toolbox or mattpocock) | `deep-review`, global |
| `orca-project-setup` | `project-setup`, global |
| `grill-me`, `improve-codebase-architecture` (mattpocock) | `grilling`, `architecture-review`, global |
| a project copy of any global skill above | the global one |

## Not ai-toolbox, worth suggesting

| Signal | Suggest |
| --- | --- |
| `wrangler.toml` / `wrangler.jsonc`, `@cloudflare/*` | the Cloudflare skills (`npx skills find cloudflare`, then add them at project scope) |
