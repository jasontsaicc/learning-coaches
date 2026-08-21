#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
ENGINE="engine/ENGINE.md"
GOVERNANCE="engine/GOVERNANCE.md"
required=(
  "## What Is Locked, What Is Free"
  "## Routing"
  "## Teaching Flow (A to H)"
  "## Feynman Gate"
  "## Adversarial Default"
  "## Failure Escalation"
  "## Phase Gates"
  "## Examiner Gate"
  "## Tiered Scorecard"
  "## Weekly Review"
  "## Spaced Repetition"
  "## Gap Mode"
  "## Comeback Protocol"
  "## Depth Ceiling"
  "## Adaptive Pacing"
  "## Teach-to-Learn"
  "## Mistake Registry"
  "## How A Coach Uses This Engine"
)
fail=0
for s in "${required[@]}"; do
  grep -qF "$s" "$ENGINE" || { echo "MISSING: $s"; fail=1; }
done
# guard against the spaced-repetition rhythm drifting
grep -qF "3 -> 7 -> 14" "$ENGINE" || { echo "MISSING: spaced repetition rhythm 3 -> 7 -> 14"; fail=1; }
# guard against the pass threshold drifting
grep -qF "60%" "$ENGINE" || { echo "MISSING: 60% pass threshold"; fail=1; }
# guard the anti-sycophancy invariant against being gutted
grep -qF "Refutation-first" "$ENGINE" || { echo "MISSING: Refutation-first LOCK row"; fail=1; }
grep -qiF "burden of proof" "$ENGINE" || { echo "MISSING: Adversarial Default burden-of-proof rule"; fail=1; }
# guard the Examiner independence lock against being gutted
grep -qiF "never the teaching transcript" "$ENGINE" || { echo "MISSING: Examiner independence lock"; fail=1; }
# guard the engine-owned progress schema (shared by every coach)
SCHEMA="engine/PROGRESS-SCHEMA.md"
[ -s "$SCHEMA" ] || { echo "MISSING or EMPTY: $SCHEMA"; fail=1; }
grep -qiE 'kubernetes|k8s|kube-proxy|system design interview|terraform' "$SCHEMA" \
  && { echo "DOMAIN LEAK in $SCHEMA"; fail=1; }
for s in "Mistake Registry" "Spaced-repetition" "breakpoint" "Curiosity branch" "Scorecard history" "Examiner ledger"; do
  grep -qiF "$s" "$SCHEMA" || { echo "MISSING in $SCHEMA: $s"; fail=1; }
done
[ -s "$GOVERNANCE" ] || { echo "MISSING or EMPTY: $GOVERNANCE"; fail=1; }
for s in "Session-start routing" "WIP limit" "Evidence lifecycle" "Portfolio promotion" "Session close"; do
  grep -qiF "$s" "$GOVERNANCE" || { echo "MISSING in $GOVERNANCE: $s"; fail=1; }
done
GOV_EVALS="engine/evals/evals.json"
[ -s "$GOV_EVALS" ] || { echo "MISSING or EMPTY: $GOV_EVALS"; fail=1; }
if [ -s "$GOV_EVALS" ]; then
  python3 - "$GOV_EVALS" <<'PY' || fail=1
import json, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as handle:
    data = json.load(handle)
evals = data.get("evals", [])
assert len(evals) >= 6, "governance eval suite needs at least 6 cases"
assert all(item.get("expectations") for item in evals), "governance eval expectations must be non-empty"
PY
fi
refs=(
  engine/references/feynman-gate.md
  engine/references/teach-to-learn.md
  engine/references/spaced-repetition.md
  engine/references/gap-mode.md
  engine/references/scorecard-frame.md
  engine/references/weekly-review.md
  engine/references/anti-sycophancy.md
  engine/references/examiner-gate.md
)
for f in "${refs[@]}"; do
  [ -s "$f" ] || { echo "MISSING or EMPTY: $f"; fail=1; }
  grep -qiE 'kubernetes|k8s|kube-proxy|system design interview|terraform' "$f" \
    && { echo "DOMAIN LEAK in engine reference: $f"; fail=1; }
done
exit $fail
