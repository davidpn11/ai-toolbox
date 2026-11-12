---
name: figma-design
description: "Design with Claude and Figma through the Figma MCP server, in both directions: turn a Figma frame into code that reuses the project's components, or push prototypes and built UI back into Figma as editable layers. Use when the user shares a Figma link or selection, asks to implement a design, wants variants explored in Figma, or asks to sync code and design."
---

# Figma design

The Figma MCP server gives the agent design context (layout, variables, component mappings, screenshots) and, on the remote server, write access to the canvas. This skill is the workflow around those tools. Tool names below are as documented by Figma at the time of writing; run the client's tool listing if one is missing, and read the docs linked at the end when in doubt.

## Setup (once per machine)

Remote server (recommended, all seats and plans, OAuth in the browser):

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

Or install Figma's own plugin, which bundles the server plus its `figma-*` skills:

```bash
claude plugin install figma@claude-plugins-official
```

Desktop server (Dev or Full seat, works from the current selection in the Figma desktop app; enable it from Dev Mode → MCP server → Enable desktop MCP server):

```bash
claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp
```

Cursor: `/add-plugin figma`. VS Code: add an HTTP server entry for `https://mcp.figma.com/mcp` in the MCP user configuration.

Rate limits are per seat and tight on View and Collab seats (single digits per month). Real use needs a Dev or Full seat. Writing to files outside drafts needs a Full seat.

## Direction 1: design to code

1. **Get the node.** Ask the user for a "Copy link to selection" URL, or use the current selection on the desktop server. One frame or component at a time. Whole screens produce slow, truncated responses; ask for `Card`, `Header`, `Sidebar` separately.
2. **Pull context in this order.** `get_design_context` first (default entry point; it returns a React + Tailwind rendering that you translate into the project's stack). If the response is truncated, call `get_metadata` for the sparse node outline and re-fetch only the nodes you need. Then `get_screenshot` for the visual reference; Figma's own guidance is that a screenshot plus the code output beats either alone. Then `get_variable_defs` for tokens, and `download_assets` for images and icons. If `get_design_context` overflows the client's MCP output cap in Claude Code, raise `MAX_MCP_OUTPUT_TOKENS`.
3. **Map to real components.** Check `get_code_connect_map` for the selection. Mapped components come back as `<CodeConnectSnippet>` blocks with the real import; use those, never a re-implementation. For unmapped components, search the project's component library (the `react-tailwind` skill in this collection covers the default stack) before writing new markup. If the design system is published, `search_design_system` finds the intended component or variable by name.
4. **Tokens, not literals.** Every colour, spacing, radius, and type value that came back as a variable becomes the project's token for it. A hardcoded hex or pixel value in the output is a finding, not a shortcut. If the Figma file has no variables, say so and ask whether to add them in Figma first (Direction 2) or hardcode with a TODO.
5. **Implement in the project's conventions.** Read the target project's `AGENTS.md`. Put the component where the project keeps such things, use its layout primitives, and keep prototype-quality code out (no inline styles, no `any`).
6. **Verify 1:1.** Render the component (the `run` or `prototype` skill, or the project's dev server), screenshot it, and compare against the Figma screenshot side by side. Check states the frame shows (hover, empty, error) and the responsive behaviour the auto layout implies. Report differences honestly; do not mark complete until they are resolved or explicitly accepted.

## Direction 2: code to design

Both write paths need the remote server.

- **Capture built UI into Figma.** `generate_figma_design` opens a capture toolbar in the browser; pick "Entire screen" or "Select element" to turn the live page into editable layers. Use it to bring a finished implementation, or a winning prototype variant, back into the design file so the file matches production. Any seat can create in drafts; editing an existing file needs a Full seat.
- **Create or edit native Figma content.** `use_figma` runs Plugin API JavaScript against a Figma Design file and produces real frames, components, variants, variables, and auto layout. Use it to add missing variables, generate component variants, or build a first-pass screen for the designer to refine. Limits at the time of writing: 20 kb per call, no images or custom fonts (fonts must be in the account), beta-quality output that needs review.
- **Diagrams and files.** `generate_diagram` turns Mermaid or natural language into a FigJam diagram (useful for architecture reviews and flows). `create_new_file` makes a blank Design, FigJam, or Slides file.

Confirm with the user before any write outside their drafts. Writes are visible to everyone in the file.

## Direction 3: exploring options with both tools

When the question is "what should this look like", combine this skill with the `prototype` skill:

1. Pull the existing frame's context so variants respect the design system (Direction 1, steps 1 to 3).
2. Build 3 structurally different variants on the real route behind `?variant=`, per the prototype skill's `UI.md`. Screenshot each.
3. Present the screenshots and a recommendation. When the user picks one (or a mix), capture the winner into Figma with `generate_figma_design` so the designer has editable layers to refine, and fold the code in properly.

For a moodboard before building, gather references first as the prototype skill describes.

## Project rules file

The first time this skill runs in a project, offer to add a short Figma section to the project's `AGENTS.md` or `CLAUDE.md` (Figma's MCP prompt `create_design_system_rules` can draft it where the client supports MCP prompts). It should state:

- The required tool order: `get_design_context`, then `get_metadata` if truncated, then `get_screenshot`, then assets.
- Where components live and which layout primitives to use.
- The token policy (no hardcoded values when a variable exists).
- "If the Figma MCP server returns a localhost source for an image or SVG, use that source directly."
- The verification bar: compare against the screenshot for 1:1 look and behaviour before marking complete.

## In Figma, for better output

Tell the designer what improves results, when relevant: repeated elements as components, variables applied to spacing, colour, radius, and type, semantic layer names (`CardContainer`, not `Frame1268`), auto layout everywhere, and Code Connect mappings for core components first. Figma's own guidance calls Code Connect "the #1 way to get consistent component reuse in code."

## Sources

Verified against Figma's first-party documentation on 2026-09-16; see `research/ADR-002-skills-survey-mattpocock-cursor-pstack.md` in the ai-toolbox repo for the cited survey. Main pages: https://developers.figma.com/docs/figma-mcp-server/ (tools and prompts, remote and local installation, rate limits, code-to-canvas, write-to-canvas, add-custom-rules, avoid-large-frames, mcp-clients-issues) and https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server. Figma's plugin and skills: https://github.com/figma/mcp-server-guide.
