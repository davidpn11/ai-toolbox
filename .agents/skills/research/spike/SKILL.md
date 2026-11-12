---
name: spike
description: "Answer one technical feasibility question in a fixed timebox: read the docs, build the smallest throwaway that tests it, measure, and write a GO / NO-GO / INCONCLUSIVE spike report with evidence. Use when the user asks 'can we do X with Y', wants to compare libraries or approaches on real numbers, or when a plan depends on an unproven technical assumption."
---

# Spike

A spike buys certainty with throwaway code. It ends in a verdict on one question, backed by something that ran.

## 1. Frame it

Agree these with the user before building, in one short exchange. Recommend an answer for each:

- **Question**: one, falsifiable. "Can the Postgres logical replication slot feed our event bus with under 1 s lag?" not "evaluate replication".
- **Decision**: what the answer unblocks, and what happens on NO-GO.
- **Success criteria**: measurable, set now so the result can't move the goalposts.
- **Timebox**: hours, not days. When it runs out, stop and report INCONCLUSIVE with what remains.

Comparing approaches is one spike with the same criteria applied to each candidate.

## 2. Read first

Call the Skill tool with "research" for each documented limit, version constraint, or known issue the question depends on. It runs in the background; start step 3 on the parts the docs won't change. If the docs already settle the question, stop and write the verdict from them.

For code the spike must plug into, call the Skill tool with "investigation", or send one `scout` for a narrow lookup.

## 3. Build the smallest thing that answers

Call the Skill tool with "prototype" and follow its rules (throwaway, trivial to run, no polish). Most spikes take the script branch: the smallest program that exercises the question. Work on a `spike/<name>` branch or a scratch directory, never on the main line.

## 4. Measure

Run each experiment and record the raw output with the exact command and environment. When the question is "is X better than what we have", measure the current baseline the same way first. Repetitive runs (benchmarks, matrix of versions, load) go to the `runner` subagent or a fast-tier subagent (see the `delegation` skill), which reports numbers and never edits code. Mark anything you did not measure as not measured.

## 5. Write the verdict

Use `SPIKE.md` and the writing rules from the `doc-templates` skill. Save it to the feature folder as `spike-<topic>.md`.

- **GO**: every criterion passed. List the constraints the real implementation must honour.
- **NO-GO**: a criterion failed for a reason the implementation can't fix. Say what failed and what the alternatives are.
- **INCONCLUSIVE**: the timebox ran out or the evidence is mixed. Say what would settle it and roughly what it costs.

If the verdict commits the project to something hard to reverse (a datastore, a vendor, a protocol), call the Skill tool with "domain-modeling" and offer an ADR.

## 6. Keep the evidence, drop the code

Commit the spike code to its `spike/<name>` branch and link it from the report. It is a primary source, never merged. The real implementation is rebuilt properly from the plan.

## Attribution

The verdict scale and baseline-versus-treatment discipline are adapted from `cursor-team-kit/skills/verify-this` in cursor/plugins (MIT, Eric Zakariasson). See `THIRD_PARTY_NOTICES.md`.
