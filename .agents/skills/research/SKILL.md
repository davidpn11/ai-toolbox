---
name: research
description: "Investigate a question against primary sources (official docs, source code, specs, git history) and capture the findings as a cited Markdown file under docs/research/. Use when the user wants a topic researched, docs or API facts gathered, asks why the code is the way it is, or wants reading legwork delegated to a background agent."
---

# Research

Spin up a **background agent** to do the research, so you keep working while it reads. Give it this whole file as its brief, plus the question.

## The agent's job

1. Investigate the question against **primary sources**: official docs, source code, specs, first-party APIs, commit messages, PRs, tickets. Not a secondary write-up of them. Follow every claim back to the source that owns it. Prefer cloning a repo and reading files over fetching a rendered web page of it.
2. Write the findings to a single Markdown file, citing each claim's source (URL, or repo path plus commit SHA).
3. Save it where the repo already keeps such notes. If the repo has no convention, use `docs/research/<slug>.md` and say so in the report.
4. Stop when every part of the question has either a cited answer or a documented gap. One file, one question. Do not widen the question.

## Rules for the agent

- You are already the research agent. Do the reading yourself. Do not spawn further research agents or re-invoke this skill; nesting has produced runaway fan-out before.
- Quote, don't paraphrase, when the wording is the evidence. Keep quotes short.
- Track what you searched, not just what you found. A search that finds nothing is still a result.
- Resist the story. If three pieces of evidence line up and a fourth contradicts them, the contradiction is the most interesting finding.
- Never cite code as evidence for its own intent. What code does is readable; why it exists lives in commits, PRs, tickets, and docs.
- Treat the user's embedded hypothesis ("I assume it's for performance?") as one candidate to test, not a conclusion to confirm.
- Record the commit SHA or doc version you read at, so the notes can be re-checked later.

## Confidence tiers

Tag every claim in the file with one of these. The tag decides the phrasing.

- `[Direct]` Something an author wrote that answers the question: a doc line, a PR description, a code comment saying why. Phrase confidently and cite.
- `[Supported]` Several indirect pieces converge. Phrase confidently but show the pieces.
- `[Inferred]` Your reading of the context. Hedge ("appears", "likely", "suggests") and make the chain explicit: given A and B, C seems likely because D.
- `[Speculative]` Plausible but thin. "One possibility is X, but we found no direct evidence."
- `[Unknown]` You looked and could not find out. Say what you searched and for what.

Words that claim evidence ("because", "was designed to", "fixes", "the team decided") need a citation in the same sentence. Avoid "obviously", "clearly", "of course", and "just".

## File layout

```md
# <Question, as a title>

Sources and provenance: <repo + SHA, doc URLs + date read>

## Summary
<3 to 8 lines. The answer, with tiers.>

## Findings
<One section per sub-question. Each claim tagged and cited.>

## What we don't know
<Specific gaps: what was searched, where, for what. Never empty; if the evidence was complete, say that and why.>

## Sources consulted
<One line per source category, including "not searched" with the reason.>
```

## When the question is "why is the code like this"

Build the code anchor first, inline, before reading anything else:

```bash
git blame -L <start>,<end> -- <file>
git log --follow --oneline -20 -- <file>
git log -p <sha> -- <file>
gh pr view <n> --json title,body,author,mergedAt,closingIssuesReferences,comments,reviews
```

Extract `(#1234)` PR numbers from commit subjects. Then follow the PR to its issue, the issue to any design doc, and the design doc to the discussion. Present contradictions between sources side by side; do not pick the tidier narrative.

## Back in the main session

When the agent reports, read the file, relay the summary and the gaps to the user, and give the path. Research feeds the thinking; it does not replace the decision. If the notes were only needed for this task, tell the user they can delete the file after acting on it. Durable decisions belong in an ADR (see the `domain-modeling` skill), not in research notes.

## Attribution

Adapted from `skills/engineering/research` in mattpocock/skills (MIT, Matt Pocock) and the epistemics and investigator rules of `pstack/skills/why` in cursor/plugins (MIT, Lauren Tan). See `THIRD_PARTY_NOTICES.md`.
