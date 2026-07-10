# LeetCode Pattern-Based Curriculum

> Target: DevOps / SRE / Cloud Engineer technical interviews
> Approach: Pattern Recognition → Feynman + Simon → Practice → Mock
> Pace: Flexible — deep understanding over speed
> Total: NeetCode 150 + extras, organized by pattern

---

## Phase 0: Problem-Solving Foundation (Days 1-3)

> **Goal**: Build the meta-skill — know HOW to approach any problem before learning specific patterns.

### Day 1: 6-Step Problem-Solving Framework + Complexity Review
- [ ] Review Big-O: O(1), O(log n), O(n), O(n log n), O(n²)
- [ ] Learn the 6-step framework (UNDERSTAND → EXAMPLES → PATTERN → PLAN → CODE → TEST)
- [ ] Practice: apply 6 steps to Two Sum (already solved — redo with framework)
- [ ] **Notes**: `notes/day01-problem-solving-framework.md`

### Day 2: Pattern Recognition Checklist Introduction
- [ ] Learn the Pattern Recognition Checklist (signals → patterns)
- [ ] Study 5 example problems: identify which signal maps to which pattern
- [ ] **Notes**: `notes/day02-pattern-recognition.md`

### Day 3: Pattern ID Drill (No Coding)
- [ ] Given 10 unseen problem descriptions, identify the pattern in < 2 min each
- [ ] Score: at least 6/10 correct to move on
- [ ] **Notes**: `notes/day03-pattern-drill.md`

---

## Phase 1: Core Patterns (Days 4-33)

> **Goal**: Master the 6 most fundamental patterns. ~45 problems.

### Hash Map Patterns (Days 4-8)

> Foundation of everything — O(1) lookup is the single most important optimization technique.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Contains Duplicate | Easy | 1 | ✅ | [筆記](arrays_and_hashing/002_contains_duplicate_notes.md) |
| 2 | Valid Anagram | Easy | 1 | ✅ | [筆記](arrays_and_hashing/003_valid_anagram_notes.md) |
| 3 | Two Sum | Easy | 1 | ✅ | [筆記](arrays_and_hashing/001_two_sum_notes.md) |
| 4 | Group Anagrams | Medium | 1 | ✅ | [筆記](arrays_and_hashing/004_group_anagrams_notes.md) |
| 5 | Top K Frequent Elements | Medium | 1 | ✅ | [筆記](arrays_and_hashing/005_top_k_frequent_notes.md) |
| 6 | Product of Array Except Self | Medium | 1 | ✅ | [筆記](arrays_and_hashing/006_product_of_array_except_self_notes.md) |
| 7 | Valid Sudoku | Medium | 1 | ✅ | [筆記](arrays_and_hashing/011_valid_sudoku_notes.md) |
| 8 | Encode and Decode Strings | Medium | 1 | ✅ | [筆記](arrays_and_hashing/012_encode_and_decode_strings_notes.md) |
| 9 | Longest Consecutive Sequence | Medium | 1 | ✅ | [筆記](arrays_and_hashing/013_longest_consecutive_sequence_notes.md) |

**Extra Practice (Hash Map)**:
| # | Problem | Difficulty | Status | Notes |
|---|---------|-----------|--------|-------|
| E1 | Single Number | Easy | ✅ | [筆記](arrays_and_hashing/007_single_number_notes.md) |
| E2 | Intersection of Two Arrays | Easy | ✅ | [筆記](arrays_and_hashing/008_intersection_of_two_arrays_notes.md) |
| E3 | Missing Number | Easy | ✅ | [筆記](arrays_and_hashing/009_missing_number_notes.md) |
| E4 | Majority Element | Easy | ✅ | [筆記](arrays_and_hashing/010_majority_element_notes.md) |

---

### Two Pointers (Days 9-12)

> Two pointers on sorted arrays — trade sorting cost for O(1) space.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Valid Palindrome | Easy | 1 | ✅ | [筆記](two_pointers/001_valid_palindrome_notes.md) |
| 2 | Two Sum II | Medium | 1 | ✅ | [筆記](two_pointers/002_two_sum_ii_notes.md) |
| 3 | 3Sum | Medium | 1 | ✅ | [筆記](two_pointers/003_3sum_notes.md) |
| 4 | Container With Most Water | Medium | 1 | ✅ | [筆記](two_pointers/004_container_with_most_water_notes.md) |
| 5 | Trapping Rain Water | Hard | 2 | ✅ | [筆記](two_pointers/005_trapping_rain_water_notes.md) |

---

