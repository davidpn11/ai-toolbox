# Page objects and fixtures

Part of the `playwright-testing` skill.

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
