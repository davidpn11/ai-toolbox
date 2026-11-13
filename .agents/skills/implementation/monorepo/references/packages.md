# Internal packages

Part of the `monorepo` skill.

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
