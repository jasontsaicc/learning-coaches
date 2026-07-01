# leetcode-coach Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `leetcode-coach` on the shared teaching engine that trains coding-interview pattern recognition for a senior-DevOps target and never leaves the student frozen at a blank page.

**Architecture:** A thin `skills/leetcode-coach/SKILL.md` reads `engine/ENGINE.md` and nine domain hook files under `references/`. The engine owns all mechanics (Feynman Gate, Failure Escalation, Phase Gate + Examiner, Tiered Scorecard, Spaced Repetition, Gap Mode, Weekly Review); the hooks supply only leetcode content. A `scripts/lab-lc.sh` pytest harness provides objective step-D verification, with a large-N timing tripwire that fails brute-force solutions even when small tests pass. Learning philosophy is ported from the author's standalone skill at `~/go_senior_devops/leetcode-coach/`.

**Tech Stack:** Bash (scaffold, lint, lab harness), Python 3 + pytest + pytest-timeout (lab), Markdown (engine + hooks).

## Global Constraints

- Spec is authoritative: `docs/superpowers/specs/2026-07-01-leetcode-coach-design.md`. Every task implements part of it.
- Coach directory: `skills/leetcode-coach/`. Optional hooks: language YES, narrative NO (anonymous peer; Yuki deferred as a trivial future add per the author's earlier explicit choice).
- The thin `SKILL.md` must read the engine and must NOT re-implement engine mechanics. `scripts/lint-coach.sh` flags leaks: it rejects the strings `failure escalation`, `two stages`, `3 -> 7 -> 14` (case-insensitive) in SKILL.md.
- No scaffold sentinels may remain anywhere under `skills/leetcode-coach/`: `TODO:`, `__COACH_NAME__`, `__COACH_TITLE__`.
- Required hooks and their lint markers (case-insensitive, from `scripts/lint-coach.sh`):
  - `north-star.md` — must contain `win condition` and `tie-break`.
  - `curriculum.md` — must contain `warm-up`; >= 3 `## ` subsections.
  - `teaching-elements.md` — must contain `step b`, `step c`, `step e`.
  - `scorecard-dims.md` — must contain `primary` and `tier 1`.
  - `phase-gates.md` — must contain `gate`; >= 1 `## ` subsection.
  - `portfolio.md` — must contain `workspace` and `artifact`.
  - `lab-manager.md` (present) — must contain `verif` or `teardown`.
- Language / writing rules (author's global CLAUDE.md): no em dashes; avoid inflated AI vocabulary (delve, leverage, comprehensive, robust, seamless, etc.); no reflex "rule of three"; no "not X but Y" reflex. Git commits: one-line subject only, no body, no attribution of any kind.
- Difficulty ceiling: NeetCode 150 Easy + Medium; DP capped at 1-D + basic 2-D. Solve language: Python only.
- Definition of done for the whole plan: `./scripts/lint-coach.sh leetcode-coach` exits 0, `./scripts/lint-all.sh` exits 0, and `skills/leetcode-coach/scripts/lab-lc.test.sh` passes (or SKIPs cleanly when pytest-timeout is absent).

---

### Task 1: Scaffold the coach and fill the thin SKILL.md

**Files:**
- Create (via script): `skills/leetcode-coach/SKILL.md` and the six required + one language hook under `skills/leetcode-coach/references/`
- Modify: `skills/leetcode-coach/SKILL.md` (fill description; add language row to Hook Map)

**Interfaces:**
- Produces: the coach directory `skills/leetcode-coach/` with stamped hook files that later tasks fill. SKILL.md Hook Map lists north-star, curriculum, teaching-elements, lab-manager, scorecard-dims, phase-gates, portfolio, and (added here) language.

- [ ] **Step 1: Scaffold**

Run: `./scripts/new-coach.sh leetcode-coach --with-language`
Expected: prints `Scaffolded skills/leetcode-coach`. Creates SKILL.md + references/{north-star,curriculum,teaching-elements,lab-manager,scorecard-dims,phase-gates,portfolio,language}.md.

- [ ] **Step 2: Confirm lint fails on the unfilled scaffold (baseline)**

Run: `./scripts/lint-coach.sh leetcode-coach; echo "exit=$?"`
Expected: non-zero exit; reports `UNFILLED SCAFFOLD` and/or `STRUCTURE` lines. This proves lint is active before we fill.

- [ ] **Step 3: Fill the SKILL.md `description` frontmatter**

Replace the `<!-- TODO: ... -->` in the `description:` field with a specific, slightly pushy trigger. Example:
```
description: LeetCode interview coach (Feynman + first-principles, Python). Use PROACTIVELY when the user wants to practice LeetCode / NeetCode 150, coding-interview prep, algorithm patterns (two pointers, sliding window, BFS/DFS, DP), or says they freeze on a problem and need step-by-step guidance from brute force to optimal.
```

- [ ] **Step 4: Add the language hook to the SKILL.md Hook Map**

The scaffold's Hook Map omits optional hooks. Add a row after `portfolio`:
```
| language | `${CLAUDE_SKILL_DIR}/references/language.md` |
```

- [ ] **Step 5: Verify SKILL.md has no leaks and reads the engine**

Run: `grep -qF 'engine/ENGINE.md' skills/leetcode-coach/SKILL.md && echo OK-engine`
Run: `grep -niE 'failure escalation|two stages|3 -> 7 -> 14' skills/leetcode-coach/SKILL.md || echo OK-noleak`
Run: `grep -nE 'TODO:|__COACH_NAME__|__COACH_TITLE__' skills/leetcode-coach/SKILL.md || echo OK-nosentinel`
Expected: `OK-engine`, `OK-noleak`, `OK-nosentinel`.

- [ ] **Step 6: Commit**

```bash
git add skills/leetcode-coach
git commit -m "leetcode-coach: scaffold skeleton and thin entrypoint"
```

---

### Task 2: Lab harness `lab-lc.sh` + its test

**Files:**
- Create: `skills/leetcode-coach/scripts/lab-lc.sh`
- Test: `skills/leetcode-coach/scripts/lab-lc.test.sh`

**Interfaces:**
- Produces: `lab-lc.sh <problem-dir>` runs pytest against a problem folder with a per-test wall-clock cap (env `LAB_LC_TIMEOUT`, default 5s). Exit 0 = all tests green (incl. the large-N timing case); non-zero = a test failed / timed out, missing dir (exit 2), or pytest/pytest-timeout absent (exit 3). This is the objective verification consumed by `lab-manager.md` (Task 8) and the Examiner (`phase-gates.md`, Task 7).

- [ ] **Step 1: Write the failing harness test**

Create `skills/leetcode-coach/scripts/lab-lc.test.sh`:
```bash
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
```

- [ ] **Step 2: Make it executable and run it to see it fail**

Run: `chmod +x skills/leetcode-coach/scripts/lab-lc.test.sh && skills/leetcode-coach/scripts/lab-lc.test.sh; echo "exit=$?"`
Expected: FAIL (lab-lc.sh does not exist yet) — non-zero exit, or `SKIP` line if pytest-timeout is absent. If it SKIPs, install first: `python3 -m pip install --user pytest pytest-timeout` then re-run.

- [ ] **Step 3: Write `lab-lc.sh`**

Create `skills/leetcode-coach/scripts/lab-lc.sh`:
```bash
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
```

- [ ] **Step 4: Make it executable and run the test to verify it passes**

Run: `chmod +x skills/leetcode-coach/scripts/lab-lc.sh && skills/leetcode-coach/scripts/lab-lc.test.sh; echo "exit=$?"`
Expected: `pass=3 fail=0`, exit 0 (or clean `SKIP` if the toolchain is unavailable in this environment).

- [ ] **Step 5: Commit**

```bash
git add skills/leetcode-coach/scripts
git commit -m "leetcode-coach: add lab-lc pytest harness with large-N tripwire"
```

---

### Task 3: north-star.md

**Files:**
- Modify: `skills/leetcode-coach/references/north-star.md`

- [ ] **Step 1: Write the hook**

Replace all TODO markers. Required sections and markers: a `## Win Condition` and a `## Tie-Break` (satisfies `win condition` + `tie-break`). Content, adapted from spec "North Star":
- Win condition (one sentence + a short derivation list): given an unseen NeetCode-150-difficulty Medium, the student can within interview time recognize the pattern, state the brute force and its complexity, derive the optimal, write clean Python that passes the harness including the large-N test, and explain the final complexity bound. Add the line: an articulated, discussable approach counts as real output even without finished code ("an articulable approach IS the deliverable").
- Tie-break: pattern transfer over problem count. Six patterns recognizable in a new problem beats sixty memorized solutions that collapse on a variant. Include a one-line derivation tying it to the interview target.
- Follow the language rules (no em dashes, no inflated vocabulary).

- [ ] **Step 2: Verify markers**

Run: `grep -iqE 'win condition' skills/leetcode-coach/references/north-star.md && grep -iqE 'tie-break' skills/leetcode-coach/references/north-star.md && grep -nE 'TODO:' skills/leetcode-coach/references/north-star.md || echo OK`
Expected: `OK` (both markers present, no TODO).

- [ ] **Step 3: Commit**

```bash
git add skills/leetcode-coach/references/north-star.md
git commit -m "leetcode-coach: fill north-star hook"
```

---

### Task 4: curriculum.md

**Files:**
- Modify: `skills/leetcode-coach/references/curriculum.md`

**Interfaces:**
- Produces: the phase names P0-P7 and per-phase focus that phase-gates.md (Task 8) and teaching-elements.md (Task 6) reference by name.

- [ ] **Step 1: Write the hook**

Replace all TODO markers. Must contain a `warm-up` section and >= 3 `## ` subsections (use one `## ` per phase, so 8 phases easily clears the bar). Content from spec "Curriculum":
- `## Warm-Up Diagnostic (new students only)`: give an unseen easy problem (e.g., Valid Anagram) and listen for whether the student can run the 4-question articulation bridge or freezes at zero. Classify strong / mid / freezes-at-zero; record in progress file. This classification decides how much I-do scaffolding P0 starts with.
- One `## ` per phase P0-P7 with: focus (one line), prerequisites (prior phase gate passed), and a per-phase reference-file pointer `references/pN-*.md` marked "(to be created in a future task)" — same convention terraform-coach uses. Phases and focus exactly per the spec table (P0 mental model + articulation bridge; P1 arrays/hashing/two-pointers; P2 sliding-window/stack; P3 binary-search/linked-list; P4 trees; P5 heap/backtracking; P6 graphs + 1-D DP; P7 interview sprint).
- Problem order follows NeetCode 150.

- [ ] **Step 2: Verify markers**

Run: `grep -iq 'warm-up' skills/leetcode-coach/references/curriculum.md && [ "$(grep -cE '^## ' skills/leetcode-coach/references/curriculum.md)" -ge 3 ] && grep -nE 'TODO:' skills/leetcode-coach/references/curriculum.md || echo OK`
Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/leetcode-coach/references/curriculum.md
git commit -m "leetcode-coach: fill curriculum hook (P0-P7)"
```

---

### Task 5: Port the reference cheatsheets

**Files:**
- Create: `skills/leetcode-coach/references/problem-solving-framework.md`
- Create: `skills/leetcode-coach/references/pattern-cheatsheet.md`
- Create: `skills/leetcode-coach/references/complexity-cheatsheet.md`
- Create: `skills/leetcode-coach/references/python-dsa-cheatsheet.md`

**Interfaces:**
- Produces: supporting references (not engine hooks) that teaching-elements.md and scorecard-dims.md cite. `problem-solving-framework.md` holds the 4-question articulation bridge and Step 2.5; `pattern-cheatsheet.md` holds the ~8-10 Python skeletons.

- [ ] **Step 1: Port `problem-solving-framework.md`**

Copy `~/go_senior_devops/leetcode-coach/references/problem-solving-framework.md` and keep it as-is (it already matches the engine philosophy: 4-step framework, Step 2.5 articulation bridge, "an articulable approach IS the deliverable"). Trim any references to standalone-skill modes that do not exist in the engine coach.

- [ ] **Step 2: Port `pattern-cheatsheet.md`**

Copy `~/go_senior_devops/leetcode-coach/references/pattern-cheatsheet.md`. Trim to the Easy+Medium ceiling: keep Arrays/Hashing, Two Pointers, Sliding Window, Stack, Binary Search, Linked List, Trees, Heap, Backtracking, Graphs, 1-D DP, 2-D DP, Greedy, Intervals; drop or mark "out of scope (Hard)" for Advanced Graphs (Dijkstra/MST) beyond what P6 needs.

- [ ] **Step 3: Port `complexity-cheatsheet.md` and `python-dsa-cheatsheet.md`**

Copy both from `~/go_senior_devops/leetcode-coach/references/`. These feed P0's complexity teaching and the mechanical-手感 flagging. Keep verbatim unless something references a nonexistent engine mode.

- [ ] **Step 4: Verify no scaffold sentinels leaked and files are non-empty**

Run: `for f in problem-solving-framework pattern-cheatsheet complexity-cheatsheet python-dsa-cheatsheet; do test -s skills/leetcode-coach/references/$f.md && echo "OK $f" || echo "EMPTY $f"; done`
Run: `grep -rnE 'TODO:|__COACH_NAME__|__COACH_TITLE__' skills/leetcode-coach/references/ || echo OK-nosentinel`
Expected: four `OK` lines and `OK-nosentinel`.

- [ ] **Step 5: Commit**

```bash
git add skills/leetcode-coach/references/problem-solving-framework.md skills/leetcode-coach/references/pattern-cheatsheet.md skills/leetcode-coach/references/complexity-cheatsheet.md skills/leetcode-coach/references/python-dsa-cheatsheet.md
git commit -m "leetcode-coach: port framework and cheatsheet references"
```

---

### Task 6: teaching-elements.md

**Files:**
- Modify: `skills/leetcode-coach/references/teaching-elements.md`

**Interfaces:**
- Consumes: phase names from curriculum.md (Task 4); the 4-question bridge and skeletons from Task 5 references.
- Produces: the content the engine pours into steps B, C, D, E. Must define the blank-page machinery once so scorecard-dims and phase-gates can reference "the articulation bridge" and "cold solve".

- [ ] **Step 1: Write the hook**

Replace all TODO markers. Must contain `step b`, `step c`, `step e` (use headers `## Step B: ...`, `## Step C: ...`, `## Step E: ...`; a `## Step D:` too). Model the structure on terraform-coach's teaching-elements.md. Required content:
- `## Blank-Page Handling (cross-cutting)`: the articulation bridge (4 questions), gradual release (I do → we do → you do), stuck-at-zero rule (never ask a frozen student to generate; show one worked think-aloud, then fade to fill-in-the-blank), skeleton-first, draw-to-teach with real numbers. Point to `references/problem-solving-framework.md` for the full bridge. This is the section that operationalizes spec "Blank-Page Handling".
- `## Step B: Scenario Intro`: a short per-phase table of one-line interview/real-world hooks (why this pattern matters), like terraform's step-B table.
- `## Step C: First-principles + chunks`: for each pattern, the underlying reason the optimal collapses the brute force (e.g., "a hash map trades O(n) space for O(1) lookup so the O(n^2) scan for a complement becomes one pass"), followed by the ordered chunk list (naive baseline → key insight → optimal template → complexity). Cite the skeleton in `pattern-cheatsheet.md`.
- `## Step D: Hands-On (guided by default)`: the we-do lab loop — articulation bridge aloud, coach presents skeleton with 2-3 blanks each paired with a "why" question, student fills, then types blind; verify with `scripts/lab-lc.sh <slug>` (all tests green incl. large-N). Scaffolding fades problem by problem.
- `## Step E: Drill`: two drills — Cold Solve (unseen problem; deliverable is a discussable approach; score mapping + articulation, not just whether code ran) and Skeleton Fluency (type a known skeleton cold, zero bugs). Both feed the Mistake Registry.
- `## Skeleton Registry` (optional domain registry): the ~8-10 skeletons with a one-line "when to use" trigger each, reusing the registry interval fields from PROGRESS-SCHEMA.md section 7.
- Do NOT restate engine mechanics (no "Failure Escalation", "two stages", "3 -> 7 -> 14"); reference them by intent only.

- [ ] **Step 2: Verify markers and no engine leak**

Run: `for m in 'step b' 'step c' 'step e'; do grep -iq "$m" skills/leetcode-coach/references/teaching-elements.md && echo "OK $m" || echo "MISS $m"; done`
Run: `grep -niE 'failure escalation|two stages|3 -> 7 -> 14' skills/leetcode-coach/references/teaching-elements.md || echo OK-noleak`
Run: `grep -nE 'TODO:' skills/leetcode-coach/references/teaching-elements.md || echo OK-nosentinel`
Expected: three `OK` lines, `OK-noleak`, `OK-nosentinel`. (Engine-leak strings are only lint-checked in SKILL.md, but keep hooks clean too.)

- [ ] **Step 3: Commit**

```bash
git add skills/leetcode-coach/references/teaching-elements.md
git commit -m "leetcode-coach: fill teaching-elements with blank-page machinery"
```

---

### Task 7: scorecard-dims.md

**Files:**
- Modify: `skills/leetcode-coach/references/scorecard-dims.md`

- [ ] **Step 1: Write the hook**

Replace all TODO markers. Must contain `primary` and `tier 1`. Model on terraform-coach's scorecard-dims.md. Content from spec "Scorecard":
- `## Primary Dimension (always on, all tiers)`: correctness plus justifying the time/space complexity with a concrete reason (not just reporting Big-O).
- `## Tier 1 (P0-P1 phases)`: primary + **approach articulation** (can the student run the 4-question bridge aloud and turn a problem into plain-language decisions?). State explicitly that articulation is scored from day one because it is the student's biggest gap and what interviews most reward.
- `## Tier 2 (P2-P3)`: + pattern recognition (name + justify the match), + code clarity.
- `## Tier 3 (P4-P5)`: + edge-case handling, + communication (think aloud while coding).
- `## Tier 4 (P6-P7)`: + optimality justification, + time management.
- Do not redefine the 60% threshold.

- [ ] **Step 2: Verify markers**

Run: `grep -iq 'primary' skills/leetcode-coach/references/scorecard-dims.md && grep -iq 'tier 1' skills/leetcode-coach/references/scorecard-dims.md && grep -nE 'TODO:' skills/leetcode-coach/references/scorecard-dims.md || echo OK`
Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/leetcode-coach/references/scorecard-dims.md
git commit -m "leetcode-coach: fill scorecard-dims (articulation at tier 1)"
```

---

### Task 8: phase-gates.md

**Files:**
- Modify: `skills/leetcode-coach/references/phase-gates.md`

**Interfaces:**
- Consumes: phase names (Task 4), scorecard tiers (Task 7), `lab-lc.sh` output shape (Task 2).
- Produces: per-phase pass conditions and the exact Examiner input list per gate.

- [ ] **Step 1: Write the hook**

Replace all TODO markers. Must contain `gate` and >= 1 `## `. Model on terraform-coach's phase-gates.md: one `## PN Gate - ...` per phase, each with a Pass condition, an **Examiner inputs** line naming the objective artifacts, and a numbered "Specifically, the student must:" list (the Examiner scores n/total against these; 60% threshold). Content from spec "Phase Gates":
- P0: run the 4-question bridge aloud on a described problem and produce a codeable plan without freezing, and correctly analyze the time/space complexity of a given snippet. Examiner input: verbatim answer only (no lab artifact).
- P1-P6: solve an unseen Medium in the phase's pattern from scratch; harness fully green including the large-N test; explain the complexity. Examiner inputs: `solution.py` (fenced) + `lab-lc.sh` pytest output + verbatim complexity/articulation explanation.
- P7: timed mock, two unseen Mediums, verbalize approach before coding, harness green, Tier 4 scorecard as the footer lens.
- State each gate is scored on its numbered criteria (60%); the tier scorecard is the footer quality lens.

- [ ] **Step 2: Verify markers**

Run: `grep -iq 'gate' skills/leetcode-coach/references/phase-gates.md && [ "$(grep -cE '^## ' skills/leetcode-coach/references/phase-gates.md)" -ge 1 ] && grep -nE 'TODO:' skills/leetcode-coach/references/phase-gates.md || echo OK`
Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/leetcode-coach/references/phase-gates.md
git commit -m "leetcode-coach: fill phase-gates (P0-P7 with Examiner inputs)"
```

---

### Task 9: lab-manager.md

**Files:**
- Modify: `skills/leetcode-coach/references/lab-manager.md`

- [ ] **Step 1: Write the hook**

Replace all TODO markers. Must contain `verif` or `teardown`. Model on terraform-coach's lab-manager.md. Content:
- What `scripts/lab-lc.sh <problem-dir>` does: runs the problem folder's pytest suite with a per-test wall-clock cap (`LAB_LC_TIMEOUT`, default 5s).
- Setup: Python 3 + `pytest` + `pytest-timeout`; the harness exits 3 with an install hint if either is missing.
- The complexity tripwire: each problem's test file carries a large-N case with `@pytest.mark.timeout(N)`; a brute-force solution passes small cases but the large-N case times out and fails. This is the objective "is it optimal" check.
- `## Verification`: a phase gate's lab half passes only when `lab-lc.sh` exits 0 (all functional tests AND the large-N timing test green). Objective, machine-checked, not self-reported.
- `## Teardown`: clear `__pycache__` / `.pytest_cache`; no cloud resources, so no cost teardown.
- Per-problem folder layout: point to portfolio.md as the canonical layout (do not duplicate it).

- [ ] **Step 2: Verify marker**

Run: `grep -iqE 'verif|teardown' skills/leetcode-coach/references/lab-manager.md && grep -nE 'TODO:' skills/leetcode-coach/references/lab-manager.md || echo OK`
Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/leetcode-coach/references/lab-manager.md
git commit -m "leetcode-coach: fill lab-manager hook"
```

---

### Task 10: portfolio.md

**Files:**
- Modify: `skills/leetcode-coach/references/portfolio.md`

- [ ] **Step 1: Write the hook**

Replace all TODO markers. Must contain `workspace` and `artifact`. Content from spec "Portfolio" (this file is the canonical workspace layout; other hooks point here):
- `## Workspace Directory`: `~/leetcode-coach/` by default; may relocate to the student's own practice repo; if unclear, ask once and record the path at the top of `progress.md`.
- The canonical layout block (verbatim from the spec): `progress.md`, `patterns.md`, and `<phase>/<slug>/{solution.py,test_<slug>.py,notes.md}`.
- Path definitions: solution `~/leetcode-coach/<phase>/<slug>/solution.py` (what `lab-lc.sh` runs and the Examiner receives); notes `~/leetcode-coach/<phase>/<slug>/notes.md` (written in engine step H); playbook `patterns.md`.
- `## Per-Phase Artifacts`: P0 no artifact (mental model). P1-P6: the solved problem folders for that phase's patterns plus the `patterns.md` entries (each pattern's skeleton, its 4-question bridge, and when to use it). P7: the full `patterns.md` playbook complete plus the timed-mock result. `patterns.md` is the Weekly Review step-6 audit target.
- `progress.md` schema is engine-owned; coach supplies only the path.

- [ ] **Step 2: Verify markers**

Run: `grep -iq 'workspace' skills/leetcode-coach/references/portfolio.md && grep -iq 'artifact' skills/leetcode-coach/references/portfolio.md && grep -nE 'TODO:' skills/leetcode-coach/references/portfolio.md || echo OK`
Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/leetcode-coach/references/portfolio.md
git commit -m "leetcode-coach: fill portfolio hook (workspace + paths)"
```

---

### Task 11: language.md

**Files:**
- Modify: `skills/leetcode-coach/references/language.md`

- [ ] **Step 1: Write the hook**

Replace all TODO markers. Content from spec "Optional Hooks":
- Default language: English. Problems, code, and complexity discussion in English to double as reading practice.
- Anchor policy: each pattern's key insight (the aha moment) may use Traditional Chinese anchor terms. This is a light anchor policy, not a full ramp: no scheduled transition, just Chinese allowed at the insight moment.

- [ ] **Step 2: Verify no sentinels**

Run: `grep -nE 'TODO:|__COACH_NAME__|__COACH_TITLE__' skills/leetcode-coach/references/language.md || echo OK`
Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/leetcode-coach/references/language.md
git commit -m "leetcode-coach: fill language hook (English + zh anchors)"
```

---

### Task 12: Full lint, plugin wiring, README

**Files:**
- Modify: `README.md`
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 1: Run the coach lint (must pass now)**

Run: `./scripts/lint-coach.sh leetcode-coach; echo "exit=$?"`
Expected: no output, `exit=0`. If any `STRUCTURE`/`MISSING`/`UNFILLED`/`ENGINE LEAK` line appears, fix that hook and re-run before continuing.

- [ ] **Step 2: Run the lab harness test**

Run: `skills/leetcode-coach/scripts/lab-lc.test.sh; echo "exit=$?"`
Expected: `pass=3 fail=0` exit 0, or a clean `SKIP` line exit 0.

- [ ] **Step 3: Run the repo-wide lint**

Run: `./scripts/lint-all.sh; echo "exit=$?"`
Expected: `exit=0` (terraform-coach and leetcode-coach both pass).

- [ ] **Step 4: Update README.md**

Change the roadmap sentence so leetcode is a live coach, not a "to follow" item. Replace:
`Initial focus: Terraform/Infrastructure-as-Code, with kubernetes, system design, and leetcode to follow.`
with:
`Initial focus: Terraform/Infrastructure-as-Code and LeetCode, with kubernetes and system design to follow.`

- [ ] **Step 5: Update plugin.json**

In `.claude-plugin/plugin.json`, change the description domains line:
`Domains: Terraform/IaC, with k8s, system design, and leetcode to follow.`
to:
`Domains: Terraform/IaC and LeetCode, with k8s and system design to follow.`

- [ ] **Step 6: Verify the JSON is still valid**

Run: `python3 -c 'import json,sys; json.load(open(".claude-plugin/plugin.json")); print("json OK")'`
Expected: `json OK`.

- [ ] **Step 7: Commit**

```bash
git add README.md .claude-plugin/plugin.json
git commit -m "leetcode-coach: mark coach live in README and plugin manifest"
```

---

## Self-Review

**1. Spec coverage:** North Star → Task 3. Curriculum P0-P7 → Task 4. Blank-Page Handling → Task 6 (+ Task 5 framework port; + Task 7 tier-1 articulation; + Task 8 P0 gate). Approach A pedagogy → Task 6. Lab harness + tripwire → Task 2; documented → Task 9. Scorecard tiers → Task 7. Phase gates + Examiner inputs → Task 8. Portfolio paths (solution/notes/patterns) → Task 10. language hook → Task 11. narrative hook → intentionally omitted (anonymous; recorded in Global Constraints). Content-to-port list → Task 5. Naming/plugin → Tasks 1 + 12. Cadence (Micro-mode / study group) → lives in teaching-elements step D/E framing (Task 6) and is an engine behavior, not a separate file.

**2. Placeholder scan:** hook-content tasks intentionally specify section + marker + source-to-port rather than reproduce full final prose, because the prose sources are real files (`~/go_senior_devops/leetcode-coach/references/`, terraform-coach hooks, and the spec) that the implementer adapts. The two code artifacts (lab-lc.sh, lab-lc.test.sh) carry complete literal content. No "TBD"/"add error handling"/"similar to Task N" placeholders remain.

**3. Type consistency:** the harness contract is stable across tasks — `lab-lc.sh <problem-dir>`, env `LAB_LC_TIMEOUT`, exit 0/2/3, per-test `@pytest.mark.timeout(N)` — referenced identically in Tasks 2, 8, 9. Paths `<phase>/<slug>/{solution.py,test_<slug>.py,notes.md}` are defined once in Task 10 and only pointed to elsewhere.
