---
name: session-check
description: "Preflight for the current session: can it run commands, write here, reach the network and GitHub, push and open PRs (gh auth, scopes, repo permission), talk to Orca, and are any project skills hidden by global ones. Read-only; prints one table with a fix per problem. Use when the user asks what this session can do or why a command was blocked, before setting up a project, before starting Workers, or when git/gh/orca fails unexpectedly."
argument-hint: "[folder]"
---

# Session check

One table that says what this session can and cannot do, with the fix for each gap. Read-only: it never edits settings, never logs in, never prints a token.

## Run

```bash
bash <this skill's folder>/check.sh "${ARGUMENTS:-$PWD}"
```

The script sits next to this file (for example `~/.agents/skills/session-check/check.sh` or `.claude/skills/session-check/check.sh`). If the harness blocks it, that is the first finding: say which tool was denied.

It checks, in order:

| Area | How |
| --- | --- |
| agent | Claude Code (`CLAUDECODE`) or Codex (`CODEX_*`; sandbox mode and network flag) |
| shell, write | that it runs; a temp file created and removed in the folder |
| network | `api.github.com` answers |
| target | Project (a git repo), Workspace (folder with repo clones or an `AGENTS.md` **Repos** section), or neither |
| git, per repo | branch, uncommitted count, `origin` reachable with `git ls-remote` |
| gh | logged in, token scopes, `viewerPermission` per GitHub repo (WRITE or above = can push and open PRs) |
| orca | `orca status`, which Orca workspace this folder is, bundled `orchestration` and `orca-cli` skills present |
| tools | node, npx, bun |
| skills | project skills whose name a global skill hides |
| guards | the `cost-guards` plugin is enabled, and `scout` and `runner` carry their guard hooks |

## Report

Show the table as printed. Under it, list the ❌ and ⚠️ rows only, each with its fix in one line. Then add what the script cannot see:

- **Claude Code permission mode.** The session cannot read its own mode. If a command was denied earlier in the session, name it and suggest the allow rule for `.claude/settings.json` (for example `Bash(gh pr create:*)`, `Bash(git push:*)`, `Bash(orca:*)`). Do not edit the settings yourself.
- **Codex approvals.** `approval_policy` and `sandbox_mode` live in `~/.codex/config.toml`; quote the current values if readable, and say which one blocks the failing command.
- **Orca in a sandbox.** An Orca error `runtime_access_denied` means the sandbox blocked the connection. Rerun with escalated permissions; do not restart Orca.

End with one line: **ready** (no ❌), or **blocked on** the ❌ rows.
