#!/usr/bin/env bash
set -euo pipefail
ENGINE="engine/ENGINE.md"
required=(
  "## What Is Locked, What Is Free"
  "## Routing"
  "## Teaching Flow (A to H)"
  "## Feynman Gate"
  "## Failure Escalation"
  "## Phase Gates"
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
refs=(
  engine/references/feynman-gate.md
  engine/references/teach-to-learn.md
  engine/references/spaced-repetition.md
  engine/references/gap-mode.md
  engine/references/scorecard-frame.md
  engine/references/weekly-review.md
)
for f in "${refs[@]}"; do
  [ -s "$f" ] || { echo "MISSING or EMPTY: $f"; fail=1; }
  grep -qiE 'kubernetes|k8s|kube-proxy|system design interview|terraform' "$f" \
    && { echo "DOMAIN LEAK in engine reference: $f"; fail=1; }
done
exit $fail
