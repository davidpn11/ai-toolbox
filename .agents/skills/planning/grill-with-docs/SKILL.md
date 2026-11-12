---
name: grill-with-docs
description: "A relentless interview to sharpen a plan or design that also writes the docs as it goes: a CONTEXT.md glossary and ADRs under docs/adr/. Use when the user says 'grill me with docs', wants a design interview whose decisions get recorded, or is starting a feature that will introduce new domain terms."
disable-model-invocation: true
---

# Grill with docs

Two skills run together for the whole session:

1. Call the Skill tool with "grilling". That drives the interview: design tree, rounds, frontier, facts found by you and decisions put to the user.
2. Call the Skill tool with "domain-modeling". That drives the writing: glossary challenges, `CONTEXT.md` updates inline, ADRs offered only when hard to reverse, surprising, and a real trade-off.

One skill per call. If the Skill tool is unavailable in this harness, find both skills' `SKILL.md` files among the installed skills and follow both.

## Self-check before the first round

State in one line that both skills are loaded. Partial loading (interview happens, files never get written) is the most common failure of this workflow. If either did not load, load it before asking anything.

## During the session

- Every round follows the grilling format. Every resolved term or gated decision is written to disk in the same turn it is resolved, and you say so.
- Read `CONTEXT.md` and `docs/adr/` before the first round so existing decisions are not re-asked.
- When a question turns out to be ungrillable (it needs something to react to), offer the `prototype` skill instead of pressing.

## At the end

The grilling summary lists the decisions. The domain-modeling summary lists the files written. Decisions that met none of the ADR gates live only in this conversation; if the user wants them kept, hand the conversation to the `spec` skill, which writes them into a spec without a new interview.

## Attribution

Adapted from `skills/engineering/grill-with-docs` in mattpocock/skills (MIT, Matt Pocock). See `THIRD_PARTY_NOTICES.md`.
