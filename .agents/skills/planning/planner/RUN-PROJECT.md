# Run a plan in a Project

Part of the `planner` skill, step **2. Run** in Project mode: one repo, and the Children are subagents. Without subagent support, apply each specialist's skill yourself, one task at a time, in wave order.

## Execute

1. Take the next wave. Every task in it whose dependencies are `completed` is ready.
2. Delegate every ready task in the same turn, one subagent per task (the specialist named in `agent`), on the task's `tier`. Write each brief in the `delegation` format: the task definition from the plan, `May edit` set to the task's files, its `context_files` as pointers, and, for wave 2 and later, the contracts its dependencies produced. Tasks in the same wave that edit code must touch disjoint files, or each runs in its own worktree (Claude Code: `isolation: worktree`).
3. When a task reports, check its claims: send its `verification` commands to the `runner` instead of trusting a reported pass.
4. Act on the response contract:
   - `completed` and verified: mark it completed in `plan.yaml` and announce it in one line.
   - `needs_revision` or `fixable`: delegate it again with the failing output added to the brief; on the second failure, one tier up (`delegation` section 2), and record the new `tier` in `plan.yaml`.
   - `transient`: retry the same brief.
   - `needs_replan`: replan (`planner` step 1, **Replanning**), then continue from the revised plan.
   - `escalate`, or three failed attempts: mark it blocked and ask the user.
5. Update `plan.yaml` after every task and every wave. Loop until every task is completed or blocked.

## Close

1. Call the Skill tool with "deep-review" against the branch the plan started from, with `spec.md` as the spec. Delegate its **Act on** findings as new tasks.
2. Run the plan's `security-engineer` wave last, after the review fixes land.
3. Report: what was built (the slices demoable now), files touched, verification results, security findings, and anything blocked. Offer to push the branch and open a PR; never merge.
