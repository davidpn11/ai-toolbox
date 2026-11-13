---
name: monorepo
description: "Turborepo + Bun monorepo blueprint — workspace layout, turbo.json pipelines, shared config packages (TypeScript, Biome, ESLint), Vite+React frontend apps, Bun+Elysia backend apps, workspace:* protocol, and conventions for adding new apps/packages."
---

# Turborepo + Bun Monorepo Blueprint

Generic instructions for scaffolding a monorepo using **Turborepo** for task orchestration and **Bun** as the package manager/runtime.

Replace `@my-scope` with your own npm scope throughout (e.g. `@acme`, `@coolapp`).

---

## 1. Directory Layout

```
root/
├── package.json               ← Root workspace config + Turbo scripts
├── turbo.json                 ← Turborepo pipeline definition
├── bun.lock                   ← Lockfile (auto-generated)
├── apps/
│   ├── web-app/               ← Deployable frontend (Vite + React)
│   └── api-service/           ← Deployable backend (Bun + Elysia)
└── packages/
    ├── typescript-config/     ← Shared tsconfig presets
    ├── biome-config/          ← Shared Biome linter/formatter presets
    └── eslint-config/         ← Shared ESLint flat-config presets
```

- **`apps/`** — Deployable applications. Each has its own `package.json`, build pipeline, and dev server.
- **`packages/`** — Internal shared packages. In this setup they are **config-only** (no runtime code). They are never published to npm — consumed via the `workspace:*` protocol.

---

## 6. Dependency Wiring Diagram

```
Root
├── turbo (orchestration)
├── typescript, prettier, @types/node (shared devDeps)
│
├── apps/web-app
│   ├── devDeps → @my-scope/biome-config       (workspace:*)
│   ├── devDeps → @my-scope/typescript-config   (workspace:*)
│   └── own deps: react, vite, tailwindcss, etc.
│
├── apps/api-service
│   └── own deps: elysia, bun-types
│
├── packages/typescript-config    ← consumed via tsconfig "extends"
├── packages/biome-config         ← consumed via biome.json "extends"
└── packages/eslint-config        ← consumed via ESLint flat config import
```

**How `workspace:*` works:** When app A declares `"@my-scope/biome-config": "workspace:*"`, Bun resolves it to the local `packages/biome-config` directory instead of fetching from npm. This creates a symlink in `node_modules` that points to the local package.

---

## 8. Patterns & Conventions

| Pattern                | Detail                                                                                        |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| **Package manager**    | Bun — used as both runtime (for Elysia backend) and package manager                           |
| **Scope**              | All packages/apps share a single `@my-scope/` prefix                                          |
| **Internal linking**   | `workspace:*` protocol in `package.json` devDependencies                                      |
| **Config sharing**     | TypeScript, Biome, and ESLint configs are internal packages; apps extend them via `"extends"` |
| **Task orchestration** | Turborepo with topological `dependsOn: ["^task"]` for build/lint/check-types                  |
| **Dev mode**           | `turbo run dev` launches all apps concurrently (`persistent: true`, `cache: false`)           |
| **Linting**            | Biome for frontend; ESLint config available for apps that need it                             |
| **Formatting**         | Biome (2-space indent, LF line endings) + Prettier at root                                    |
| **TypeScript**         | Strict mode, `noUncheckedIndexedAccess`, Bundler module resolution, `~/` path alias           |
| **Lockfile**           | Single `bun.lock` at the root — covers all workspaces                                         |

---

## 9. Adding a New App

1. Create `apps/my-new-app/package.json` with name `@my-scope/my-new-app`.
2. Add `"@my-scope/typescript-config": "workspace:*"` and/or `"@my-scope/biome-config": "workspace:*"` to `devDependencies`.
3. Create `tsconfig.json` that extends the appropriate shared preset.
4. Create `biome.json` that extends the appropriate shared preset.
5. Add `dev`, `build`, `lint`, and `check-types` scripts matching the task names in `turbo.json`.
6. Run `bun install` from the root.

## 10. Adding a New Internal Package

1. Create `packages/my-package/package.json` with name `@my-scope/my-package`, set `"private": true`.
2. If the package exports named presets, use the `"exports"` field in `package.json`.
3. Reference it from apps via `"@my-scope/my-package": "workspace:*"`.
4. Run `bun install` from the root.

## References

The sections above are what most tasks need. The detail lives in `references/`, next to this file. Read only the file the task needs. If you don't know this skill's folder, find it with a glob for `**/monorepo/references/*.md` under `.claude/skills`, `.agents/skills`, or `~/.claude/skills`.

| File | Covers | Read it when |
|------|--------|--------------|
| [references/root-config.md](references/root-config.md) | Root `package.json` and `turbo.json` | setting up or changing the root scripts, workspaces, or the Turborepo pipeline |
| [references/packages.md](references/packages.md) | Internal packages | creating or changing a shared package (config, UI, types, utilities) |
| [references/apps.md](references/apps.md) | Applications | creating or changing an app (web, API) and its package wiring |
| [references/setup.md](references/setup.md) | Step-by-step setup | scaffolding a new monorepo from scratch |
