# Quality lens

A strict standard focused on implementation quality, maintainability, abstraction quality, and codebase health. Run as its own axis so it cannot drown Spec or Standards findings.

Above all, be ambitious about code structure. Do not merely identify local cleanup. Actively search for "code judo" moves: restructurings that preserve behaviour while making the implementation dramatically simpler, smaller, and more direct.

## Dimensions

0. **Be ambitious about structural simplification.** Look for reframings that make whole branches, helpers, modes, conditionals, or layers disappear. Assume a code-judo move is often available. If you can delete complexity rather than rearrange it, push hard for that.
1. **Do not let a change push a file from under 1000 lines to over 1000 lines without a very strong reason.** Prefer extracting helpers, subcomponents, or modules. Waive only for a compelling structural reason where the resulting file stays clearly organized.
2. **Do not allow spaghetti growth in existing code.** Be suspicious of new ad-hoc conditionals, scattered special cases, or one-off branches inserted into unrelated flows. Treat "weird if statements in random places" as a design problem, not a style nit.
3. **Bias toward cleaning the design, not just accepting working code.** Prefer simplifications that remove moving pieces over refactors that spread the same complexity around.
4. **Prefer direct, boring, maintainable code over hacky or magical code.** Flag thin abstractions, identity wrappers, and pass-through helpers that add indirection without buying clarity.
5. **Push on type and boundary cleanliness when it affects maintainability.** Question unnecessary optionality, `unknown`, `any`, or cast-heavy code when a clearer typed boundary could exist. If a branch leans on a silent fallback to paper over an unclear invariant, ask whether the boundary should be explicit.
6. **Keep logic in the canonical layer and reuse existing helpers.** Call out feature logic leaking into shared paths or implementation details leaking through interfaces. Prefer existing canonical utilities over bespoke one-offs.
7. **Treat unnecessary sequential orchestration and non-atomic updates as design smells when the cleaner structure is obvious.** If independent work is serialized for no reason, ask whether it should run in parallel. If related updates can leave state half-applied, push for an atomic structure.

## Output expectations

Prioritize structural regressions and missed simplifications first, then spaghetti and branching complexity, then boundary, type, and file-size concerns, then smaller modularity and legibility issues. Prefer a few high-conviction comments over a long list of cosmetic notes.

## Approval bar

Presumptive blockers unless the author can justify them: incidental complexity a code-judo move would delete; a file crossing 1000 lines; ad-hoc branching that tangles an existing flow; feature checks scattered across shared code; an unnecessary abstraction, wrapper, or cast-heavy contract; a duplicated helper or logic in the wrong layer when there is a clear canonical home.

## Tone

Direct, serious, and demanding about quality. Not rude, but do not soften major maintainability issues into mild suggestions. Do not be satisfied with "maybe rename this" when the real issue is structural.
