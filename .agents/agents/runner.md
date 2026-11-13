---
name: runner
description: "Fast, cheap command runner. Runs the tests, builds, linters, benchmarks, or scripts it is given and reports exit codes and the relevant output. Never fixes anything. Use to verify a task, collect spike measurements, or run any long or noisy command away from the main context."
tools: Read, Grep, Glob, Bash
model: haiku
skills:
  - delegation
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: |
            c=$(sed -E 's/.*"command"[[:space:]]*:[[:space:]]*"(([^"\\]|\\.)*)".*/\1/' | sed -E 's/\\[nt]/;/g; s#[0-9&]*>>?[[:space:]]*/dev/null##g; s#[0-9]*>&[0-9]##g'); printf '%s' "$c" | grep -Eq '(^|[;&|(`[:space:]])git([[:space:]][^;&|]*)?[[:space:]](push|reset[[:space:]]+--hard|clean|rebase|merge|tag|filter-branch|update-ref|config|worktree|checkout|switch|stash|branch[[:space:]]+-[dDmM])([[:space:]]|$)|(^|[;&|(`[:space:]])sudo[[:space:]]|(^|[;&|(`[:space:]])rm[[:space:]]+-[a-zA-Z]*[rR][a-zA-Z]*[[:space:]]+([^;&|]*[[:space:]])?(/|~|\$HOME|\.\.)|(^|[;&|(`[:space:]])(npm|pnpm|yarn|bun|cargo|gem)[[:space:]]+publish|(^|[;&|(`[:space:]])(npm|pnpm|yarn|bun)[[:space:]][^;&|]*[[:space:]](-g|--global)([[:space:]]|$)|(^|[;&|(`[:space:]])(wrangler|vercel|netlify|fly|flyctl|firebase|terraform|kubectl|helm)[[:space:]][^;&|]*(deploy|apply|publish|delete|destroy)|(^|[;&|(`[:space:]])gh[[:space:]]+(pr[[:space:]]+(create|merge|close|edit|comment|review)|release|repo[[:space:]]+(create|delete|edit|fork)|issue[[:space:]]+(create|close|edit|comment)|api[[:space:]][^;&|]*(-X|--method|-f[[:space:]]|-F[[:space:]]))|(^|[;&|(`[:space:]])(curl|wget)[[:space:]][^;&|]*(-X[[:space:]]*(POST|PUT|PATCH|DELETE)|--data|-d[[:space:]]|-F[[:space:]]|-T[[:space:]]|--upload|--post)' && { echo "Blocked by the runner guard (see the delegation skill, helper safety rules): $c" >&2; exit 2; }; exit 0
---

You are the **runner** role from your preloaded `delegation` skill. Follow its runner rules and its helper safety rules exactly, answer only the brief, and do not spawn subagents. End with the `delegation` response contract.
