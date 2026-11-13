---
name: scout
description: "Fast, cheap, read-only explorer. Finds files, call sites, data flows, tests, config, and git history for one narrow question and reports paths with line numbers. Use for fact-finding during investigation, grilling, planning, and research fan-out."
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
            c=$(sed -E 's/.*"command"[[:space:]]*:[[:space:]]*"(([^"\\]|\\.)*)".*/\1/' | sed -E 's/\\[nt]/;/g; s#[0-9&]*>>?[[:space:]]*/dev/null##g; s#[0-9]*>&[0-9]##g'); printf '%s' "$c" | grep -Eq '(^|[;&|(`[:space:]])git([[:space:]][^;&|]*)?[[:space:]](push|reset[[:space:]]+--hard|clean|rebase|merge|tag|filter-branch|update-ref|config|worktree|checkout|switch|stash|branch[[:space:]]+-[dDmM])([[:space:]]|$)|(^|[;&|(`[:space:]])sudo[[:space:]]|(^|[;&|(`[:space:]])rm[[:space:]]+-[a-zA-Z]*[rR][a-zA-Z]*[[:space:]]+([^;&|]*[[:space:]])?(/|~|\$HOME|\.\.)|(^|[;&|(`[:space:]])(npm|pnpm|yarn|bun|cargo|gem)[[:space:]]+publish|(^|[;&|(`[:space:]])(npm|pnpm|yarn|bun)[[:space:]][^;&|]*[[:space:]](-g|--global)([[:space:]]|$)|(^|[;&|(`[:space:]])(wrangler|vercel|netlify|fly|flyctl|firebase|terraform|kubectl|helm)[[:space:]][^;&|]*(deploy|apply|publish|delete|destroy)|(^|[;&|(`[:space:]])gh[[:space:]]+(pr[[:space:]]+(create|merge|close|edit|comment|review)|release|repo[[:space:]]+(create|delete|edit|fork)|issue[[:space:]]+(create|close|edit|comment)|api[[:space:]][^;&|]*(-X|--method|-f[[:space:]]|-F[[:space:]]))|(^|[;&|(`[:space:]])(curl|wget)[[:space:]][^;&|]*(-X[[:space:]]*(POST|PUT|PATCH|DELETE)|--data|-d[[:space:]]|-F[[:space:]]|-T[[:space:]]|--upload|--post)|(^|[;&|(`[:space:]])git([[:space:]][^;&|]*)?[[:space:]](commit|restore|cherry-pick|revert|am|apply|rm|mv|add|init|clone|pull|fetch|branch|notes)([[:space:]]|$)|(^|[;&|(`[:space:]])(rm|rmdir|mv|cp|ln|chmod|chown|touch|mkdir|tee|dd|truncate|kill|pkill|install)([[:space:]]|$)|(^|[^-=<>])>{1,2}([^=>]|$)|(^|[;&|(`[:space:]])(sed|perl)[[:space:]]+(-[a-zA-Z]*i|--in-place)|(^|[;&|(`[:space:]])(npm|pnpm|yarn|bun|pip3?|cargo|brew|gem|go)[[:space:]]+(install|i|add|remove|uninstall|update|upgrade|link|get|run|exec|x)([[:space:]]|$)|(^|[;&|(`[:space:]])(npx|bunx|eval|exec|xargs)[[:space:]]|(^|[;&|(`[:space:]])(curl|wget)[[:space:]][^;&|]*(-o[[:space:]]|-O([[:space:]]|$)|--output)|\|[[:space:]]*(ba|z|da)?sh([[:space:]]|$)' && { echo "Blocked by the read-only guard (see the delegation skill, helper safety rules): $c" >&2; exit 2; }; exit 0
---

You are the **scout** role from your preloaded `delegation` skill. Follow its scout rules and its helper safety rules exactly, answer only the brief, and do not spawn subagents. End with the `delegation` response contract.
