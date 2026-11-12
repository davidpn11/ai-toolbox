# Investigation report template

How a part of the current system works, why it is that way, and what a planned change will touch. Follow the rules in [SKILL.md](SKILL.md). Use the `CONTEXT.md` vocabulary for domain terms.

```md
# How <area> works today

Sources and provenance: <repo + SHA, PRs and tickets read, docs + date read>
Planned change: <one line, or "none, understanding only">

## Overview

<One paragraph a new engineer could act on.>

## Key concepts

<The terms a reader needs, each in one line. Link to CONTEXT.md entries where they exist.>

## How it works

<The main path as numbered steps from entry point to effect, each with `file:line`.>

## Where things live

<Table: concern | path | notes.>

## Why it is this way

<History and intent, tagged with confidence tiers and cited to commits, PRs, tickets, or ADRs. Contradictions shown side by side.>

## Impact of the planned change

<What the change touches: call sites, data, tests, config, other teams' code. Which tests cover it today and which gaps exist. Skip if no change is planned.>

## Gotchas

<Constraints and traps that are not obvious from the code.>

## What we don't know

<Specific gaps and what was searched.>
```
