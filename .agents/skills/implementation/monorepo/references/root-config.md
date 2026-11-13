# Root `package.json` and `turbo.json`

Part of the `monorepo` skill.

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
