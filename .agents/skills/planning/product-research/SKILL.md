---
name: product-research
description: "Work out what problem a feature solves, for whom, how people cope today, and how comparable products solve it, by fanning out parallel research subagents and writing a product brief whose open questions seed the planning interview. Use when starting a user-facing feature or product, when the user asks for competitor or market research, user needs, jobs to be done, success metrics, or 'what should this product do'."
---

# Product research

Before anyone decides what to build, find out what the problem is and how others have solved it. The output is a product brief: evidence and recommendations for the agent, decisions for the user.

## 1. Start from what is known

Read the feature folder (see the `doc-templates` skill), `CONTEXT.md`, and any existing research. Then ask the user one round, in the `grilling` format, only for what you cannot look up:

- Who is this for, and what are they trying to get done?
- Why now: what prompted it?
- Which products, competitors, or internal tools do they already have in mind?
- What would tell them, three months after launch, that it worked?

Accept "don't know" for any of these; it becomes a research question.

## 2. Fan out the research

Turn the gaps into separate questions and call the Skill tool with "research" once per question, all in the same turn, each told to save under the feature folder's `research/`. Typical questions:

- How do 3 to 5 comparable products solve this? One question per product or per cluster, asking for the flow, the feature set, the pricing or packaging if it matters, and where users complain.
- What evidence is there that the problem is real and how it hurts: support threads, reviews, forum posts, issue trackers, analytics the project can reach.
- Which standards, regulations, or platform rules constrain the feature (privacy, payments, accessibility law, app store rules)?
- What do the project's own users already do about it? Send a `scout` (see the `delegation` skill) through the codebase, issues, and docs for existing workarounds or half-built versions.

Research runs in the background. While it runs, draft the problem and segment sections from what the user said.

## 3. Write the brief

When the notes are back, read them and write `product-brief.md` with `PRODUCT-BRIEF.md` and the writing rules from the `doc-templates` skill. Link each claim to the research note behind it rather than restating it.

Push on these while writing, because they decide everything downstream:

- **The smallest version that solves the core problem.** Name it, then the increments after it.
- **The riskiest assumption.** The one that, if false, makes the feature pointless. Say how to test it cheaply (a `spike`, a `prototype`, a `questionnaire` to someone who knows).
- **Success signals you can measure** with what the project already has. A metric nobody can collect is a wish.

## 4. Hand over

End the brief with **Open questions for grilling**: numbered decisions, each with your recommended answer. Relay the summary, the riskiest assumption, and those questions to the user. The next step is the `design-research` skill for user-facing work, or the `grilling` skill straight away for backend work.
