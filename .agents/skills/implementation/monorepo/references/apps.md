# Applications

Part of the `monorepo` skill.

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
