#!/usr/bin/env bash
# Tests the shared plugin PreToolUse Bash guard against cases.txt.
# Usage: bash scripts/agent-guards/test.sh
set -u
cd "$(dirname "$0")/../.."
fail=0
agent_for() { case $1 in read-only) echo scout;; runner) echo runner;; writer) echo fe-engineer;; esac; }
n=0
while IFS='|' read -r level want cmd; do
  [ -z "$level" ] && continue
  n=$((n + 1))
  cmd=$(printf '%b' "$cmd")
  json=$(python3 -I -c 'import json,sys; print(json.dumps({"agent_type": sys.argv[1], "tool_name": "Bash", "tool_input": {"command": sys.argv[2], "description": "push and delete it"}}))' "$(agent_for "$level")" "$cmd")
  printf '%s' "$json" | python3 plugins/cost-guards/hooks/agent_guard.py 2>/dev/null
  rc=$?; got=allow; [ $rc -eq 2 ] && got=block
  [ "$got" = "$want" ] || { echo "FAIL [$level] want $want, got $got: $cmd"; fail=1; }
done < scripts/agent-guards/cases.txt
[ $fail -eq 0 ] && echo "ok: $n cases" || exit 1
