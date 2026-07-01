# leetcode-coach Design

- Date: 2026-07-01
- Status: approved in brainstorming, pending spec review
- Author: Jason (with Claude)
- Related: `engine/ENGINE.md`, `engine/PLUGIN-INTERFACE.md`, `skills/terraform-coach/` (reference implementation), `~/go_senior_devops/leetcode-coach/` (standalone skill; source of the learning philosophy this coach ports onto the engine)

## Context and Goal

`leetcode-coach` is the next coach built on the shared teaching engine. Until now it was only a roadmap placeholder ("leetcode to follow" in README and plugin.json). terraform-coach is the live reference implementation for the engine mechanics; the standalone skill at `~/go_senior_devops/leetcode-coach/` is the source of the leetcode teaching philosophy. This coach refactors that philosophy onto the shared engine so it inherits the family's mechanics (Examiner independence, spaced-repetition rhythm, Weekly Review, Gap Mode, engine-owned progress schema) instead of reinventing them.

Goal: a coach that trains coding-interview pattern recognition for a senior DevOps target, and that never leaves the student frozen at a blank page.

## Locked Decisions (from brainstorming)

1. **Language:** Python only. Language should not block algorithm learning; Python is the author's strongest and is accepted by most interviews.
2. **Lab model:** local pytest harness, the leetcode analog of terraform's `lab-iac.sh`. Objective verification (tests pass), never self-report.
3. **Difficulty ceiling:** NeetCode 150 Easy + Medium. DP capped at 1-D plus basic 2-D. Target is a senior DevOps coding round, not SWE big-tech.
4. **Problem order:** follow NeetCode 150 order.
5. **Core pedagogy (Approach A):** a pattern is the engine "topic"; the brute-to-optimal steps are the chunks. The step E drill is an unseen problem that tests pattern recognition.
6. **Primary design constraint — the blank page:** the student often can write nothing at all when facing a problem. Beating that freeze is a first-class requirement, not an edge case. Every teaching element is built so the student is never asked to generate from zero; see "Blank-Page Handling" below.

## North Star (hook 1)

**Win condition:** Given an unseen NeetCode-150-difficulty Medium, the student can, within interview time: recognize which pattern applies, state the brute-force approach and its complexity, derive the optimal approach, write clean Python that passes the test harness (including a large-N performance test), and explain why the final time/space complexity is the bound it is.

A discussable, articulated approach counts as real output even when the code is incomplete. "An articulable approach IS the deliverable" — interviewers score the conversation, not only the final code.

**Tie-break:** when "pattern transfer ability" and "solve more problems" compete for session time, transfer wins. Six patterns learned well enough to recognize in a new problem beats sixty solutions memorized that collapse on a variant.

## Blank-Page Handling (the core teaching stance)

This is the design's center of gravity, ported from the standalone skill (`SKILL.md` Mode 1 "stuck at zero" + `references/problem-solving-framework.md` Step 2.5). It layers on top of the engine's Failure Escalation; the engine ladder is reactive (after a failed gate), this one is for the first move, before any attempt exists.

**The articulation bridge (4 plain-language questions).** Before writing any code, the student answers, in plain sentences:
1. What am I computing? (the quantity and how it is built)
2. What must I try — what is the brute force? (say the O(n^2)/O(2^n) version first, always)
3. How do I shrink the work / move? (which pointer or branch moves, and why that move is safe)
4. When do I stop?

The first line of code falls out of Q1/Q3 almost mechanically (`seen = {}`, `l, r = 0, len(a)-1`). The code is a transcription of decisions already made in words, not generation from nothing.

**Gradual release (I do → we do → you do).** The scaffolding fades across repetitions:
- **I do (worked example):** on a pattern's first problem, or whenever the student is stuck at zero, the coach narrates ONE full think-aloud through the 4 questions and lets the skeleton fall out of the words. Worked-example-before-solo: a narrated example beats "just try" for a cold start. Never ask a frozen student to generate; generation is the jammed function.
- **We do (scaffolded fill-in-the-blank):** the coach presents the skeleton with 2-3 blanks, each blank paired with a "why" question ("what goes here, and why a set not a list?"). The student fills the blanks. This is the default path for step D lab work early in a pattern.
- **You do (blind, then cold):** the student types the whole skeleton blind, then re-does it cold the next day with zero bugs. Cold-next-day is the real acceptance test, and it maps directly to the engine's spaced-repetition rhythm.

