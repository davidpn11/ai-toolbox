"""PreToolUse guard for Read and Bash: blocks whole-file reads of large text files in the main session.

A large file read in full lands in the expensive model's context. The guard sends that read to a
cheap reader instead (the `scout` subagent), or to a targeted read of the section that matters.
Passes through: subagents (they are the cheap readers), Read with offset or limit, small files,
binary files, and shell reads whose output is piped onward.

Settings (environment): AI_TOOLBOX_READ_LINES (default 350), AI_TOOLBOX_READ_GUARD=off to disable.
Fails open: any error allows the call, because this is a cost guard, not a safety boundary.
"""
import json
import os
import re
import shlex
import sys

READERS = {"cat", "less", "more", "bat", "nl"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".ipynb", ".svg", ".ico", ".zip", ".gz"}


def threshold():
    try:
        return int(os.environ.get("AI_TOOLBOX_READ_LINES", "350"))
    except ValueError:
        return 350


def line_count(path, cwd, limit):
    """Lines in a text file, counting only up to limit + 1. None for missing or binary files."""
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(cwd, path)
    if os.path.splitext(path)[1].lower() in SKIP_EXT or not os.path.isfile(path):
        return None
    lines = 0
    with open(path, "rb") as f:
        head = f.read(8192)
        if b"\0" in head:
            return None
        lines = head.count(b"\n")
        while lines <= limit:
            chunk = f.read(65536)
            if not chunk:
                break
            lines += chunk.count(b"\n")
    return lines


def big_files_read_by_shell(command, cwd, limit):
    """Files over the limit that a pipeline's last command prints straight to the model."""
    found = []
    for chain in re.split(r"&&|\|\||;|\n", command):
        stages = chain.split("|")
        try:
            argv = shlex.split(stages[-1])
        except ValueError:
            continue
        if not argv or os.path.basename(argv[0]) not in READERS:
            continue
        for arg in argv[1:]:
            if arg.startswith("-"):
                continue
            n = line_count(arg, cwd, limit)
            if n is not None and n > limit:
                found.append((arg, n))
    return found


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))


def advice(path, n, limit):
    return (f"{path} has more than {limit} lines (counted {n}). Reading it whole puts it all in the main "
            f"model's context. Instead: Grep for what you need, then Read with offset and limit; or send "
            f"the `scout` subagent (fast tier) to read it and report the relevant sections with line numbers. "
            f"Subagents are not blocked. To turn this off, set AI_TOOLBOX_READ_GUARD=off.")


def main():
    if os.environ.get("AI_TOOLBOX_READ_GUARD", "").lower() == "off":
        return
    event = json.load(sys.stdin)
    if event.get("agent_id"):
        return
    tool = event.get("tool_name")
    inp = event.get("tool_input") or {}
    cwd = event.get("cwd") or os.getcwd()
    limit = threshold()
    if tool == "Read":
        if inp.get("offset") is not None or inp.get("limit") is not None:
            return
        n = line_count(inp.get("file_path", ""), cwd, limit)
        if n is not None and n > limit:
            deny(advice(inp["file_path"], n, limit))
    elif tool == "Bash":
        found = big_files_read_by_shell(inp.get("command", ""), cwd, limit)
        if found:
            path, n = found[0]
            deny(advice(path, n, limit) + " Piping the output onward (to grep, head, wc) is allowed.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