### Sliding Window (Days 13-17)

> Fixed or variable window over contiguous elements — core for monitoring/metrics scenarios.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Best Time to Buy and Sell Stock | Easy | 1 | ⬜ | |
| 2 | Longest Substring Without Repeating | Medium | 1 | 🔄 | [code](sliding_window/001_longest_substring_without_repeating.py) (brute, 待收尾) |
| 3 | Longest Repeating Character Replacement | Medium | 2 | ⬜ | |
| 4 | Permutation in String | Medium | 1 | 🔄 | [code](sliding_window/002_permutation_in_string.py) (到 Step E) |
| 5 | Minimum Window Substring | Hard | 2 | ⬜ | |
| 6 | Sliding Window Maximum | Hard | 2 | ✅ | [筆記](sliding_window/003_sliding_window_maximum_notes.md) |

---

### Stack (Days 18-22)

> LIFO for matching, nesting, and monotonic problems — like undo stacks and call stacks.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Valid Parentheses | Easy | 1 | ✅ | [code](stack/001_valid_parentheses.py) |
| 2 | Min Stack | Medium | 1 | ✅ | [筆記](stack/003_min_stack_notes.md) |
| 3 | Evaluate Reverse Polish Notation | Medium | 1 | ✅ | [code](stack/002_evaluate_rpn.py) |
| 4 | Generate Parentheses | Medium | 2 | ⬜ | (屬 backtracking，先跳) |
| 5 | Daily Temperatures | Medium | 1 | ✅ | [code](stack/004_daily_temperatures.py) |
| 6 | Car Fleet | Medium | 2 | ✅ | [code](stack/005_car_fleet.py) |
| 7 | Largest Rectangle in Histogram | Hard | 2 | ✅ | [筆記](stack/006_largest_rectangle_in_histogram_notes.md)（stack optimal 未冷寫，待 re-do） |

---

### Binary Search (Days 23-27)

> Halve the search space each step — like `git bisect` finding the breaking commit.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Binary Search | Easy | 1 | ⬜ | |
| 2 | Search a 2D Matrix | Medium | 1 | ⬜ | |
| 3 | Koko Eating Bananas | Medium | 1 | ⬜ | |
| 4 | Find Minimum in Rotated Sorted Array | Medium | 1 | ⬜ | |
| 5 | Search in Rotated Sorted Array | Medium | 1 | ⬜ | |
| 6 | Time Based Key-Value Store | Medium | 2 | ⬜ | |
| 7 | Median of Two Sorted Arrays | Hard | 2 | ⬜ | |

---

### Linked List (Days 28-33)

> Pointer manipulation — like middleware pipelines where each node points to the next handler.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Reverse Linked List | Easy | 1 | ⬜ | |
| 2 | Merge Two Sorted Lists | Easy | 1 | ⬜ | |
| 3 | Reorder List | Medium | 2 | ⬜ | |
| 4 | Remove Nth Node From End | Medium | 1 | ⬜ | |
| 5 | Copy List with Random Pointer | Medium | 2 | ⬜ | |
| 6 | Add Two Numbers | Medium | 2 | ⬜ | |
| 7 | Linked List Cycle | Easy | 1 | ⬜ | |
| 8 | Find the Duplicate Number | Medium | 2 | ⬜ | |
| 9 | LRU Cache | Medium | 1 | ⬜ | |
| 10 | Merge K Sorted Lists | Hard | 2 | ⬜ | |
| 11 | Reverse Nodes in K-Group | Hard | 2 | ⬜ | |

---

### 🎯 Checkpoint: Pattern ID Drill (Day 34)

Given 10 problem descriptions (unseen), identify the correct pattern in < 30 sec each.
**Pass**: 8/10 correct → proceed to Phase 2.
**Fail**: Review weak patterns before continuing.

---

## Phase 2: Structure Patterns (Days 35-68)

> **Goal**: Tackle hierarchical and graph-based problems. ~44 problems.

### Trees (Days 35-43)

