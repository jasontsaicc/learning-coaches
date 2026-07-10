# Phase Gates

The engine enforces the 3-attempt cap, the failure protocol, and Examiner
independence. This hook defines what "pass" means per phase. Every gate is scored on
its numbered criteria at the engine's 60% threshold; the tier scorecard
(`scorecard-dims.md`) is the footer quality lens.

Examiner inputs for lab-backed gates (P1-P7) are objective artifacts: `solution.py`
(fenced), the full `lab-lc.sh` pytest output including the large-N timing test, and
the student's verbatim articulation/complexity explanation. Self-report is never an
Examiner input.

## P0 Gate - Mental Model

Pass condition: on a problem described aloud (not previously discussed), the student
runs the 4-question articulation bridge unaided and produces a codeable plan without
freezing; then correctly analyzes the time/space complexity of a given code snippet.

Specifically, the student must:
1. Answer all four bridge questions in concrete plain sentences.
2. State the brute force and its complexity before any optimization talk.
3. Derive the first line of code from their own bridge answers.
4. Give the correct time AND space complexity of the shown snippet, with the reason.

Examiner input: verbatim answers only (no lab artifact at this phase).

## P1 Gate - Arrays / Hashing / Two Pointers

Pass condition: from scratch, solve an unseen hashing or two-pointer Medium; harness
fully green including the large-N test; explain why the hash map (or pointer move)
makes it O(n).

Specifically, the student must:
1. Name the pattern from the problem's signals before coding.
2. State the brute force and its complexity.
3. Produce `solution.py` with `lab-lc.sh` exit 0 (all tests, large-N included).
4. Justify the optimal bound with the mechanism, not a recital.

## P2 Gate - Sliding Window / Stack

Pass condition: same shape as P1 on an unseen window or stack Medium; must include a
correct amortized argument where the pattern relies on one (each element enters and
leaves once).

Specifically, the student must:
1. Choose between fixed window / variable window / monotonic stack and justify from
   the problem's signals.
2. State the brute force and show what work it repeats.
3. Produce `solution.py` with `lab-lc.sh` exit 0.
4. Explain the amortized O(n) argument without prompting.

## P3 Gate - Binary Search / Linked List

Pass condition: solve an unseen binary-search Medium (index-space or answer-space)
with a green harness, and state the three binary-search death traps (`r` init,
`<=` boundary, `mid±1` progress) unprompted.

Specifically, the student must:
1. Identify whether the search runs on the index space or the answer space, and why.
2. State the monotonic property that makes discarding half safe.
3. Produce `solution.py` with `lab-lc.sh` exit 0.
4. Name the three death traps and what breaks when each is wrong.

## P4 Gate - Trees

Pass condition: solve an unseen tree Medium choosing DFS or BFS deliberately, harness
green, and explain the recursion's base case and trust step (why the subtree call can
be assumed correct).

Specifically, the student must:
1. Justify DFS vs BFS from the question's shape (path/property vs level/distance).
2. State the base case before writing the recursion.
3. Produce `solution.py` with `lab-lc.sh` exit 0.
4. Explain the complexity in nodes visited, not loop syntax.

## P5 Gate - Heap / Backtracking

Pass condition: solve an unseen top-k heap Medium with a green harness and justify why
a heap beats sorting for the access pattern; sketch (not drill) the backtracking
template on a recognition question.

Specifically, the student must:
1. Justify heap vs sort with the k-vs-n trade-off.
2. Produce `solution.py` with `lab-lc.sh` exit 0.
3. State the backtracking template's three moves (choose, explore, undo) on a
   described combinations problem, without writing full code.

## P6 Gate - Graphs / 1-D DP

Pass condition: solve an unseen graph Medium (traversal or topological sort) with a
green harness, and solve a basic 1-D DP with the recurrence stated in words before
code.

Specifically, the student must:
1. Build the adjacency structure from the problem input and say why BFS or DFS fits.
2. For the topological-sort case, explain what a cycle means for the answer.
3. Produce `solution.py` with `lab-lc.sh` exit 0 for the graph problem.
4. State the DP recurrence and its base cases in words, then code it.

## P7 Gate - Interview Sprint

Pass condition: a timed mock with two unseen Mediums; approach verbalized before any
code on both; harness green on both; scored with the Tier 4 scorecard as the footer
lens.

Specifically, the student must:
1. Verbalize the bridge and the chosen pattern before coding, per problem.
2. Land both problems inside the time budget.
3. Produce green harness runs for both (`lab-lc.sh` exit 0).
4. Close each with the optimality argument for the final bound.