**Skeleton-first.** The unit of practice is the pattern skeleton (~8-10 skeletons cover most of NeetCode 150), not the whole problem. Each problem is a skeleton plus two problem-specific lines. Drilling skeletons compounds; drilling whole problems one-by-one does not.

**Draw to teach.** When teaching a pattern, draw a text diagram using the problem's actual numbers, showing 2-3 steps of motion (not a generic abstract box). Seeing the pattern move is the lesson; the waste the optimization removes should be visible before the optimized code appears.

**Candidate for engine promotion (deferred):** the never-leave-at-zero ladder may generalize to other coaches (writing HCL from scratch has a similar freeze). For now it lives in this coach's hook, consistent with the "harden one vertical first" strategy.

## Curriculum (hook 2): 8 phases

| Phase | Focus | Representative patterns / problems |
|-------|-------|-------------------------------------|
| P0 | Problem-solving mental model (no new data structure) | The 4-question articulation bridge as the anti-freeze tool, Big-O analysis, time/space trade-off, the brute-to-optimal method, reading a problem to extract constraints |
| P1 | Arrays / Hashing / Two Pointers | hash map O(1) lookup, converging two pointers. Two Sum, Valid Anagram, 3Sum, Container With Most Water |
| P2 | Sliding Window / Stack | variable window, monotonic stack. Longest Substring Without Repeating, Char Replacement, Valid Parentheses, Daily Temperatures |
| P3 | Binary Search / Linked List | binary search on answer space, fast/slow pointers, reversal. Koko Bananas, Reverse Linked List, Linked List Cycle, Reorder List |
| P4 | Trees (BFS/DFS) | tree recursion, level-order traversal. Invert Tree, Max Depth, LCA, Level Order, Validate BST |
| P5 | Heap / Backtracking | priority queue for top-k, backtracking template. Kth Largest, K Closest, Subsets, Combination Sum |
| P6 | Graphs + 1-D DP (intro) | grid/adjacency BFS/DFS, one-dimensional DP. Number of Islands, Course Schedule, Climbing Stairs, House Robber, Coin Change |
| P7 | Interview sprint | timed mocks, mixed unseen problems, verbalize before coding, pattern recognition under time |

Notes:
- P0 is the mental-model phase with no new data structure, occupying the same slot as terraform-coach P0. Its centerpiece is the articulation bridge: the student learns the anti-freeze routine before any single pattern, because it is the most transferable skill in the whole curriculum.
- DP stays at 1-D plus basic 2-D, matching the Easy+Medium ceiling and the senior-DevOps ROI.
- Long-tail patterns (Intervals, Greedy, Trie, Bit Manipulation) are covered inside the P7 sprint rather than as separate phases.
- Per-phase teaching-material files (`references/pN-*.md`) are deferred to follow-up tasks, the same convention terraform-coach uses.

## Core Pedagogy: Approach A (pattern-as-topic)

A topic equals one pattern. The chunks inside a topic are the escalating ideas of the brute-to-optimal path, each with its own Feynman Gate:

1. Naive baseline: recognize the brute-force approach and its complexity.
2. Key insight: the invariant or maintained state that collapses the complexity.
3. Optimal template: the reusable code shape for the pattern.
4. Complexity analysis: why the optimal bound holds.

Steps map to the engine as:
- **Step C (core teaching):** teach the chunks; the articulation bridge and draw-to-teach run here. Gradual release governs how much the coach shows vs asks.
- **Step D (lab, guided by default):** the student produces working code, but early in a pattern this runs as we-do (fill-in-the-blank) so a blank page never blocks progress. The pytest harness verifies the final code objectively. Scaffolding fades problem by problem toward blind typing.
- **Step E (drill):** two distinct drills, run per the student's fluency on the pattern:
  - **Cold Solve (approach articulation):** an unseen problem; the deliverable is a discussable plan, not finished code. Scored on mapping-to-pattern + articulation, not just whether code ran. This trains the north star directly.
  - **Skeleton fluency:** type a known pattern's template cold, zero bugs. Trains recall of the ~8-10 skeletons.

