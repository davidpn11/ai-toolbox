---
name: grilling
description: "Grill the user relentlessly about a plan, decision, or idea until nothing is silently assumed. Use when the user wants to stress-test their thinking, says 'grill me', 'interview me', 'poke holes', or asks to sharpen a plan or design before building. Facts are found by the agent; decisions are put to the user."
---

# Grilling

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

## Before the first round

- Start from what exists. Read the target project's `AGENTS.md`, `CONTEXT.md`, and `docs/adr/` if present, so you don't re-ask what is already decided. In a feature folder (see the `doc-templates` skill), read the briefs, research, and spikes too: their **Open questions** sections seed the first round, and their findings are facts you no longer need to ask about.
- Leave plan mode off. Plan mode pushes toward producing a plan; grilling is about finding out what the plan should contain.
- Classify each candidate question before asking it. If the answer is a fact you could observe by running or reading something (behavior, timing, layout, output, what the code does today), it is not the user's to answer. Find it yourself, or build a throwaway to observe it (load the `prototype` skill). Only decisions go to the user.

## Rounds and the frontier

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask *now* without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a *later* round, not this one.

If the user says "one question at a time", switch to single-question rounds for the rest of the session.

## Facts versus decisions

Finding *facts* is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, docs, running code), dispatch a fast-tier sub-agent (the `scout`, see the `delegation` skill) to find it, or load the `research` skill when the fact lives outside the repo; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The *decisions* are the user's: put each to them and wait.

Some answers sit in someone else's head (a stakeholder, legal, a customer). Offer the `questionnaire` skill for those and keep grilling the rest of the frontier.

Some questions are **ungrillable**: "one long form or three pages?", "how should this interaction feel?" They need something to react to. Say so, and offer to build the throwaway version with the `prototype` skill instead of asking.

## Probing the tree

Every branch gets the same sweep before it is considered settled:

- Edge cases, empty states, error states, and what the user sees when each happens.
- Concurrency and repeat runs. What happens if it runs twice, or crashes halfway?
- Permission and ownership. Who can do this, and who can see the result?
- Scope. What is deliberately out, and what is the smallest version that still answers the need?
- Reversibility. Which choices are hard to undo, and are those the ones being decided now?

## Ending the session

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Close with a short summary of every decision made, in the order they were made. Do not act on it until the user confirms you have reached a shared understanding.

A session with no pushback from the user is a session that wasn't needed. If every recommendation was accepted unchanged, say so and ask whether the plan was already settled.

## Attribution

Adapted from `skills/productivity/grilling` in mattpocock/skills (MIT, Matt Pocock). See `THIRD_PARTY_NOTICES.md`.
