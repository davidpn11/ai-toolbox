---
name: planner
description: "Break an approved spec (or, for simple work, a clear request) into plan.yaml: tracer-bullet vertical slices split into single-specialist tasks, with waves, dependencies, contracts, model tiers, acceptance criteria, and a pre-mortem for complex work. Use when a spec is ready to be turned into executable tasks, or when the architect needs a plan."
---

# Planner

Turn a spec into a plan the `architect` can execute without coming back with questions. Never write source code; only read, analyze, and write `plan.yaml`.

## 1. Check the input

- **An approved `spec.md`** in the feature folder (see the `doc-templates` skill): plan from it.
- **No spec, but the request is simple** (one domain, known pattern, no open decisions): plan straight from the request. Ask at most one round of questions, in the `grilling` format.
- **No spec, and the request is vague or spans domains**: stop. Say the planning phase comes first and point at the `lifecycle` skill, or call the Skill tool with "spec" if the conversation already holds the decisions.

Read the target project's `AGENTS.md`, `CONTEXT.md`, the ADRs in the area, and any investigation reports. Check package manifests and folder structure yourself or with a `scout` (see the `delegation` skill). Plan against the code as it is.

## 2. Slice vertically

Break the spec into **tracer-bullet slices**:

- Each slice cuts a narrow but complete path through every layer it needs (schema, API, UI, tests). Not a horizontal layer.
- A finished slice is demoable or verifiable on its own.
- Prefactoring comes first: make the change easy, then make the easy change.
- **Wide refactors** (one mechanical change that breaks many call sites, like renaming a column) are the exception. Sequence them expand, migrate in batches, contract, each its own slice.

## 3. Split slices into tasks

A task is one specialist's work: at most 3 files or about 500 lines. A slice that spans specialists becomes several tasks with the same `slice` value, joined by a contract (the interface the producer hands the consumer).

- Title by deliverable ("Search API returns paged results"), not by code ("Create SearchHandler").
- Every task gets acceptance criteria, verification commands, and `context_files` that point at the spec section, research, and code it needs.
- Assign agents from the `architect` roster: React or UI component to `fe-engineer`, Bun or Node API to `be-js-engineer`, Rust to `be-rust-engineer`, accessibility or SEO to `ui-engineer`, test suites to `quality-engineer`, security review to `security-engineer`.
- Assign a `tier` per task. Well-specified implementation is `standard`. Mechanical work with exact instructions is `fast`. Keep `deep` for tasks that need design judgment.

## 4. Order into waves

- Wave 1: prefactors, shared types, scaffolding, and every task with no dependencies.
- Later waves: tasks whose dependencies are done. Independent tasks share a wave; maximize parallel work.
- After the slices: a `quality-engineer` wave for cross-slice and e2e tests, then a `security-engineer` review wave. Every plan that changes code ends with both.

No circular dependencies, every dependency id exists, ids are sequential (`task_001`, `task_002`, ...).

## 5. Pre-mortem (complex plans only)

Imagine the plan failed. Write the 2 or 3 most likely reasons, with likelihood, impact, and mitigation, and the assumptions that would invalidate the plan. Pull them from the spec's risks, spike verdicts, and investigation gotchas.

## 6. Review with the user

Present the breakdown as a numbered list of slices, each with its tasks, waves, and blockers. Ask:

- Does the granularity feel right, too coarse or too fine?
- Is each blocking edge real?
- Should any slice be merged or split?

Iterate until the user approves. Then write `plan.yaml` to the feature folder with `PLAN.md` from the `doc-templates` skill, status `approved`, and report the slice count, task count, waves, and agents involved. The next step is the `architect` skill.

When replanning after a `needs_replan` failure, read the current plan and the error first, and change only what the failure invalidated.

## Attribution

Slicing rules adapted from `skills/engineering/to-tickets` in mattpocock/skills (MIT, Matt Pocock). See `THIRD_PARTY_NOTICES.md`.
