---
name: bun-api
description: "Bun.js API development patterns — Bun.serve() HTTP server, Hono routing, middleware, Zod validation, Bun SQLite, Bun test runner, WebSocket support, and TypeScript API conventions. Use when building backend APIs with Bun.js."
---

# Bun.js API Development

Patterns and conventions for building high-performance APIs with Bun.js and TypeScript.

## Project Setup

```bash
bun init
bun add hono @hono/zod-validator zod
bun add -d @types/bun
```

### Project Structure

```
src/
├── index.ts            # Entry point — Bun.serve()
├── app.ts              # Hono app with all routes mounted
├── routes/
│   ├── items.ts        # /api/items routes
│   └── auth.ts         # /api/auth routes
├── middleware/
│   ├── auth.ts         # Authentication middleware
│   └── logger.ts       # Request logging
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

## Bun.serve() Entry Point

```typescript
// src/index.ts
import { app } from "./app";

const server = Bun.serve({
  port: Number(Bun.env.PORT) || 3000,
  fetch: app.fetch,
  // Optional: WebSocket upgrade
  websocket: {
    message(ws, message) {
      /* handle */
    },
    open(ws) {
      /* handle */
    },
    close(ws) {
      /* handle */
    },
  },
});

console.log(`Server running at http://localhost:${server.port}`);
```

## Hono App Setup

```typescript
// src/app.ts
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { secureHeaders } from "hono/secure-headers";
import { itemRoutes } from "./routes/items";
import { authRoutes } from "./routes/auth";
import { errorHandler } from "./middleware/error-handler";

export const app = new Hono()
  .use("*", logger())
  .use("*", cors({ origin: Bun.env.CORS_ORIGIN || "*" }))
  .use("*", secureHeaders())
  .route("/api/items", itemRoutes)
  .route("/api/auth", authRoutes)
  .onError(errorHandler);

// Export type for RPC client (Hono Client)
export type AppType = typeof app;
```

## Route Definition

```typescript
// src/routes/items.ts
import { Hono } from "hono";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";
import { requireAuth } from "../middleware/auth";
import { ItemService } from "../services/item.service";

const createItemSchema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().max(1000).optional(),
  price: z.number().positive(),
});

const querySchema = z.object({
  limit: z.coerce.number().int().min(1).max(100).default(20),
  offset: z.coerce.number().int().min(0).default(0),
  search: z.string().optional(),
});

export const itemRoutes = new Hono()
  // Public: list items
  .get("/", zValidator("query", querySchema), async (c) => {
    const query = c.req.valid("query");
    const items = await ItemService.list(query);
    return c.json(items);
  })

  // Public: get single item
  .get("/:id", async (c) => {
    const id = c.req.param("id");
    const item = await ItemService.getById(id);
    if (!item) return c.json({ error: "Item not found" }, 404);
    return c.json(item);
  })

  // Protected: create item
  .post("/", requireAuth(), zValidator("json", createItemSchema), async (c) => {
    const data = c.req.valid("json");
    const user = c.get("user");
    const item = await ItemService.create({ ...data, createdBy: user.id });
    return c.json(item, 201);
  })

  // Protected: delete item
  .delete("/:id", requireAuth(), async (c) => {
    const id = c.req.param("id");
    await ItemService.delete(id);
    return c.body(null, 204);
  });
```

## Middleware

### Authentication

```typescript
// src/middleware/auth.ts
import type { MiddlewareHandler } from "hono";
import { HTTPException } from "hono/http-exception";

interface AuthUser {
  id: string;
  email: string;
  role: string;
}

// Extend Hono context
declare module "hono" {
  interface ContextVariableMap {
    user: AuthUser;
  }
}

