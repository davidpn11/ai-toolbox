---
name: architecture-review
description: "Scan a codebase for deepening opportunities (shallow modules, leaky seams, untestable clusters), present them as a visual report with before/after diagrams, then interview the user through whichever candidate they pick. Use when the user asks for an architecture review, wants to know where the codebase hurts, or asks what to refactor next."
disable-model-invocation: true
---

# Architecture review

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

Call the Skill tool with "codebase-design" first. Its vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real") are used exactly in every suggestion; never drift into "component," "service," "API," or "boundary." If the Skill tool is unavailable, read `../codebase-design/SKILL.md`.

The domain language in `CONTEXT.md` gives names to good seams; ADRs in `docs/adr/` record decisions this review should not re-litigate.

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. A deepening opportunity in code nobody touches is a refactor you'll never cash in. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline --stat`) to find the hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the project's `AGENTS.md`, its domain glossary (`CONTEXT.md`), and any ADRs in the area you're touching first.

Then spawn a read-only sub-agent to walk the codebase. Don't follow rigid heuristics; explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?
- Which of the four red flags in the `codebase-design` skill's `DESIGN-RED-FLAGS.md` (shallow module, information leakage, temporal decomposition, pass-through method) show up, and where?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

For every candidate, classify its dependencies with the categories in `DEEPENING.md` (in-process, local-substitutable, ports & adapters, mock). The category decides how the deepened module gets tested and belongs on the card.

### 2. Present candidates

Default to the HTML report. Offer the Markdown report instead when the user asked for it, the environment is offline, or the user cannot open a browser.

**HTML report.** Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user (`open` on macOS, `xdg-open` on Linux, `start` on Windows) and tell them the absolute path. Scaffold, diagram patterns, and styling are in [HTML-REPORT.md](HTML-REPORT.md). Each candidate gets a **before/after visualisation**. Be visual.

**Markdown report.** Same cards, written to `<tmpdir>/architecture-review-<timestamp>.md`, with before/after as Mermaid blocks or ASCII boxes.

Each candidate card has:

- **Files**: which files/modules are involved.
- **Problem**: why the current architecture is causing friction. One sentence.
- **Solution**: plain English description of what would change. One sentence.
- **Wins**: bullets of six words or fewer, in terms of locality and leverage, and how tests improve. Not "easier to maintain" or "cleaner code".
- **Before / After diagram**: side by side, illustrating the shallowness and the deepening.
- **Dependency category** tag and **Recommendation strength** badge: one of `Strong`, `Worth exploring`, `Speculative`.

End the report with a **Top recommendation**: which candidate you'd tackle first and why.

**Use CONTEXT.md vocabulary for the domain, and the `codebase-design` vocabulary for the architecture.** If `CONTEXT.md` defines "Order," talk about "the Order intake module," not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (a warning callout: _"contradicts ADR-0007, but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

A report where every candidate is `Speculative` means the scan found nothing worth doing. Say that plainly rather than inflating a badge.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?" If the user said up front they only want the report, stop here.

### 3. Grilling loop

Once the user picks a candidate, call the Skill tool with "grilling" to walk the decision tree with them: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallize; call the Skill tool with "domain-modeling" to keep the domain model current as you go:

- **Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md`. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing; skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces for the deepened module?** Use the design-it-twice parallel sub-agent pattern in the `codebase-design` skill's `DESIGN-IT-TWICE.md`, then write the chosen design up with its `RATIONALE.md` template before implementing.

### 4. Hand-off

The output of this skill is a chosen candidate, its rationale page, and any glossary or ADR updates. Implementation is a separate step: hand the rationale to the `planner` skill (or implement directly if the change is small), and watch for the scrap signals listed in `DESIGN-RED-FLAGS.md` while building.

## Attribution

Adapted from `skills/engineering/improve-codebase-architecture` in mattpocock/skills (MIT, Matt Pocock). See `THIRD_PARTY_NOTICES.md`.