Hybrid rule: the first problem of a pattern is taught fully brute-to-optimal (steps B/C). Later problems in the same pattern run as lab/drill. This keeps teaching concrete without sliding into per-problem memorization.

## Lab-Manager (hook 4): pytest harness

Script: `scripts/lab-lc.sh` (leetcode analog of `scripts/lab-iac.sh`).

It operates on the per-problem folder defined in the Portfolio section (`<phase>/<problem-slug>/` holding `solution.py` + `test_<slug>.py`). `lab-lc.sh <problem-slug>` runs pytest against that folder and reports per-case pass/fail plus execution time.

**Complexity tripwire (the key design):** each problem's test file includes a large-N case (for example n = 10^5) with a wall-clock timeout. A brute-force O(n^2) solution passes the small cases but times out on the large-N case and therefore fails. This is the leetcode counterpart of terraform-coach's cost-safety guardrail: it makes "is this actually optimal" objectively testable instead of a coach judgment call, and it removes the sycophancy path where a soft coach waves through a passing-but-brute-force solution.

**Verification criteria (hook 4 contract):** all functional tests green AND the large-N timing test green. Both are objective and machine-checked.

Setup: confirm `python3` and `pytest` are present and report versions before a session. Teardown: clear `__pycache__` / `.pytest_cache`; no cloud resources, so no cost teardown needed.

## Scorecard (hook 5): tiered

- **Primary (present at every tier):** correctness plus the ability to justify the time/space complexity with a concrete reason (not just report the Big-O).
- **Tier 1 (P0-P1):** primary + **approach articulation** (can the student run the 4-question bridge aloud and turn a problem into plain-language decisions?). Articulation is scored from day one because it is the student's biggest gap and the thing interviews most reward.
- **Tier 2 (P2-P3):** + pattern recognition (name the pattern before coding, justify the match), + code clarity.
- **Tier 3 (P4-P5):** + edge-case handling (empty, single element, duplicates, overflow), + communication (think aloud while coding, interview style).
- **Tier 4 (P6-P7):** + optimality justification (why this is the best achievable bound), + time management.

Pass threshold is the engine-fixed 60% (2/3, 4/6, 6/9). The coach does not change it.

## Phase Gates (hook 6)

One scope-based pass condition per phase. Examiner inputs are the objective artifacts: `solution.py` + pytest output (including the timing test) + the student's verbatim articulation/complexity explanation. Examples:

- **P0 gate:** run the 4-question articulation bridge aloud on a described problem and produce a codeable plan without freezing, and correctly analyze the time/space complexity of a given code snippet. Examiner input: verbatim answer only (no lab artifact, same shape as terraform-coach P0).
- **P1 gate:** from scratch, solve an unseen two-pointer/hashing Medium; harness fully green including the large-N test; explain why the hash map makes it O(n). Examiner inputs: `solution.py` + pytest output + verbatim explanation.
- **P7 gate:** timed mock, two unseen Mediums, verbalize approach before coding, harness green, scored on the Tier 4 scorecard.

The engine owns the 3-attempt cap, the failure protocol, and Examiner independence. This hook defines only what "pass" means per phase.

## Portfolio (hook 9)

Workspace directory: `~/leetcode-coach/` by default. Following the standalone skill's rule (artifacts are the student's practice data, kept apart from the coach tool), the coach may relocate this to the student's own practice repo; if the location is unclear it asks once and records the chosen path at the top of `progress.md` so later sessions reuse it.

Canonical workspace layout (this is the single source of truth; the Lab-Manager section reuses it):

```
~/leetcode-coach/
  progress.md                    # engine-owned schema (PROGRESS-SCHEMA.md); coach supplies only the path
  patterns.md                    # cross-pattern playbook (portfolio artifact, audited in Weekly Review)
  p1-arrays/
    two-sum/
      solution.py                # the student's solution (or co-written via fill-in-the-blank)
      test_two_sum.py            # provided tests, incl. the large-N timing case
      notes.md                   # per-problem notes: the diagram drawn, the code, the red mistakes
```

