---
name: lifecycle
description: "Take a feature from idea to merged code through three phases (research, planning, implementation), picking the next skill from what already exists in the feature folder. Resumable across sessions."
disable-model-invocation: true
argument-hint: "[feature idea or feature-slug]"
---

# Lifecycle

The conductor for one feature. Each phase leaves documents in the feature folder, and the next phase reads them, so the work survives a cleared context, a new session, or a teammate picking it up.

Before stating what a skill does or skipping a step, read that skill: the summaries here are for orientation only.

## Start

1. **Find or create the feature.** If `$ARGUMENTS` names an existing `docs/features/<slug>/`, load it. Otherwise write the objective as one paragraph (what, for whom, why now), propose a slug, and confirm both with the user. Create the folder lazily, with the first document (layout in the `doc-templates` skill).
2. **Detect the phase** from what the folder holds, and say which one you are entering and why:

| The folder has | Phase | Next |
|----------------|-------|------|
| nothing, or open unknowns | Research | below |
| research done, no `spec.md` | Planning | below |
| `spec.md` draft | Planning | finish and approve the spec |
| approved `spec.md`, no `plan.yaml` | Planning | `planner` |
| `plan.yaml` with pending tasks | Implementation | `architect` |
| every task completed | Close | below |

The user can jump phases ("skip research, I know this code"). Say what the skipped phase would have checked, then go.

## Phase 1: Research

Goal: no unknown left that would change the plan. List the unknowns with the user in one round, then route each one:

| Unknown | Skill | Runs as |
|---------|-------|---------|
| How the code we are changing works, why it is that way, what the change touches | `investigation` | fast-tier scouts, you verify |
| Whether an approach works at all, or which of two is better | `spike` | throwaway code and measurements |
| A fact outside the repo: a library's limits, an API's behaviour, a standard | `research` | standard-tier background subagent |
| How a state model or interaction feels | `prototype` | throwaway code |

Launch independent ones in the same turn. They run in the background; their reports land in the folder. The phase is done when every unknown has a report or a recorded gap. A feature that touches only well-understood code can have an empty research phase; say so.

## Phase 2: Planning

Goal: an approved spec and an approved plan. Run the steps that fit; skip what the feature does not need and say why.

1. **Product.** Call the Skill tool with "product-research" for anything user-facing or any feature whose value is not obvious. It writes `product-brief.md`.
2. **Design.** Call the Skill tool with "design-research" for anything with a UI. It writes `design-brief.md` and may detour through `prototype` or `figma-design`.
3. **Grill.** Call the Skill tool with "grilling" and, in a separate call, with "domain-modeling". The briefs' open questions seed the first round. The interview writes `CONTEXT.md` terms and ADRs as decisions land. Questions only someone else can answer go to the `questionnaire` skill; questions that need something to react to go to `prototype`.
4. **Shape the code.** When the feature adds or reshapes a module, call the Skill tool with "codebase-design": design it twice for anything load-bearing, and write a rationale page.
5. **Spec.** Call the Skill tool with "spec". The user approves it.
6. **Plan.** Call the Skill tool with "planner". The user approves the slice breakdown.

Steps 1 and 2 can run back to back without the user; from step 3 on, the user is in the loop.

## Phase 3: Implementation

Call the Skill tool with "architect". It executes `plan.yaml` wave by wave through the specialist subagents, runs `code-review` over the result, and ends with a security wave.

## Close

Report what shipped against the spec's user stories, what was cut, and any follow-ups. Offer to delete research notes that only mattered for this feature; keep ADRs, `CONTEXT.md`, the spec, and spike reports.

## Context hygiene

- Keep research and planning in one session where it fits, so the grilling builds on the same thinking. When the context gets long, clear it at a phase boundary: the folder holds everything the next session needs, and running this skill again resumes from it.
- Implementation runs in a fresh session. The architect works from the plan and pointers, not from the planning conversation.
- Send reading and running work to subagents on the cheapest tier that can do it (the `delegation` skill). Keep decisions and the user conversation here.

## Off the main flow

- Codebase health: `architecture-review` finds deepening opportunities; a chosen one enters this flow at planning.
- Review any branch: `code-review`. Resolve a conflicted merge: `resolve-merge-conflicts`.
- Writing quality anywhere: `unslop`.
