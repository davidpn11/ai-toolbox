---
name: resolve-merge-conflicts
description: "Resolve an in-progress git merge, rebase, or cherry-pick conflict by intent, not by flag. Use when git reports conflicts, the working tree has conflict markers, or the user asks to fix, resolve, or finish a merge or rebase."
---

# Resolve merge conflicts

Resolve by understanding what each side meant, never by picking a side wholesale. You cannot preserve an intent you have not read.

## Steps

1. **See the current state.** `git status` for the operation in progress (merge, rebase, cherry-pick) and the conflicting files. `git log --oneline --left-right --merge` or `git log <ours>...<theirs> --oneline` for the commits on each side. Grep the tree for `<<<<<<<` so no marker is missed, including in files git does not list as conflicted (lockfiles, generated code).

2. **Find the primary sources for each conflict.** Understand why each change was made and what the original intent was. Read the commit messages on both sides (`git log -p <sha> -- <file>`), the PRs (`gh pr view <n>` when a `(#n)` reference exists), and the original issues or tickets. When resolving, quote them, not just the diff hunks.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour: nothing should appear in the result that was on neither branch. Always resolve; never `--abort`. Aborting throws away the resolution work and returns you to the same conflict.

4. **Handle generated files properly.** Regenerate lockfiles with the package manager (`bun install`, `pnpm install`, `cargo generate-lockfile`, and so on) instead of hand-editing them. Re-run codegen for generated code rather than merging its output by hand.

5. **Run the project's automated checks.** Discover them from `package.json`, `Cargo.toml`, `Makefile`, or CI config, then run typecheck, then tests, then lint and format. Fix anything the merge broke. Checks run green *before* the commit, not after.

6. **Finish the operation.** Stage everything and commit (or `git rebase --continue` / `git cherry-pick --continue`). If rebasing, continue until every commit is rebased, repeating steps 1 to 5 for each stop. Confirm with `git status` that the tree is clean and no operation is in progress.

## Guardrails

- Keep changes minimal and readable. No refactors, renames, or cleanups while resolving; note them for a follow-up instead.
- Do not leave conflict markers in any file.
- Do not push, tag, or force-update any ref during resolution.
- If the conflict is in a branch someone else is actively driving (for example inside an automated PR loop), report which branch needs the rebase and stop, rather than resolving over their work.

## Report

- Files resolved, one line each.
- Notable resolution choices, quoting the commit, PR, or issue that decided each one, and any intent that had to be dropped and why.
- Build and test outcome, with the commands run.

## Attribution

Steps adapted from `skills/engineering/resolving-merge-conflicts` in mattpocock/skills (MIT, Matt Pocock); guardrails adapted from `cursor-team-kit/skills/fix-merge-conflicts` in cursor/plugins (MIT, Eric Zakariasson). See `THIRD_PARTY_NOTICES.md`.
