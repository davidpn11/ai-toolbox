#!/usr/bin/env bash
# session-check: read-only preflight. Prints a markdown table of what this session can do.
# Usage: bash check.sh [dir]   (default: current directory). Never prints secrets.
set -u
DIR="${1:-$PWD}"
cd "$DIR" 2>/dev/null || { echo "cannot cd to $DIR"; exit 2; }

ROWS=()
row() { ROWS+=("| $1 | $2 | $3 | $4 |"); }   # status, area, detail, fix
has() { command -v "$1" >/dev/null 2>&1; }
# Run "$@" with a time limit (macOS has no `timeout`).
limit() { local s=$1; shift; "$@" & local p=$!; ( sleep "$s"; kill "$p" 2>/dev/null ) & local w=$!; wait "$p"; local rc=$?; kill "$w" 2>/dev/null; wait "$w" 2>/dev/null; return $rc; }

# Agent and sandbox
if [ "${CLAUDECODE:-}" = 1 ]; then
  row "✅" "agent" "Claude Code (${CLAUDE_CODE_ENTRYPOINT:-cli})" "-"
elif env | grep -q '^CODEX_'; then
  sb="${CODEX_SANDBOX:-none}"; net=on; [ "${CODEX_SANDBOX_NETWORK_DISABLED:-}" = 1 ] && net=off
  row "✅" "agent" "Codex (sandbox: $sb, network: $net)" "-"
else
  row "⚠️" "agent" "unknown harness" "-"
fi

# Shell and filesystem
row "✅" "shell" "runs commands ($(basename "${SHELL:-sh}"))" "-"
if t=$(mktemp "$DIR/.session-check.XXXXXX" 2>/dev/null); then rm -f "$t"; row "✅" "write" "can write in $DIR" "-"
else row "❌" "write" "cannot write in $DIR" "allow edits in this folder (Claude: acceptEdits or an Edit/Write rule; Codex: sandbox_mode = \"workspace-write\")"; fi

# Network
code=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 6 https://api.github.com 2>/dev/null || true)
if [ "$code" = 200 ]; then row "✅" "network" "github.com reachable" "-"
else row "❌" "network" "api.github.com: ${code:-no answer}" "enable network (Codex: sandbox_workspace_write.network_access = true; Claude: allow curl/gh/git, or check the proxy)"; fi

# Target kind
KIND=none
if top=$(git rev-parse --show-toplevel 2>/dev/null); then KIND=project
elif grep -qs '^## Repos' AGENTS.md || ls -d */.git >/dev/null 2>&1; then KIND=workspace; fi
case $KIND in
  project) row "✅" "target" "Project (git repo at $top)" "-";;
  workspace) row "✅" "target" "Workspace ($(ls -d */.git 2>/dev/null | wc -l | tr -d ' ') repo clones inside)" "-";;
  none) row "⚠️" "target" "plain folder, not a repo or Workspace" "-";;
esac

# Git
REPOS=()
if [ $KIND = project ]; then REPOS=("$top"); elif [ $KIND = workspace ]; then for g in */.git; do [ -e "$g" ] && REPOS+=("$DIR/${g%/.git}"); done; fi
if ! has git; then row "❌" "git" "git not installed" "install git"; fi
for r in ${REPOS[@]+"${REPOS[@]}"}; do
  n=$(basename "$r"); br=$(git -C "$r" branch --show-current 2>/dev/null); url=$(git -C "$r" remote get-url origin 2>/dev/null || true)
  dirty=$(git -C "$r" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  if [ -z "$url" ]; then row "⚠️" "git $n" "branch ${br:-?}, no origin remote, $dirty uncommitted" "add a GitHub remote"; continue; fi
  if GIT_TERMINAL_PROMPT=0 limit 10 git -C "$r" ls-remote --heads origin >/dev/null 2>&1; then
    row "✅" "git $n" "branch ${br:-detached}, origin reachable, $dirty uncommitted" "-"
  else row "❌" "git $n" "cannot reach origin ($url)" "check network and git credentials (gh auth setup-git)"; fi
done

# GitHub CLI
if ! has gh; then row "❌" "gh" "gh not installed" "brew install gh"
elif gh auth status >/dev/null 2>&1; then
  scopes=$(gh auth status 2>&1 | grep -i 'token scopes' | head -1 | sed -E 's/.*[Ss]copes: *//' | tr -d "'")
  row "✅" "gh auth" "logged in (scopes: ${scopes:-unknown})" "-"
  for r in ${REPOS[@]+"${REPOS[@]}"}; do
    url=$(git -C "$r" remote get-url origin 2>/dev/null || true); case $url in *github.com*) ;; *) continue;; esac
    slug=$(echo "$url" | sed -E 's#.*github.com[:/]##; s#\.git$##')
    perm=$(cd "$r" && limit 10 gh repo view "$slug" --json viewerPermission -q .viewerPermission 2>/dev/null || true)
    case $perm in ADMIN|MAINTAIN|WRITE) row "✅" "gh $slug" "$perm: can push and open PRs" "-";;
      "") row "❌" "gh $slug" "repo not visible to this token" "gh auth refresh -s repo";;
      *) row "⚠️" "gh $slug" "$perm: read only, cannot push" "ask for write access, or fork";; esac
  done
