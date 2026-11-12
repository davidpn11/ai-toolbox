---
name: onboard-repo
description: "Bring a repo into the planner hub: inspect its manifests, scripts and layout, write or refresh its AGENTS.md (stack per path, verify commands, contracts, conventions) from the template, and add or update its row in the hub's repo registry with its Orca repo id. Use when the user wants to add a repo to the hub, when the planner finds a touched repo with no AGENTS.md, or when a repo's stack or commands changed."
argument-hint: "[path to the repo]"
---

# Onboard repo

Give the hub the facts it needs about one repo, and nothing else. The repo gets one file, `AGENTS.md`; the hub gets one registry row. No skills, agents or config are installed into the repo: workers get their instructions through spec files (the `delegation` skill).

## 1. Locate

- The repo is `$ARGUMENTS`, or the one the user or planner named. Resolve it to an absolute path and confirm it is a git repo.
- Find the hub: the folder whose `AGENTS.md` has a "Repo registry" section (usually the session's working directory). No hub means stop and say so.
- Get the Orca repo id with `orca repo list --json`. If the repo is not registered, ask before running `orca repo add --path <abs path>`.

## 2. Inspect

Read, do not guess. Send a `scout` for anything wide.

- Manifests: `package.json` (and workspaces), `bun.lock`/`pnpm-lock.yaml`/`package-lock.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `Package.swift`, and so on. They give the stack and the package manager.
- Scripts and CI: `package.json` scripts, `Makefile`, `justfile`, `.github/workflows/*`. CI shows which commands the project actually trusts.
- Layout: top-level folders and what lives in each, so the Stack table can be per path.
- Contracts: exported packages, API route definitions, schemas, OpenAPI or protobuf files, CLI flags, file formats other repos read. Cross-check against the hub registry's Provides and Consumes columns.
- Existing docs: `README`, any current `AGENTS.md` or `CLAUDE.md`, `CONTEXT.md`, `docs/adr/`.

## 3. Verify the commands

Send the candidate verify commands to the `runner` (install, typecheck or lint, unit tests, build, end-to-end), in that order. Record each as it actually behaved. A command that fails for a reason unrelated to setup is still the right command: keep it and note the current failure. One that cannot run here (needs secrets, a device, a service) is marked `(not run: <reason>)`.

## 4. Write

1. **The repo's `AGENTS.md`**, from `AGENTS-REPO.md` in the `doc-templates` skill. If one exists, keep its human-written content and fill or correct only the template's sections; show the user the diff. Specialist names come only from the `planner` skill's roster.
2. **The hub registry row**, in the hub's `AGENTS.md` (`AGENTS-HUB.md` template): add the row, or update it in place. Keep Provides and Consumes consistent with the other rows: if this repo consumes something, the provider's row should list it.

Touch nothing else in the repo. Do not commit in the repo unless the user asks; when they do, use a branch and a PR, never the default branch.

## 5. Report

The repo, its stack in one line, the verify commands with their results, the contracts found, and every gap (a command that could not run, a contract you were unsure of).
