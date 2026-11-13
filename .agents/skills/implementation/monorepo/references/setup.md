# Step-by-step setup

Part of the `monorepo` skill.

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
