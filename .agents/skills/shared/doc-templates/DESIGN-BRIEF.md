# Design brief template

How the feature should behave and look for the user. Follow the rules in [SKILL.md](SKILL.md).

```md
# Design brief: <feature>

Sources and provenance: <product brief, research notes, Figma links, prototype branches, design system paths>

## Primary flows

<One numbered list per flow: trigger, each step the user takes, what the system shows, where it ends. Mark the happy path.>

## States

<Table per screen or component: state | what triggers it | what the user sees | what they can do. Cover empty, loading, partial, success, error, permission denied, offline, and first-run where they apply.>

## Patterns from prior art

<What comparable products do for each flow, with screenshots or links, and which pattern is recommended.>

## Design system fit

<Existing components, tokens, and layout primitives to reuse (paths or Figma names). Gaps that need a new component.>

## Accessibility

<Keyboard path, focus order, announcements for dynamic changes, contrast, target sizes, reduced motion. WCAG 2.1 AA unless the project sets a higher bar.>

## Responsive and platform behaviour

<Breakpoints, touch versus pointer, what changes on small screens.>

## Content

<Copy that needs writing: labels, empty-state text, error messages, confirmations.>

## Explored options

<Prototype variants or Figma explorations, the evidence for each, and the recommendation.>

## Open questions for grilling

<Numbered decisions only the user can make, each with a recommended answer. Mark the ones that need a prototype instead of a question.>
```
