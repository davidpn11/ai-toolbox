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

## 2. Root `package.json`

```jsonc
{
  "name": "my-monorepo",
  "private": true,
  "packageManager": "bun@1.3.0",
  "engines": { "node": ">=24" },
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "check-types": "turbo run check-types",
  },
  "devDependencies": {
    "prettier": "^3.6.2",
    "turbo": "^2.6.0",
    "typescript": "5.9.2",
    "@types/node": "^24.10.0",
  },
}
```

**Key points:**

- `"private": true` — prevents accidental publishing of the root.
- `"workspaces"` — tells Bun to treat `apps/*` and `packages/*` as workspace members.
- `"packageManager"` — pins the Bun version for reproducibility.
- All scripts delegate to `turbo run <task>` so Turborepo handles caching, parallelism, and dependency ordering.
- `turbo` and `typescript` live at the root as shared dev dependencies.
- If multiple apps share the same runtime dependency, you can optionally hoist it into root `dependencies`.

---

## 3. Root `turbo.json`

```jsonc
{
  "$schema": "https://turborepo.com/schema.json",
  "ui": "tui",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["$TURBO_DEFAULT$", ".env*"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"],
    },
    "lint": {
      "dependsOn": ["^lint"],
    },
    "check-types": {
      "dependsOn": ["^check-types"],
    },
    "dev": {
      "cache": false,
      "persistent": true,
    },
  },
}
```

**Key points:**

- `"dependsOn": ["^build"]` — the `^` prefix means "run this task in all workspace dependencies first" (topological ordering). This ensures internal packages build before the apps that consume them.
- `"inputs"` — files that Turbo watches for cache invalidation. `$TURBO_DEFAULT$` includes all tracked files.
- `"outputs"` — directories Turbo caches after a successful build. Adjust per framework (`dist/`, `.next/`, `build/`, etc.).
- `"dev"` is `persistent: true` (long-running process) and `cache: false` (never cached).

---

## 4. Internal Packages

All internal packages follow the same pattern:

- Scoped name: `@my-scope/<package-name>`
- `"private": true` — they are not published
- No build step — they export raw config files (JSON or JS)
- Consumed by apps via the `workspace:*` protocol

### 4a. `@my-scope/typescript-config`

Provides shareable `tsconfig.json` presets that apps extend.

```
packages/typescript-config/
├── package.json
├── base.json
├── react-app.json
└── nextjs.json
```

**`package.json`:**

```jsonc
{
  "name": "@my-scope/typescript-config",
  "version": "0.0.0",
  "private": true,
}
```

No `exports` field needed — consumers reference the JSON files directly by path.

**`base.json`** — the foundation all presets extend:

```jsonc
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "esModuleInterop": true,
    "skipLibCheck": true,
    "target": "es2022",
    "allowJs": true,
    "resolveJsonModule": true,
    "moduleDetection": "force",
    "isolatedModules": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "lib": ["dom", "dom.iterable", "ES2022"],
    "noEmit": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "preserve",
    "incremental": true,
    "baseUrl": ".",
    "paths": { "~/*": ["./src/*"] },
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist/", "public/", "coverage/"],
}
```

**`react-app.json`** — for Vite + React apps:

```jsonc
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./base.json",
  "compilerOptions": {
    "jsx": "react-jsx",
    "incremental": false,
  },
}
```

**`nextjs.json`** — for Next.js apps:

```jsonc
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./base.json",
  "compilerOptions": {
    "plugins": [{ "name": "next" }],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "allowJs": true,
    "jsx": "preserve",
    "noEmit": true,
  },
}
```

---

### 4b. `@my-scope/biome-config`

