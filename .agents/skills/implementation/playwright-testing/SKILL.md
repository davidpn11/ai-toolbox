---
name: playwright-testing
description: "Playwright e2e testing patterns — project setup, Page Object Model, test fixtures, common assertions, accessibility testing with @axe-core/playwright, visual regression, CI configuration, and debugging. Use when writing or fixing Playwright tests."
---

# Playwright E2E Testing

Patterns and conventions for writing reliable end-to-end tests with Playwright.

## Common Assertions

```typescript
// Visibility
await expect(locator).toBeVisible();
await expect(locator).toBeHidden();

// Text content
await expect(locator).toHaveText("exact text");
await expect(locator).toContainText("partial");

// Attributes
await expect(locator).toHaveAttribute("aria-expanded", "true");
await expect(locator).toHaveClass(/active/);

// URL and title
await expect(page).toHaveURL("/dashboard");
await expect(page).toHaveTitle(/Dashboard/);

// Count
await expect(page.getByRole("listitem")).toHaveCount(5);

// Input values
await expect(input).toHaveValue("expected value");
await expect(input).toBeEmpty();

// State
await expect(button).toBeEnabled();
await expect(button).toBeDisabled();
await expect(checkbox).toBeChecked();
```

## Locator Priority (Best to Worst)

1. `page.getByRole()` — accessible role + name
2. `page.getByLabel()` — form inputs
3. `page.getByPlaceholder()` — inputs without labels
4. `page.getByText()` — visible text
5. `page.getByAltText()` — images
6. `page.getByTitle()` — title attribute
7. `page.getByTestId()` — last resort

## Debugging Tips

```bash
# Run with headed browser
npx playwright test --headed

# Run with UI mode (interactive)
npx playwright test --ui

# Debug single test
npx playwright test --debug tests/auth.spec.ts

# Generate test from browser interaction
npx playwright codegen http://localhost:3000

# View last HTML report
npx playwright show-report
```

## References

The sections above are what most tasks need. The detail lives in `references/`, next to this file. Read only the file the task needs. If you don't know this skill's folder, find it with a glob for `**/playwright-testing/references/*.md` under `.claude/skills`, `.agents/skills`, or `~/.claude/skills`.

| File | Covers | Read it when |
|------|--------|--------------|
| [references/setup.md](references/setup.md) | Project setup and CI | configuring Playwright or its GitHub Actions job |
| [references/page-objects.md](references/page-objects.md) | Page objects and fixtures | writing or changing page objects or custom fixtures |
| [references/examples.md](references/examples.md) | Test and accessibility examples | writing a new spec or an axe accessibility check |
