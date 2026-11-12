---
name: design-research
description: "Work out how a feature should behave and look: user flows, every screen state, interaction patterns from comparable products, fit with the existing design system and Figma files, accessibility, and responsive behaviour, then write a design brief. Branches to throwaway UI prototypes when a look-and-feel question cannot be settled by asking. Use when planning any user-facing feature, when the user asks for UX or UI research, flows, wireframes, design options, or 'how should this work for the user'."
---

# Design research

Turn "what the product should do" into "what the user sees and does", with every state accounted for before anyone writes a component.

## 1. Inputs

Read `product-brief.md` in the feature folder if it exists (see the `doc-templates` skill); its segments and scope drive the flows. Without one, ask the user for the target user and the core job in one exchange.

## 2. Inventory what exists

In parallel, in one turn:

- Send a `scout` (fast tier, see the `delegation` skill) to list the project's design system: component library paths, tokens and theme config, layout primitives, existing screens that do something similar. Ask for paths, not opinions.
- If the user has a Figma file or frame, call the Skill tool with "figma-design" and pull the context for the relevant frames (Direction 1, steps 1 to 3).
- Call the Skill tool with "research" for interaction prior art: how 3 to 5 named products handle this flow, with screenshots or links. One call per product or pattern. Save under the feature folder's `research/`.

## 3. Draft flows and states

While research runs, draft from the product brief:

- **Flows**: each job as a numbered list from trigger to finish.
- **State table** per screen or component: empty, loading, partial, success, error, permission denied, offline, first run. Most missed requirements hide in these rows.
- **Accessibility**: keyboard path and focus order, what screen readers announce on change, contrast and target size. The `ui-engineer` skill holds the WCAG 2.1 AA checklist this brief is checked against later.
- **Content**: every label, empty-state line, error message, and confirmation that needs writing.

## 4. Settle what can't be asked

Questions like "one long form or three steps?" or "should this feel instant or deliberate?" need something to react to. Call the Skill tool with "prototype" and take its UI branch: several structurally different variants on one route behind `?variant=`, each screenshotted. If the team designs in Figma, use the `figma-design` skill's Direction 3 to send the winner back to the canvas.

Record each variant, its evidence, and your recommendation. The user picks.

## 5. Write the brief

Write `design-brief.md` with `DESIGN-BRIEF.md` and the writing rules from the `doc-templates` skill. End it with **Open questions for grilling**, each with a recommended answer, marking the ones that still need a prototype. Relay the flows, the riskiest state, and the open questions to the user. The next step is the `grilling` skill.
