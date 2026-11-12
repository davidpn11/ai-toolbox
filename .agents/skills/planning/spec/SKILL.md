---
name: spec
description: "Synthesize the feature folder (research, investigation, spikes, product and design briefs, grilling decisions, ADRs) and the current conversation into one buildable spec, with no new interview. Use after planning research and grilling are done, when the user says 'write the spec', 'turn this into a PRD', or before breaking work into a plan."
---

# Spec

Collapse everything learned so far into one document that a planner can break into tasks and a reviewer can check the code against. Do not interview; synthesize.

## 1. Gather

Read every file in the feature folder (see the `doc-templates` skill), `CONTEXT.md`, and the ADRs in the area. Use the conversation's grilling decisions as the highest authority: when a decision contradicts a brief, the decision wins and the spec says so.

If you have not explored the code the feature touches, load the `investigation` skill first, or send a `scout` for a narrow question.

## 2. Find the gaps before writing

List anything the spec needs that nobody has decided: a missing state, an undecided error behaviour, a requirement with no testing approach. Show the list to the user with a recommended answer for each. Settle small ones in this conversation; for a long list, load the `grilling` skill for one more round. Do not paper over a gap with a guess.

## 3. Choose the test seams

Load the `codebase-design` skill for its vocabulary, then sketch the seams the feature will be tested at. Prefer existing seams; when new ones are needed, put them as high as possible. Fewer is better; one is ideal. Confirm the seams with the user.

## 4. Write it

Write `spec.md` with `SPEC.md` and the writing rules from the `doc-templates` skill, status `draft`. Link the briefs, research, spikes, ADRs, and rationale pages instead of restating them. The user stories list should be long: every actor, every flow, every state from the design brief.

If the project's `AGENTS.md` names an issue tracker for specs, also publish it there and link both ways.

## 5. Approve

Relay the problem, the scope, the out-of-scope list, and the remaining risks. When the user approves, set the status to `approved`. The next step is the `planner` skill.

## Attribution

Adapted from `skills/engineering/to-spec` in mattpocock/skills (MIT, Matt Pocock). See `THIRD_PARTY_NOTICES.md`.
