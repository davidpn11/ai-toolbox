"""PreToolUse Bash guard for bundled ai-toolbox subagents.

Profiles are selected by Claude Code's `agent_type` hook input. This keeps the
agent definitions readable while preserving the same per-role command rules.
"""
import json
import re
import sys


SEP = r"(^|[;&|(`\s])"
GIT = SEP + r"git(\s[^;&|]*)?\s"

OUTWARD = [
    GIT + r"""(
        push|reset\s+--hard|clean|rebase|merge|tag|filter-branch|update-ref|
        config|worktree|checkout|switch|stash|branch\s+-[dDmM]
    )(\s|$)""",
    SEP + r"sudo\s",
    SEP + r"rm\s+-[a-zA-Z]*[rR][a-zA-Z]*\s+([^;&|]*\s)?(/|~|\$HOME|\.\.)",
    SEP + r"(npm|pnpm|yarn|bun|cargo|gem)\s+publish",
    SEP + r"(npm|pnpm|yarn|bun)\s[^;&|]*\s(-g|--global)(\s|$)",
    SEP + r"""(wrangler|vercel|netlify|fly|flyctl|firebase|terraform|kubectl|helm)
        \s[^;&|]*(deploy|apply|publish|delete|destroy)""",
    SEP + r"""gh\s+(
        pr\s+(create|merge|close|edit|comment|review)|release|
        repo\s+(create|delete|edit|fork)|issue\s+(create|close|edit|comment)|
        api\s[^;&|]*(-X|--method|-f\s|-F\s)
    )""",
    SEP + r"""(curl|wget)\s[^;&|]*
        (-X\s*(POST|PUT|PATCH|DELETE)|--data|-d\s|-F\s|-T\s|--upload|--post)""",
]

READ_ONLY = OUTWARD + [
    GIT + r"""(
        commit|restore|cherry-pick|revert|am|apply|rm|mv|add|init|clone|pull|
        fetch|branch|notes
    )(\s|$)""",
    SEP + r"""(rm|rmdir|mv|cp|ln|chmod|chown|touch|mkdir|tee|dd|truncate|
        kill|pkill|install)(\s|$)""",
    r"(^|[^-=<>])>{1,2}([^=>]|$)",
    SEP + r"(sed|perl)\s+(-[a-zA-Z]*i|--in-place)",
    SEP + r"""(npm|pnpm|yarn|bun|pip3?|cargo|brew|gem|go)\s+(
        install|i|add|remove|uninstall|update|upgrade|link|get|run|exec|x
    )(\s|$)""",
    SEP + r"(npx|bunx|eval|exec|xargs)\s",
    SEP + r"(curl|wget)\s[^;&|]*(-o\s|-O(\s|$)|--output)",
    r"\|\s*(ba|z|da)?sh(\s|$)",
]

PROFILES = {
    "scout": ("read-only", READ_ONLY),
    "security-engineer": ("read-only", READ_ONLY),
    "runner": ("runner", OUTWARD),
    "fe-engineer": ("writer", OUTWARD),
    "ui-engineer": ("writer", OUTWARD),
    "be-js-engineer": ("writer", OUTWARD),
    "be-rust-engineer": ("writer", OUTWARD),
    "quality-engineer": ("writer", OUTWARD),
}


def command_from_event(event):
    command = (event.get("tool_input") or {}).get("command", "")
    # These redirects are harmless for the guard itself and were ignored by
    # the previous shell hook's write-detection pattern.
    command = re.sub(r"[0-9&]*>>?\s*/dev/null", "", command)
    return re.sub(r"[0-9]*>&[0-9]", "", command)


def main():
    event = json.load(sys.stdin)
    agent_type = event.get("agent_type")
    profile = PROFILES.get(agent_type)
    if not profile or event.get("tool_name") != "Bash":
        return

    name, patterns = profile
    command = command_from_event(event)
    if any(re.search(pattern, command, re.VERBOSE) for pattern in patterns):
        print(
            f"Blocked by the {name} guard (see the delegation skill, helper safety rules): {command}",
            file=sys.stderr,
        )
        raise SystemExit(2)


if __name__ == "__main__":
    main()
