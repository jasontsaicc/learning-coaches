# Teaching Elements

Domain content that fills Teaching Flow steps B, C, D, and E. The engine governs the
structure (scenario before terminology, principle before mechanism, one Feynman Gate
per chunk); this file supplies the leetcode content the engine pours into each step.

A topic is a pattern (Approach A). The chunks inside a topic are the escalating ideas
of the brute-to-optimal path. Hybrid rule: the first problem of a pattern is taught
fully brute-to-optimal (steps B/C); later problems in the same pattern run as lab/drill.
This keeps teaching concrete without sliding into per-problem memorization.

Cadence note: the daily one-problem study group sitting runs B → C → D for one problem,
passes the Feynman Gate, saves a breakpoint, and stops clean (engine Micro-mode). Steps
F and G run once per pattern wrap-up, over the pattern's accumulated problems, not per
problem. The study group is a natural Teach-to-Learn target: close a problem with
"when you explain this to your colleague tomorrow, be ready to be asked X."

---

## Blank-Page Handling (cross-cutting, the coach's center of gravity)

The student's biggest failure mode is the blank page: they understand the problem, may
even know the pattern, and still cannot produce a first line. This machinery runs
before any attempt exists; the engine's escalation ladder is reactive and takes over
only after a failed attempt.

- **The articulation bridge (4 plain-language questions).** Before any code: (1) What
  am I computing? (2) What must I try — what is the brute force? (3) How do I shrink
  the work / move? (4) When do I stop? Answers are plain sentences; the first line of
  code is a transcription of them (`seen = {}`, `l, r = 0, len(a)-1`). Full version
  with a worked example: `references/problem-solving-framework.md` (Step 2.5).
- **Gradual release (I do → we do → you do).** Pattern's first problem, or any
  stuck-at-zero moment: the coach narrates ONE full think-aloud through the 4 questions
  (I do). Never ask a frozen student to generate; generation is the jammed function.
  Default step-D path early in a pattern: skeleton with 2-3 blanks, each blank paired
  with a "why" question (we do). Fade to blind typing, then cold-next-day (you do).
- **Skeleton-first.** The unit of practice is the pattern skeleton (~8-10 skeletons
  cover most of NeetCode 150), not the whole problem. Each problem is a skeleton plus
  two problem-specific lines. Skeletons live in `references/pattern-cheatsheet.md`.
- **Draw to teach.** Teach a pattern by drawing a text diagram with the problem's
  actual numbers, showing 2-3 steps of motion. The waste the optimization removes must
  be visible before the optimized code appears.

---

## Step B: Scenario Intro

One-line hooks that make a pattern matter before any jargon. DevOps analogies are the
default register (the student is a DevOps engineer; the migrated analogy bank has one
per pattern).

| Pattern | Scenario hook |
|---------|--------------|
| Hash Map | DNS lookup: domain → IP in O(1). A config store is a hash map you query all day. |
| Two Pointers | Comparing two sorted server logs: one cursor at each end, walking inward to find the discrepancy. |
| Sliding Window | A CloudWatch dashboard always shows the last 5 minutes: old points drop off, new ones enter, the aggregate updates without rescanning history. |
| Stack | Rollback order: the last change applied is the first to undo. Config parsers and call stacks work the same way. |
| Binary Search | `git bisect`: find the breaking commit in log2(n) checkouts instead of n. |
| Linked List | A middleware pipeline: each handler holds a pointer to the next. |
| Trees | A directory tree: `ls -R` is DFS; `find -maxdepth 2` is BFS. |
| Heap | The incident queue: P1 pages always pop before P2, regardless of arrival order. |
| Backtracking | Trying every combination of config flags, undoing each failed branch. |
| Graphs | `terraform graph`: service dependencies form a DAG; Course Schedule is CI/CD job ordering with a cycle check. |
| 1-D DP | Redis memoization: cache the answer to each subproblem so it is never recomputed. |
| Intervals | Merging overlapping maintenance windows; finding gaps in the on-call rotation. |
| Greedy | Autoscaling: pick the locally cheapest instance that meets the current requirement. |

---

## Step C: Core Teaching (first principles + chunks)

**Core chain (applies to every pattern):** an optimal solution exists because some
piece of work the brute force repeats can be remembered or ruled out. The pattern is
the data structure or invariant that holds that memory. Teach the waste first (show
the brute force redoing work on real numbers), then the insight that removes it, then
the template. A student who sees the waste can re-derive the template; a student who
memorizes the template cannot.

Per-pattern chunk order (each chunk gets its own Feynman Gate):

1. **Naive baseline:** state the brute force and its complexity. Always aloud, always
   first; it anchors the optimization and scores interview points by itself.
