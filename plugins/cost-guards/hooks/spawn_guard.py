"""PreToolUse guard for Agent: stops subagents from silently running on the expensive main model.

- No `model` given, and the subagent type does not pin one: denied. Pick a tier from the
  `delegation` skill and pass its model.
- An explicit top-tier model (opus, fable): asks the user first, because deep-tier helpers are rare.
- Anything else passes.

A subagent type pins a model when its definition in .claude/agents/ or ~/.claude/agents/ sets
`model:` to something other than `inherit`. Built-in types (general-purpose, Explore, Plan) must
pass `model` explicitly.
Setting: AI_TOOLBOX_SPAWN_GUARD=off to disable. Fails open on any error.
"""
import json
import os
import re
import sys

TOP = {"opus", "fable"}


def agent_model(agent_type, cwd):
    for d in (os.path.join(cwd, ".claude", "agents"), os.path.expanduser("~/.claude/agents")):
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if not f.endswith(".md"):
                continue
            text = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
            fm = text.split("\n---", 1)[0]
            if re.search(r"^name:\s*['\"]?%s['\"]?\s*$" % re.escape(agent_type), fm, re.M):
                m = re.search(r"^model:\s*['\"]?([\w.-]+)", fm, re.M)
                return m.group(1) if m else None
    return None


def decide(kind, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": kind,
        "permissionDecisionReason": reason,
    }}))


def tier_of(model):
    model = (model or "").lower()
    return next((t for t in TOP if t in model), None)


def main():
    if os.environ.get("AI_TOOLBOX_SPAWN_GUARD", "").lower() == "off":
        return
    event = json.load(sys.stdin)
    inp = event.get("tool_input") or {}
    agent_type = inp.get("subagent_type") or "general-purpose"
    model = inp.get("model") or agent_model(agent_type, event.get("cwd") or os.getcwd())
    if not model or model == "inherit":
        decide("deny", f"This `{agent_type}` subagent would inherit the main session's model. Choose the "
                       f"tier from the `delegation` skill and pass `model` (haiku for scout and runner work, "
                       f"sonnet for research, reviews and specified tasks). If the job needs the top model, "
                       f"do it in the main session or pass model explicitly. Set AI_TOOLBOX_SPAWN_GUARD=off "
                       f"to disable.")
    elif tier_of(model):
        decide("ask", f"Spawning a `{agent_type}` subagent on {model}, the top tier. The `delegation` skill "
                      f"keeps deep work in the main session. Allow this one?")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
