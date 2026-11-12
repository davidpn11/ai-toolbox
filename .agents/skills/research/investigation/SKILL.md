---
name: investigation
description: "Find out how part of the current system works, why it is that way, and what a planned change would touch, by fanning out cheap read-only explorers across code, tests, git history, and tickets, then writing one cited investigation report. Use when the user asks how something works, why the code is like this, what a change would break or touch, or before planning a feature in unfamiliar code."
---

# Investigation

Understand the system as it is before changing it. Explorers on the fast tier do the reading in parallel; you check what they found and write the report.

## 1. Frame it

Write down, before dispatching anything:

- **The area**: entry points, a feature name, or a file the user pointed at.
- **The questions**: what must be known for the next decision. "How does checkout apply discounts?", "Why is the cache per-tenant?", "What touches `orders.status`?"
- **The planned change**, if there is one, in one line. It decides how much of the impact map matters.

Read the project's `AGENTS.md`, `CONTEXT.md`, and any ADRs in the area first, so you don't send explorers after answers already written down.

## 2. Fan out

Launch one read-only explorer per angle in the same turn: the `scout` subagent, or a read-only subagent on the fast tier (see the `delegation` skill). Each brief names the area, its one angle, and asks for `file:line` evidence for every claim. Pick the angles that fit:

| Angle | The explorer reports |
|-------|----------------------|
| Code path | The main flow from entry point to effect, step by step. |
| Data | Types, schemas, tables, and who reads and writes each. |
| Tests | Which tests cover the area, at which seam, and what is untested. |
| History | Why it is this way: `git log --follow -- <file>`, `git blame -L`, the PRs and issues those commits reference (`gh pr view <n> --json title,body,comments`). |
| Config and runtime | Flags, env vars, jobs, infra definitions that change behaviour. |
| Impact | Every call site and consumer the planned change would touch. |

For a question about a third-party library or API the area depends on, load the `research` skill instead of a scout.

Keep the user informed while explorers run, and ask nothing that they will answer.

## 3. Check what came back

Fast-tier explorers miss things and sometimes invent them. Before writing:

- Open the cited lines for every claim the report will lean on.
- Where two explorers disagree, read the code yourself and record both readings if it stays unclear.
- Never cite code as evidence for its own intent. What code does is readable; why it exists lives in commits, PRs, tickets, and docs.

## 4. Write the report

Use `INVESTIGATION.md` and the writing rules from the `doc-templates` skill. Save it to the feature folder as `investigation-<topic>.md`, or `docs/research/` for standalone work. Relay the overview, the impact, and the gaps, and give the path.

If the investigation surfaces a term the glossary lacks or contradicts, flag it for the `domain-modeling` skill rather than editing `CONTEXT.md` from here.

## Attribution

The explorer fan-out and report shape are adapted from `pstack/skills/how` and the history method from `pstack/skills/why` in cursor/plugins (MIT, Lauren Tan). See `THIRD_PARTY_NOTICES.md`.
