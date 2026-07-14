#!/usr/bin/env bash
# Lab harness for leetcode-coach. Usage: scripts/lab-lc.sh <problem-dir>
# Exit 0 = all tests green (incl. large-N tripwire). 2 = bad dir. 3 = missing deps.
set -euo pipefail

dir="${1:-}"
[ -d "$dir" ] || { echo "problem dir not found: $dir"; exit 2; }

python3 -c 'import pytest, pytest_timeout' 2>/dev/null \
  || { echo "missing deps. run: pip install pytest pytest-timeout"; exit 3; }

exec python3 -m pytest "$dir" -v --timeout="${LAB_LC_TIMEOUT:-5}" "${@:2}"
