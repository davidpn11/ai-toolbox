#!/usr/bin/env bash
# Tests the PreToolUse Bash guard as shipped in .agents/agents/*.md against cases.txt.
# Usage: bash scripts/agent-guards/test.sh
set -u
cd "$(dirname "$0")/../.."
hook() { awk '/command: \|/{getline; sub(/^ +/, ""); print; exit}' ".agents/agents/$1.md"; }
fail=0
# Agents at one level must ship the same guard.
for group in "scout security-engineer" "fe-engineer ui-engineer be-js-engineer be-rust-engineer quality-engineer"; do
  set -- $group; ref=$(hook "$1")
  for a in "$@"; do [ "$(hook "$a")" = "$ref" ] || { echo "FAIL: $a guard differs from $1"; fail=1; }; done
done
agent_for() { case $1 in read-only) echo scout;; runner) echo runner;; writer) echo fe-engineer;; esac; }
n=0
while IFS='|' read -r level want cmd; do
  [ -z "$level" ] && continue
  n=$((n + 1))
  cmd=$(printf '%b' "$cmd")
  json=$(python3 -I -c 'import json,sys; print(json.dumps({"tool_name": "Bash", "tool_input": {"command": sys.argv[1], "description": "push and delete it"}}))' "$cmd")
  printf '%s' "$json" | sh -c "$(hook "$(agent_for "$level")")" 2>/dev/null
  rc=$?; got=allow; [ $rc -eq 2 ] && got=block
  [ "$got" = "$want" ] || { echo "FAIL [$level] want $want, got $got: $cmd"; fail=1; }
done < scripts/agent-guards/cases.txt
[ $fail -eq 0 ] && echo "ok: $n cases" || exit 1
