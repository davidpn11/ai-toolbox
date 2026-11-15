---
name: opencode-session
description: "Start an opencode agent (for example a local Ollama model such as Bonsai 2) as a child session in Orca, never as a headless CLI run. Use every time you are about to open, start, spawn or run opencode for any task: 'run this through opencode', 'ask bonsai/qwen/ollama to ...', 'use opencode as a subagent'. Never run `opencode run` headless from your own shell; create a child Orca workspace with opencode as its agent instead, then wait for it and read its answer."
argument-hint: "<task brief>"
---

# opencode session

Run opencode as a child Orca session that the user can watch. Never run it headless.

## Never

- `opencode run ...` from your own shell, in the foreground or in the background. A local model often takes more than 10 minutes, so the shell call times out and gets moved to the background. If anyone stops it there, its output is lost, and the user never sees what it did.
- Piping opencode through `tail`, `head` or any other buffering filter.

## Start it

Use the `orca-cli` skill to choose the Orca executable. From inside the parent project:

```bash
orca worktree create --name <short-task-slug> --parent-worktree active \
  --agent opencode --prompt "<self-contained task brief>" --json
```

- `--parent-worktree active` makes it a child of the current workspace.
- Leave out `--model`. Orca refuses it for opencode on a workspace that does not exist yet (`capability_unsupported`). The model comes from the opencode config (`~/.config/opencode/opencode.json` `model`, for example `ollama/bonsai-2-32k`). Check that this default is the model the user asked for before you launch. If the user wants a different model, create the workspace without `--agent`, then run `orca agent launch --agent opencode --worktree <id> --model <provider/model> --prompt "..." --json`.
- If the task is read-only, say so in the brief ("Do not modify any files").
- Small local models drift. Give them the exact commands to run and the exact output format you want.

Check `result.launch`: `outcome.kind` (`structured` means a chat tab), `prompt.outcome` (whether the brief arrived), and the `worktree.id` to use for later commands.

## Close the setup terminal

`worktree create` always opens a first terminal and runs the repo's setup hook in it (for example `bun install`). No flag prevents this. So that only the opencode chat tab is left, close that terminal once setup has finished. Closing it earlier kills the install halfway.

```bash
# wait up to 5 min; a repo without a setup hook never prints the marker
for i in $(seq 150); do orca terminal list --worktree <id> --json | grep -q '__ORCA_SETUP_COMPLETE__' && break; sleep 2; done
orca terminal list --worktree <id> --json   # take result.terminals[0].handle
orca terminal close --terminal <handle> --json
```

The chat tab has no terminal handle, so `terminal list` shows only the setup terminal. If it lists more than one terminal, close only the one whose preview has the setup marker.

## Wait for it

Chat tabs have no terminal handle, so poll the agent state in a background shell. That way you get one notification when it finishes:

```bash
while true; do
  s=$(orca worktree ps --json | python3 -c 'import json,sys;d=json.load(sys.stdin);a=[x for w in d["result"]["worktrees"] if w["worktreeId"].endswith("<short-task-slug>") for x in (w.get("agents") or [])];print(a[0]["state"] if a else "gone")')
  [ -n "$s" ] && [ "$s" != "working" ] && { echo "state=$s"; break; }
  sleep 15
done
```

## Read the answer

- `orca worktree ps --json`: the agent's `lastAssistantMessage`.
- For the full transcript, run `opencode session list` in the child worktree's path, then `opencode session export <sessionId>`. The transcript also shows which model actually answered.

Check what the agent claims before you pass it on. A small model can invent advisories, versions or file paths, so confirm the important ones yourself.

## Clean up

The child workspace stays after the run. Tell the user its name, and remove it only when they ask.
