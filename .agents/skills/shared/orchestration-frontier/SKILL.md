---
name: orchestration-frontier
description: "Cost mode for the rest of the session: the expensive main model (Claude Opus/Fable, Codex Sol/Astra) keeps planning, judgment and review, and every bounded job goes to the cheapest helper that can do it: a subagent, or an Orca Worker when it needs the other model family or its own worktree. Run only when the user invokes /orchestration-frontier; never self-activate."
disable-model-invocation: true
argument-hint: "[task, or 'off']"
---

# Orchestration frontier

A session mode. Without it, you delegate when a skill or plan says to. With it on, you delegate **every** bounded job in the session, ad hoc work included, and you stay at the frontier: deciding, integrating, reviewing. It stays on until the user says `off`.

The rules are in the `delegation` skill: call the Skill tool with "delegation" now, and apply all of it. This mode adds only the four points below.

1. **Check your own tier first.** If you are already on a cheap tier (Haiku, Sonnet, Luna, Terra), say so and work normally: the mode saves money only from the top.
2. **Default to out.** Before any job that reads a lot, runs commands, or edits code to a clear spec, ask "which role and tier from `delegation` can do this?" and send it there. Keep only what `delegation` section 1 says to keep: the blocker, jobs smaller than their brief, decisions, and the user conversation.
3. **Check everything that comes back.** Open the cited lines or have a `runner` rerun the check before you claim done.
4. **Report cost.** End each task with one line: how many helper runs at which tiers, and what you kept ("8 helper runs: 5 fast, 3 standard; review and decisions kept here").

With other skills: under `planner`, tasks already carry tiers, and this mode covers everything around the plan (investigation, reviews, checks). Under `lifecycle`, research fan-out is already on cheap tiers.

## Attribution

Adapted from `efficient-orchestrator` in BuilderIO/skills. See `THIRD_PARTY_NOTICES.md`.
