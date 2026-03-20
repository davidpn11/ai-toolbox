---
name: owasp-security
description: "OWASP Top 10 security review checklist with vulnerable vs secure code examples. Use when auditing code for security vulnerabilities, reviewing authentication, scanning for secrets, or checking dependency safety."
---

# OWASP Top 10 Security Checklist

Comprehensive security review guide covering the OWASP Top 10 (2021) with actionable code examples.

## A01 — Broken Access Control

The most critical web application security risk.

### What to Check

- [ ] Authorization on every endpoint (not just authentication)
- [ ] Users can't access other users' data by changing IDs (IDOR)
- [ ] Admin functions protected by role checks
- [ ] CORS policy is restrictive (not `*` in production)
- [ ] Directory traversal prevented
- [ ] Rate limiting on sensitive endpoints

### Vulnerable vs Secure

```typescript
// VULNERABLE — No authorization check
app.get("/api/users/:id/profile", async (c) => {
  return c.json(await getUser(c.req.param("id")));
});

// SECURE — Verify user owns the resource
app.get("/api/users/:id/profile", requireAuth(), async (c) => {
  const requestedId = c.req.param("id");
  const currentUser = c.get("user");
  if (currentUser.id !== requestedId && currentUser.role !== "admin") {
    return c.json({ error: "Forbidden" }, 403);
  }
  return c.json(await getUser(requestedId));
});
```

```rust
// VULNERABLE — No ownership check
async fn get_document(Path(id): Path<String>) -> Result<Json<Document>, AppError> {
    let doc = db::get_document(&id).await?;
    Ok(Json(doc))
}

// SECURE — Verify ownership
async fn get_document(
    Path(id): Path<String>,
    Extension(user): Extension<AuthUser>,
) -> Result<Json<Document>, AppError> {
    let doc = db::get_document(&id).await?;
    if doc.owner_id != user.id {
        return Err(AppError::Forbidden("Not your document".into()));
    }
    Ok(Json(doc))
}
```

## A02 — Cryptographic Failures

### What to Check

- [ ] Passwords hashed with bcrypt/scrypt/argon2 (NOT MD5/SHA1/SHA256)
- [ ] No secrets in source code (API keys, passwords, tokens)
- [ ] HTTPS enforced (no HTTP in production)
- [ ] Sensitive data encrypted at rest
- [ ] JWT secrets strong (32+ chars), tokens expire
- [ ] No sensitive data in URLs or logs

### Vulnerable vs Secure

```typescript
// VULNERABLE — Weak hashing
import crypto from "crypto";
const hash = crypto.createHash("md5").update(password).digest("hex");

// SECURE — Bun's built-in password hashing (bcrypt)
const hash = await Bun.password.hash(password);
const isValid = await Bun.password.verify(input, hash);
```

```typescript
// VULNERABLE — Secret in code
const JWT_SECRET = "my-super-secret-key";

// SECURE — From environment
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET || JWT_SECRET.length < 32) {
  throw new Error("JWT_SECRET must be at least 32 characters");
}
```

## A03 — Injection

### What to Check

- [ ] SQL queries use parameterized statements (prepared statements)
- [ ] User input never interpolated into queries, commands, or HTML
- [ ] ORMs used with parameterized queries
- [ ] No `eval()`, `new Function()`, or dynamic code execution with user input
- [ ] Shell commands avoided; if necessary, args properly escaped

### Vulnerable vs Secure

```typescript
// VULNERABLE — SQL injection
const query = `SELECT * FROM users WHERE email = '${email}'`;

// SECURE — Parameterized query (Bun SQLite)
const stmt = db.prepare("SELECT * FROM users WHERE email = ?");
const user = stmt.get(email);
```

```rust
// VULNERABLE — String interpolation in SQL
let query = format!("SELECT * FROM users WHERE email = '{}'", email);

// SECURE — sqlx parameterized query
let user = sqlx::query_as!(User, "SELECT * FROM users WHERE email = $1", email)
    .fetch_optional(&pool)
    .await?;
```

```typescript
// VULNERABLE — XSS via innerHTML
element.innerHTML = userInput;

// SECURE — React escapes by default, but be careful with:
// Never use dangerouslySetInnerHTML with unsanitized input
// Use DOMPurify if you must render HTML
import DOMPurify from "dompurify";
const clean = DOMPurify.sanitize(userInput);
```

## A04 — Insecure Design

### What to Check

- [ ] Input validation at API boundaries (Zod schemas)
- [ ] Rate limiting on authentication endpoints
- [ ] Business logic protected against abuse
- [ ] Fail securely — errors don't expose internals
- [ ] Principle of least privilege applied

### Secure Patterns

```typescript
// Rate limiting on auth endpoints
import { rateLimiter } from "hono-rate-limiter";

app.use(
  "/api/auth/*",
  rateLimiter({
    windowMs: 15 * 60 * 1000, // 15 minutes
    limit: 5, // 5 attempts
    message: { error: "Too many attempts, try again later" },
  }),
);
```

## A05 — Security Misconfiguration

### What to Check

