#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
COACH="${1:?usage: lint-coach.sh <coach-dir-name>}"
base="skills/$COACH"
[ -f "$base/SKILL.md" ] || { echo "MISSING: $base/SKILL.md"; exit 1; }
required=(
  references/north-star.md
  references/curriculum.md
  references/teaching-elements.md
  references/scorecard-dims.md
  references/phase-gates.md
  references/portfolio.md
)
fail=0
for f in "${required[@]}"; do
  [ -s "$base/$f" ] || { echo "MISSING or EMPTY: $base/$f"; fail=1; }
done
# the thin SKILL.md must read the engine, not re-implement it
grep -qF "engine/ENGINE.md" "$base/SKILL.md" || { echo "SKILL.md does not read the engine"; fail=1; }
# guard against engine mechanics being copied into the coach
if grep -qiE 'failure escalation|two stages|3 -> 7 -> 14' "$base/SKILL.md"; then
  echo "ENGINE LEAK: $base/SKILL.md re-implements engine mechanics"; fail=1
fi
# an unfilled scaffold must not pass: no TODO sentinels or placeholder tokens may remain
if grep -rqE 'TODO:|__COACH_NAME__|__COACH_TITLE__' "$base"; then
  echo "UNFILLED SCAFFOLD: TODO marker or placeholder token remains in $base"; fail=1
fi
# structural markers: each hook must contain its canonical content words, not just be non-empty.
# markers are case-insensitive and chosen to match existing coaches (terraform uses '## P0 -',
# so we never require the literal word 'phase' -- we count '## ' subsections instead).
check_markers() { # <file> <marker1> [marker2 ...]
  local file="$base/$1"; shift
  [ -s "$file" ] || return 0  # existence is already reported above
  local m
  for m in "$@"; do
    grep -qiE "$m" "$file" || { echo "STRUCTURE: $file missing marker /$m/"; fail=1; }
  done
}
min_subsections() { # <file> <n>
  local file="$base/$1" n="$2"
  [ -s "$file" ] || return 0
  local c; c="$(grep -cE '^## ' "$file" || true)"
  [ "$c" -ge "$n" ] || { echo "STRUCTURE: $file has $c '## ' subsections, needs >= $n"; fail=1; }
}
check_markers references/north-star.md 'win condition' 'tie-break'
check_markers references/curriculum.md 'warm-up'
min_subsections references/curriculum.md 3
check_markers references/teaching-elements.md 'step b' 'step c' 'step e'
check_markers references/scorecard-dims.md 'primary' 'tier 1'
check_markers references/phase-gates.md 'gate'
min_subsections references/phase-gates.md 1
check_markers references/portfolio.md 'workspace' 'artifact'
# lab-manager is conditional; check structure only if present
[ -s "$base/references/lab-manager.md" ] && check_markers references/lab-manager.md 'verif|teardown'
exit $fail
