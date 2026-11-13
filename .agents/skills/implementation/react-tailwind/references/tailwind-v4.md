# Tailwind CSS v4 configuration

Part of the `react-tailwind` skill.

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
