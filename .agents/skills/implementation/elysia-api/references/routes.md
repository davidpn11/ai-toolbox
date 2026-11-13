# Routes, plugins, lifecycle hooks

Part of the `elysia-api` skill.

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
