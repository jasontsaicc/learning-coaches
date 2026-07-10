# LeetCode Interview Curriculum (NeetCode 150 — Easy + Medium)

> Target: DevOps coding interviews + general tech interviews
> Pace: ~1 problem/day, pattern-based deep learning
> Language: Python
> Source: NeetCode 150 (Hard problems skipped) + interview frequency extras (marked ★)

---

## Phase 0: Foundation Patterns

### Arrays & Hashing

**Core concept:** Use hash maps and sets to trade memory for O(1) lookups and eliminate nested loops.
**Prerequisites:** None (entry point)

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Contains Duplicate | Easy | NeetCode 150 | HashSet basics |
| 2 | Valid Anagram | Easy | NeetCode 150 | Frequency counter |
| 3 | Two Sum | Easy | NeetCode 150 | HashMap complement |
| 4 | Group Anagrams | Medium | NeetCode 150 | Sorted key + HashMap |
| 5 | Top K Frequent Elements | Medium | NeetCode 150 | Bucket sort / heap |
| 6 | Encode and Decode Strings | Medium | NeetCode 150 (Premium) | Delimiter design |
| 7 | Product of Array Except Self | Medium | NeetCode 150 | Prefix/suffix |
| 8 | Valid Sudoku | Medium | NeetCode 150 | HashSet per row/col/box |
| 9 | Longest Consecutive Sequence | Medium | NeetCode 150 | HashSet + sequence detection |
| ★ | Move Zeroes | Easy | Interview Freq | In-place two-pass |
| ★ | Merge Sorted Array | Easy | Interview Freq | Two-pointer merge |

### Two Pointers

**Core concept:** Use two indices moving toward each other (or in the same direction) to reduce O(n²) brute force to O(n).
**Prerequisites:** Arrays & Hashing

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Valid Palindrome | Easy | NeetCode 150 | Basic two pointer |
| 2 | Two Sum II | Medium | NeetCode 150 | Sorted array two pointer |
| 3 | 3Sum | Medium | NeetCode 150 | Sort + two pointer |
| 4 | Container With Most Water | Medium | NeetCode 150 | Greedy two pointer |
| ★ | Remove Duplicates from Sorted Array | Easy | Interview Freq | In-place dedup |

### Sliding Window

**Core concept:** Maintain a dynamic subarray window — expand right, shrink left — to solve substring/subarray problems in O(n).
**Prerequisites:** Arrays & Hashing, Two Pointers

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Best Time to Buy and Sell Stock | Easy | NeetCode 150 | Single pass / Kadane variant |
| 2 | Longest Substring Without Repeating Characters | Medium | NeetCode 150 | HashMap + window |
| 3 | Longest Repeating Character Replacement | Medium | NeetCode 150 | Frequency + window |
| 4 | Permutation in String | Medium | NeetCode 150 | Fixed window + frequency match |
| ★ | Maximum Average Subarray I | Easy | Interview Freq | Fixed-size window basics |

### Stack

**Core concept:** LIFO structure that enables tracking of "most recent unresolved" elements — essential for matching, evaluation, and monotonic patterns.
**Prerequisites:** Arrays & Hashing

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Valid Parentheses | Easy | NeetCode 150 | Matching brackets |
| 2 | Min Stack | Medium | NeetCode 150 | Track minimum |
| 3 | Evaluate Reverse Polish Notation | Medium | NeetCode 150 | Stack evaluation |
| 4 | Generate Parentheses | Medium | NeetCode 150 | Backtracking + stack concept |
| 5 | Daily Temperatures | Medium | NeetCode 150 | Monotonic stack |
| 6 | Car Fleet | Medium | NeetCode 150 | Stack + sorting |

---

**Phase 0 Gate:** One unseen Easy problem, 15 min, must produce working code.

---

## Phase 1: Core Data Structures

### Binary Search

**Core concept:** Eliminate half the search space each step — works on any sorted or monotonic structure, not just arrays.
**Prerequisites:** Arrays & Hashing

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Binary Search | Easy | NeetCode 150 | Standard template |
| 2 | Search a 2D Matrix | Medium | NeetCode 150 | Flatten + binary search |
| 3 | Koko Eating Bananas | Medium | NeetCode 150 | Binary search on answer |
| 4 | Find Minimum in Rotated Sorted Array | Medium | NeetCode 150 | Rotated array |
| 5 | Search in Rotated Sorted Array | Medium | NeetCode 150 | Two-part search |
| 6 | Time Based Key-Value Store | Medium | NeetCode 150 | Binary search on timestamps |

