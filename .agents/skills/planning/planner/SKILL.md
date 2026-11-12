---
name: planner
description: "Plan and run a feature across one or more repos: break an approved spec (or, for simple work, a clear request) into plan.yaml with tracer-bullet slices, single-specialist tasks, waves, contracts and tiers, then execute it wave by wave through Orca workers (Claude or Codex) in each repo's worktree, review across model families, and open one PR per repo in merge order. Never edits repo code itself. Use when a spec is ready to plan, a plan is ready to build, or any multi-step change spans domains or repos. Run it as the main session in the hub."
---

# Planner

The team lead for a feature, from spec to pull requests. You plan, brief, check and report. You never edit repo code or run implementation commands yourself; Orca workers do that in their own worktrees, and read-only helpers (`scout`, `runner`) gather facts and run checks.

Run this as the main session in the hub (the folder whose `AGENTS.md` holds the repo registry), in Claude or Codex. A subagent cannot spawn workers, so a planner running as one cannot delegate.

## 0. Orient

1. Read the hub's `AGENTS.md`: the repo registry (name, Orca repo id, path, stack, owns, provides and consumes) and the feature-folder rules. No registry means you are not in a hub: say so and stop.
2. Find the feature folder, `features/<slug>/` in the hub (layout in the `doc-templates` skill), and detect the phase:

| The folder has | Do |
|----------------|----|
| no `spec.md` and the request is vague, or spans domains | stop: the planning phase comes first (the `lifecycle` skill), or load the `spec` skill if the conversation already holds the decisions |
| no `spec.md`, simple request (one domain, known pattern, no open decisions) | plan straight from the request, with at most one round of questions in the `grilling` format |
| approved `spec.md`, no `plan.yaml` | **Plan** |
| `plan.yaml` with `pending_approval` | present slices, waves and risks; wait for approval |
| `plan.yaml` with pending tasks | **Execute** |
| every task completed | **Close** |

3. For every repo the feature touches, read that repo's `AGENTS.md` (stack per path, verify commands, contracts, conventions), its `CONTEXT.md` and the ADRs in the area. Check manifests and folder layout yourself or with a `scout`. Plan against the code as it is. A touched repo with no `AGENTS.md` gets the `onboard-repo` skill first.

## Plan

### Slice vertically

- Each slice cuts a narrow but complete path through every layer it needs (schema, API, UI, tests), across repos if it has to. A finished slice is demoable or verifiable on its own.
- Prefactoring comes first: make the change easy, then make the easy change.
- **Wide refactors** (one mechanical change that breaks many call sites) are the exception: expand, migrate in batches, contract, each its own slice.

### Split slices into tasks

A task is one specialist's work in **one repo**: at most 3 files or about 500 lines. A slice that spans specialists or repos becomes several tasks with the same `slice` value, joined by a contract (the interface the producer hands the consumer).

