# Run a plan in a Workspace

Part of the `planner` skill, step **2. Run** in Workspace mode: several repos, and the Children are Orca Workers. You run at the Workspace root (Claude or Codex). Workers edit the code, each in its own worktree of its repo. Read-only helpers (`scout`, `runner`, or a general-purpose subagent on a cheap model) gather facts and run checks.

## Before the first wave

1. `AGENTS.md` **Repos** lists each repo: Orca repo id, path (normally a clone inside the Workspace), stack per path, verify commands, contracts.
2. Load the `orchestration` skill (it ships with Orca) for the Worker protocol: starting Workers, `worker_done`, questions, decision gates.
3. In each repo, `git fetch` and confirm the base branch is current with its GitHub remote. Workers branch from there.

## Execute

For each wave:

1. **Write one spec file per ready task** at `<feature folder>/tasks/<task_id>.md`. A Worker sees only its own worktree, so paste what it needs instead of pointing at it:

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

   ## Safety
   <the helper safety rules from `delegation` section 5, pasted in full>

   ## Finish
   Run the verify commands until they pass. Commit on your worktree's branch. Do not push,
   open a PR, or merge. Do not ask the user anything; ask the coordinator through Orca if
   you are blocked. End with the response contract from the `delegation` skill, then report
   done through Orca.
   ```

2. **Start every ready task at once**, one Worker per task, as a Child of this Workspace:

   ```bash
   orca orchestration worker-start --spec-file <feature folder>/tasks/<task_id>.md \
     --worktree new-child --repo id:<repo id from AGENTS.md> \
     --name <slug>-<task_id> --agent <runtime> --model <id for the task's tier>
   ```

   The model id for each tier and runtime is in the `delegation` table. Never leave a Worker on the expensive default when its tier is `fast` or `standard`.

   Never create worktrees by hand. A task that builds on an earlier task in the same repo starts from that task's branch (`--base-branch <branch>`). If a flag is rejected, check `orca orchestration worker-start --help`; the `orchestration` skill is the authority.
3. **Wait** for `worker_done`; do not poll. Answer Worker questions with `orca orchestration reply`. Anything only the user can answer becomes a decision gate.
4. **Check claims.** Have the `runner` run the task's verify commands in the Worker's worktree. A reported pass is not proof.
5. **Act on the response contract** (`delegation`): `completed` and verified, mark it done in `plan.yaml`; `fixable`, add the failing output to the spec file and start it again, one tier up on the second failure; `transient`, start it again; `needs_replan`, replan and continue; `escalate` or three failed attempts, mark it blocked and ask the user.
6. Update `plan.yaml` after every task and every wave.

## Close

1. **Review across families.** Each repo's diff is reviewed by the family that did not write most of it: a read-only Worker of the other runtime on that worktree (`--worktree <selector>`), or the `deep-review` skill when you are the other family. Findings go back to the owning task as `fixable`; never fix them yourself.
2. Run the plan's security wave after the review fixes land.
3. **One PR per repo, in merge order**, providers first. Show the user the branches, the merge order, and the PR titles, and wait for a yes before pushing anything. Then push each repo's branch to its GitHub remote and open the PR (`gh pr create`). Each PR body says what that repo's part does, links its sibling PRs, and states which merges first. Record the PR on the worktree (`orca worktree set --worktree <selector> --pr <number>`). **Never merge.**
4. Report: the slices demoable now, PRs in merge order, verification results, security findings, and anything blocked.
5. After the user merges, `git pull` in each repo clone so the next plan starts from the merged base.

## Directives

- Only Workers edit repo code. You edit only Workspace files (feature folder, `plan.yaml`, spec files).
- Keep the user conversation here. Workers never ask the user.
- Announce in one or two lines: wave start and end, failures, completion.