### Linked List

**Core concept:** Chain of nodes with pointers — master pointer manipulation, two-pointer tricks, and in-place reversal.
**Prerequisites:** None (entry point)

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Reverse Linked List | Easy | NeetCode 150 | Iterative/recursive |
| 2 | Merge Two Sorted Lists | Easy | NeetCode 150 | Merge pattern |
| 3 | Linked List Cycle | Easy | NeetCode 150 | Floyd's cycle detection |
| 4 | Reorder List | Medium | NeetCode 150 | Find middle + reverse + merge |
| 5 | Remove Nth Node From End of List | Medium | NeetCode 150 | Two pointer gap |
| 6 | Copy List with Random Pointer | Medium | NeetCode 150 | HashMap clone |
| 7 | Add Two Numbers | Medium | NeetCode 150 | Digit-by-digit addition |
| 8 | Find The Duplicate Number | Medium | NeetCode 150 | Floyd's cycle |
| 9 | LRU Cache | Medium | NeetCode 150 | HashMap + doubly linked list |

### Trees

**Core concept:** Recursive tree traversal — DFS for depth/paths, BFS for level-order — underpins graphs, heaps, and DP on trees.
**Prerequisites:** Linked List (recursion concepts)

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Invert Binary Tree | Easy | NeetCode 150 | Recursive swap |
| 2 | Maximum Depth of Binary Tree | Easy | NeetCode 150 | DFS depth |
| 3 | Diameter of Binary Tree | Easy | NeetCode 150 | DFS with global max |
| 4 | Balanced Binary Tree | Easy | NeetCode 150 | Height-balanced check |
| 5 | Same Tree | Easy | NeetCode 150 | Recursive comparison |
| 6 | Subtree of Another Tree | Easy | NeetCode 150 | Recursive match |
| 7 | Lowest Common Ancestor of BST | Medium | NeetCode 150 | BST property |
| 8 | Binary Tree Level Order Traversal | Medium | NeetCode 150 | BFS with deque |
| 9 | Binary Tree Right Side View | Medium | NeetCode 150 | BFS level last |
| 10 | Count Good Nodes in Binary Tree | Medium | NeetCode 150 | DFS with max |
| 11 | Validate Binary Search Tree | Medium | NeetCode 150 | Inorder / range check |
| 12 | Kth Smallest Element in BST | Medium | NeetCode 150 | Inorder traversal |
| 13 | Construct Binary Tree from Preorder and Inorder | Medium | NeetCode 150 | Recursive build |

### Heap / Priority Queue

**Core concept:** Efficiently maintain the min or max of a dynamic set — the backbone of "top K" and scheduling problems.
**Prerequisites:** Arrays & Hashing, Trees

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Kth Largest Element in a Stream | Easy | NeetCode 150 | Min-heap of size K |
| 2 | Last Stone Weight | Easy | NeetCode 150 | Max-heap simulation |
| 3 | K Closest Points to Origin | Medium | NeetCode 150 | Heap by distance |
| 4 | Kth Largest Element in an Array | Medium | NeetCode 150 | Quickselect / heap |
| 5 | Task Scheduler | Medium | NeetCode 150 | Greedy + heap |
| 6 | Design Twitter | Medium | NeetCode 150 | Merge K sorted + heap |

---

**Phase 1 Gate:** One unseen Medium problem, 25 min, Scorecard ≥ 3/5.

---

## Phase 2: Advanced Algorithms

### Backtracking

**Core concept:** Systematically explore all possibilities by making a choice, recursing, then undoing the choice — prune branches early to stay efficient.
**Prerequisites:** Trees (recursion)

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Subsets | Medium | NeetCode 150 | Subset generation |
| 2 | Combination Sum | Medium | NeetCode 150 | Unlimited picks |
| 3 | Combination Sum II | Medium | NeetCode 150 | No duplicates |
| 4 | Permutations | Medium | NeetCode 150 | All arrangements |
| 5 | Subsets II | Medium | NeetCode 150 | Duplicates handling |
| 6 | Word Search | Medium | NeetCode 150 | Grid DFS |
| 7 | Palindrome Partitioning | Medium | NeetCode 150 | Partition + palindrome check |
| 8 | Letter Combinations of a Phone Number | Medium | NeetCode 150 | Digit mapping |
| ★ | Combinations | Medium | Interview Freq | Choose k from n (LeetCode 77) |

### Tries

