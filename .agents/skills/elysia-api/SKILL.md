---
name: elysia-api
description: "Elysia + Bun API development patterns — Elysia routing, type-safe plugins, request validation with TypeBox, Elysia Eden treaty client, lifecycle hooks, Bun SQLite, Bun test runner, WebSocket support, and TypeScript API conventions."
---

# Elysia API Development

Patterns and conventions for building high-performance, end-to-end type-safe APIs with Elysia on the Bun runtime.

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

## Route Definition

```typescript
// src/routes/items.ts
import { Elysia, t } from "elysia";
import { authPlugin } from "../plugins/auth";
import { ItemService } from "../services/item.service";

export const itemRoutes = new Elysia({ prefix: "/api/items" })
  // Public: list items
  .get(
    "/",
    async ({ query }) => {
      return ItemService.list(query);
    },
    {
      query: t.Object({
        limit: t.Optional(t.Number({ minimum: 1, maximum: 100, default: 20 })),
        offset: t.Optional(t.Number({ minimum: 0, default: 0 })),
        search: t.Optional(t.String()),
      }),
    },
  )

  // Public: get single item
  .get(
    "/:id",
    async ({ params, error }) => {
      const item = await ItemService.getById(params.id);
      if (!item) return error(404, { message: "Item not found" });
      return item;
    },
    {
      params: t.Object({ id: t.String() }),
    },
  )

  // Protected: create item (guard applies auth to all routes below)
  .use(authPlugin)
  .post(
    "/",
    async ({ body, store }) => {
      const item = await ItemService.create({
        ...body,
        createdBy: store.user.id,
      });
      return item;
    },
    {
      body: t.Object({
        name: t.String({ minLength: 1, maxLength: 255 }),
        description: t.Optional(t.String({ maxLength: 1000 })),
        price: t.Number({ minimum: 0 }),
      }),
    },
  )

  // Protected: delete item
  .delete(
    "/:id",
    async ({ params, set }) => {
      await ItemService.delete(params.id);
      set.status = 204;
    },
    {
      params: t.Object({ id: t.String() }),
    },
  );
```

## Plugins

### Authentication Plugin (derive pattern)

```typescript
// src/plugins/auth.ts
import { Elysia } from "elysia";
import { bearer } from "@elysiajs/bearer";

interface AuthUser {
  id: string;
  email: string;
  role: string;
}

export const authPlugin = new Elysia({ name: "auth" })
  .use(bearer())
  .derive(async ({ bearer, error }) => {
    if (!bearer) return error(401, { message: "Missing authorization token" });

    const user = await verifyToken(bearer);
    if (!user) return error(401, { message: "Invalid or expired token" });

    return { user: user as AuthUser };
  });

export const requireRole = (role: string) =>
  new Elysia({ name: `role:${role}` })
    .use(authPlugin)
    .derive(({ user, error }) => {
      if (user.role !== role)
        return error(403, { message: "Insufficient permissions" });
      return {};
    });
```

### Logging Plugin (onRequest lifecycle)

```typescript
// src/plugins/logger.ts
import { Elysia } from "elysia";

export const loggerPlugin = new Elysia({ name: "logger" })
  .onRequest(({ request }) => {
    console.log(`→ ${request.method} ${new URL(request.url).pathname}`);
  })
  .onAfterResponse(({ request, set }) => {
    console.log(
      `← ${request.method} ${new URL(request.url).pathname} ${set.status}`,
    );
  });
```

## Elysia Lifecycle Hooks

```
onRequest → onParse → onTransform → onBeforeHandle → handler → onAfterHandle → onAfterResponse
                                                                       ↘ onError (if thrown)
```

- **`onRequest`** — earliest hook, before parsing (logging, rate limiting)
- **`onBeforeHandle`** — after validation, before handler (auth checks)
- **`derive`** — inject values into handler context (user, db, etc.)
- **`onAfterHandle`** — modify response before sending (headers, transforms)
- **`onError`** — catch errors and return structured responses

## Eden Treaty Client (End-to-End Type Safety)

```typescript
// client-side or another service
import { treaty } from "@elysiajs/eden";
import type { App } from "../api/app";

const api = treaty<App>("http://localhost:3000");

// Fully typed — params, body, and response inferred from the server
const { data, error } = await api.api.items.post({
  name: "New Item",
  price: 29.99,
});

// data is typed as the return type of the POST handler
// error is typed as the error shape from onError
```

## Bun SQLite

