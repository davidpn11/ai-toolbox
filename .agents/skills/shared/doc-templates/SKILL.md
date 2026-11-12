---
name: doc-templates
description: "Shared templates and writing rules for every document the lifecycle produces: research notes, investigation reports, spike reports, ADRs, product and design briefs, specs, plans, design rationales, and questionnaires. Use when writing or reviewing any of those documents, or when another skill says to fill a template."
---

# Doc templates

One place for the shape of every document, so a research note written by `research` reads like one written by `spike`, and the planning skills can consume any of them without guessing.

## Where documents live

Work on one feature keeps its documents in one **feature folder**, so any session (or subagent) can pick up the work from paths alone:

```
docs/features/<feature-slug>/
├── research/<topic>.md        research notes (RESEARCH.md)
├── investigation-<topic>.md   how the current system works (INVESTIGATION.md)
├── spike-<topic>.md           feasibility verdicts (SPIKE.md)
├── product-brief.md           PRODUCT-BRIEF.md
├── design-brief.md            DESIGN-BRIEF.md
├── questionnaire-<who>.md     QUESTIONNAIRE.md
├── rationale-<module>.md      RATIONALE.md
├── spec.md                    SPEC.md
└── plan.yaml                  PLAN.md
```

Project-wide records live outside the feature folder: the glossary in `CONTEXT.md` and decisions in `docs/adr/` (ADR.md). If the target project's `AGENTS.md` or existing docs use other locations, follow those and say so. Create folders lazily, when the first file needs them.

Standalone work with no feature (a one-off research question) goes to `docs/research/<slug>.md`.

## Rules for every document

1. **Provenance first.** Under the title, list what was read and at which version: repo and commit SHA, doc URLs and the date read, the feature folder files used as input.
2. **Tag claims with a confidence tier** in research, investigation, and spike documents:
   - `[Direct]`: an author wrote it (doc line, PR description, code comment saying why). Phrase confidently and cite.
   - `[Supported]`: several indirect pieces converge. Show the pieces.
   - `[Inferred]`: your reading of the context. Hedge, and make the chain explicit.
   - `[Speculative]`: plausible but thin. Say no direct evidence was found.
   - `[Unknown]`: you looked and could not find out. Say what you searched.
   Words that claim evidence ("because", "was designed to", "the team decided") need a citation in the same sentence.
3. **Never leave out what you don't know.** Every research, investigation, spike, and brief ends with a gaps or open-questions section. It is never empty; if the evidence was complete, say why.
4. **Link, don't restate.** A brief points at the research note that holds the detail; a spec points at the briefs and ADRs. A fact lives in one document.
5. **Sentence-case headings, no filler.** Before saving, call the Skill tool with "unslop" and apply it to the prose.
6. **Replace every italic note** in a template with content, or delete the section if it truly does not apply and say why in one line.

## Templates

| Template | Written by | Read by |
|----------|------------|---------|
| [RESEARCH.md](RESEARCH.md) | `research` | everything downstream |
| [INVESTIGATION.md](INVESTIGATION.md) | `investigation` | `spike`, `spec`, `planner` |
| [SPIKE.md](SPIKE.md) | `spike` | `spec`, `domain-modeling` (ADR) |
| [PRODUCT-BRIEF.md](PRODUCT-BRIEF.md) | `product-research` | `design-research`, `grilling`, `spec` |
| [DESIGN-BRIEF.md](DESIGN-BRIEF.md) | `design-research` | `grilling`, `spec` |
| [QUESTIONNAIRE.md](QUESTIONNAIRE.md) | `questionnaire` | the recipient, then `grilling` |
| [ADR.md](ADR.md) | `domain-modeling` | every later session |
| [RATIONALE.md](RATIONALE.md) | `codebase-design` | `spec`, implementers |
| [SPEC.md](SPEC.md) | `spec` | `planner`, `code-review` (Spec axis) |
| [PLAN.md](PLAN.md) | `planner` | `architect` |
