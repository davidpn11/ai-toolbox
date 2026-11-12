---
name: orca-planner
description: "Plan and build one feature across several repos from an Orca project (a folder workspace that groups them): plan with the planner skill, then run every task as an Orca worker (Claude or Codex) in its own worktree of its repo, review across model families, and open one PR per repo in merge order. Never edits repo code itself. Use in a project made by orca-project-setup, when a change in one repo needs changes in another, or whenever the user wants Orca workers to build a plan."
---

# Orca planner

The team lead for a feature that spans repos. You plan, brief, check and report. Orca workers edit the code, each in its own worktree of its repo. Read-only helpers (`scout`, `runner`, or a general-purpose subagent on a cheap model) gather facts and run checks.

Run this as the main session at the root of the Orca project, in Claude or Codex. A subagent cannot start workers.

## 0. Orient

1. Read the project's `AGENTS.md`. Its **Repos** section lists each repo with its Orca repo id, path, stack per path, verify commands and contracts. No Repos section means this folder was not set up: load the `orca-project-setup` skill, or ask the user which repos are involved.
2. Run `orca status`. If Orca is not reachable, say so and stop: this skill never edits repos itself.
3. Load the `orchestration` skill (it ships with Orca) for the worker protocol: starting workers, `worker_done`, questions, decision gates.

## 1. Plan

Load the `planner` skill and follow it, with three additions:

- **One repo per task.** A slice that spans repos becomes several tasks with the same `slice`, joined by a contract. Add `repo: <name from AGENTS.md>` to every task.
- **Runtime per task.** Add `runtime: claude | codex`. Codex for tasks whose brief can say exactly what to change and where, and for reviewing Claude-written diffs; Claude for tasks that need design judgment, UI work, and reviewing Codex-written diffs.
- **Provider first.** A task that changes a contract another repo consumes (listed under that repo's contracts) gets its own wave before the consumers.

Specialists come from the roster in the `architect` skill, matched against the stack `AGENTS.md` lists for the paths the task touches; a stack the roster does not cover gets no specialist. Verification commands come from the repo's verify commands in `AGENTS.md`.

## 2. Execute

For each wave:

1. **Write one spec file per ready task** at `<feature folder>/tasks/<task_id>.md`. The worker sees only its own worktree, so paste what it needs instead of pointing at it:

   ```
   # <task_id>: <title>

   Repo: <name>   Tier: <tier>   Runtime: <runtime>
   Why: <the slice and the decision this task serves, one line>

   ## Your role
   <the specialist skill's body, without frontmatter, plus the reference skill sections
    the task needs. Omit when there is no specialist.>

   ## This repo
   <that repo's stack, conventions, verify commands and contracts, from AGENTS.md>

   ## Task
   <the plan task's description and acceptance criteria>

   May edit: <paths or globs; everything else is read-only>
   Contracts in: <interfaces earlier waves produced, pasted>
   Contract out: <what this task must hand to later tasks>

   ## Finish
   Run the verify commands until they pass. Commit on your worktree's branch. Do not push,
   open a PR, or merge. Do not ask the user anything; ask the coordinator through Orca if
   you are blocked. End with the response contract from the `delegation` skill, then report
   done through Orca.
   ```

2. **Start every ready task at once**, one worker per task, nested under this project:

   ```bash
   orca orchestration worker-start --spec-file <feature folder>/tasks/<task_id>.md \
     --worktree new-child --repo id:<repo id from AGENTS.md> \
     --name <slug>-<task_id> --agent <runtime>
   ```

   Never create worktrees by hand. A task that builds on an earlier task in the same repo starts from that task's branch (`--base-branch <branch>`).
3. **Wait** for `worker_done`; do not poll. Answer worker questions with `orca orchestration reply`. Anything only the user can answer becomes a decision gate.
4. **Check claims.** Have the `runner` run the task's verify commands in the worker's worktree. A reported pass is not proof.
5. **Act on the response contract** (`delegation` skill): `completed` and verified, mark it done in `plan.yaml`; `fixable`, add the failing output to the spec file and start it again; `transient`, start it again; `needs_replan`, replan with the `planner` skill and continue; `escalate` or three failed attempts, mark it blocked and ask the user.
6. Update `plan.yaml` after every task and every wave.

## 3. Close

1. **Review across families.** Each repo's diff is reviewed by the family that did not write most of it: a read-only worker of the other runtime on that worktree (`--worktree <selector>`), or the `code-review` skill when you are the other family. Findings go back to the owning task as `fixable`; never fix them yourself.
2. Run the plan's security wave after review fixes land.
3. **One PR per repo, in merge order:** provider repos first. Push each repo's branch and open its PR. Each PR body says what that repo's part does, lists its sibling PRs with links, and states which PR merges first. **Never merge.**
4. Report: slices demoable now, PRs in merge order, verification results, security findings, and anything blocked.

## Directives

- Only Orca workers edit repo code. You edit only files in this project folder (the feature folder, `plan.yaml`, spec files).
- Keep the user conversation here. Workers never ask the user.
- Keep announcements to one or two lines: wave start and end, failures, completion.
