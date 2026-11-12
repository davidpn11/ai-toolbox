---
name: delegation
description: "How to hand work to subagents and Orca workers: which tier and runtime (Claude or Codex) fits which job, how to write a self-contained brief or worker spec file, and the response contract every helper returns. Use whenever a skill or plan says to dispatch, fan out, spawn, delegate, or start a worker, or when choosing a cheaper model for research, exploration, or running commands."
---

# Delegation

A helper is a fresh context with one job. Delegate to keep the main session's context clean, to run independent work in parallel, and to put cheap work on a cheap model. Keep the conversation with the user, every decision, and the final synthesis in the main session.

There are two kinds of helper:

- **In-session subagents** (`scout`, `runner`, a general-purpose subagent): read-only. They find facts, run checks and review. They share your checkout.
- **Orca workers** (`orca orchestration worker-start`, see the `orchestration` skill): the only helpers that edit repo code. Each runs in its own worktree of its repo, as Claude or Codex.

## Pick the tier

Choose the smallest tier that can do the job. Name the tier in the brief so the choice is visible.

| Tier | Claude | Codex | Use it for |
|------|--------|-------|------------|
| **Fast** | `haiku`, the `scout` or `runner` subagent | low reasoning effort | Finding files and facts, listing call sites, reading git history, running tests, builds or linters and reporting the output, mechanical edits with exact instructions. |
| **Standard** | `sonnet` | medium reasoning effort | Research against primary sources, one review axis, implementing a well-specified plan task, writing a report from notes. |
| **Deep** | `opus` or `inherit` | high reasoning effort | Interviewing the user, synthesis across many reports, design trade-offs, planning, lead judgment over reviews. This usually stays in the main session. |

Fast-tier output is a lead, not a fact. Before a load-bearing claim from a fast-tier helper goes into a report, spec or plan, open the cited file or rerun the command yourself.

If the harness has no subagents, do the read-only work inline, one task at a time, in the same order.

## Pick the runtime (Orca workers)

Each plan task names `runtime: claude | codex`. Defaults:

- **Codex** for `fast` tasks whose spec says exactly what to change and where, and for review of Claude-written diffs.
- **Claude** for tasks that need design judgment, UI work, and review of Codex-written diffs.

Spread a wave across both runtimes when it has many tasks, so neither queue is the bottleneck. The family that did not write most of a diff reviews it.

## Bundled subagents

This collection ships thin read-only Claude Code subagents in `.agents/agents/`: `scout` (answers "where is X", "what calls Y" with paths and line numbers) and `runner` (runs the commands it is given and reports exit codes and output, never fixes anything). When a named subagent is not installed, use the harness's general-purpose subagent on the tier's model with the same instructions.

## Write the brief (in-session subagents)

The subagent sees only the brief. Write it so a stranger could do the job.

```
Task: <one sentence, the deliverable>
Tier: fast | standard | deep
Why: <the decision this result feeds, one line>

Context pointers:
- <path or URL>: <what to take from it>

Do:
- <steps or questions, numbered if order matters>

Done when:
- <checkable criteria>

Write to: <path, or "reply only">
Report: the response contract below, summary under <N> words.
Do not ask the user anything, do not spawn subagents, and do not widen the task.
```

Rules for the brief:

- **Pointers, not pastes.** Pass paths to the spec, plan, research notes and files. Paste only what has no path.
- **One job per subagent.** Two questions are two subagents, launched in the same turn.
- **No nesting.** A helper never spawns more helpers or re-invokes the skill that launched it. Fan-out happens only from the main session.
- **Background by default.** Launch independent helpers together and keep working; block only on the results the next step needs.

## Write the spec file (Orca workers)

A worker sees only its own worktree plus globally installed skills, so pointers into the hub do not reach it. The spec file is self-contained: paste what a pointer cannot reach. Write it to `features/<slug>/tasks/<task_id>.md` in the hub and pass it with `--spec-file`.

```
# <task_id>: <title, the deliverable>

Repo: <name>   Tier: fast | standard | deep   Runtime: claude | codex
Why: <the slice and the decision this task serves, one line>

## Your role
<the body of the specialist skill named in the plan, pasted without its frontmatter,
 plus the reference skill sections the task needs (for example monorepo or elysia-api).
 Omit when the plan names no specialist.>

## This repo
<pasted from the repo's AGENTS.md: the stack for the paths you touch, the conventions,
 the verify commands, and any contract this task provides or consumes>

## Task
<the plan task's description>

May edit: <paths or globs; anything else is read-only>
Contracts in: <interfaces produced by earlier waves, pasted>
Contract out: <the interface this task must hand to later tasks>

## Done when
- <acceptance criteria>
- Verify: <the task's verification commands, run in your worktree, all passing>

## Finish
Commit on your worktree's branch. Do not push, open a PR, or merge. Do not ask the user
anything; ask the coordinator through Orca if you are blocked. End with the response
contract, then report done through Orca (`worker_done`).
```

## Response contract

Every helper ends with this block. Persona-specific numbers go in `extra`.

```json
{
  "status": "completed | failed | needs_revision",
  "task_id": "string, or null outside a plan",
  "summary": "what was done or found, at most 3 sentences",
  "artifacts": ["paths written or changed"],
  "verified": "the verify commands run and their result, or null if none ran",
  "failure_type": "transient | fixable | needs_replan | escalate | null",
  "extra": {}
}
```

`failure_type` tells the caller what to do next:

- `transient`: retry the same brief.
- `fixable`: re-delegate with the error output added to the brief.
- `needs_replan`: the task itself is wrong; send it back to the `planner` skill.
- `escalate`: blocked on something only the user can answer or do; stop and ask.

Retry a task at most three times, then escalate. A `completed` with `verified: null` on a task that has verification commands is not done: run them through the `runner` first.
