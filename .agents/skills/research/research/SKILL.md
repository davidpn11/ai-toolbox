---
name: research
description: "Answer one question against primary sources (official docs, source code, specs, first-party APIs, changelogs) and save the cited findings as one Markdown note. Runs in a background subagent on a mid-tier model. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated; other skills call it once per question to fan out research in parallel."
context: fork
agent: general-purpose
model: sonnet
---

# Research

## The question

$ARGUMENTS

If the line above is empty or still reads as a placeholder, the question is the latest request in the conversation.

## Who does the reading

- **You are running as a subagent** (you have this brief but no earlier conversation): you are the researcher. Do the reading yourself, below.
- **You are in the main session**: hand this file and the question to one background subagent on the standard tier (see the `delegation` skill), and keep working. To research several questions, launch one subagent per question in the same turn. When each reports, read its note and relay the summary and the gaps.

## The researcher's job

1. Investigate the question against **primary sources**: official docs, source code, specs, first-party APIs, changelogs, release notes. Not a secondary write-up of them. Follow every claim back to the source that owns it. Prefer cloning a repo and reading files over fetching a rendered page of it.
2. Write the findings to one Markdown note, using `RESEARCH.md` and the writing rules from the `doc-templates` skill (call the Skill tool with "doc-templates"). Every claim gets a confidence tier and a citation (URL, or repo path plus commit SHA). Before saving, call the Skill tool with "unslop" and apply it to the prose.
3. Save it where the brief says. Otherwise, in a feature folder at `research/<slug>.md`; otherwise where the repo keeps such notes; otherwise `docs/research/<slug>.md`. Say where.
4. Stop when every part of the question has a cited answer or a documented gap. One file, one question. Do not widen it.
5. Reply with the response contract from the `delegation` skill: the path, the answer in at most 3 sentences, and the biggest gap.

## Rules

- Do not spawn subagents or re-invoke this skill. Nested research has caused runaway fan-out.
- Do not ask the user anything. If the question is ambiguous, pick the most useful reading, say which in the note, and answer it.
- Quote, don't paraphrase, when the wording is the evidence. Keep quotes short.
- Track what you searched, not just what you found. A search that finds nothing is still a result.
- Resist the story. When three pieces of evidence agree and a fourth contradicts them, the contradiction is the finding.
- Treat a hypothesis embedded in the question ("I assume it's for performance?") as one candidate to test.
- Record the version or commit you read, so the note can be re-checked later.

Research feeds a decision; it does not make it. Durable decisions belong in an ADR (the `domain-modeling` skill). Questions about why the project's own code is the way it is belong to the `investigation` skill.

## Attribution

Adapted from `skills/engineering/research` in mattpocock/skills (MIT, Matt Pocock) and the epistemics rules of `pstack/skills/why` in cursor/plugins (MIT, Lauren Tan). See `THIRD_PARTY_NOTICES.md`.
