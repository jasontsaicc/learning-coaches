# leetcode-coach Design

- Date: 2026-07-01
- Status: approved in brainstorming, pending spec review
- Author: Jason (with Claude)
- Related: `engine/ENGINE.md`, `engine/PLUGIN-INTERFACE.md`, `skills/terraform-coach/` (reference implementation)

## Context and Goal

`leetcode-coach` is the next coach built on the shared teaching engine. Until now it was only a roadmap placeholder ("leetcode to follow" in README and plugin.json). terraform-coach is the live reference implementation; this coach reuses every engine mechanic (Feynman Gate, Failure Escalation, Phase Gate + Examiner, Tiered Scorecard, Spaced Repetition, Gap Mode, Weekly Review) and supplies only the nine domain hooks.

Goal: a coach that trains coding-interview pattern recognition for a senior DevOps target, not solution memorization.

## Locked Decisions (from brainstorming)

1. **Language:** Python only. Language should not block algorithm learning; Python is the author's strongest and is accepted by most interviews.
2. **Lab model:** local pytest harness, the leetcode analog of terraform's `lab-iac.sh`. Objective verification (tests pass), never self-report.
3. **Difficulty ceiling:** NeetCode 150 Easy + Medium. DP capped at 1-D plus basic 2-D. Target is a senior DevOps coding round, not SWE big-tech.
4. **Problem order:** follow NeetCode 150 order.
5. **Core pedagogy (Approach A):** a pattern is the engine "topic"; the brute-to-optimal steps are the chunks. The step E drill is an unseen problem that tests pattern recognition.

## North Star (hook 1)

**Win condition:** Given an unseen NeetCode-150-difficulty Medium, the student can, within interview time: recognize which pattern applies, state the brute-force approach and its complexity, derive the optimal approach, write clean Python that passes the test harness (including a large-N performance test), and explain why the final time/space complexity is the bound it is.

**Tie-break:** when "pattern transfer ability" and "solve more problems" compete for session time, transfer wins. Six patterns learned well enough to recognize in a new problem beats sixty solutions memorized that collapse on a variant.

## Curriculum (hook 2): 8 phases

| Phase | Focus | Representative patterns / problems |
|-------|-------|-------------------------------------|
| P0 | Problem-solving mental model (no new data structure) | Big-O analysis, time/space trade-off, the brute-to-optimal method itself, reading a problem to extract constraints |
| P1 | Arrays / Hashing / Two Pointers | hash map O(1) lookup, converging two pointers. Two Sum, Valid Anagram, 3Sum, Container With Most Water |
| P2 | Sliding Window / Stack | variable window, monotonic stack. Longest Substring Without Repeating, Char Replacement, Valid Parentheses, Daily Temperatures |
| P3 | Binary Search / Linked List | binary search on answer space, fast/slow pointers, reversal. Koko Bananas, Reverse Linked List, Linked List Cycle, Reorder List |
| P4 | Trees (BFS/DFS) | tree recursion, level-order traversal. Invert Tree, Max Depth, LCA, Level Order, Validate BST |
| P5 | Heap / Backtracking | priority queue for top-k, backtracking template. Kth Largest, K Closest, Subsets, Combination Sum |
| P6 | Graphs + 1-D DP (intro) | grid/adjacency BFS/DFS, one-dimensional DP. Number of Islands, Course Schedule, Climbing Stairs, House Robber, Coin Change |
| P7 | Interview sprint | timed mocks, mixed unseen problems, verbalize before coding, pattern recognition under time |

Notes:
- P0 is the mental-model phase with no new data structure, occupying the same slot as terraform-coach P0 (declarative model + state file). The transferable core of leetcode is complexity analysis plus the brute-to-optimal method, taught before any single pattern.
- DP stays at 1-D plus basic 2-D, matching the Easy+Medium ceiling and the senior-DevOps ROI.
- Long-tail patterns (Intervals, Greedy, Trie, Bit Manipulation) are covered inside the P7 sprint rather than as separate phases.
- Per-phase teaching-material files (`references/pN-*.md`) are deferred to follow-up tasks, the same convention terraform-coach uses (its phase reference files are marked "to be created").

## Core Pedagogy: Approach A (pattern-as-topic)

A topic equals one pattern. The chunks inside a topic are the escalating ideas of the brute-to-optimal path, each with its own Feynman Gate:

1. Naive baseline: recognize the brute-force approach and its complexity.
2. Key insight: the invariant or maintained state that collapses the complexity.
3. Optimal template: the reusable code shape for the pattern.
4. Complexity analysis: why the optimal bound holds.

- **Step D (lab):** solve 2-3 representative problems with the pytest harness.
- **Step E (drill):** one unseen problem to test whether the student recognizes the pattern. This is the interview skill and the thing that gets gated.

Hybrid rule: the first problem of a pattern is taught fully brute-to-optimal (steps B/C). Later problems in the same pattern run as lab/drill. This keeps the teaching concrete without sliding into per-problem memorization.

## Lab-Manager (hook 4): pytest harness

Script: `scripts/lab-lc.sh` (leetcode analog of `scripts/lab-iac.sh`).

Per-problem directory layout under the student workspace:

