# Spec template

The buildable description of a feature, synthesized from the feature folder. No file paths or code snippets, which go stale fast. Exception: a prototype snippet that encodes a decision more precisely than prose (a state machine, a schema, a type shape), trimmed to the decision and marked as coming from a prototype.

```md
# Spec: <feature>

Status: draft | approved
Inputs: <links to the product brief, design brief, research, investigation, spikes, ADRs used>

## Problem

<From the user's side. Link the product brief for evidence.>

## Solution

<From the user's side, one or two paragraphs.>

## User stories

<A long numbered list covering every aspect of the feature: "As a <actor>, I want <capability>, so that <benefit>.">

## Flows and states

<The agreed flows and the state table, or a link to the design brief section when it is final.>

## Implementation decisions

<Modules built or changed and their interfaces, schema changes, API contracts, integrations, architectural choices. Use CONTEXT.md and codebase-design vocabulary. Link ADRs and rationale pages instead of restating them.>

## Testing decisions

<The seams the feature is tested at (fewest possible, highest possible), what a good test looks like here, prior art in the codebase.>

## Non-functional requirements

<Performance budgets, security and privacy, accessibility, observability, rollout and migration, each measurable.>

## Out of scope

<What this spec deliberately does not do, with one line of why.>

## Risks and open questions

<What could still change the plan. Empty only when every question is settled.>
```
