# Curriculum

Each phase has a one-line focus, prerequisites, and the reference filename that holds
its detailed teaching material (to be filled in future tasks). Phases are sequential;
the engine enforces prerequisite checks via Routing branch 5. Problem order follows
NeetCode 150 (Easy + Medium only; DP capped at 1-D plus basic 2-D).

**DevOps priority annotation:** the student's daily study group walks NeetCode 150 in
order, and the interview target is a senior DevOps coding round. Each phase lists its
DevOps-priority patterns (from the migrated relevance ratings: Hash Map, Sliding
Window, Binary Search, Graphs at the top; Backtracking and 2-D DP at the bottom).
Priority patterns get the extra drill reps and the phase-gate problems; low-priority
patterns are covered once for recognition and not drilled to fluency.

---

## Warm-Up Diagnostic (new students only)

Give an unseen easy problem (e.g., Valid Anagram) described aloud. Listen for whether
the student can run the 4-question articulation bridge (what am I computing / what is
the brute force / how do I shrink the work / when do I stop) or freezes at zero.

Classify: strong (runs the bridge unprompted) / mid (answers when prompted question
by question) / freezes-at-zero (cannot start without a worked example). Record the
classification in the progress file; it decides how much I-do scaffolding P0 starts
with.

---

## P0 - Problem-Solving Mental Model

**Focus:** The 4-question articulation bridge as the anti-freeze tool, Big-O analysis,
the time/space trade-off, the brute-to-optimal method, and reading a problem to
extract constraints. No new data structure.

**Prerequisites:** none (entry phase). Python basics assumed.

**DevOps priority:** the bridge and Big-O apply to every pattern; nothing is skippable
here.

**Reference file:** `references/p0-mental-model.md` (to be created in a future task)

---

## P1 - Arrays / Hashing / Two Pointers

**Focus:** Hash map O(1) lookup as the first space-for-time trade, frequency counting,
converging two pointers. Two Sum, Valid Anagram, Group Anagrams, 3Sum, Container With
Most Water.

**Prerequisites:** P0 gate passed — student runs the bridge without freezing and can
analyze a snippet's complexity.

**DevOps priority:** Hash Map is top priority (config stores, log parsing, frequency
counting are daily DevOps work). Two Pointers is mid priority: one solid template is
enough.

**Reference file:** `references/p1-arrays-hashing.md` (to be created in a future task)

---

## P2 - Sliding Window / Stack

**Focus:** Fixed and variable windows, monotonic stack, FILO matching. Best Time to
Buy and Sell Stock, Longest Substring Without Repeating Characters, Valid Parentheses,
Min Stack, Daily Temperatures.

**Prerequisites:** P1 gate passed — student solves an unseen hashing/two-pointer
Medium with a green harness.

**DevOps priority:** Sliding Window is top priority (rolling metrics, monitoring
windows, rate limiting). Stack is high (config parsing, undo semantics, call stacks).

**Reference file:** `references/p2-window-stack.md` (to be created in a future task)

---

## P3 - Binary Search / Linked List

**Focus:** Binary search on an index range and on an answer space, fast/slow pointers,
in-place reversal. Binary Search, Search a 2D Matrix, Koko Eating Bananas, Reverse
Linked List, Linked List Cycle.

**Prerequisites:** P2 gate passed.

**DevOps priority:** Binary Search is top priority (git bisect, threshold finding,
log search). Linked List is low: cover the Easy set for recognition, do not over-drill.

**Reference file:** `references/p3-binsearch-linkedlist.md` (to be created in a future task)

---

## P4 - Trees (BFS/DFS)

**Focus:** Tree recursion, level-order traversal, the DFS/BFS choice. Invert Binary
Tree, Maximum Depth, Lowest Common Ancestor, Level Order Traversal, Validate BST.

**Prerequisites:** P3 gate passed.

**DevOps priority:** mid (directory trees, DNS hierarchy). Trees matter mainly as the
prerequisite for Graphs, which is a top DevOps pattern; teach with that arrow in view.

**Reference file:** `references/p4-trees.md` (to be created in a future task)

---

## P5 - Heap / Backtracking

**Focus:** Priority queue for top-k problems, the backtracking template. Kth Largest
Element, K Closest Points, Last Stone Weight, Subsets, Combination Sum.

**Prerequisites:** P4 gate passed.

**DevOps priority:** Heap is mid (job scheduling, incident priority queues); do the
Easy set plus one Medium. Backtracking is the lowest-priority pattern in the whole
curriculum: one template pass for recognition, no fluency drilling.

**Reference file:** `references/p5-heap-backtracking.md` (to be created in a future task)

---

## P6 - Graphs + 1-D DP (intro)

**Focus:** Grid and adjacency BFS/DFS, topological sort, one-dimensional DP. Number of
Islands, Clone Graph, Rotting Oranges, Course Schedule I & II, Connected Components,
Climbing Stairs, House Robber, Coin Change.

**Prerequisites:** P5 gate passed.

**DevOps priority:** Graphs is THE DevOps pattern (service dependency DAGs, network
topology, Terraform resource ordering, incident blast radius); give it the most reps
of any phase. Course Schedule maps directly to CI/CD dependency resolution. 1-D DP is
low priority: basics only, per the difficulty ceiling.

**Reference file:** `references/p6-graphs-dp.md` (to be created in a future task)

---

## P7 - Interview Sprint

**Focus:** Timed mocks on mixed unseen problems, verbalize before coding, pattern
recognition under time. Long-tail patterns (Intervals, Greedy, Trie, Bit Manipulation)
are covered inside this sprint rather than as separate phases.

**Prerequisites:** P6 gate passed.

**DevOps priority:** Intervals and Greedy get one drill each (maintenance windows and
autoscaling analogies make them fast to absorb); Trie and Bit Manipulation are
recognition-only.

**Reference file:** `references/p7-interview-sprint.md` (to be created in a future task)
