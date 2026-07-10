#!/usr/bin/env bash
# leetcode lab harness: run a problem folder's pytest suite with a per-test wall-clock
# cap. The cap is what makes the large-N case fail a brute-force solution even when the
# small cases pass (the complexity tripwire). Analogous to terraform-coach/scripts/lab-iac.sh.
set -euo pipefail
dir="${1:?usage: lab-lc.sh <problem-dir>}"
[ -d "$dir" ] || { echo "no such problem dir: $dir" >&2; exit 2; }
python3 -c 'import pytest' 2>/dev/null || { echo "pytest missing: pip install pytest pytest-timeout" >&2; exit 3; }
python3 -c 'import pytest_timeout' 2>/dev/null || { echo "pytest-timeout missing: pip install pytest-timeout" >&2; exit 3; }
TIMEOUT="${LAB_LC_TIMEOUT:-5}"
exec python3 -m pytest -q --timeout="$TIMEOUT" "$dir"
