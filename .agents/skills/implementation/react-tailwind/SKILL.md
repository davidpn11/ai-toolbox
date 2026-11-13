---
name: react-tailwind
description: "React 19 + Tailwind CSS v4 patterns and conventions. Use when building React components with Tailwind styling, configuring Tailwind v4 themes, using Zustand stores, React Query data fetching, Next.js App Router conventions, or Vite setup."
---

# React 19 + Tailwind CSS v4

Patterns, conventions, and best practices for building modern React applications with Tailwind CSS v4.

## Next.js App Router Conventions

```
app/
├── layout.tsx          # Root layout (wraps all pages)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI (automatic Suspense boundary)
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── (auth)/             # Route group (no URL segment)
│   ├── login/page.tsx
│   └── register/page.tsx
├── dashboard/
│   ├── layout.tsx      # Dashboard layout
│   └── page.tsx
└── api/
    └── items/
        └── route.ts    # API route handler
```

- **Server Components** by default — add `'use client'` only when needed (hooks, events, browser APIs)
- **Metadata API**: Export `metadata` or `generateMetadata` from pages for SEO
- **Loading states**: `loading.tsx` creates automatic Suspense boundaries
- **Error handling**: `error.tsx` creates automatic error boundaries

## Vite Setup

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: { "@": "/src" },
  },
});
```

## References

The sections above are what most tasks need. The detail lives in `references/`, next to this file. Read only the file the task needs. If you don't know this skill's folder, find it with a glob for `**/react-tailwind/references/*.md` under `.claude/skills`, `.agents/skills`, or `~/.claude/skills`.

| File | Covers | Read it when |
|------|--------|--------------|
| [references/tailwind-v4.md](references/tailwind-v4.md) | Tailwind CSS v4 configuration | theme tokens, `@theme`, dark mode, or Tailwind setup |
| [references/react-19.md](references/react-19.md) | React 19 patterns | components, actions, forms, `use()`, refs, metadata |
| [references/state.md](references/state.md) | Zustand and React Query | client state stores or server-state queries and mutations |
