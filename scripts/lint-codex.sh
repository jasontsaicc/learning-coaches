#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

fail=0

[ -s AGENTS.md ] || { echo "MISSING or EMPTY: AGENTS.md"; fail=1; }

for coach_dir in skills/*/; do
  coach="$(basename "$coach_dir")"
  [ "$coach" = "_probe" ] && continue
  link=".agents/skills/$coach"

  [ -L "$link" ] || { echo "MISSING CODEX SKILL LINK: $link"; fail=1; continue; }

  expected="$(realpath "$coach_dir")"
  if ! actual="$(realpath "$link")"; then
    echo "BROKEN CODEX SKILL LINK: $link"
    fail=1
    continue
  fi
  [ "$actual" = "$expected" ] || {
    echo "WRONG CODEX SKILL LINK: $link -> $actual (expected $expected)"
    fail=1
  }
  [ -s "$link/SKILL.md" ] || { echo "UNREADABLE CODEX SKILL: $link/SKILL.md"; fail=1; }
done

if grep -RIn 'CLAUDE_SKILL_DIR' skills engine templates/coach; then
  echo "HOST-SPECIFIC SKILL PATH: use paths relative to SKILL.md"
  fail=1
fi

exit "$fail"