Provides shareable [Biome](https://biomejs.dev/) linter and formatter presets.

```
packages/biome-config/
├── package.json
├── base.json
├── react-internal.json
└── next.json
```

**`package.json`:**

```jsonc
{
  "name": "@my-scope/biome-config",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "exports": {
    "./base": "./base.json",
    "./next-js": "./next.json",
    "./react-internal": "./react-internal.json",
  },
  "devDependencies": {
    "@biomejs/biome": "2.0.6",
  },
  "peerDependencies": {
    "@biomejs/biome": ">=1.9.0",
  },
}
```

Uses `exports` so consumers can write `"extends": ["@my-scope/biome-config/base"]` in their `biome.json`.

**`base.json`** (core formatting + linting rules):

```jsonc
{
  "$schema": "https://biomejs.dev/schemas/2.0.6/schema.json",
  "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineEnding": "lf",
    "lineWidth": 80,
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": {
        "noExtraBooleanCast": "error",
        "noUselessCatch": "error",
        "noUselessTypeConstraint": "error",
      },
      "correctness": {
        "noConstAssign": "error",
        "noConstantCondition": "error",
        "noGlobalObjectCalls": "error",
        "noPrecisionLoss": "error",
      },
    },
  },
}
```

**`react-internal.json`** — extends base with React-specific rules:

```jsonc
{
  "$schema": "https://biomejs.dev/schemas/2.0.6/schema.json",
  "extends": ["./base.json"],
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "a11y": { "recommended": true },
      "correctness": {
        "useExhaustiveDependencies": "warn",
        "useHookAtTopLevel": "error",
        "noUnusedImports": "error",
      },
      "style": {
        "useImportType": "error",
      },
      "suspicious": {
        "noExplicitAny": "warn",
      },
    },
  },
}
```

---

### 4c. `@my-scope/eslint-config`

Provides shareable ESLint **flat config** presets (for workspaces that use ESLint instead of or alongside Biome).

```
packages/eslint-config/
├── package.json
├── base.js
├── react-internal.js
└── next.js
```

**`package.json`:**

```jsonc
{
  "name": "@my-scope/eslint-config",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "exports": {
    "./base": "./base.js",
    "./next-js": "./next.js",
    "./react-internal": "./react-internal.js",
  },
  "devDependencies": {
    "@eslint/js": "^9.34.0",
    "@next/eslint-plugin-next": "^15.5.0",
    "eslint": "^9.38.0",
    "eslint-config-prettier": "^10.1.1",
    "eslint-plugin-only-warn": "^1.1.0",
    "eslint-plugin-react": "^7.37.5",
    "eslint-plugin-react-hooks": "^5.2.0",
    "eslint-plugin-turbo": "^2.5.0",
    "globals": "^16.3.0",
    "typescript": "^5.9.2",
    "typescript-eslint": "^8.40.0",
  },
}
```

**`base.js`:**

```js
import js from "@eslint/js";
import eslintConfigPrettier from "eslint-config-prettier";
import turboPlugin from "eslint-plugin-turbo";
import tseslint from "typescript-eslint";
import onlyWarn from "eslint-plugin-only-warn";

export const config = [
  js.configs.recommended,
  eslintConfigPrettier,
  ...tseslint.configs.recommended,
  {
    plugins: { turbo: turboPlugin },
    rules: { "turbo/no-undeclared-env-vars": "warn" },
  },
  { plugins: { onlyWarn } },
  { ignores: ["dist/**"] },
];
```

**`react-internal.js`** — extends base, adds React + React Hooks rules.
**`next.js`** — extends base, adds Next.js plugin, ignores `.next/`, `out/`, `build/`.

---

## 5. Applications

### 5a. Frontend — Vite + React SPA

```
apps/web-app/
├── package.json
├── tsconfig.json
├── biome.json
├── vite.config.ts
├── postcss.config.js
├── index.html
└── src/
```

**`package.json`:**

```jsonc
{
  "name": "@my-scope/web-app",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "biome lint .",
    "lint:fix": "biome lint --write .",
    "format": "biome format .",
    "format:fix": "biome format --write .",
    "check": "biome check .",
    "check:fix": "biome check --write --unsafe .",
    "preview": "vite preview",
    "check-types": "tsc --noEmit",
  },
  "dependencies": {
    "react": "19.2.0",
    "react-dom": "19.2.0",
    "react-router-dom": "^6.28.0",
    "tailwindcss": "4.1.13",
    "zustand": "5.0.8",
    "zod": "4.1.13",
  },
  "devDependencies": {
    "@my-scope/biome-config": "workspace:*",
    "@my-scope/typescript-config": "workspace:*",
    "@biomejs/biome": "2.0.6",
    "@tailwindcss/postcss": "4.1.13",
    "@tailwindcss/vite": "4.1.13",
    "@types/react": "19.2.0",
    "@types/react-dom": "19.2.0",
    "@vitejs/plugin-react": "^4.3.3",
    "typescript": "^5.6.3",
    "vite": "^5.4.10",
  },
}
```

**`tsconfig.json`** — extends the shared preset:

```jsonc
{
  "extends": "@my-scope/typescript-config/react-app.json",
  "include": ["src"],
  "exclude": ["node_modules", "dist", "build"],
}
```

**`biome.json`** — extends the shared preset:

```jsonc
{
  "extends": ["@my-scope/biome-config/base"],
}
```

**`vite.config.ts`:**

```ts
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { port: 3000, open: true },
  build: { outDir: "dist", sourcemap: true },
});
```

**`postcss.config.js`:**

```js
export default {
  plugins: { "@tailwindcss/postcss": {} },
};
```

---

### 5b. Backend — Bun + Elysia API

```
apps/api-service/
├── package.json
├── tsconfig.json
└── src/
    ├── index.ts
    └── routes.ts
```

**`package.json`:**

```jsonc
{
  "name": "@my-scope/api-service",
  "version": "1.0.0",
  "module": "src/index.js",
  "scripts": {
    "dev": "bun run --watch src/index.ts",
  },
  "dependencies": {
    "elysia": "1.4.18",
  },
  "devDependencies": {
    "bun-types": "1.3.3",
  },
}
```

**`tsconfig.json`** — standalone (Bun uses Node-style resolution, different from Bundler):

```jsonc
{
  "compilerOptions": {
    "target": "ES2021",
    "module": "ES2022",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "skipLibCheck": true,
  },
}
```

> **Note:** The backend intentionally does NOT extend the shared TypeScript config because it uses `"moduleResolution": "node"` instead of `"Bundler"`. If your backend can use Bundler resolution, you can extend the shared config instead.

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

## 7. Step-by-Step Setup

```bash
# 1. Create the monorepo root
mkdir my-monorepo && cd my-monorepo
bun init

# 2. Install Turborepo
bun add -D turbo typescript prettier @types/node

# 3. Create workspace directories
mkdir -p apps/web-app/src apps/api-service/src
mkdir -p packages/typescript-config packages/biome-config packages/eslint-config

# 4. Create root turbo.json (see Section 3)

# 5. Create each package's package.json + config files (see Section 4)

# 6. Create each app's package.json, tsconfig.json, etc. (see Section 5)
#    — Use "workspace:*" to reference internal packages

# 7. Install everything from the root
bun install

# 8. Run all apps in dev mode
bun run dev
```

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