2. **Key insight:** the invariant or maintained state that collapses the complexity
   ("the hash map remembers complements, so the second scan disappears"; "each element
   enters and leaves the stack once, so the total is O(n) amortized").
3. **Optimal template:** the reusable skeleton (see `pattern-cheatsheet.md`), taught
   by transcribing the bridge answers, not by pasting code.
4. **Complexity analysis:** why the optimal bound holds, argued from the insight (an
   amortized argument, a halving argument), not recited.

First-principles examples by phase: hashing trades O(n) space for O(1) lookup so the
O(n^2) complement scan becomes one pass (P1); a monotonic stack works because each
index enters and leaves at most once, so nested-looking work is O(n) amortized (P2);
binary search requires the sorted/monotonic property because discarding half is only
safe when order guarantees the target cannot be in the discarded half (P3); tree
recursion is safe because subtrees are smaller instances of the same problem (P4);
a heap keeps the top-k reachable in O(log n) because it maintains only a partial
order, not a full sort (P5); BFS finds shortest paths in unweighted graphs because it
explores in distance layers (P6); DP is recursion plus a memory that collapses an
exponential tree into a linear table (P6).

---

## Step D: Hands-On (guided by default)

The lab is a per-problem folder (layout in `portfolio.md`) verified by
`scripts/lab-lc.sh <problem-dir>`: all functional tests green AND the large-N timing
test green (see `lab-manager.md`).

The we-do loop, early in a pattern:

1. Student runs the articulation bridge aloud for this problem.
2. Coach presents the skeleton with 2-3 blanks; each blank is paired with a "why"
   question ("what goes here, and why a set instead of a list?").
3. Student fills the blanks, then types the whole solution blind.
4. Run the harness. Read failures aloud; the student debugs from the error message
   before the coach explains anything.

Scaffolding fades problem by problem: blanks shrink, then disappear, then the student
writes from the bridge alone. Late in a pattern, step D is a cold write.

**Answer-debt rule.** If the student views solution code they did not produce cold
(tired, deadline, "just show me"), allow it, log it immediately as a cold re-do debt
due in 3 days, and the pattern cannot be marked fluent until that cold re-do passes
with zero bugs. Evidence from the standalone era: a Hard problem was viewed under
study-group pressure, never cold-redone, and fluency stalled with no trace.

**Compressed-sitting rule.** A short study-group sitting may compress the session, but
never drops due re-tests to zero (minimum one). Anything a compressed sitting skips
(transfer questions, teach-back, the weekly review) gets a dated debt entry in the
registry, and the next full session clears debts before any new content. Evidence:
every compressed sprint in 2026-06/07 skipped the warm-up entirely and five due
re-tests sat unresolved for weeks.

---

## Step E: Drill

Two distinct drills, chosen by the student's fluency on the pattern. Both feed the
Mistake Registry; a drill that logs nothing was too easy.

- **Cold Solve (approach articulation).** An unseen problem in a learned pattern. The
  deliverable is a discussable plan: pattern named and justified, bridge run aloud,
  brute force stated with complexity. Scored on mapping + articulation, not on whether
  code ran. This trains the north-star skill directly (the interview is an unseen
  problem, always).
- **Skeleton Fluency.** Type a known pattern's template cold into a blank file, zero
  bugs. One blind success is not fluency; the acceptance test is cold-next-day with
  zero bugs, which maps to the engine's review rhythm.

Drill selection guardrail: transfer questions ("would this survive negative numbers?",
"what breaks if the array is not sorted?") test the mechanism, never trivia about a
specific problem's number or title. The student explicitly rejected title-keyed recall
questions; honor that.

---

## Skeleton Registry (domain registry)

Declared in `portfolio.md`; rows reuse the registry fields from PROGRESS-SCHEMA.md
section 7. One row per core skeleton, with a one-line "when to use" trigger. The
canonical skeleton list and code live in `references/pattern-cheatsheet.md`; the
registry tracks recall scheduling only.

| Skeleton | When to use (trigger) |
|----------|----------------------|
| Frequency counter (hash map) | "count / group / frequency" over unsorted data |
| Complement lookup (hash map) | "find a pair summing to X" without sorting |
| Converging two pointers | sorted input + pair/containment question |
| Fixed sliding window | contiguous subarray/substring of known size k |
| Variable sliding window | longest/shortest contiguous run under a constraint |
| Monotonic stack | "next greater/smaller element", histogram spans |
| Binary search (index) | sorted array + find target/boundary |
| Binary search (answer space) | "minimize the max / find the threshold" with a monotonic feasibility check |
| Tree DFS (recursive) | whole-tree property or path question |
| Tree/graph BFS (deque) | level order or shortest unweighted path |
| Backtracking template | "all combinations/permutations" (recognition only) |
| 1-D DP table | "how many ways / min cost" with overlapping subproblems |
