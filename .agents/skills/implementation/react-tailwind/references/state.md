# Zustand and React Query

Part of the `react-tailwind` skill.

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
