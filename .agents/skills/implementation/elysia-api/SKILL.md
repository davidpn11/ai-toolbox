---
name: elysia-api
description: "Elysia + Bun API development patterns — Elysia routing, type-safe plugins, request validation with TypeBox, Elysia Eden treaty client, lifecycle hooks, Bun SQLite, Bun test runner, WebSocket support, and TypeScript API conventions."
---

# Elysia API Development

Patterns and conventions for building high-performance, end-to-end type-safe APIs with Elysia on the Bun runtime.

## Key Conventions

1. **Validate ALL input with TypeBox schemas** — Elysia validates automatically via route schemas
2. **Parameterized queries only** — never interpolate user input into SQL
3. **Environment variables for secrets** — validated at startup
4. **onError catches all** — clients never see stack traces
5. **TypeScript strict** — no `any`, end-to-end type safety via Eden treaty
6. **Test with `app.handle()`** — no need for a running server
7. **Use plugins for cross-cutting concerns** — auth, logging, rate limiting as composable Elysia plugins
8. **Name plugins** — always pass `{ name: "..." }` to `new Elysia()` for deduplication

## References

The sections above are what most tasks need. The detail lives in `references/`, next to this file. Read only the file the task needs. If you don't know this skill's folder, find it with a glob for `**/elysia-api/references/*.md` under `.claude/skills`, `.agents/skills`, or `~/.claude/skills`.

| File | Covers | Read it when |
|------|--------|--------------|
| [references/setup.md](references/setup.md) | Project setup, entry point, app setup | starting a new Elysia service or changing its bootstrap |
| [references/routes.md](references/routes.md) | Routes, plugins, lifecycle hooks | adding or changing endpoints, validation, plugins, or hooks |
| [references/features.md](references/features.md) | Eden Treaty, environment, WebSockets, file I/O | typed clients, config, real-time endpoints, or files |
| [references/sqlite.md](references/sqlite.md) | Bun SQLite | database access with `bun:sqlite` |
| [references/testing.md](references/testing.md) | Testing with the Bun test runner | writing or fixing API tests |
