---
name: orca-project-setup
description: "Set up an Orca project for work that spans several repos: create a folder workspace that groups them, install the ai-toolbox planning and orchestration skills into it for Claude and Codex, and write one AGENTS.md describing each repo (stack, verify commands, contracts). The repos themselves are not changed. Install this one skill globally. Use when the user says a change in one repo needs changes in another, wants a project for repos A and B, or asks to set up the planner or orchestration for some repos."
argument-hint: "[repo names or paths] [project name]"
---

# Orca project setup

Turn "A needs changes in B" into a ready Orca project in one go. You do every step; the user only answers the questions below. Never write to the repos themselves: everything lands in the new project folder.

## 1. Ask once

Ask in a single message, with your guess for each answer:

- **Repos:** from `$ARGUMENTS`, or ask. Accept names or paths; resolve each to an absolute path of a git repo.
- **Project name:** a short slug (for example `crepe-bun`). The folder goes next to the repos, `<their common parent>/<name>`, unless the user names a place.

## 2. Check the tools

- `orca status`: Orca must be running. If not, ask the user to open it (`orca open`) and stop.
- `orca skills installed`: the Orca `orchestration` and `orca-cli` skills must be there. If not, run `orca skills install`.
- `npx skills --help` works (Node is installed).

## 3. Register in Orca

1. `orca repo list --json`. Note each repo's id. A repo that is missing: ask, then `orca repo add --path <abs path> --json`.
2. Create the project folder (it must not exist yet, or must be empty), then register it as a folder workspace:

   ```bash
   orca repo add --path <project folder> --kind folder --json
   ```

   Do not `git init` it: Orca folder workspaces are plain folders.

## 4. Install the skills into the project

From inside the project folder (project scope, never `-g`):

```bash
npx skills add davidpn11/ai-toolbox --skill '*' --agent claude-code --agent codex -y
mkdir -p .claude/agents
for a in scout runner; do
  curl -fsSL "https://raw.githubusercontent.com/davidpn11/ai-toolbox/master/.agents/agents/$a.md" -o ".claude/agents/$a.md"
done
```

If a flag is rejected, check `npx skills add --help` and adjust; the goal is every ai-toolbox skill, for both agents, in this folder.

Then check for **name clashes**: `npx skills ls -g`. Claude Code prefers a global skill over a project skill with the same name, so a global `planner`, `architect`, `grilling` or similar would silently replace the project's copy. List any clash and ask whether to remove the global one (`npx skills remove -g <name> -y`). Do not remove anything without a yes.

## 5. Describe the repos

For each repo, read (do not guess; send a `scout` for anything wide):

- manifests (`package.json` and workspaces, lock files, `Cargo.toml`, `go.mod`, `pyproject.toml`, `Package.swift`, ...) for the stack and package manager;
- scripts and CI (`package.json` scripts, `Makefile`, `justfile`, `.github/workflows/*`) for the commands the project trusts;
- the top-level layout, so the stack can be given per path;
- contracts: exported packages, API routes, schemas, OpenAPI or protobuf files, CLI flags, file formats. Mark which repo provides each and which consumes it;
- the repo's own `README`, `AGENTS.md` or `CLAUDE.md`, if present.

Have the `runner` run each candidate verify command once (install, typecheck or lint, tests, build) and record what happened. A command that cannot run here (needs secrets, a device, a service) is marked `(not run: <reason>)`. If the user wants setup fast, skip this and mark the commands `(not run: unverified)`.

## 6. Write the project files

1. `AGENTS.md` from [PROJECT-AGENTS.md](PROJECT-AGENTS.md), filled with what you found. Specialist names come only from the roster in the `architect` skill.
2. `CLAUDE.md` with the single line `@AGENTS.md`, so Claude reads the same file Codex does.

## 7. Hand over

Report in a few lines:

- the project folder and its Orca id;
- each repo's stack and verify commands, with results;
- the contracts between them;
- any gap (a command that did not run, a name clash left in place).

Then tell the user how to use it: open the project in Orca, start Claude or Codex at its root, and ask for the feature ("use orca-planner: add X to A and the API it needs in B"). Bigger features can start with the `lifecycle` skill, which plans first and then builds through `orca-planner`.