- [ ] Debug/dev modes disabled in production
- [ ] Default credentials removed
- [ ] Security headers set (CSP, X-Frame-Options, Strict-Transport-Security)
- [ ] Stack traces not exposed to clients
- [ ] Unused features/endpoints removed
- [ ] CORS not set to `*` in production

### Secure Headers (Hono)

```typescript
import { secureHeaders } from "hono/secure-headers";

app.use(
  "*",
  secureHeaders({
    contentSecurityPolicy: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
    // Defaults already include:
    // X-Frame-Options: SAMEORIGIN
    // X-Content-Type-Options: nosniff
    // X-XSS-Protection: 0
    // Referrer-Policy: no-referrer
  }),
);
```

## A06 — Vulnerable and Outdated Components

### What to Check

- [ ] Run `npm audit` / `bun audit` / `cargo audit`
- [ ] No known CVEs in dependencies
- [ ] Dependencies are recent (within 1-2 major versions)
- [ ] Lock files committed (bun.lockb, Cargo.lock)
- [ ] Unused dependencies removed

### Audit Commands

```bash
# JavaScript/Bun
bun audit
npm audit
npx npm-check-updates

# Rust
cargo install cargo-audit
cargo audit
```

## A07 — Identification and Authentication Failures

### What to Check

- [ ] Passwords have minimum complexity requirements
- [ ] Account lockout after failed attempts
- [ ] Session tokens are httpOnly, secure, sameSite
- [ ] Password reset tokens expire quickly
- [ ] No credentials in URLs

### Secure Cookie Configuration

```typescript
// Secure session cookie
c.header(
  "Set-Cookie",
  [
    `session=${token}`,
    "HttpOnly",
    "Secure",
    "SameSite=Lax",
    "Path=/",
    `Max-Age=${60 * 60 * 24}`, // 24 hours
  ].join("; "),
);
```

## A08 — Software and Data Integrity Failures

### What to Check

- [ ] CI/CD pipeline has security checks
- [ ] Dependencies verified via lockfile
- [ ] Code review required for merges
- [ ] Subresource integrity (SRI) for CDN scripts

## A09 — Security Logging and Monitoring Failures

### What to Check

- [ ] Authentication failures logged
- [ ] Authorization failures logged
- [ ] Sensitive operations have audit trail
- [ ] Logs don't contain PII, secrets, or tokens
- [ ] Log injection prevented (sanitize user input in logs)

```typescript
// VULNERABLE — Log injection
console.log(`Login attempt for: ${email}`);
// Attacker sends: "admin\n[INFO] Login successful for admin@evil.com"

// SECURE — Structured logging
logger.info({ event: "login_attempt", email: sanitize(email) });
```

## A10 — Server-Side Request Forgery (SSRF)

### What to Check

- [ ] User-provided URLs validated against allowlist
- [ ] Internal network addresses blocked (127.0.0.1, 10.x, 172.16-31.x, 192.168.x)
- [ ] Redirects don't follow to internal resources
- [ ] DNS rebinding mitigated

```typescript
// VULNERABLE — Fetch any URL
app.post("/api/fetch", async (c) => {
  const { url } = await c.req.json();
  const res = await fetch(url); // SSRF!
  return c.json(await res.json());
});

// SECURE — URL validation
function isAllowedUrl(url: string): boolean {
  const parsed = new URL(url);
  const blockedHosts = ["localhost", "127.0.0.1", "0.0.0.0"];
  const blockedPrefixes = ["10.", "172.16.", "192.168."];

  if (blockedHosts.includes(parsed.hostname)) return false;
  if (blockedPrefixes.some((p) => parsed.hostname.startsWith(p))) return false;
  if (parsed.protocol !== "https:") return false;

  return true;
}
```

## Secret Detection Patterns

Grep patterns for finding hardcoded secrets:

```bash
# API keys and tokens
grep -rn --include='*.{ts,js,tsx,jsx,rs}' -E '(api[_-]?key|secret|token|password)\s*[:=]\s*["\x27][A-Za-z0-9+/=]{16,}'

# AWS access keys
grep -rn 'AKIA[0-9A-Z]{16}'

# Private keys
grep -rn 'BEGIN.*PRIVATE KEY'

# Connection strings with credentials
grep -rn -E '(postgres|mysql|mongodb|redis)://[^:]+:[^@]+@'

# .env files that shouldn't be committed
find . -name '.env' -not -path './node_modules/*' -not -path './.git/*'

# Check .gitignore includes sensitive files
grep -q '\.env' .gitignore || echo "WARNING: .env not in .gitignore"
```

## Review Report Template

```markdown
# Security Review: {component}

**Date**: YYYY-MM-DD
**Scope**: {what was reviewed}
**Risk Level**: {high|medium|low}

## Summary

{1-2 sentence overview of findings}

## Critical (Must Fix Before Deploy)

1. **{Issue}** — {file}:{line}
   - Risk: {what could happen}
   - Fix: {specific recommendation}

## High

1. **{Issue}** — {location}

## Medium

1. **{Issue}** — {location}

## Low / Recommendations

1. **{Issue}** — {location}

## Secret Scan: {Clean / N issues found}

## Dependency Audit: {Clean / N vulnerabilities}
```
