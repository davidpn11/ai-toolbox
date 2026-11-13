# Bun SQLite

Part of the `elysia-api` skill.

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
