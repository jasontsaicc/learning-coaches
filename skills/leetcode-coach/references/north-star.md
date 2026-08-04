# North Star

## Win Condition

Given an unseen NeetCode-150-difficulty Medium, the student can, within interview
time: recognize which pattern applies, state the brute-force approach and its
complexity, derive the optimal approach, write clean Python that passes the test
harness (including the large-N performance test), and explain why the final
time/space complexity is the bound it is.

**Derivation:**
- "Recognize which pattern applies" — the interview skill is mapping an unseen
  problem to a known shape. A student who can only replay memorized solutions
  collapses on the first variant.
- "State the brute force first" — it proves the student understands the problem
  before optimizing it, and it is the expected interview opening move.
- "Passes the harness including large-N" — correctness and optimality are
  machine-checked (`scripts/lab-lc.sh`), never self-reported. The large-N timing
  test is what makes "is it actually optimal" objective.
- "Explain the bound" — reporting Big-O is recall; justifying it with a concrete
  reason (each element enters and leaves the stack once, so the total is O(n)) is
  understanding. Interviews score the second.

An articulated, discussable approach counts as real output even when the code is
incomplete. An articulable approach IS the deliverable: interviewers score the
conversation, not only the final code.

Retention is part of the win condition: a pattern counts as owned only after its
+60-day cold rewrite passes (the retention ladder in `teaching-elements.md` 第 6 步).
Solved-today-forgotten-in-two-months is a loss, not a slow win.

## Tie-Break Rule

When "pattern transfer ability" and "solve more problems" compete for session
time, transfer wins.

When a fancier optimal solution and a simpler interview-passable solution compete,
the simplest understandable solution wins; elegant variants are parked in the
curiosity branch, never taught in the main pass.

**Derivation:** six patterns learned well enough to recognize in a new problem
beat sixty memorized solutions that collapse on a variant. The target is a senior
DevOps coding round: breadth of solved-problem count impresses nobody there, but
freezing on an unseen Medium fails the round.
