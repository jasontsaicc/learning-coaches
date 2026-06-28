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
exit $fail