else row "❌" "gh auth" "not logged in" "gh auth login"; fi

# Orca
ORCA=${ORCA_CLI_COMMAND:-orca}; [ "$(uname)" = Linux ] && [ -z "${ORCA_CLI_COMMAND:-}" ] && ORCA=orca-ide
if ! has "$ORCA"; then row "⚠️" "orca" "$ORCA CLI not found" "only needed for Workspaces and Workers"
elif limit 10 "$ORCA" status --json >/dev/null 2>&1; then
  cur=$(limit 10 "$ORCA" worktree current --json 2>/dev/null | grep -o '"displayName": *"[^"]*"' | head -1 | sed 's/.*: *"//; s/"$//')
  row "✅" "orca" "running; this folder: ${cur:-not an Orca workspace}" "$([ -z "$cur" ] && echo 'orca repo add --path <dir> (add --kind folder for a Workspace)' || echo -)"
  sk=$(limit 10 "$ORCA" skills installed --json 2>/dev/null)
  for s in orchestration orca-cli; do echo "$sk" | grep -q "\"name\": *\"$s\"" || row "⚠️" "orca skills" "$s missing" "$ORCA skills install"; done
else row "⚠️" "orca" "installed but not reachable" "open Orca ($ORCA open), or allow the connection from this sandbox"; fi

# Tooling
for t in node npx bun; do has $t && row "✅" "$t" "$($t --version 2>/dev/null | head -1)" "-" || row "⚠️" "$t" "not installed" "install if the project needs it"; done

# Skill name clashes: a global skill hides a project skill of the same name
skills_in() { for d in "$@"; do for s in "$d"/*/; do [ -f "$s/SKILL.md" ] && basename "$s"; done; done 2>/dev/null | sort -u; }
g=$(skills_in "$HOME/.claude/skills" "$HOME/.agents/skills")
p=$(skills_in .claude/skills .agents/skills)
if [ -n "$p" ]; then
  clash=$(comm -12 <(echo "$g") <(echo "$p") | grep -v '^$' | tr '\n' ' ')
  if [ -n "$clash" ]; then row "⚠️" "skills" "project copies hidden by globals: $clash" "run /project-setup here to remove them"
  else row "✅" "skills" "$(echo "$p" | grep -c .) project skills, no clash with globals" "-"; fi
fi

# Guards: shared ai-toolbox hooks from the cost-guards plugin
cg=$(grep -ls '"cost-guards@' "$HOME/.claude/settings.json" .claude/settings.json .claude/settings.local.json 2>/dev/null | head -1)
if [ -n "$cg" ]; then row "✅" "cost guards" "plugin enabled ($cg)" "-"
else row "⚠️" "cost guards" "cost-guards plugin not installed: cost and bundled-agent Bash guards are not enforced" "claude plugin marketplace add davidpn11/ai-toolbox && claude plugin install cost-guards@ai-toolbox"; fi
for a in scout runner; do
  f="$HOME/.claude/agents/$a.md"; [ -f ".claude/agents/$a.md" ] && f=".claude/agents/$a.md"
  if [ ! -f "$f" ]; then row "⚠️" "agent $a" "not installed" "copy .agents/agents/$a.md from ai-toolbox to ~/.claude/agents/"
  else row "✅" "agent $a" "installed ($f)" "-"; fi
done

echo "| | Check | Result | Fix |"
echo "|---|---|---|---|"
printf '%s\n' "${ROWS[@]}"