```typescript
// src/db/index.ts
import { Database } from "bun:sqlite";

const DB_PATH = Bun.env.DB_PATH || "data/app.db";

export const db = new Database(DB_PATH, { create: true });
db.exec("PRAGMA journal_mode = WAL");
db.exec("PRAGMA foreign_keys = ON");

// Migration
db.exec(`
  CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    created_by TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
  )
`);

// Prepared statements (parameterized — prevents SQL injection)
export const queries = {
  listItems: db.prepare<
    { id: string; name: string; price: number },
    [number, number]
  >(
    "SELECT id, name, price FROM items ORDER BY created_at DESC LIMIT ? OFFSET ?",
  ),
  getItem: db.prepare<
    { id: string; name: string; description: string | null; price: number },
    [string]
  >("SELECT * FROM items WHERE id = ?"),
  createItem: db.prepare(
    "INSERT INTO items (name, description, price, created_by) VALUES ($name, $description, $price, $createdBy) RETURNING *",
  ),
  deleteItem: db.prepare("DELETE FROM items WHERE id = ?"),
};
```

## Environment Variables

```typescript
// src/lib/env.ts
import { t } from "elysia";

// Using TypeBox (comes with Elysia) for env validation
import { Value } from "@sinclair/typebox/value";

const EnvSchema = t.Object({
  PORT: t.Number({ default: 3000 }),
  DB_PATH: t.String({ default: "data/app.db" }),
  JWT_SECRET: t.String({ minLength: 32 }),
  CORS_ORIGIN: t.String({ default: "*" }),
  NODE_ENV: t.Union(
    [t.Literal("development"), t.Literal("production"), t.Literal("test")],
    { default: "development" },
  ),
});

export const env = Value.Decode(EnvSchema, Bun.env);
```

## Testing with Bun Test Runner

```typescript
// src/routes/__tests__/items.test.ts
import { describe, expect, it } from "bun:test";
import { app } from "../../app";

describe("GET /api/items", () => {
  it("returns a list of items", async () => {
    const res = await app.handle(new Request("http://localhost/api/items"));
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(Array.isArray(body)).toBe(true);
  });

  it("supports pagination", async () => {
    const res = await app.handle(
      new Request("http://localhost/api/items?limit=5&offset=0"),
    );
    expect(res.status).toBe(200);
  });

  it("rejects invalid limit", async () => {
    const res = await app.handle(
      new Request("http://localhost/api/items?limit=-1"),
    );
    expect(res.status).toBe(400);
  });
});

describe("POST /api/items", () => {
  it("requires authentication", async () => {
    const res = await app.handle(
      new Request("http://localhost/api/items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: "Test", price: 10 }),
      }),
    );
    expect(res.status).toBe(401);
  });

  it("validates input", async () => {
    const res = await app.handle(
      new Request("http://localhost/api/items", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer valid-test-token",
        },
        body: JSON.stringify({ name: "", price: -5 }),
      }),
    );
    expect(res.status).toBe(400);
  });
});
```

## WebSocket Support

```typescript
// src/routes/ws.ts
import { Elysia, t } from "elysia";

export const wsRoutes = new Elysia().ws("/ws", {
  body: t.Object({
    type: t.String(),
    payload: t.Unknown(),
  }),
  query: t.Object({
    room: t.String(),
  }),
  open(ws) {
    ws.subscribe(ws.data.query.room);
  },
  message(ws, { type, payload }) {
    ws.publish(
      ws.data.query.room,
      JSON.stringify({ type, payload, from: ws.id }),
    );
  },
  close(ws) {
    ws.unsubscribe(ws.data.query.room);
  },
});
```

## File I/O with Bun

```typescript
// Read file
const content = await Bun.file("data/config.json").json();

// Write file
await Bun.write("data/output.json", JSON.stringify(data, null, 2));

// Check existence
const exists = await Bun.file("data/config.json").exists();

// Hash password
const hash = await Bun.password.hash(password);
const isValid = await Bun.password.verify(password, hash);
```

## Key Conventions

1. **Validate ALL input with TypeBox schemas** — Elysia validates automatically via route schemas
2. **Parameterized queries only** — never interpolate user input into SQL
3. **Environment variables for secrets** — validated at startup
4. **onError catches all** — clients never see stack traces
5. **TypeScript strict** — no `any`, end-to-end type safety via Eden treaty
6. **Test with `app.handle()`** — no need for a running server
7. **Use plugins for cross-cutting concerns** — auth, logging, rate limiting as composable Elysia plugins
8. **Name plugins** — always pass `{ name: "..." }` to `new Elysia()` for deduplication
