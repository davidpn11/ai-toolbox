# Spike report template

A time-boxed answer to one feasibility question. Follow the rules in [SKILL.md](SKILL.md).

```md
# Spike: <the question>

Verdict: GO | NO-GO | INCONCLUSIVE
Timebox: <planned> / <used>
Code: <branch `spike/<name>` or scratch path, plus commit SHA>
Sources and provenance: <docs + date read, research notes used>

## Question and decision

<The falsifiable question, and the decision that waits on the answer.>

## Success criteria

<Set before building. Measurable: "p95 under 200 ms at 1k rows", "the SDK can stream partial results".>

## What we tried

<Numbered attempts. For each: what was built, the command that ran it, and the raw observation.>

## Evidence

<Output, numbers, screenshots, with the exact command or environment that produced them. Mark anything not measured as such.>

## Verdict

<Which criteria passed or failed, and why that gives this verdict. For INCONCLUSIVE, what would settle it and roughly what it costs.>

## Consequences for the plan

<Constraints the implementation must honour, rejected approaches, the follow-up work. Note whether this meets the ADR gates.>

## What we don't know

<Gaps, untested conditions, and the risks they leave.>
```