```
~/leetcode-coach/p1-arrays/two-sum/
  solution.py        # student writes
  test_two_sum.py    # provided: normal cases + edge cases + one large-N case
```

`lab-lc.sh <problem-slug>` runs pytest against the problem directory and reports per-case pass/fail plus execution time.

**Complexity tripwire (the key design):** each problem's test file includes a large-N case (for example n = 10^5) with a wall-clock timeout. A brute-force O(n^2) solution passes the small cases but times out on the large-N case and therefore fails. This is the leetcode counterpart of terraform-coach's cost-safety guardrail: it makes "is this actually optimal" objectively testable instead of a coach judgment call, and it removes the sycophancy path where a soft coach waves through a passing-but-brute-force solution.

**Verification criteria (hook 4 contract):** all functional tests green AND the large-N timing test green. Both are objective and machine-checked.

Setup: confirm `python3` and `pytest` are present and report versions before a session. Teardown: clear `__pycache__` / `.pytest_cache`; no cloud resources, so no cost teardown needed.

## Scorecard (hook 5): tiered

- **Primary (present at every tier):** correctness plus the ability to justify the time/space complexity with a concrete reason (not just report the Big-O).
- **Tier 1 (P0-P1):** primary + complexity analysis.
- **Tier 2 (P2-P3):** + pattern recognition (name the pattern before coding), + code clarity.
- **Tier 3 (P4-P5):** + edge-case handling (empty, single element, duplicates, overflow), + communication (verbalize approach before coding, interview style).
- **Tier 4 (P6-P7):** + optimality justification (why this is the best achievable bound), + time management.

Pass threshold is the engine-fixed 60% (2/3, 4/6, 6/9). The coach does not change it.

## Phase Gates (hook 6)

One scope-based pass condition per phase. Examiner inputs are the objective artifacts: `solution.py` + pytest output (including the timing test) + the student's verbatim complexity explanation. Examples:

- **P0 gate:** correctly analyze the time/space complexity of a given code snippet, and, without writing code, explain the brute-to-optimal path for a described problem. Examiner input: verbatim answer only (no lab artifact, same shape as terraform-coach P0).
- **P1 gate:** from scratch, solve an unseen two-pointer/hashing Medium; harness fully green including the large-N test; explain why the hash map makes it O(n). Examiner inputs: `solution.py` + pytest output + verbatim explanation.
- **P7 gate:** timed mock, two unseen Mediums, verbalize approach before coding, harness green, scored on the Tier 4 scorecard.

The engine owns the 3-attempt cap, the failure protocol, and Examiner independence. This hook defines only what "pass" means per phase.

## Portfolio (hook 9)

- Workspace directory: `~/leetcode-coach/`.
- Per-phase artifact: the solved problem directories (`solution.py` files) plus a `patterns.md` playbook where the student writes, in their own words, each pattern's reusable template and when to use it. The playbook is the real pre-interview review artifact and the target of Weekly Review step 6 (artifact audit).
- `progress.md` also lives here. Its schema is engine-owned (`PROGRESS-SCHEMA.md`); the coach supplies only the path.

## Optional Hooks

- **language.md (hook 7):** English default. Problems, code, and complexity discussion are in English to double as reading practice. Each pattern's key insight (the aha moment) may use Traditional Chinese anchor terms, matching the author's 30/70 study style. This is a light hook, not a full ramp policy.
- **narrative.md (hook 8):** skipped for v1. The Teach-to-Learn confused peer stays anonymous (engine default), same as terraform-coach.

## Cadence: daily one-problem study group

The author runs a daily study group with a colleague, one problem per day. This maps to the engine's Micro-mode (one unit of value per sitting):

- A daily sitting runs B to C to D for one problem (teach, solve, harness), passes the Feynman Gate, saves a breakpoint, and stops clean.
- Steps F (Teach-to-Learn) and G (Interview Q&A) do not run per problem; they run once when a pattern is wrapped up, over the pattern's accumulated problems.
- The real study group is a natural Teach-to-Learn target: the coach can close a problem with a one-line prompt such as "when you explain this to your colleague tomorrow, be ready to be asked X."

## Scaffolding and Naming

- Scaffold with: `./scripts/new-coach.sh leetcode-coach --with-language` (lab included by default, narrative omitted).
- Directory name `leetcode-coach` matches the roadmap and the terraform-coach convention. A standalone global skill of the same bare name exists in the environment; the plugin namespace (`learning-coaches:leetcode-coach`) disambiguates. Rename is trivial if collision proves annoying at deploy time; not a design blocker.

## Out of Scope / Deferred

- Hard problems, advanced graphs, advanced DP: not in this coach. Possible future optional phase.
- Go (and any second language): deferred. The lab harness is Python-only for v1.
- Per-phase teaching-material reference files (`references/pN-*.md`): filled in follow-up implementation tasks, not in the scaffold.

## Self-Review Notes

- No placeholders or TODOs remain in this spec; per-phase teaching files are an explicit deferred task, not an unfilled gap.
- Internal consistency checked: the lab tripwire, the Examiner inputs, and the scorecard "optimality" dimension all point at the same objective signal (large-N timing), so optimality is enforced consistently across lab, gate, and scorecard.
- Scope: one coach, following the established 9-hook contract. Focused enough for a single implementation plan.
