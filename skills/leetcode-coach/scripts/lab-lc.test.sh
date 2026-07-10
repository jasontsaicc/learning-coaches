#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
SH=./lab-lc.sh
pass=0; fail=0
check() { if eval "$1"; then pass=$((pass+1)); else echo "FAIL: $2"; fail=$((fail+1)); fi; }

# The tripwire relies on pytest-timeout. If the toolchain is absent, skip cleanly.
if ! python3 -c 'import pytest, pytest_timeout' 2>/dev/null; then
  echo "SKIP: pytest / pytest-timeout not installed"; exit 0
fi

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

# Fixture A: correct O(n) solution — passes basic AND the large-N timing case.
mkdir -p "$WORK/fast"
cat > "$WORK/fast/solution.py" <<'PY'
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []
PY
cat > "$WORK/fast/test_two_sum.py" <<'PY'
import pytest
from solution import two_sum

def test_basic():
    assert sorted(two_sum([2, 7, 11, 15], 9)) == [0, 1]

@pytest.mark.timeout(3)
def test_large_n():
    n = 100_000
    nums = list(range(n))
    assert two_sum(nums, n * 2 - 3) == [n - 2, n - 1]
PY

# Fixture B: brute-force O(n^2) solution — passes basic, times out on large-N.
mkdir -p "$WORK/slow"
cat > "$WORK/slow/solution.py" <<'PY'
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
PY
cp "$WORK/fast/test_two_sum.py" "$WORK/slow/test_two_sum.py"

if LAB_LC_TIMEOUT=3 $SH "$WORK/fast" >/dev/null 2>&1; then a=1; else a=0; fi
check '[[ "$a" -eq 1 ]]' "correct O(n) solution passes the harness"

if LAB_LC_TIMEOUT=3 $SH "$WORK/slow" >/dev/null 2>&1; then b=1; else b=0; fi
check '[[ "$b" -eq 0 ]]' "brute-force trips the large-N timeout (tripwire fires)"

if $SH "$WORK/does-not-exist" >/dev/null 2>&1; then c=1; else c=0; fi
check '[[ "$c" -eq 0 ]]' "missing problem dir exits non-zero"

echo "pass=$pass fail=$fail"
[ "$fail" -eq 0 ]