**Core concept:** A prefix tree where each node represents one character — enables O(m) lookup/insert for strings instead of O(m·n) scanning.
**Prerequisites:** Trees, Arrays & Hashing

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Implement Trie (Prefix Tree) | Medium | NeetCode 150 | Core data structure |
| 2 | Design Add and Search Words Data Structure | Medium | NeetCode 150 | Trie + DFS for wildcard |
| ★ | Word Search II | Hard (optional stretch) | NeetCode 150 | Trie + grid backtracking |

### Graphs

**Core concept:** Model relationships as nodes + edges — BFS for shortest path / level order, DFS for connectivity, Union-Find for components.
**Prerequisites:** Trees, Heap

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Number of Islands | Medium | NeetCode 150 | BFS/DFS flood fill |
| 2 | Max Area of Island | Medium | NeetCode 150 | DFS with area |
| 3 | Clone Graph | Medium | NeetCode 150 | BFS/DFS clone with HashMap |
| 4 | Walls and Gates | Medium | NeetCode 150 (Premium) | Multi-source BFS |
| 5 | Rotting Oranges | Medium | NeetCode 150 | Multi-source BFS |
| 6 | Pacific Atlantic Water Flow | Medium | NeetCode 150 | Reverse DFS from edges |
| 7 | Surrounded Regions | Medium | NeetCode 150 | Border DFS |
| 8 | Course Schedule | Medium | NeetCode 150 | Topological sort / cycle detection |
| 9 | Course Schedule II | Medium | NeetCode 150 | Topological sort ordering |
| 10 | Graph Valid Tree | Medium | NeetCode 150 (Premium) | Union-Find or DFS cycle |
| 11 | Number of Connected Components | Medium | NeetCode 150 (Premium) | Union-Find / DFS |
| 12 | Redundant Connection | Medium | NeetCode 150 | Union-Find cycle detection |

### Advanced Graphs

**Core concept:** Weighted shortest path (Dijkstra, Bellman-Ford) and minimum spanning trees (Prim's, Kruskal's) for optimisation on graphs.
**Prerequisites:** Graphs

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Network Delay Time | Medium | NeetCode 150 | Dijkstra |
| 2 | Cheapest Flights Within K Stops | Medium | NeetCode 150 | Modified Dijkstra / Bellman-Ford |
| 3 | Min Cost to Connect All Points | Medium | NeetCode 150 | Prim's MST |
| 4 | Swim in Rising Water | Medium | NeetCode 150 | Binary search + BFS |
| ★ | Reconstruct Itinerary | Medium | Interview Freq | Euler path |

---

**Phase 2 Gate:** One unseen Medium problem, 25 min, Scorecard ≥ 3/5.

---

## Phase 3: Optimization Techniques

### 1-D Dynamic Programming

**Core concept:** Break a problem into overlapping subproblems and store results — convert exponential recursion into linear or polynomial time.
**Prerequisites:** Arrays & Hashing, Binary Search

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Climbing Stairs | Easy | NeetCode 150 | Fibonacci DP |
| 2 | Min Cost Climbing Stairs | Easy | NeetCode 150 | Cost DP |
| 3 | House Robber | Medium | NeetCode 150 | Skip-one DP |
| 4 | House Robber II | Medium | NeetCode 150 | Circular variation |
| 5 | Longest Palindromic Substring | Medium | NeetCode 150 | Expand around center / DP |
| 6 | Palindromic Substrings | Medium | NeetCode 150 | Count palindromes |
| 7 | Decode Ways | Medium | NeetCode 150 | String DP |
| 8 | Coin Change | Medium | NeetCode 150 | Unbounded knapsack |
| 9 | Maximum Product Subarray | Medium | NeetCode 150 | Track min/max |
| 10 | Word Break | Medium | NeetCode 150 | String + DP |
| 11 | Longest Increasing Subsequence | Medium | NeetCode 150 | LIS with binary search |
| 12 | Partition Equal Subset Sum | Medium | NeetCode 150 | 0/1 knapsack |

### 2-D Dynamic Programming

**Core concept:** Extend 1-D DP to a 2-D table when the state depends on two dimensions — common in string comparison and grid problems.
**Prerequisites:** 1-D Dynamic Programming

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Unique Paths | Medium | NeetCode 150 | Grid paths |
| 2 | Longest Common Subsequence | Medium | NeetCode 150 | Classic 2D DP |
| 3 | Best Time to Buy and Sell Stock with Cooldown | Medium | NeetCode 150 | State machine DP |
| 4 | Coin Change II | Medium | NeetCode 150 | Count combinations |
| 5 | Target Sum | Medium | NeetCode 150 | Subset sum variant |
| 6 | Interleaving String | Medium | NeetCode 150 | Two-string interleave |