export function requireAuth(): MiddlewareHandler {
  return async (c, next) => {
    const header = c.req.header("Authorization");
    if (!header?.startsWith("Bearer ")) {
      throw new HTTPException(401, { message: "Missing authorization header" });
    }
    const token = header.slice(7);
    const user = await verifyToken(token);
    if (!user) {
      throw new HTTPException(401, { message: "Invalid or expired token" });
    }
    c.set("user", user);
    await next();
  };
}

export function requireRole(role: string): MiddlewareHandler {
  return async (c, next) => {
    const user = c.get("user");
    if (user.role !== role) {
      throw new HTTPException(403, { message: "Insufficient permissions" });
    }
    await next();
  };
}
```

### Error Handler

```typescript
// src/middleware/error-handler.ts
import type { ErrorHandler } from "hono";
import { HTTPException } from "hono/http-exception";
import { ZodError } from "zod";

interface ApiError {
  code: string;
  message: string;
  details?: unknown;
}

export const errorHandler: ErrorHandler = (err, c) => {
  if (err instanceof HTTPException) {
    return c.json<ApiError>(
      { code: "HTTP_ERROR", message: err.message },
      err.status,
    );
  }

  if (err instanceof ZodError) {
    return c.json<ApiError>(
      {
        code: "VALIDATION_ERROR",
        message: "Invalid input",
        details: err.flatten(),
      },
      400,
    );
  }

  console.error("Unhandled error:", err);
  return c.json<ApiError>(
    { code: "INTERNAL_ERROR", message: "Internal server error" },
    500,
  );
};
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
import { z } from "zod";

const envSchema = z.object({
  PORT: z.coerce.number().default(3000),
  DB_PATH: z.string().default("data/app.db"),
  JWT_SECRET: z.string().min(32),
  CORS_ORIGIN: z.string().default("*"),
  NODE_ENV: z
    .enum(["development", "production", "test"])
    .default("development"),
});

export const env = envSchema.parse(Bun.env);
```

## Testing with Bun Test Runner

```typescript
// src/routes/__tests__/items.test.ts
import { describe, expect, it, beforeAll, afterAll } from "bun:test";
import { app } from "../../app";

describe("GET /api/items", () => {
  it("returns a list of items", async () => {
    const res = await app.request("/api/items");
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(Array.isArray(body)).toBe(true);
  });

  it("supports pagination", async () => {
    const res = await app.request("/api/items?limit=5&offset=0");
    expect(res.status).toBe(200);
  });

  it("rejects invalid limit", async () => {
    const res = await app.request("/api/items?limit=-1");
    expect(res.status).toBe(400);
  });
});

describe("POST /api/items", () => {
  it("requires authentication", async () => {
    const res = await app.request("/api/items", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: "Test", price: 10 }),
    });
    expect(res.status).toBe(401);
  });

  it("validates input", async () => {
    const res = await app.request("/api/items", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer valid-test-token",
      },
      body: JSON.stringify({ name: "", price: -5 }),
    });
    expect(res.status).toBe(400);
  });
});
```

## WebSocket Support

```typescript
// src/routes/ws.ts
import type { ServerWebSocket } from "bun";

interface WsData {
  userId: string;
  room: string;
}

export const websocket = {
  message(ws: ServerWebSocket<WsData>, message: string | Buffer) {
    const data = JSON.parse(message.toString());
    // Broadcast to same room
    ws.publish(
      ws.data.room,
      JSON.stringify({
        userId: ws.data.userId,
        ...data,
      }),
    );
  },
  open(ws: ServerWebSocket<WsData>) {
    ws.subscribe(ws.data.room);
  },
  close(ws: ServerWebSocket<WsData>) {
    ws.unsubscribe(ws.data.room);
  },
};
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

1. **Validate ALL input at API boundaries** with Zod
2. **Parameterized queries only** — never interpolate user input
3. **Environment variables for secrets** — validated at startup
4. **Error handler catches all** — clients never see stack traces
5. **TypeScript strict** — no `any`, explicit return types
6. **Test with `app.request()`** — no need for a running server
