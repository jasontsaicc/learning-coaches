#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
COACH="${1:?usage: lint-coach.sh <coach-dir-name>}"
base="skills/$COACH"
[ -f "$base/SKILL.md" ] || { echo "MISSING: $base/SKILL.md"; exit 1; }
# standalone coach: carries its own teaching loop, does not hang off engine/.
# Check SKILL.md and evals only; skip the engine-coupling checks and the six
# engine hook files below.
if grep -qF 'engine: standalone' "$base/SKILL.md"; then
  [ -s "$base/evals/evals.json" ] || { echo "MISSING or EMPTY: $base/evals/evals.json"; exit 1; }
  exit 0
fi
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
grep -qF "engine/GOVERNANCE.md" "$base/SKILL.md" || { echo "SKILL.md does not read governance"; fail=1; }
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
# Evals are required for every live coach; assertions must carry structured expectations.
evals="$base/evals/evals.json"
[ -s "$evals" ] || { echo "MISSING or EMPTY: $evals"; fail=1; }
if [ -s "$evals" ]; then
  python3 - "$evals" <<'PY' || fail=1
import json, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as handle:
    data = json.load(handle)
assert data.get("evals"), "eval suite must contain at least one case"
for item in data["evals"]:
    assert item.get("id") is not None, "eval case missing id"
    assert item.get("prompt"), "eval case missing prompt"
PY
fi
# lab-manager is conditional; check structure only if present
[ -s "$base/references/lab-manager.md" ] && check_markers references/lab-manager.md 'verif|teardown'
exit $fail