> Hierarchical structures — directory trees, DNS hierarchy, org charts.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Invert Binary Tree | Easy | 1 | ⬜ | |
| 2 | Maximum Depth of Binary Tree | Easy | 1 | ⬜ | |
| 3 | Diameter of Binary Tree | Easy | 2 | ⬜ | |
| 4 | Balanced Binary Tree | Easy | 2 | ⬜ | |
| 5 | Same Tree | Easy | 2 | ⬜ | |
| 6 | Subtree of Another Tree | Easy | 2 | ⬜ | |
| 7 | Lowest Common Ancestor of BST | Medium | 1 | ⬜ | |
| 8 | Binary Tree Level Order Traversal | Medium | 1 | ⬜ | |
| 9 | Binary Tree Right Side View | Medium | 2 | ⬜ | |
| 10 | Count Good Nodes in Binary Tree | Medium | 2 | ⬜ | |
| 11 | Validate Binary Search Tree | Medium | 1 | ⬜ | |
| 12 | Kth Smallest Element in a BST | Medium | 1 | ⬜ | |
| 13 | Construct Binary Tree | Medium | 2 | ⬜ | |
| 14 | Binary Tree Max Path Sum | Hard | 2 | ⬜ | |
| 15 | Serialize and Deserialize Binary Tree | Hard | 2 | ⬜ | |

---

### Tries (Days 44-45)

> Prefix tree — like autocomplete in a search bar, or route matching in a URL router.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Implement Trie (Prefix Tree) | Medium | 1 | ⬜ | |
| 2 | Design Add and Search Words Data Structure | Medium | 2 | ⬜ | |
| 3 | Word Search II | Hard | 2 | ⬜ | |

---

### Graphs (Days 46-54)

> Service dependency DAG, network topology, Terraform dependency graph.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Number of Islands | Medium | 1 | ⬜ | |
| 2 | Clone Graph | Medium | 1 | ⬜ | |
| 3 | Max Area of Island | Medium | 2 | ⬜ | |
| 4 | Pacific Atlantic Water Flow | Medium | 2 | ⬜ | |
| 5 | Surrounded Regions | Medium | 2 | ⬜ | |
| 6 | Rotting Oranges | Medium | 1 | ⬜ | |
| 7 | Walls and Gates | Medium | 2 | ⬜ | |
| 8 | Course Schedule | Medium | 1 | ⬜ | |
| 9 | Course Schedule II | Medium | 1 | ⬜ | |
| 10 | Redundant Connection | Medium | 2 | ⬜ | |
| 11 | Number of Connected Components | Medium | 2 | ⬜ | |
| 12 | Graph Valid Tree | Medium | 2 | ⬜ | |
| 13 | Word Ladder | Hard | 2 | ⬜ | |

---

### Advanced Graphs (Days 55-57)

> Weighted edges, shortest paths, topological ordering — like network latency optimization and dependency resolution.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Reconstruct Itinerary | Hard | 2 | ⬜ | |
| 2 | Min Cost to Connect All Points | Medium | 2 | ⬜ | |
| 3 | Network Delay Time | Medium | 1 | ⬜ | |
| 4 | Swim in Rising Water | Hard | 2 | ⬜ | |
| 5 | Alien Dictionary | Hard | 2 | ⬜ | |
| 6 | Cheapest Flights Within K Stops | Medium | 1 | ⬜ | |

---

### Heap / Priority Queue (Days 58-61)

> PagerDuty incident queue — always process the highest priority first.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Kth Largest Element in a Stream | Easy | 1 | ⬜ | |
| 2 | Last Stone Weight | Easy | 1 | ⬜ | |
| 3 | K Closest Points to Origin | Medium | 2 | ⬜ | |
| 4 | Kth Largest Element in an Array | Medium | 2 | ⬜ | |
| 5 | Task Scheduler | Medium | 1 | ⬜ | |
| 6 | Design Twitter | Medium | 2 | ⬜ | |
| 7 | Find Median from Data Stream | Hard | 1 | ⬜ | |

---

### Intervals + Greedy (Days 62-67)

> Maintenance windows, on-call scheduling, autoscaling decisions.

**Intervals:**
| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Insert Interval | Medium | 1 | ⬜ | |
| 2 | Merge Intervals | Medium | 1 | ⬜ | |
| 3 | Non-overlapping Intervals | Medium | 2 | ⬜ | |
| 4 | Meeting Rooms | Easy | 1 | ⬜ | |
| 5 | Meeting Rooms II | Medium | 1 | ⬜ | |
| 6 | Minimum Interval to Include Each Query | Hard | 2 | ⬜ | |

**Greedy:**
| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Maximum Subarray | Medium | 1 | ⬜ | |
| 2 | Jump Game | Medium | 1 | ⬜ | |
| 3 | Jump Game II | Medium | 2 | ⬜ | |
| 4 | Gas Station | Medium | 2 | ⬜ | |
| 5 | Hand of Straights | Medium | 2 | ⬜ | |
| 6 | Merge Triplets to Form Target | Medium | 2 | ⬜ | |
| 7 | Partition Labels | Medium | 1 | ⬜ | |
| 8 | Valid Parenthesis String | Medium | 2 | ⬜ | |

