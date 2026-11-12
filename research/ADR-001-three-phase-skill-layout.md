# ADR-001: Skills grouped by lifecycle phase, documents passed by path

Status: accepted (2026-10-19)

The skills are grouped into `shared/`, `research/`, `planning/`, and `implementation/` under `.agents/skills/`, and a `lifecycle` skill moves one feature through the phases by reading what its feature folder (`docs/features/<slug>/`) already holds. Skills hand work to each other through documents in that folder, never through the conversation, so any phase can resume in a fresh session or a subagent. Reusable document shapes live in one `doc-templates` skill, and model-tier and subagent rules live in one `delegation` skill.

## Consequences

- **Discovery.** The `skills` CLI stops descending once it finds a `SKILL.md`, and walks at most three levels below `.agents/skills/`. A phase folder must never hold a `SKILL.md` of its own, and skills sit exactly at `.agents/skills/<phase>/<skill>/SKILL.md`. Before this change, `research/SKILL.md` hid `unslop`, `grilling`, `grill-with-docs`, and `prototype` from installation (vercel-labs/skills `src/skills.ts`, `walkSkillDirs`, read at `a80e4c9d`).
- **Cross-skill references** use skill names ("call the Skill tool with ..."), never relative paths, because installation flattens the phase folders.
- **Subagents are thin.** `.agents/agents/*.md` hold frontmatter (tools, model tier, `skills:` to preload) and a few lines. The persona content lives once, in the matching skill. Claude Code reads subagents from `.claude/agents/`, so they are copied there.
- **Model tiers.** `research` runs forked on `sonnet` (`context: fork`, `model: sonnet`); `scout` and `runner` run on `haiku`; specialists on `sonnet`; the architect and every user-facing interview on the main model. Other harnesses ignore these frontmatter keys and read the same instructions in the skill body.
- **The architect runs in the main session**, because a Claude Code subagent cannot spawn subagents.
- **`AGENTS.md` was removed** from this repo. Its delegation protocol moved to the `delegation` skill and its plan schema to `doc-templates/PLAN.md`. Skills still read the target project's `AGENTS.md`.

## Considered options

- **Templates inside each owning skill** (ADR format in `domain-modeling`, spike format in `spike`). Rejected: research, investigation, and spike reports share provenance and confidence-tier rules, and copies drift.
- **Keeping the full persona text in both the subagent and the skill.** Rejected: about 1,500 duplicated lines, already drifting (stale model ids such as `claude-sonnet-4-20250514`).
- **Porting `wayfinder`** from mattpocock/skills for huge efforts. Deferred: it depends on an issue tracker with native blocking links, and the feature folder covers efforts that fit a few sessions.

Survey behind the adapted skills: [ADR-002](ADR-002-skills-survey-mattpocock-cursor-pstack.md).
