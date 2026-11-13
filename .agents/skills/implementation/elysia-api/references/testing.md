# Testing with the Bun test runner

Part of the `elysia-api` skill.

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