---

### 🎯 Checkpoint: Mock Interview #1 (Day 68)

30 minutes, 1 Medium problem, full interview format.
- Must use 6-step framework
- Must identify pattern before coding
- Must discuss complexity and trade-offs

---

## Phase 3: Advanced Patterns (Days 69-87)

> **Goal**: Backtracking, DP, and bit manipulation. ~30 problems.
> **Note**: Phase 3 Tier 2 items are optional for DevOps roles. Include for FAANG SRE targets.

### Backtracking (Days 69-73)

> Try all combinations — like exploring every possible config permutation.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Subsets | Medium | 1 | ⬜ | |
| 2 | Combination Sum | Medium | 1 | ⬜ | |
| 3 | Permutations | Medium | 1 | ⬜ | |
| 4 | Subsets II | Medium | 2 | ⬜ | |
| 5 | Combination Sum II | Medium | 2 | ⬜ | |
| 6 | Word Search | Medium | 2 | ⬜ | |
| 7 | Palindrome Partitioning | Medium | 2 | ⬜ | |
| 8 | Letter Combinations of a Phone Number | Medium | 2 | ⬜ | |
| 9 | N-Queens | Hard | 2 | ⬜ | |

---

### 1-D Dynamic Programming (Days 74-79)

> Memoization — like Redis caching computed results to avoid recomputing.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Climbing Stairs | Easy | 1 | ⬜ | |
| 2 | Min Cost Climbing Stairs | Easy | 2 | ⬜ | |
| 3 | House Robber | Medium | 1 | ⬜ | |
| 4 | House Robber II | Medium | 2 | ⬜ | |
| 5 | Longest Palindromic Substring | Medium | 2 | ⬜ | |
| 6 | Palindromic Substrings | Medium | 2 | ⬜ | |
| 7 | Decode Ways | Medium | 2 | ⬜ | |
| 8 | Coin Change | Medium | 1 | ⬜ | |
| 9 | Maximum Product Subarray | Medium | 2 | ⬜ | |
| 10 | Word Break | Medium | 1 | ⬜ | |
| 11 | Longest Increasing Subsequence | Medium | 1 | ⬜ | |
| 12 | Partition Equal Subset Sum | Medium | 2 | ⬜ | |

---

### 2-D Dynamic Programming (Days 80-84)

> Multi-dimensional state transitions — like capacity planning across regions AND time.

| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Unique Paths | Medium | 1 | ⬜ | |
| 2 | Longest Common Subsequence | Medium | 1 | ⬜ | |
| 3 | Best Time to Buy/Sell Stock with Cooldown | Medium | 1 | ⬜ | |
| 4 | Coin Change II | Medium | 2 | ⬜ | |
| 5 | Target Sum | Medium | 2 | ⬜ | |
| 6 | Interleaving String | Medium | 2 | ⬜ | |
| 7 | Longest Increasing Path in a Matrix | Hard | 2 | ⬜ | |
| 8 | Distinct Subsequences | Hard | 2 | ⬜ | |
| 9 | Edit Distance | Hard | 2 | ⬜ | |
| 10 | Burst Balloons | Hard | 2 | ⬜ | |
| 11 | Regular Expression Matching | Hard | 2 | ⬜ | |

---

### Bit Manipulation + Math & Geometry (Days 85-87)

> Bit tricks for low-level optimization; matrix/geometry for spatial problems.

**Bit Manipulation:**
| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Single Number | Easy | 1 | ⬜ | |
| 2 | Number of 1 Bits | Easy | 1 | ⬜ | |
| 3 | Counting Bits | Easy | 2 | ⬜ | |
| 4 | Reverse Bits | Easy | 2 | ⬜ | |
| 5 | Missing Number | Easy | 2 | ⬜ | |
| 6 | Sum of Two Integers | Medium | 2 | ⬜ | |
| 7 | Reverse Integer | Medium | 2 | ⬜ | |

**Math & Geometry:**
| # | Problem | Difficulty | Tier | Status | Notes |
|---|---------|-----------|------|--------|-------|
| 1 | Rotate Image | Medium | 1 | ⬜ | |
| 2 | Spiral Matrix | Medium | 2 | ⬜ | |
| 3 | Set Matrix Zeroes | Medium | 1 | ⬜ | |
| 4 | Happy Number | Easy | 2 | ⬜ | |
| 5 | Plus One | Easy | 2 | ⬜ | |
| 6 | Pow(x, n) | Medium | 2 | ⬜ | |
| 7 | Multiply Strings | Medium | 2 | ⬜ | |
| 8 | Detect Squares | Medium | 2 | ⬜ | |

