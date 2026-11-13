---
name: project-setup
description: "Wizard that installs ai-toolbox skills into a Project (one repo) or a Workspace (a folder grouping repos, cloned from GitHub, registered in Orca), for Claude and Codex. Reads the existing code and installed skills first, picks skills by stack, removes retired or shadowed copies, and writes AGENTS.md. Asks once before changing anything. Use when the user wants to set up skills, the planner or Orca for a repo or a set of repos, says a change in repo A needs changes in repo B, or wants to clean up old skills in a project."
argument-hint: "[folder or repos] [workspace name]"
---

# Project setup

Turn a folder into a place where the `planner` can build. You do the work; the user answers one round of questions and approves one plan.

**Words.** *Project*: one git repo. *Workspace*: a plain folder grouping Projects. It is registered in Orca as a folder workspace, it is never a git repo, and it has no submodules. The repos inside it are ordinary clones from GitHub. *Worker*: a one-task Orca agent in its own worktree. [CATALOG.md](CATALOG.md) lists every skill and its scope.

## 1. Preflight

Run the `session-check` skill on the target. Stop on a ❌ for shell, write, or network, because `npx skills` needs them. Note any ❌ for gh or Orca: they limit the steps below and the plan says so.

## 2. Classify the target

From `$ARGUMENTS`, or the cwd:

| What is there | Kind |
| --- | --- |
| a git repo | **Project** |
| a folder holding repo clones, or with an `AGENTS.md` **Repos** section | **Workspace** |
| an empty folder, or the user names several repos | **new Workspace**: ask which repos (names, paths or `owner/repo`) |
| a repo given with another repo | **new Workspace** that groups them; ask for its name and place (default `~/orca/workspaces/<name>`) |

## 3. Read what is there

Read; do not guess. Send a `scout` for anything wide.

- **Docs:** `AGENTS.md`, `CLAUDE.md`, `README`, `CONTEXT.md`, `docs/adr/`.
- **Skills:** `skills-lock.json`, `.claude/skills/`, `.agents/skills/`, `.codex/`, `.claude/agents/`. Sort each skill into one bucket:
  - *current*: an ai-toolbox project skill from the catalog → keep, update;
  - *retired*: in the catalog's **Retired names** → remove;
  - *shadowed*: the same name is installed globally (`npx skills ls -g`) → remove the project copy;
  - *foreign*: from another source in the lock file → keep, list it;
  - *custom*: no lock entry, not in the catalog (for example a repo-specific `docs-engineer`) → keep, list it, and ask whether the planner should treat it as a specialist.
- **Code, per repo:** manifests (`package.json` + workspaces, lock files, `Cargo.toml`, `go.mod`, `pyproject.toml`, `Package.swift`), scripts and CI (`package.json` scripts, `Makefile`, `.github/workflows/*`), the top-level layout (stack per path), and contracts (exported packages, API routes, schemas, CLI flags, file formats; who provides, who consumes).
- **Git, per repo:** the GitHub remote, the default branch, uncommitted work, and existing worktrees (`git worktree list`).
- **Orca** (when `orca status` answers): `orca repo list --json` (registered?), `orca worktree ps --json` (is the folder already a workspace?), `orca skills installed --json`.

## 4. Propose one plan, ask once

Show a short plan and wait for a yes. Include only the rows that apply.

1. **Orca and GitHub (Workspace):**
   - each repo is cloned into the Workspace from its GitHub remote: `gh repo clone <owner/repo> <workspace>/<repo>`. A repo with no GitHub remote: say so and offer `gh repo create`, or register its current path as is;
   - a clone with uncommitted work in the *old* checkout: warn, and do not delete the old checkout;
   - each clone registered: `orca repo add --path <clone> --json`;
   - the Workspace registered: `orca repo add --path <workspace> --kind folder --json`;
   - Orca's bundled skills, if missing: `orca skills install`.
2. **Orca (Project):** register the repo if it is not registered.
3. **Install:** the project skills the catalog's `Install when` column picks for the stack (in a Workspace, the union over all repos), plus their subagents.
4. **Remove:** retired and shadowed skills, by name.
5. **Keep:** foreign and custom skills, by name.
6. **AGENTS.md:** create it or merge into it (never overwrite what is there), and add `CLAUDE.md` = `@AGENTS.md` if missing.
7. **Where the change lands:** a Workspace is a plain folder, so the changes are written in place. A Project is a repo: Workers and other worktrees only see skills once they are committed, so the change goes on a branch `chore/project-setup` with a PR, unless the user says to leave it uncommitted.

## 5. Apply

Work from the target root (from each clone for its own changes).

**Install** (project scope; never `-g` here):

```bash
npx skills add davidpn11/ai-toolbox --skill <name> --skill <name> ... --agent claude-code --agent codex -y
```

**Subagents** (Claude Code): copy the ones the catalog pairs with the installed skills.

```bash
SRC=$(mktemp -d) && git clone -q --depth 1 https://github.com/davidpn11/ai-toolbox "$SRC"
mkdir -p .claude/agents && cp "$SRC"/.agents/agents/{planner,<persona>,...}.md .claude/agents/
rm -rf "$SRC"
```

In a Workspace the Children are Workers, which get their persona pasted into the spec file, so copy only `planner`. `scout` and `runner` are global (`~/.claude/agents/`); copy them too only if they are missing there.

**Remove:** `npx skills remove <name> ... -y` for names in the lock file. For copies with no lock entry, delete `.claude/skills/<name>`, `.agents/skills/<name>`, and `.claude/agents/<name>.md` once the user has said yes. In a repo they stay in git history; outside git, move them to `<target>/.skills-removed/` first.

If a flag is rejected, check `npx skills add --help` and adjust.

**AGENTS.md:** Workspace → [WORKSPACE-AGENTS.md](WORKSPACE-AGENTS.md); Project → [PROJECT-AGENTS.md](PROJECT-AGENTS.md). Fill them with what step 3 found. Have the `runner` run each verify command once (in a Workspace, inside each clone) and record the result; a command that cannot run here is `not run: <reason>`. Specialist names come only from the `planner` roster.

**Project on a branch:** `git switch -c chore/project-setup`, commit the skill folders, `skills-lock.json`, `.claude/agents/`, `AGENTS.md`, `CLAUDE.md`, push, `gh pr create`. Never merge.

## 6. Verify and report

- `npx skills ls` in the target: every installed skill is project scope, and no name is also global.
- Workspace: `orca worktree ps --json` lists it as a folder workspace; each clone's `origin` is GitHub; `git status` is clean.
- Run `session-check` again; the skills row is clean.

Report in a few lines: the target and its Orca id, each repo's stack and verify results, the contracts, what was installed, removed and kept, the PR if one was opened, and any gap. Then tell the user how to start: open the folder in Orca, start Claude or Codex at its root, and run `/planner <feature>` (`/lifecycle <idea>` for bigger features, which plans first).

## Directives

- Change nothing before the user's yes in step 4. Removing skills, cloning, registering in Orca, and opening a PR are all on that list.
- Never `git init` a Workspace. Never use submodules.
- Never write inside a repo that is not the target. In a Workspace, the clones get changes only when the user asked to clean their skills, and then on a branch with a PR in each.
- Never delete an old checkout or worktree; say which are now redundant and let the user decide.