### Greedy

**Core concept:** Make the locally optimal choice at each step — works when local optima combine into a global optimum (prove it, don't assume it).
**Prerequisites:** Arrays & Hashing, Sliding Window

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Maximum Subarray | Medium | NeetCode 150 | Kadane's algorithm |
| 2 | Jump Game | Medium | NeetCode 150 | Reachability |
| 3 | Jump Game II | Medium | NeetCode 150 | Min jumps |
| 4 | Gas Station | Medium | NeetCode 150 | Circular greedy |
| 5 | Hand of Straights | Medium | NeetCode 150 | Grouping |
| 6 | Merge Triplets to Form Target Triplet | Medium | NeetCode 150 | Bitwise greedy |
| 7 | Partition Labels | Medium | NeetCode 150 | Last occurrence |

### Intervals

**Core concept:** Sort intervals by start time, then scan once — merging, inserting, or counting overlaps becomes a single linear pass.
**Prerequisites:** Arrays & Hashing, Greedy

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Insert Interval | Medium | NeetCode 150 | Insert + merge |
| 2 | Merge Intervals | Medium | NeetCode 150 | Sort + merge |
| 3 | Non-overlapping Intervals | Medium | NeetCode 150 | Greedy removal |
| ★ | Meeting Rooms | Easy | Interview Freq | Overlap detection |
| ★ | Meeting Rooms II | Medium | Interview Freq (Premium) | Min rooms |
| ★ | Minimum Number of Arrows to Burst Balloons | Medium | Interview Freq | Greedy intervals |

### Math & Geometry

**Core concept:** Recognise mathematical patterns — modular arithmetic, digit manipulation, matrix transformations — that short-circuit brute-force search.
**Prerequisites:** Arrays & Hashing

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Happy Number | Easy | NeetCode 150 | Cycle detection |
| 2 | Plus One | Easy | NeetCode 150 | Carry propagation |
| 3 | Rotate Image | Medium | NeetCode 150 | Matrix rotation |
| 4 | Spiral Matrix | Medium | NeetCode 150 | Layer traversal |
| 5 | Set Matrix Zeroes | Medium | NeetCode 150 | In-place marking |
| 6 | Pow(x, n) | Medium | NeetCode 150 | Fast exponentiation |
| 7 | Multiply Strings | Medium | NeetCode 150 | Digit multiplication |
| 8 | Detect Squares | Medium | NeetCode 150 | HashMap geometry |

### Bit Manipulation

**Core concept:** Operate directly on binary representations — XOR, shifts, and masks — to solve problems in O(1) space with minimal arithmetic.
**Prerequisites:** None (entry point)

| # | Problem | Difficulty | Source | Focus |
|---|---------|------------|--------|-------|
| 1 | Single Number | Easy | NeetCode 150 | XOR |
| 2 | Number of 1 Bits | Easy | NeetCode 150 | Hamming weight |
| 3 | Counting Bits | Easy | NeetCode 150 | DP + bit |
| 4 | Reverse Bits | Easy | NeetCode 150 | Bit shifting |
| 5 | Missing Number | Easy | NeetCode 150 | XOR or math |
| 6 | Sum of Two Integers | Medium | NeetCode 150 | Bit addition |
| 7 | Reverse Integer | Medium | NeetCode 150 | Digit extraction |

---

**Final Gate:** Mock interview — 2 Medium problems, 45 min, both Scorecard ≥ 5/7.

---

## Prerequisites Map

```
Arrays & Hashing       → (entry point)
Two Pointers           → Arrays & Hashing
Sliding Window         → Arrays & Hashing, Two Pointers
Stack                  → Arrays & Hashing
Binary Search          → Arrays & Hashing
Linked List            → (entry point)
Trees                  → Linked List (recursion concepts)
Heap                   → Arrays & Hashing, Trees
Backtracking           → Trees (recursion)
Tries                  → Trees, Arrays & Hashing
Graphs                 → Trees, Heap
Advanced Graphs        → Graphs
1-D DP                 → Arrays & Hashing, Binary Search
2-D DP                 → 1-D DP
Greedy                 → Arrays & Hashing, Sliding Window
Intervals              → Arrays & Hashing, Greedy
Math & Geometry        → Arrays & Hashing
Bit Manipulation       → (entry point)
```
