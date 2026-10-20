# Design rationale template

The prose that ships alongside a type sketch. One page. Sentence-case headings, no boilerplate. Replace the italic notes with actual content. Uses the vocabulary in [SKILL.md](SKILL.md).

```md
## Problem

*One paragraph. What we're trying to do, and what about the existing system or constraints makes the shape non-obvious. Name the constraints the design must honor: existing types to interop with, callers we can't break, invariants that cross the seam.*

## Usage (caller's view)

*Write this first, before the type sketch. Show the README or quickstart the consumer reads, plus two or three realistic call sites in their own code. What they import, what they call, what comes back. The sketch in Shape is derived from this. When they diverge, reconcile the sketch to the usage, not the reverse.*

## Shape

*The recommended module structure. Data structures first. Then how data flows through the signatures. Name the load-bearing decisions. State which invariants are encoded in types, where validation lives, and what the module deliberately does not do. Judge depth explicitly: what complexity the interface hides, what remains exposed to callers, and why the interface is no larger than needed. Mark unimplemented bodies with `not implemented` and tricky logic with TODO pseudocode so a reader can trace input to output from types and signatures alone.*

## Tradeoffs accepted

*One bullet per tradeoff. Form: "we accept X in exchange for Y." Name anything a future reader might mistake for an oversight.*

## Alternatives considered

*Required. At least one concrete alternative shape, with one line on why it lost, judged on depth rather than implementation simplicity alone. Avoid listing flavors of the same shape. If the constraints forced the answer, say "this was the only viable shape because...".*

## Open questions and risks

*Things the user needs to weigh in on, and risks worth flagging before implementation. Phrase as questions, so the answer is the resolution.*

## Next implementation step

*The first thing to build against the sketch. One sentence.*
```

If any decision here meets all three ADR gates (hard to reverse, surprising without context, a real trade-off), record it with the `domain-modeling` skill's ADR format instead of leaving it only in this page.
