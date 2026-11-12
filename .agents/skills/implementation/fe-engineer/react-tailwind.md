# React 19 + Tailwind CSS v4

Patterns, conventions, and best practices for building modern React applications with Tailwind CSS v4.

## Tailwind CSS v4 — CSS-First Configuration

Tailwind v4 uses CSS-first configuration with the `@theme` directive instead of `tailwind.config.js`.

### Setup

```css
/* app.css */
@import "tailwindcss";

@theme {
  /* Colors */
  --color-primary: oklch(0.6 0.2 260);
  --color-primary-light: oklch(0.8 0.15 260);
  --color-primary-dark: oklch(0.4 0.25 260);
  --color-secondary: oklch(0.7 0.15 150);
  --color-background: oklch(0.98 0 0);
  --color-surface: oklch(1 0 0);
  --color-text: oklch(0.2 0 0);
  --color-text-muted: oklch(0.5 0 0);
  --color-border: oklch(0.9 0 0);
  --color-error: oklch(0.6 0.25 25);
  --color-success: oklch(0.6 0.2 145);

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  /* Typography */
  --font-sans: "Inter", "system-ui", sans-serif;
  --font-mono: "JetBrains Mono", "Fira Code", monospace;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;

  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px oklch(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px oklch(0 0 0 / 0.07);
  --shadow-lg: 0 10px 15px oklch(0 0 0 / 0.1);

  /* Breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;

  /* Animations */
  --animate-fade-in: fade-in 0.2s ease-out;
  --animate-slide-up: slide-up 0.3s ease-out;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Dark mode variant */
@variant dark (&:where(.dark, .dark *));
```

### Key Differences from v3

- **No tailwind.config.js** — use `@theme` in CSS
- **CSS-native** — `@import "tailwindcss"` replaces `@tailwind` directives
- **OKLCH colors** — perceptually uniform color space (recommended)
- **No `@apply` needed** — compose in JSX with utility classes, use `@apply` sparingly
- **Automatic content detection** — no `content` array config needed
- **Dark mode** — use `@variant dark` for custom dark mode strategy

## React 19 Patterns

### Component Template

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  children,
  onClick,
}: ButtonProps) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={cn(
        'inline-flex items-center justify-center font-medium rounded-md transition-colors',
        'focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary',
        {
          'bg-primary text-white hover:bg-primary-dark': variant === 'primary',
          'bg-surface text-text border border-border hover:bg-background': variant === 'secondary',
          'text-text hover:bg-background': variant === 'ghost',
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
          'opacity-50 cursor-not-allowed': disabled,
        }
      )}
    >
      {children}
    </button>
  );
}
```

### Class Name Utility (cn)

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### use() Hook — Promise Handling

```typescript
import { use, Suspense } from 'react';

function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);
  return <h2 className="text-xl font-semibold text-text">{user.name}</h2>;
}

export function UserPage({ userId }: { userId: string }) {
  const userPromise = fetchUser(userId);
  return (
    <Suspense fallback={<div className="animate-pulse bg-surface rounded-md h-8 w-48" />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}
```

### useOptimistic — Optimistic Updates

```typescript
import { useOptimistic, useTransition } from 'react';

export function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimistic] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, newTodo]
  );
  const [, startTransition] = useTransition();

  const handleAdd = (text: string) => {
    const tempTodo: Todo = { id: `temp-${Date.now()}`, text, completed: false };
    addOptimistic(tempTodo);
    startTransition(async () => {
      const saved = await createTodo(text);
      // React will reconcile when transition completes
    });
  };

  return (
    <ul className="space-y-2">
      {optimisticTodos.map((todo) => (
        <li key={todo.id} className="flex items-center gap-2 p-2 rounded-md bg-surface">
          {todo.text}
        </li>
      ))}
    </ul>
  );
}
```

### Form with Actions + useActionState

```typescript
import { useActionState } from 'react';
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button
      type="submit"
      disabled={pending}
      className="px-4 py-2 bg-primary text-white rounded-md disabled:opacity-50"
    >
      {pending ? 'Saving...' : 'Save'}
    </button>
  );
}

export function ContactForm() {
  const [state, formAction] = useActionState(submitContact, { error: null, success: false });

  return (
    <form action={formAction} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-text">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          required
          className="mt-1 w-full rounded-md border border-border px-3 py-2 text-text focus:border-primary focus:ring-1 focus:ring-primary"
        />
      </div>
      {state.error && <p className="text-error text-sm">{state.error}</p>}
      {state.success && <p className="text-success text-sm">Message sent!</p>}
      <SubmitButton />
    </form>
  );
}
```

## Zustand Store Patterns

```typescript
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        isAuthenticated: false,
        login: async (credentials) => {
          const user = await api.login(credentials);
          set({ user, isAuthenticated: true });
        },
        logout: () => set({ user: null, isAuthenticated: false }),
      }),
      { name: "auth-store" },
    ),
  ),
);

// Selector pattern — prevents unnecessary re-renders
export const useUser = () => useAuthStore((s) => s.user);
export const useIsAuthenticated = () => useAuthStore((s) => s.isAuthenticated);
```

## React Query Patterns

```typescript
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

// Query keys factory
export const itemKeys = {
  all: ["items"] as const,
  lists: () => [...itemKeys.all, "list"] as const,
  list: (filters: Filters) => [...itemKeys.lists(), filters] as const,
  details: () => [...itemKeys.all, "detail"] as const,
  detail: (id: string) => [...itemKeys.details(), id] as const,
};

// Query hook
export function useItems(filters: Filters) {
  return useQuery({
    queryKey: itemKeys.list(filters),
    queryFn: () => fetchItems(filters),
    staleTime: 5 * 60 * 1000,
  });
}

// Mutation with optimistic update
export function useCreateItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createItem,
    onMutate: async (newItem) => {
      await queryClient.cancelQueries({ queryKey: itemKeys.lists() });
      const previous = queryClient.getQueryData(itemKeys.lists());
      queryClient.setQueryData(itemKeys.lists(), (old: Item[]) => [
        ...old,
        { ...newItem, id: "temp" },
      ]);
      return { previous };
    },
    onError: (_err, _item, context) => {
      queryClient.setQueryData(itemKeys.lists(), context?.previous);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: itemKeys.lists() });
    },
  });
}
```

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
