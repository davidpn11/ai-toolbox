# Eden Treaty, environment, WebSockets, file I/O

Part of the `elysia-api` skill.

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
