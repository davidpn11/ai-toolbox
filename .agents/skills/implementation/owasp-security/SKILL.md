---
name: owasp-security
description: "OWASP Top 10 security review checklist with vulnerable vs secure code examples. Use when auditing code for security vulnerabilities, reviewing authentication, scanning for secrets, or checking dependency safety."
---

# OWASP Top 10 Security Checklist

Comprehensive security review guide covering the OWASP Top 10 (2021) with actionable code examples.

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

## References

The sections above are what most tasks need. The detail lives in `references/`, next to this file. Read only the file the task needs. If you don't know this skill's folder, find it with a glob for `**/owasp-security/references/*.md` under `.claude/skills`, `.agents/skills`, or `~/.claude/skills`.

| File | Covers | Read it when |
|------|--------|--------------|
| [references/top-10.md](references/top-10.md) | OWASP Top 10 checks with examples | auditing a category in depth, or when a finding needs the vulnerable and fixed pattern |
| [references/top-10.md](references/top-10.md) | OWASP Top 10 checks with examples | auditing a category in depth, or when a finding needs the vulnerable and fixed pattern |
| [references/top-10.md](references/top-10.md) | OWASP Top 10 checks with examples | auditing a category in depth, or when a finding needs the vulnerable and fixed pattern |
| [references/top-10.md](references/top-10.md) | OWASP Top 10 checks with examples | auditing a category in depth, or when a finding needs the vulnerable and fixed pattern |
| [references/top-10.md](references/top-10.md) | OWASP Top 10 checks with examples | auditing a category in depth, or when a finding needs the vulnerable and fixed pattern |
| [references/top-10.md](references/top-10.md) | OWASP Top 10 checks with examples | auditing a category in depth, or when a finding needs the vulnerable and fixed pattern |
| [references/top-10.md](references/top-10.md) | OWASP Top 10 checks with examples | auditing a category in depth, or when a finding needs the vulnerable and fixed pattern |
| [references/top-10.md](references/top-10.md) | OWASP Top 10 checks with examples | auditing a category in depth, or when a finding needs the vulnerable and fixed pattern |
| [references/top-10.md](references/top-10.md) | OWASP Top 10 checks with examples | auditing a category in depth, or when a finding needs the vulnerable and fixed pattern |
| [references/top-10.md](references/top-10.md) | OWASP Top 10 checks with examples | auditing a category in depth, or when a finding needs the vulnerable and fixed pattern |
