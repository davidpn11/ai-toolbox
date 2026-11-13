"""Checks the skills and agents: every SKILL.md is discoverable by the `skills` CLI, frontmatter is valid,
and every skill, subagent, and Markdown link that a file names exists.
Usage: python3 scripts/check-skills.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, '.agents/skills')
found = {}

def walk(d, depth=1):
    # Mirrors vercel-labs/skills walkSkillDirs: stops below a found skill, at most 3 levels deep.
    for e in sorted(os.listdir(d)):
        c = os.path.join(d, e)
        if not os.path.isdir(c):
            continue
        if os.path.isfile(os.path.join(c, 'SKILL.md')):
            found[e] = c
        elif depth < 3:
            walk(c, depth + 1)

walk(BASE)
errors = []
all_md = {os.path.join(dp, 'SKILL.md') for dp, _, fs in os.walk(BASE) if 'SKILL.md' in fs}
hidden = all_md - {os.path.join(d, 'SKILL.md') for d in found.values()}
errors += [f"hidden from the skills CLI: {os.path.relpath(h, ROOT)}" for h in sorted(hidden)]

user_only = set()
for name, d in found.items():
    fm = re.match(r'---\n(.*?)\n---\n', open(os.path.join(d, 'SKILL.md')).read(), re.S)
    if not fm:
        errors.append(f"{name}: no frontmatter"); continue
    n = re.search(r'^name: (.+)$', fm.group(1), re.M)
    if not n or n.group(1).strip() != name:
        errors.append(f"{name}: frontmatter name does not match its folder")
    if not re.search(r'^description: ', fm.group(1), re.M):
        errors.append(f"{name}: no description")
    if 'disable-model-invocation: true' in fm.group(1):
        user_only.add(name)

agents = {f[:-3] for f in os.listdir(os.path.join(ROOT, '.agents/agents')) if f.endswith('.md')}
for dp, _, fs in os.walk(os.path.join(ROOT, '.agents')):
    for f in fs:
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f)
        s = open(p).read()
        rel = os.path.relpath(p, ROOT)
        for m in re.findall(r'Skill tool with [`"]([a-z-]+)[`"]', s):
            if m not in found:
                errors.append(f"{rel}: calls missing skill {m}")
            elif m in user_only:
                errors.append(f"{rel}: calls user-only skill {m}")
        for m in re.findall(r'the `([a-z-]+)` (?:skill|subagent)', s):
            if m not in found and m not in agents and m not in ('orchestration', 'orca-cli'):  # Orca ships those two
                errors.append(f"{rel}: names missing {m}")
        if rel.startswith('.agents/agents'):
            fm = s.split('\n---\n', 1)[0]
            block = re.search(r'^skills:\n((?:  - .*\n)+)', fm + '\n', re.M)
            for m in re.findall(r'  - ([a-z-]+)', block.group(1) if block else ''):
                if m not in found:
                    errors.append(f"{rel}: preloads missing skill {m}")
                elif m in user_only:
                    errors.append(f"{rel}: preloads user-only skill {m}")
        prose = re.sub(r'```.*?```', '', s, flags=re.S)  # links inside code blocks are examples
        for m in re.findall(r'\]\(([^)#:]+\.md)\)', prose):
            if not os.path.exists(os.path.join(dp, m)):
                errors.append(f"{rel}: broken link {m}")
        if re.search(r'\]\(\.\./|`\.\./[a-z-]+/SKILL\.md', s):
            errors.append(f"{rel}: relative path into another skill (breaks after install)")

print(f"{len(found)} skills discoverable, {len(agents)} subagents, user-only: {sorted(user_only)}")
print('\n'.join(errors) or 'no errors')
sys.exit(1 if errors else 0)
