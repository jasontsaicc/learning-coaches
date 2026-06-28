#!/usr/bin/env bash
set -euo pipefail
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
if grep -qiE 'failure escalation|two-stage verification|3 -> 7 -> 14' "$base/SKILL.md"; then
  echo "ENGINE LEAK: $base/SKILL.md re-implements engine mechanics"; fail=1
fi
exit $fail
