# Lab Manager

The lab is a local pytest harness; no cloud resources, no cost exposure. The script is
`scripts/lab-lc.sh <problem-dir>`: it runs the problem folder's pytest suite with a
per-test wall-clock cap (`LAB_LC_TIMEOUT`, default 5s) via pytest-timeout.

## Environment Setup

Python 3 with `pytest` and `pytest-timeout` importable. Confirm before a session:
`python3 -m pytest --version`. The harness self-checks: exit 3 with an install hint
when either package is missing, exit 2 when the problem dir does not exist.

## Per-Topic Lab Steps

Each problem lives in its own folder (canonical layout in `portfolio.md`):
`solution.py` plus `test_<slug>.py`. The coach provides the test file; the student
produces `solution.py` per the step-D loop in `teaching-elements.md`. Run:

```
scripts/lab-lc.sh workspaces/leetcode/<phase>/<slug>/
```

**The complexity tripwire (key design):** every test file carries a large-N case
(e.g., n = 10^5) marked `@pytest.mark.timeout(N)`. A brute-force O(n^2) solution
passes the small cases but times out on large-N and fails the run. This makes "is it
actually optimal" machine-checked instead of a coach judgment call, and it removes the
sycophancy path where a soft coach waves through a passing-but-brute-force solution.
When step D targets the brute force deliberately (naive baseline chunk), run pytest
against the small tests only by deselecting the large-N test (`-k "not large_n"`);
the tripwire is for the optimal step and the gates.

## Verification

A lab step passes only when `lab-lc.sh` exits 0: all functional tests green AND the
large-N timing test green. Objective and machine-checked, never self-reported. The
same exit-0 output is the Examiner's lab artifact at phase gates.

## Teardown

Remove `__pycache__/` and `.pytest_cache/` from the problem folders after a session
(`find <workspace> -name '__pycache__' -o -name '.pytest_cache' | xargs rm -rf`).
No cloud resources, so no cost teardown.
