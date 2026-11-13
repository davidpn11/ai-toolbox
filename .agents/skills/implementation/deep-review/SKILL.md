---
name: deep-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along separate axes: Standards (repo conventions plus a code-smell baseline), Spec (does it do what the issue asked), and optionally Quality (structural simplification) and Blast radius (what it breaks elsewhere). Runs each axis in a parallel read-only sub-agent, then applies lead judgment into Act on / Consider / Noted / Dismissed. Use when the user wants a deep review of a branch, a PR, work-in-progress changes, or asks to 'review since X'; the planner runs it after every build. Claude Code's built-in /code-review is a separate command."
---

# Deep review

Two things make this review different from reading the diff yourself. The axes are kept separate so one cannot mask another, and the findings are filtered by a lead who has context the reviewers lack. The deliverable is a verdict. Do NOT auto-apply changes.

Run it in a fresh session where possible. The same context reviewing its own work is confirmation bias with a slash command.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`). If they didn't specify one, use the repo's default branch and say so.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the commits via `git log <fixed-point>..HEAD --oneline`. If the user wants uncommitted work reviewed too, add `git diff HEAD` and say both are in scope; the three-dot diff alone excludes the working tree.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here, not inside parallel sub-agents.

### 2. State the intent and find the spec

Write one paragraph stating what the change is meant to do, derived from the user's message, commit messages, the PR description, and the code. If you are unsure of the intent, ask before spawning anything.

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`), fetched with `gh issue view` / `gh pr view` or the tracker the project's `AGENTS.md` names.
2. A path the user passed as an argument.
3. A `spec.md` in a feature folder (`docs/features/<slug>/`, see the `doc-templates` skill), or a spec or plan file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If there isn't one, the Spec axis is skipped and the report says "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how code should be written: `AGENTS.md`, `CLAUDE.md`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`, lint and formatter configs. On top of that, the Standards axis always carries the **smell baseline** in [references/smells.md](references/smells.md). Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Skip anything tooling already enforces.

### 4. Pick the axes

Always: **Standards** and **Spec** (when a spec exists). Add on request, or when the change warrants it:

- **Quality**: for changes that add structure (new modules, new branching, files growing past 1000 lines). Uses [references/quality-lens.md](references/quality-lens.md).
- **Blast radius**: for small diffs the user doesn't trust, or changes to shared code. Uses [references/blast-radius.md](references/blast-radius.md) and must run real code to prove the one safety fact.

For high-stakes changes, run the same brief against a second model where the harness allows (Claude Code: the `model` parameter on the sub-agent). A second opinion is the same prompt against a different model; agreement between them is the strongest signal.

### 5. Spawn the sub-agents in parallel

One read-only sub-agent per axis, all launched in one turn, on the standard tier (see the `delegation` skill). The lead judgment in step 7 stays with you. Every brief is self-contained: the sub-agent has no other access to this file. Each brief includes:

- The diff command and commit list, the intent paragraph, and the reviewer contract in [references/reviewer-brief.md](references/reviewer-brief.md) pasted in full.
- **Standards**: the standards files found in step 3, the full smell baseline pasted in, and the instruction: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard, citing the standard (file + rule); and (b) any baseline smell you spot, naming it and quoting the hunk. Distinguish hard violations from judgement calls. Skip anything tooling enforces. Under 400 words."
- **Spec**: the path or fetched contents of the spec, and the instruction: "Report (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."
- **Quality**: the quality lens pasted in full, and the instruction: "Prioritise structural regressions and missed simplifications first. A few high-conviction findings over a long list of nits. Under 400 words."
- **Blast radius**: the blast-radius brief pasted in full.

Every brief ends with this line, verbatim: "Do not invoke `/deep-review` or `/code-review`, or spawn additional agents: perform this review directly."

### 6. Aggregate per axis

Present each report under its own heading (`## Standards`, `## Spec`, `## Quality`, `## Blast radius`), verbatim or lightly cleaned. Do **not** merge or rerank findings across axes. A change can follow every standard and implement the wrong thing, or do exactly what the issue asked and break the project's conventions; reporting separately stops one axis masking the other.

When two reviewers ran the same axis, merge duplicates within that axis and note which reviewers raised each finding. Findings raised independently by more than one reviewer are the highest signal.

### 7. Lead judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Apply [references/lead-judgment.md](references/lead-judgment.md) and sort every finding, still within its axis, into:

- **Act on**. Real issues affecting correctness, security, spec conformance, or maintainability given the actual goals. These would block a real PR.
- **Consider**. Legitimate points, but you're not sure they outweigh the cost of addressing them now.
- **Noted**. Technically valid but not actionable now: context-dependent, premature, or low-impact at this stage.
- **Dismissed**. Wrong, nitpicky, hypothetical, or missing context. One line on why. This section is a trust mechanism; keep it visible so the user can overrule you.

If Act on has more than five items across all axes, you are probably not filtering hard enough.

## Output

```
### Intent
> one paragraph

### Reviewers
- Standards: <model>, N findings
- Spec: <model>, N findings (or "skipped, no spec available")
- ...

## Standards
### Act on / Consider / Noted / Dismissed

## Spec
### Act on / Consider / Noted / Dismissed

## Quality  (if run)
## Blast radius  (if run)

### Summary
One line per axis: finding count and the worst issue within that axis. No single winner across axes.
```

## Known limits

- The review does not converge. Do not loop it until it comes back clean; fix the Act on items, then ship or re-review once.
- Reviewers see a diff and a paragraph. The lead has the conversation. Findings that reveal missing context are dismissed politely, not argued with.

## Attribution

Skeleton, two-axis rule, and smell baseline adapted from `skills/engineering/code-review` in mattpocock/skills (MIT, Matt Pocock). Reviewer contract, rubric, lead judgment, quality lens, and blast radius adapted from `pstack/skills/interrogate` and `pstack/skills/blast-radius` in cursor/plugins (MIT, Lauren Tan) and `cursor-team-kit/skills/thermo-nuclear-code-quality-review` (MIT, Eric Zakariasson). See `THIRD_PARTY_NOTICES.md`.