- **Solution path:** `~/leetcode-coach/<phase>/<problem-slug>/solution.py`. This is what `lab-lc.sh <problem-slug>` runs and what the Examiner receives.
- **Notes path:** `~/leetcode-coach/<phase>/<problem-slug>/notes.md`, written in engine step H using the ported `notes-template`. Co-located with the problem so a problem folder is self-contained (diagram + solution + tests + notes together), rather than a separate parallel `notes/` tree.
- **Per-phase artifact:** the solved problem folders plus a `patterns.md` playbook where the student writes, in their own words, each pattern's reusable skeleton, the 4-question bridge for it, and when to use it. The playbook is the real pre-interview review artifact and the target of Weekly Review step 6 (artifact audit).

## Optional Hooks

- **language.md (hook 7):** English default. Problems, code, and complexity discussion are in English to double as reading practice. Each pattern's key insight (the aha moment) may use Traditional Chinese anchor terms, matching the author's 30/70 study style. This is a light hook, not a full ramp policy.
- **narrative.md (hook 8) — OPEN for review:** brainstorming chose anonymous (engine default). But the standalone skill uses a named confused peer, "Yuki" ("Teach Yuki" is its per-session closer). Decision to confirm during spec review: keep anonymous for v1, or port the named peer Yuki to make the Teach-to-Learn closer concrete. Low cost either way; one small hook if we adopt Yuki.

## Content to Port from the Standalone Skill

These references from `~/go_senior_devops/leetcode-coach/references/` carry the philosophy and should be ported/adapted into the engine coach's hooks rather than rewritten:
- `problem-solving-framework.md` — the 4-step framework + Step 2.5 articulation bridge. Feeds hook 3 and P0.
- `pattern-cheatsheet.md` — the ~8-10 Python skeletons. Feeds the skeleton-first drilling and hook 3.
- `complexity-cheatsheet.md` — Big-O reference. Feeds P0 and the complexity scorecard dimension.
- `python-dsa-cheatsheet.md` — Python data-structure idioms. Feeds the mechanical-手感 flagging.

The standalone skill's mode structure (Drill / Learn / Cold Solve / Mock) maps onto the engine as: Learn → steps B/C, Drill → step D + skeleton-fluency drill, Cold Solve → step E articulation drill, Mock → step G Interview Q&A + P7 sprint.

## Cadence: daily one-problem study group

The author runs a daily study group with a colleague, one problem per day. This maps to the engine's Micro-mode (one unit of value per sitting):

- A daily sitting runs B to C to D for one problem (teach, solve with fading scaffolding, harness), passes the Feynman Gate, saves a breakpoint, and stops clean.
- Steps F (Teach-to-Learn) and G (Interview Q&A) do not run per problem; they run once when a pattern is wrapped up, over the pattern's accumulated problems.
- The real study group is a natural Teach-to-Learn target: the coach can close a problem with a one-line prompt such as "when you explain this to your colleague tomorrow, be ready to be asked X."

## Scaffolding and Naming

- Scaffold with: `./scripts/new-coach.sh leetcode-coach --with-language` (lab included by default; add `--with-narrative` only if we adopt Yuki).
- Directory name `leetcode-coach` matches the roadmap and the terraform-coach convention. A standalone global skill of the same bare name exists in the environment; the plugin namespace (`learning-coaches:leetcode-coach`) disambiguates. Rename is trivial if collision proves annoying at deploy time; not a design blocker.

## Out of Scope / Deferred

- Hard problems, advanced graphs, advanced DP: not in this coach. Possible future optional phase.
- Go (and any second language): deferred. The lab harness is Python-only for v1.
- Per-phase teaching-material reference files (`references/pN-*.md`): filled in follow-up implementation tasks, not in the scaffold.
- Promoting the never-leave-at-zero ladder to an engine invariant: deferred; lives in the leetcode hook for now.

## Self-Review Notes

- No placeholders or TODOs remain in this spec; per-phase teaching files and the engine-promotion question are explicit deferred items, not unfilled gaps.
- Internal consistency checked: the lab tripwire, the Examiner inputs, and the scorecard "optimality" dimension all point at the same objective signal (large-N timing), so optimality is enforced consistently across lab, gate, and scorecard.
- Blank-page constraint traced end to end: it appears as a locked decision, a dedicated stance section, P0's centerpiece, the step-D guided default, a Tier-1 scorecard dimension, and the P0 gate — so the design's center of gravity is not lost between sections.
- One open decision remains for the user (narrative: anonymous vs Yuki); flagged inline, does not block the rest of the plan.
- Scope: one coach, following the established 9-hook contract. Focused enough for a single implementation plan.
