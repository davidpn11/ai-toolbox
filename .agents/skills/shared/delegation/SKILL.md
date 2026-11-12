---
name: delegation
description: "How to hand work to subagents: which model tier fits which job, how to write a self-contained brief, and the response contract every subagent returns. Use whenever a skill or plan says to dispatch, fan out, spawn, or delegate to a subagent, or when choosing a cheaper model for research, exploration, or running commands."
---

# Delegation

A subagent is a fresh context window with one job. Delegate to keep the main session's context clean, to run independent work in parallel, and to put cheap work on a cheap model. Keep the conversation with the user, every decision, and the final synthesis in the main session.

## Pick the tier

Choose the smallest tier that can do the job. Name the tier in the brief so the choice is visible.

| Tier | Claude Code | Use it for |
|------|-------------|------------|
| **Fast** | `model: haiku`, the `scout` or `runner` subagent | Finding files and facts in the codebase, listing call sites, reading git history, running tests, builds, linters, or scripts and reporting the output, mechanical edits with exact instructions. |
| **Standard** | `model: sonnet` | Research against primary sources, one review axis, implementing a well-specified plan task, writing a report from notes, one design variant. |
| **Deep** | `model: opus` or `inherit` | Interviewing the user, synthesis across many reports, design trade-offs, planning, lead judgment over reviews. This usually stays in the main session. |

Fast-tier output is a lead, not a fact. Before a load-bearing claim from a fast-tier subagent goes into a report, spec, or plan, open the cited file or rerun the command yourself.

In other harnesses, map the tiers onto whatever models the harness offers. If the harness has no subagents, do the work inline, one task at a time, in the same order.

## Bundled subagents

This collection ships thin Claude Code subagents in `.agents/agents/`. Copy them to `.claude/agents/` to use them by name.

- `scout` (fast, read-only): answers "where is X", "what calls Y", "what changed in Z" with paths and line numbers.
- `runner` (fast): runs the commands it is given and reports exit codes and output. It never fixes anything.
- One persona per specialist (`fe-engineer`, `be-js-engineer`, and so on, standard tier) that preloads its persona and reference skills.

When a named subagent is not installed, use the harness's general-purpose subagent with the tier's model.

## Write the brief

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

- **Pointers, not pastes.** Pass paths to the spec, plan, research notes, and files. Paste only what has no path (the intent paragraph, a diff command).
- **One job per subagent.** Two questions are two subagents, launched in the same turn.
- **No nesting.** A subagent never spawns more subagents or re-invokes the skill that launched it. Fan-out happens only from the main session.
- **Writers need separate files.** Read-only subagents can share a checkout. Two subagents that edit code must touch disjoint files, or each must run in its own worktree (Claude Code: `isolation: worktree`).
- **Background by default.** Launch independent subagents together and keep working; block only on the results the next step needs.

## Response contract

Every subagent ends with this block. Persona-specific numbers go in `extra`.

```json
{
  "status": "completed | failed | needs_revision",
  "task_id": "string, or null outside a plan",
  "summary": "what was done or found, at most 3 sentences",
  "artifacts": ["paths written or changed"],
  "failure_type": "transient | fixable | needs_replan | escalate | null",
  "extra": {}
}
```

`failure_type` tells the caller what to do next:

- `transient`: retry the same brief.
- `fixable`: re-delegate with the error output added to the brief.
- `needs_replan`: the task itself is wrong; send it back to the `planner` skill.
- `escalate`: blocked on something only the user can answer or do; stop and ask.

Retry a task at most three times, then escalate.