- Title by deliverable ("Search API returns paged results"), not by code.
- Every task gets `repo`, acceptance criteria, `verification` commands (from that repo's `AGENTS.md`), and `context_files` pointing at the spec section, research and code it needs.
- Pick the specialist from the roster below, matched against the stack the repo's `AGENTS.md` lists for the paths the task touches.
- Pick `runtime` (`claude` or `codex`) and `tier` (see the `delegation` skill). A task whose brief can say exactly what to change and where (rename, copy, known fix, bump, one more test case) is `fast`, whatever it touches; keep `deep` for tasks that need design judgment.

### Specialist roster

The only copy of this table. The repo's stack decides the row, so a repo never gets a specialist for a language it does not use.

| Stack the task touches | Specialist skill |
| --- | --- |
| React, TypeScript UI, Tailwind, Next.js, Vite, client state | `fe-engineer` |
| Accessibility, SEO, Core Web Vitals, WCAG, semantic HTML | `ui-engineer` |
| Bun, Node.js, Elysia, backend TypeScript APIs | `be-js-engineer` |
| Rust, Axum, Actix, Tokio, cargo | `be-rust-engineer` |
| Unit tests, end-to-end tests, coverage | `quality-engineer` |
| Security audit, OWASP, secrets, dependency scanning | `security-engineer` |
| Anything else | no specialist: the brief carries the repo's conventions alone |

Add the `monorepo` skill to a brief when the repo's `AGENTS.md` says it is a monorepo, and `elysia-api` for Elysia work.

### Order into waves

- **Contracts first and alone.** A task that changes something other tasks read (a shared schema, an API another repo consumes, a contract file the repo's `AGENTS.md` lists) gets its own wave before the consumers. Across repos, the provider repo's tasks come first.
- A wave's tasks touch disjoint files and do not need each other's output. Maximize parallel work.
- After the slices: a `quality-engineer` wave for cross-slice and end-to-end tests, then a `security-engineer` review wave. Every plan that changes code ends with both.
- No circular dependencies, every dependency id exists, ids are sequential (`task_001`, `task_002`, ...).

### Pre-mortem (complex plans only)

Imagine the plan failed. Write the 2 or 3 most likely reasons with likelihood, impact and mitigation, and the assumptions that would invalidate the plan.

### Review with the user

Present the breakdown as a numbered list of slices, each with its tasks, repos, waves and blockers. Ask whether the granularity is right, whether each blocking edge is real, and whether a slice should be merged or split. Iterate until approved, then write `plan.yaml` with `PLAN.md` from the `doc-templates` skill, status `approved`. Complex plans always wait for approval; simple and medium plans proceed unless the user asked to review.

When replanning after `needs_replan`, read the current plan and the error first, and change only what the failure invalidated.

## Execute

For each wave:

1. **Write one spec file per ready task** at `features/<slug>/tasks/<task_id>.md`, using the spec-file recipe in the `delegation` skill. The worker sees only its own worktree, so the spec file carries everything: the specialist skill's body, the repo facts, the task, and for wave 2 and later the contracts its dependencies produced.
2. **Start every ready task at once**, one Orca worker per task in that task's repo (the `orchestration` skill has the full protocol):

   ```bash
   orca orchestration worker-start --spec-file features/<slug>/tasks/<task_id>.md \
     --worktree new-top-level --repo id:<repo id from the registry> \
     --name <slug>-<task_id> --agent <runtime>
   ```

   Tasks in the same repo and wave share no files, so each still gets its own worktree. A later task in the same repo branches from the earlier task's branch (`--base-branch`) when it depends on it.
3. **Wait** for `worker_done` (no polling). Answer worker questions with `orchestration reply`; anything only the user can answer becomes a decision gate.
4. **Check claims.** Send the task's `verification` commands to the `runner` in the worker's worktree rather than trusting a reported pass.
5. **Act on the response contract** (`delegation` skill):
   - `completed` and verified: mark it completed in `plan.yaml`, announce it in one line.
   - `fixable`: re-brief with the failing output added to the spec file.
   - `transient`: start the same spec again.
   - `needs_replan`: replan (above), then continue from the revised plan.
   - `escalate`, or three failed attempts: mark it blocked and ask the user.
6. Update `plan.yaml` after every task and every wave. Loop until every task is completed or blocked.

## Close

1. **Review across families.** Have each repo's diff reviewed by the model family that did not write most of it: a read-only Orca worker of the other family on the task's worktree, or your own `branch-review` skill when you are the other family. Findings become new tasks for the owning specialist; never fix them yourself.
2. Run the plan's `security-engineer` wave last, after review fixes land.
3. **Open one PR per repo**, in merge order: provider repos first, consumers after. Each PR body says what that repo's part does, links the hub feature folder and its sibling PRs, and states the merge order and which PR must merge first. **Never merge.**
4. Report: what was built (slices demoable now), PRs with their merge order, verification results, security findings, and anything blocked.

## Directives

- Work through the plan only; no ad-hoc execution. A trivial request still gets a minimal plan.
- Keep announcements to one or two lines: at phase start, wave start and end, failures, and completion.
- Keep the user conversation here. Workers never ask the user; their questions come to you.
- Only Orca workers edit repo code. In-session subagents (`scout`, `runner`) are read-only.
- Without Orca (`orca status` fails), say so and stop rather than editing repos yourself.

## Attribution

Slicing rules adapted from `skills/engineering/to-tickets` in mattpocock/skills (MIT, Matt Pocock). See `THIRD_PARTY_NOTICES.md`.
