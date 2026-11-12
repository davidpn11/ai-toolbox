---
name: playwright-testing
description: "Playwright e2e testing patterns — project setup, Page Object Model, test fixtures, common assertions, accessibility testing with @axe-core/playwright, visual regression, CI configuration, and debugging. Use when writing or fixing Playwright tests."
---

# Playwright E2E Testing

Patterns and conventions for writing reliable end-to-end tests with Playwright.

## Project Setup

```bash
bun add -d @playwright/test @axe-core/playwright
npx playwright install
```

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? "github" : "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
    { name: "mobile-chrome", use: { ...devices["Pixel 5"] } },
    { name: "mobile-safari", use: { ...devices["iPhone 12"] } },
  ],
  webServer: {
    command: "bun run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
```

### Directory Structure

```
e2e/
├── fixtures/
│   └── test.ts           # Extended test with custom fixtures
├── pages/
│   ├── base.page.ts      # Base page with shared methods
│   ├── home.page.ts
│   ├── login.page.ts
│   └── dashboard.page.ts
├── tests/
│   ├── auth.spec.ts
│   ├── dashboard.spec.ts
│   └── a11y.spec.ts
└── utils/
    └── helpers.ts
```

## Page Object Model

### Base Page

```typescript
// e2e/pages/base.page.ts
import type { Page, Locator } from "@playwright/test";

export class BasePage {
  readonly heading: Locator;
  readonly notification: Locator;

  constructor(protected page: Page) {
    this.heading = page.getByRole("heading", { level: 1 });
    this.notification = page.getByRole("alert");
  }

  async waitForPageLoad() {
    await this.page.waitForLoadState("networkidle");
  }

  async getNotificationText() {
    await this.notification.waitFor();
    return this.notification.textContent();
  }
}
```

### Page Object

```typescript
// e2e/pages/login.page.ts
import type { Page, Locator } from "@playwright/test";
import { BasePage } from "./base.page";

export class LoginPage extends BasePage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.getByRole("textbox", { name: /email/i });
    this.passwordInput = page.getByLabel(/password/i);
    this.submitButton = page.getByRole("button", { name: /sign in/i });
    this.errorMessage = page.getByRole("alert");
    this.forgotPasswordLink = page.getByRole("link", { name: /forgot/i });
  }

  async goto() {
    await this.page.goto("/login");
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }
}
```

### Dashboard Page

```typescript
// e2e/pages/dashboard.page.ts
import type { Page, Locator } from "@playwright/test";
import { BasePage } from "./base.page";

export class DashboardPage extends BasePage {
  readonly welcomeMessage: Locator;
  readonly itemsList: Locator;
  readonly createButton: Locator;
  readonly searchInput: Locator;

  constructor(page: Page) {
    super(page);
    this.welcomeMessage = page.getByText(/welcome/i);
    this.itemsList = page.getByRole("list", { name: /items/i });
    this.createButton = page.getByRole("button", { name: /create/i });
    this.searchInput = page.getByRole("searchbox");
  }

  async goto() {
    await this.page.goto("/dashboard");
  }

  async getItemCount() {
    return this.itemsList.getByRole("listitem").count();
  }

  async searchItems(query: string) {
    await this.searchInput.fill(query);
    await this.page.waitForResponse("**/api/items*");
  }

  async createItem(name: string) {
    await this.createButton.click();
    await this.page.getByLabel(/name/i).fill(name);
    await this.page.getByRole("button", { name: /save/i }).click();
  }
}
```

## Custom Fixtures

```typescript
// e2e/fixtures/test.ts
import { test as base } from "@playwright/test";
import { LoginPage } from "../pages/login.page";
import { DashboardPage } from "../pages/dashboard.page";

interface Pages {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
}

export const test = base.extend<Pages>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },
});

export { expect } from "@playwright/test";
```

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

## CI Configuration (GitHub Actions)

```yaml
name: E2E Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

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
