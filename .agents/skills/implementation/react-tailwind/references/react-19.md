# React 19 patterns

Part of the `react-tailwind` skill.

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
