# Lead judgment

The reviewers have produced their findings. Apply pragmatic engineering judgment. Don't aggregate. Filter, contextualize, and decide.

## Why this step matters

Adversarial reviewers are useful because they're aggressive. But aggression without context produces noise. The reviewers only saw a diff and a one-paragraph intent. They don't know what was already tried and rejected, what constraints exist outside the code (timeline, dependencies, migration plans), which parts are temporary scaffolding, or what the next PR in the stack will address. You have the full conversation context. Use it.

## Filtering principles

- **Nitpick gravity.** Reviewers fill their review. If a reviewer's findings are all nits and style preferences, the code is probably fine. Say so.
- **Hypothetical vs actual.** "What if someone passes null here?" is only a finding if the caller can actually pass null. Trace the call site. If the input is validated upstream or the type system prevents it, dismiss.
- **Premature abstraction warnings.** Does this code need to change in a second way? If not, the suggested abstraction is premature. Simple inline code that works beats an abstraction that's overkill for the current scope.
- **"I would have done it differently."** The most common false positive in code review. Not a bug, not a design flaw, not actionable unless the reviewer shows a concrete problem. Dismiss, and say why.
- **Missing context signals.** Changes suggested to code the author didn't touch; patterns flagged that are consistent with the rest of the codebase; approaches that conflict with constraints you know about. Honest mistakes from limited information. Dismiss gracefully.

## When reviewers are right

Don't dismiss findings because they're uncomfortable. Signs a finding deserves attention:

- More than one reviewer flagged it independently.
- It identifies a concrete execution path, not a hypothetical.
- It reveals a gap in your mental model of the code.
- You read it and think "...yeah, actually".

Be especially careful about dismissing security findings, correctness bugs, and spec gaps. These deserve scrutiny even from a single reviewer.

## Verdict calibration

A good verdict is useful, not comprehensive. The user should be able to read Act on, fix those, and ship with confidence. If Act on has more than five items, you're probably not filtering hard enough.

Dismissed is not busywork. It's a trust mechanism. Showing what you rejected and why lets the user override your judgment where they disagree.
