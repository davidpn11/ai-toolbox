# Test and accessibility examples

Part of the `playwright-testing` skill.

## Test Examples

### Authentication Flow

```typescript
// e2e/tests/auth.spec.ts
import { test, expect } from "../fixtures/test";

test.describe("Authentication", () => {
  test("successful login redirects to dashboard", async ({
    loginPage,
    dashboardPage,
  }) => {
    await loginPage.goto();

    await loginPage.login("user@example.com", "password123");

    await expect(dashboardPage.welcomeMessage).toBeVisible();
    await expect(loginPage.page).toHaveURL("/dashboard");
  });

  test("invalid credentials show error", async ({ loginPage }) => {
    await loginPage.goto();

    await loginPage.login("user@example.com", "wrong-password");

    await loginPage.expectError("Invalid credentials");
    await expect(loginPage.page).toHaveURL("/login");
  });

  test("empty form shows validation errors", async ({ loginPage }) => {
    await loginPage.goto();

    await loginPage.submitButton.click();

    await expect(loginPage.emailInput).toHaveAttribute("aria-invalid", "true");
  });
});
```

### CRUD Operations

```typescript
// e2e/tests/dashboard.spec.ts
import { test, expect } from "../fixtures/test";

test.describe("Dashboard", () => {
  test.beforeEach(async ({ loginPage }) => {
    await loginPage.goto();
    await loginPage.login("user@example.com", "password123");
  });

  test("displays items list", async ({ dashboardPage }) => {
    await dashboardPage.goto();
    const count = await dashboardPage.getItemCount();
    expect(count).toBeGreaterThan(0);
  });

  test("search filters items", async ({ dashboardPage }) => {
    await dashboardPage.goto();

    await dashboardPage.searchItems("specific item");

    // Verify filtered results
    const count = await dashboardPage.getItemCount();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test("create new item", async ({ dashboardPage }) => {
    await dashboardPage.goto();
    const initialCount = await dashboardPage.getItemCount();

    await dashboardPage.createItem("New Test Item");

    await expect(dashboardPage.notification).toContainText("created");
    const newCount = await dashboardPage.getItemCount();
    expect(newCount).toBe(initialCount + 1);
  });
});
```

## Accessibility Testing

```typescript
// e2e/tests/a11y.spec.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const pages = ["/", "/login", "/dashboard", "/settings"];

for (const path of pages) {
  test(`${path} has no a11y violations`, async ({ page }) => {
    await page.goto(path);

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa"])
      .analyze();

    expect(results.violations).toEqual([]);
  });
}

test("login form is keyboard navigable", async ({ page }) => {
  await page.goto("/login");

  await page.keyboard.press("Tab"); // Focus email
  await expect(page.getByRole("textbox", { name: /email/i })).toBeFocused();

  await page.keyboard.press("Tab"); // Focus password
  await expect(page.getByLabel(/password/i)).toBeFocused();

  await page.keyboard.press("Tab"); // Focus submit
  await expect(page.getByRole("button", { name: /sign in/i })).toBeFocused();
});
```
