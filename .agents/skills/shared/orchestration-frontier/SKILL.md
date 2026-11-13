---
name: orchestration-frontier
description: "Cost mode for the rest of the session: the expensive main model (Claude Opus/Fable, Codex Sol/Astra) keeps planning, judgment and review, and every bounded job goes to the cheapest helper that can do it: a subagent, or an Orca Worker when it needs the other model family or its own worktree. Run only when the user invokes /orchestration-frontier; never self-activate."
disable-model-invocation: true
argument-hint: "[task, or 'off']"
---

# Orchestration frontier

You stay at the frontier: deciding, integrating, reviewing. Cheaper helpers do the token-heavy, bounded work. The mode stays on for the rest of the session until the user says `off`.

If you are already on a cheap tier (Haiku, Sonnet, Luna, Terra), say so and do the work yourself: this mode only saves money from the top.

## What stays with you

Architecture, prioritization, anything ambiguous or risky, the user conversation, synthesis across results, and the final review. Also the **blocker**: the result your very next step depends on. Waiting on a helper for it costs more than doing it.

## What goes out

| Job | Helper |
| --- | --- |
| Find files, call sites, history; scan a repo; extract from docs | `scout` or a fast-tier subagent |
| Run tests, builds, browsers, benchmarks; reduce logs; cluster failures | `runner` |
| A narrow patch with clear file ownership; research against sources; one review axis | standard-tier subagent |
| Work for the **other model family** (Codex from Claude or the reverse), a change that needs **its own worktree**, or several **parallel edits** to one repo | an Orca Worker through the `orchestration` skill (when `orca status` answers), with the tier's model |

Model ids per tier and runtime live only in the `delegation` skill. Set the tier on every spawn; never let a helper inherit the expensive model.

**Not worth delegating:** a job smaller than its own brief (one grep, one file read, a two-line edit). Do those inline.

## How

1. **Brief** in the `delegation` format: a self-contained packet with the objective, scope and out-of-scope, files or search targets, the verify command, the return format, and stop conditions.
2. **Run them together.** 3 to 5 helpers at once at most. Never give two helpers the same files. Helpers never spawn helpers.
3. **Compact returns.** The `delegation` response contract: findings, changed files, commands run, evidence, open decisions.
4. **Verify what matters.** Delegated output is evidence, not a verdict. Before you claim done, open the cited lines or have the `runner` rerun the check.
5. **Cut losses.** A helper that returns nothing usable twice: do that step yourself. Close each helper as soon as its result is in.

## With other skills

- Under `planner`, its tasks already carry a tier; this mode adds the cost discipline above to everything around the plan (investigation, reviews, checks).
- Under `lifecycle`, research fan-out (`research`, `investigation`) is already cheap-tier by design.

## End of each task

One line on cost: roughly how much was delegated and at which tiers ("8 helper runs: 5 fast, 3 standard; review and decisions kept here").

## Attribution

Adapted from `efficient-orchestrator` in BuilderIO/skills. See `THIRD_PARTY_NOTICES.md`.
