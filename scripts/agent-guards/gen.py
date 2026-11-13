"""Writes the PreToolUse Bash guard into each bundled agent. Run after editing a pattern:
    python3 scripts/agent-guards/gen.py && bash scripts/agent-guards/test.sh
"""
SEP = r'(^|[;&|(`[:space:]])'
GIT = SEP + r'git([[:space:]][^;&|]*)?[[:space:]]'
OUT = [  # outward or irreversible: blocked for every bundled agent
  GIT + r'(push|reset[[:space:]]+--hard|clean|rebase|merge|tag|filter-branch|update-ref|config|worktree|checkout|switch|stash|branch[[:space:]]+-[dDmM])([[:space:]]|$)',
  SEP + r'sudo[[:space:]]',
  SEP + r'rm[[:space:]]+-[a-zA-Z]*[rR][a-zA-Z]*[[:space:]]+([^;&|]*[[:space:]])?(/|~|\$HOME|\.\.)',
  SEP + r'(npm|pnpm|yarn|bun|cargo|gem)[[:space:]]+publish',
  SEP + r'(npm|pnpm|yarn|bun)[[:space:]][^;&|]*[[:space:]](-g|--global)([[:space:]]|$)',
  SEP + r'(wrangler|vercel|netlify|fly|flyctl|firebase|terraform|kubectl|helm)[[:space:]][^;&|]*(deploy|apply|publish|delete|destroy)',
  SEP + r'gh[[:space:]]+(pr[[:space:]]+(create|merge|close|edit|comment|review)|release|repo[[:space:]]+(create|delete|edit|fork)|issue[[:space:]]+(create|close|edit|comment)|api[[:space:]][^;&|]*(-X|--method|-f[[:space:]]|-F[[:space:]]))',
  SEP + r'(curl|wget)[[:space:]][^;&|]*(-X[[:space:]]*(POST|PUT|PATCH|DELETE)|--data|-d[[:space:]]|-F[[:space:]]|-T[[:space:]]|--upload|--post)',
]
READONLY = OUT + [
  GIT + r'(commit|restore|cherry-pick|revert|am|apply|rm|mv|add|init|clone|pull|fetch|branch|notes)([[:space:]]|$)',
  SEP + r'(rm|rmdir|mv|cp|ln|chmod|chown|touch|mkdir|tee|dd|truncate|kill|pkill|install)([[:space:]]|$)',
  r'(^|[^-=<>])>{1,2}([^=>]|$)',
  SEP + r'(sed|perl)[[:space:]]+(-[a-zA-Z]*i|--in-place)',
  SEP + r'(npm|pnpm|yarn|bun|pip3?|cargo|brew|gem|go)[[:space:]]+(install|i|add|remove|uninstall|update|upgrade|link|get|run|exec|x)([[:space:]]|$)',
  SEP + r'(npx|bunx|eval|exec|xargs)[[:space:]]',
  SEP + r'(curl|wget)[[:space:]][^;&|]*(-o[[:space:]]|-O([[:space:]]|$)|--output)',
  r'\|[[:space:]]*(ba|z|da)?sh([[:space:]]|$)',
]
WRITER = OUT
def hook(name, pats):
    pat = '|'.join(pats)
    cmd = ("c=$(sed -E 's/.*\"command\"[[:space:]]*:[[:space:]]*\"(([^\"\\\\]|\\\\.)*)\".*/\\1/' "
           "| sed -E 's/\\\\[nt]/;/g; s#[0-9&]*>>?[[:space:]]*/dev/null##g; s#[0-9]*>&[0-9]##g'); "
           f"printf '%s' \"$c\" | grep -Eq '{pat}' "
           f"&& {{ echo \"Blocked by the {name} guard (see the delegation skill, helper safety rules): $c\" >&2; exit 2; }}; exit 0")
    return cmd

import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEVELS = {'read-only': READONLY, 'runner': WRITER, 'writer': WRITER}
AGENTS = {'scout': 'read-only', 'security-engineer': 'read-only', 'runner': 'runner',
          'fe-engineer': 'writer', 'ui-engineer': 'writer', 'be-js-engineer': 'writer',
          'be-rust-engineer': 'writer', 'quality-engineer': 'writer'}

def block(level):
    return ("hooks:\n  PreToolUse:\n    - matcher: \"Bash\"\n      hooks:\n        - type: command\n"
            "          command: |\n            " + hook(level, LEVELS[level]) + "\n")

if __name__ == '__main__':
    for agent, level in AGENTS.items():
        p = os.path.join(ROOT, '.agents/agents', agent + '.md')
        s = open(p).read()
        fm_end = s.index('\n---\n', 4)
        fm = re.sub(r'\nhooks:\n(  .*\n?)*', '\n', s[:fm_end] + '\n').rstrip('\n')
        open(p, 'w').write(fm + '\n' + block(level).rstrip('\n') + s[fm_end:])
    print(f"wrote hooks into {len(AGENTS)} agents")