---

## Phase 4: Mock & Mastery (Days 88-95)

> **Goal**: Speed, pattern recognition under pressure, and interview simulation.

### Days 88-89: Pattern Recognition Speed Drill
- [ ] Identify pattern for 30 problems in 15 min (30 sec each)
- [ ] Target: 25/30 correct

### Days 90-91: Timed Mock Interview #2
- [ ] 45 min, 2 problems (1 Medium + 1 Medium/Hard)
- [ ] Full interview format with follow-up questions

### Days 92-93: Weak Spot Reinforcement
- [ ] Revisit lowest-scoring patterns from drills
- [ ] Re-solve 3-4 problems from weak areas

### Days 94-95: Full Mock Interview #3
- [ ] 60 min, 2 problems + follow-up questions
- [ ] Score against interview rubric

---

## DevOps Priority Guide

> If you only have time for ~50 problems, focus on Tier 1 in this order:

| Priority | Pattern | Why (DevOps Relevance) | Tier 1 Count |
|----------|---------|----------------------|--------------|
| 1 | Hash Map | Foundation of everything — DNS lookup, config stores | 9 (7 done ✅) |
| 2 | Two Pointers | Log comparison, sorted data processing | 4 (3 done ✅) |
| 3 | Sliding Window | **HIGH** — monitoring windows, rolling metrics | 3 |
| 4 | Stack | **HIGH** — parsing configs, call stacks, undo ops | 4 |
| 5 | Binary Search | **HIGH** — git bisect, log search, threshold finding | 5 |
| 6 | Graphs | **HIGH** — dependency resolution, network topology | 5 |
| 7 | Advanced Graphs | **HIGH** — shortest path = network latency, Dijkstra | 2 |
| 8 | Trees | MEDIUM — directory trees, basic traversal | 6 |
| 9 | Tries | MEDIUM — autocomplete, route matching, prefix lookup | 1 |
| 10 | Heap | MEDIUM — job scheduling, priority queues | 4 |
| 11 | Intervals | MEDIUM — maintenance windows, on-call rotation | 4 |
| 12 | Greedy | MEDIUM — autoscaling, resource allocation | 3 |
| 13 | Backtracking | LOW — Subsets + Combo Sum + Permutations only | 3 |
| 14 | 1-D DP | LOW — Climbing Stairs + Coin Change + Word Break only | 5 |
| 15 | 2-D DP | LOW — Unique Paths + LCS only | 3 |
| 16 | Bit + Math | LOW — Single Number + Rotate Image only | 3 |

**Minimum viable set**: ~60 Tier 1 problems covers 90% of interview patterns.

---

## Weekly Review Flow

> Every Saturday (or after completing a pattern section), run this review.

1. **Pick 3 Topics**: 1 from this week + 2 from past weeks (random)
2. **Blind Recall**: For each topic:
   - What pattern does it use? When do you use it?
   - Walk through the template/approach
   - Name 2 problems that use this pattern
3. **Score**: `Pattern Name: X/3` (pattern ID, approach, examples)
4. **Gap Check**: Open notes, compare with recall, mark blind spots
5. **Quick Drill**: Re-solve 1 problem from weakest pattern (no peeking at notes)

---

## Progress Summary

```
NeetCode 150 Progress: 21 / 150 (14%)
Extra Practice:         4 / 4   (100%)
Total Completed:        25 problems (+2 in progress: Sliding Window #2, #4)

Total Duration:         ~95 days (flexible)
NeetCode 150:           150 problems (60 Tier 1 + 90 Tier 2)
Checkpoints:            1 pattern drill (Day 34) + 1 mock (Day 68)
Mock Interviews:        3 (Day 68, Day 90-91, Day 94-95)

Phase 0: ⬜ Not started (Days 1-3)
Phase 1: 🔄 In progress (Days 4-34)
         Hash Map 9/9 ✅ + Extra 4/4 ✅ | Two Pointers 5/5 ✅
         Sliding Window 1/6 (+2 in progress) | Stack 6/7 ✅ (Generate Parentheses skipped)
         Binary Search 0/7 ⬜ | Linked List 0/11 ⬜
Phase 2: ⬜ Not started (Days 35-68)
Phase 3: ⬜ Not started (Days 69-87)
Phase 4: ⬜ Not started (Days 88-95)

Current: Phase 1 — finish Sliding Window, then Binary Search
```
