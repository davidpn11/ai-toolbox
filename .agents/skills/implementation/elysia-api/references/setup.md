# Project setup, entry point, app setup

Part of the `elysia-api` skill.

## Project Setup

```bash
bun init
bun add elysia @elysiajs/cors @elysiajs/bearer
bun add -d @types/bun
```

### Project Structure

```
src/
├── index.ts            # Entry point — Elysia app listen
├── app.ts              # Elysia app with all plugins + routes mounted
├── routes/
│   ├── items.ts        # /api/items routes
│   └── auth.ts         # /api/auth routes
├── plugins/
│   ├── auth.ts         # Authentication plugin (derive)
│   └── logger.ts       # Request logging plugin
├── services/
│   ├── item.service.ts # Business logic
│   └── auth.service.ts
├── db/
│   ├── index.ts        # Database connection
│   └── schema.ts       # Type definitions / migrations
├── lib/
│   ├── errors.ts       # Error types
│   └── env.ts          # Environment variable validation
└── types/
    └── index.ts        # Shared types
```

## Entry Point

```typescript
// src/index.ts
import { app } from "./app";

app.listen(Number(Bun.env.PORT) || 3000, ({ hostname, port }) => {
  console.log(`Server running at http://${hostname}:${port}`);
});
```

## Elysia App Setup

```typescript
// src/app.ts
import { Elysia } from "elysia";
import { cors } from "@elysiajs/cors";
import { itemRoutes } from "./routes/items";
import { authRoutes } from "./routes/auth";

export const app = new Elysia()
  .use(cors({ origin: Bun.env.CORS_ORIGIN || "*" }))
  .use(itemRoutes)
  .use(authRoutes)
  .onError(({ code, error, set }) => {
    if (code === "VALIDATION") {
      set.status = 400;
      return { code: "VALIDATION_ERROR", message: error.message };
    }
    if (code === "NOT_FOUND") {
      set.status = 404;
      return { code: "NOT_FOUND", message: "Resource not found" };
    }
    console.error("Unhandled error:", error);
    set.status = 500;
    return { code: "INTERNAL_ERROR", message: "Internal server error" };
  });

// Export type for Eden treaty client
export type App = typeof app;
```
