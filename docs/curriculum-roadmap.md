# LeetCode Curriculum Roadmap & Daily Tracker

> One-stop reference: learning path → daily tracking → pattern dependencies

---

## 1. Learning Roadmap

### Phase Overview

```
Phase 0          Phase 1                    Phase 2                    Phase 3              Phase 4
Foundation ──→  Core Patterns ──→          Structure Patterns ──→     Advanced ──→         Mock & Mastery
Day 1-3         Day 4-34                   Day 35-68                  Day 69-87            Day 88-95
                     │                          │                         │
                  Checkpoint               Mock Interview #1         Mock Interview #2    Final Mock #3
                  (Day 34)                 (Day 68)                  (Day 90-91)          (Day 94-95)
```

### Pattern Dependency Map

```
Hash Map (foundation) ─┬──→ Sliding Window (uses hash map for tracking)
                       ├──→ Two Pointers (complement lookup)
                       └──→ Graph (adjacency list = hash map)

Two Pointers ──→ Linked List (fast/slow pointer)
             └──→ Binary Search (left/right pointers)

Tree DFS ──→ Graph DFS ──→ Backtracking (DFS + undo)
Tree BFS ──→ Graph BFS

Hash Map + Sorting ──→ Intervals (sort + sweep)
Greedy ──→ Intervals (local optimal choice)
Recursion (Trees) ──→ Dynamic Programming (recursion + memoization)
```

### DevOps Relevance Ratings

| Pattern | DevOps Relevance | Why |
|---------|:---:|-----|
| Hash Map | ★★★★★ | DNS lookup, config store, key-value everything |
| Two Pointers | ★★★☆☆ | Log comparison, sorted data processing |
| Sliding Window | ★★★★★ | Monitoring dashboards, rolling metrics, rate limiting |
| Stack | ★★★★☆ | Config parsing, call stacks, Terraform state (LIFO) |
| Binary Search | ★★★★★ | git bisect, log search, binary deploy |
| Linked List | ★★☆☆☆ | Middleware pipeline concept, but rarely coded directly |
| Trees | ★★★☆☆ | Directory trees, DNS hierarchy |
| Tries | ★★★☆☆ | Autocomplete, URL route matching, prefix lookup |
| Graphs | ★★★★★ | Service dependency DAG, network topology, Terraform graph |
| Advanced Graphs | ★★★★☆ | Shortest path = network latency, Dijkstra for routing |
| Heap | ★★★☆☆ | Job scheduling, PagerDuty priority queue |
| Intervals | ★★★☆☆ | Maintenance windows, on-call rotation |
| Greedy | ★★★☆☆ | Autoscaling decisions, resource allocation |
| Backtracking | ★☆☆☆☆ | Rare in DevOps interviews |
| 1-D DP | ★★☆☆☆ | Occasionally appears, know basics |
| 2-D DP | ★☆☆☆☆ | Very rare for DevOps roles |
| Bit Manipulation | ★★☆☆☆ | Subnet masks, permissions (chmod) |
| Math & Geometry | ★☆☆☆☆ | Rarely tested |

---

## 2. Daily Progress Tracker

### Phase 0: Problem-Solving Foundation (Day 1-3)

| Day | Topic | Goal | Output | Done |
|-----|-------|------|--------|------|
| 1 | 6-Step Framework + Big-O Review | Build structured approach | `notes/day01-problem-solving-framework.md` | ⬜ |
| 2 | Pattern Recognition Checklist | Learn signal → pattern mapping | `notes/day02-pattern-recognition.md` | ⬜ |
| 3 | Pattern ID Drill (no coding) | Score 6/10 on blind pattern ID | `notes/day03-pattern-drill.md` | ⬜ |

### Phase 1: Core Patterns (Day 4-34)

| Day | Pattern / Topic | Problems | Tier 1 Done | Total Done | Done |
|-----|----------------|----------|:-----------:|:----------:|------|
| 4-8 | Hash Map Patterns | 9 NeetCode + 4 Extra | 7/9 | 11/13 | 🔄 |
| 9-12 | Two Pointers | 5 | 3/4 | 3/5 | 🔄 |
| 13-17 | Sliding Window | 6 | 0/3 | 0/6 | ⬜ |
| 18-22 | Stack | 7 | 0/4 | 0/7 | ⬜ |
| 23-27 | Binary Search | 7 | 0/5 | 0/7 | ⬜ |
| 28-33 | Linked List | 11 | 0/5 | 0/11 | ⬜ |
| **34** | **🎯 Pattern ID Checkpoint** | **10 blind IDs** | **—** | **—** | ⬜ |

### Phase 2: Structure Patterns (Day 35-68)

| Day | Pattern / Topic | Problems | Tier 1 Done | Total Done | Done |
|-----|----------------|----------|:-----------:|:----------:|------|
| 35-43 | Trees | 15 | 0/6 | 0/15 | ⬜ |
| 44-45 | Tries | 3 | 0/1 | 0/3 | ⬜ |
| 46-54 | Graphs | 13 | 0/5 | 0/13 | ⬜ |
| 55-57 | Advanced Graphs | 6 | 0/2 | 0/6 | ⬜ |
| 58-61 | Heap / Priority Queue | 7 | 0/4 | 0/7 | ⬜ |
| 62-67 | Intervals + Greedy | 14 | 0/7 | 0/14 | ⬜ |
| **68** | **🎯 Mock Interview #1** | **1 Medium, 30 min** | **—** | **—** | ⬜ |

### Phase 3: Advanced Patterns (Day 69-87)

| Day | Pattern / Topic | Problems | Tier 1 Done | Total Done | Done |
|-----|----------------|----------|:-----------:|:----------:|------|
| 69-73 | Backtracking | 9 | 0/3 | 0/9 | ⬜ |
| 74-79 | 1-D DP | 12 | 0/5 | 0/12 | ⬜ |
| 80-84 | 2-D DP | 11 | 0/3 | 0/11 | ⬜ |
| 85-87 | Bit Manipulation + Math | 15 | 0/3 | 0/15 | ⬜ |

### Phase 4: Mock & Mastery (Day 88-95)

| Day | Activity | Goal | Done |
|-----|----------|------|------|
| 88-89 | Pattern Recognition Speed Drill | 25/30 in 15 min | ⬜ |
| 90-91 | Timed Mock Interview #2 | 45 min, 2 problems | ⬜ |
| 92-93 | Weak Spot Reinforcement | Re-solve 3-4 weak problems | ⬜ |
| 94-95 | Full Mock Interview #3 | 60 min, 2 problems + follow-ups | ⬜ |

---

## 3. Concept Coverage Matrix

> Track which core concepts you've practiced across patterns.

| Concept | Hash Map | Two Ptr | Sliding Win | Stack | Binary Search | Linked List | Trees | Graphs | Heap | Intervals | Greedy | DP |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Hash table lookup | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Two pointer technique | — | ✅ | — | — | — | — | — | — | — | — | — | — |
| Sorting as preprocessing | ✅ | ✅ | — | — | — | — | — | — | — | — | — | — |
| Space-time trade-off | ✅ | ✅ | — | — | — | — | — | — | — | — | — | — |
| Edge case handling | ✅ | ✅ | — | — | — | — | — | — | — | — | — | — |
| Deduplication | ✅ | ✅ | — | — | — | — | — | — | — | — | — | — |
| Prefix/suffix processing | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| Recursion | — | — | — | — | — | — | — | — | — | — | — | — |
| BFS / DFS | — | — | — | — | — | — | — | — | — | — | — | — |
| Memoization | — | — | — | — | — | — | — | — | — | — | — | — |

---

## 4. Quick Stats

```
Total Duration:        ~95 days (flexible)
NeetCode 150:          150 problems (60 Tier 1 + 90 Tier 2)
Extra Practice:        4 problems (completed)
Checkpoints:           1 pattern drill (Day 34)
Mock Interviews:       3 (Day 68, Day 90-91, Day 94-95)
Patterns Covered:      16 (Hash Map through Bit Manipulation, incl. Tries + Advanced Graphs)
Current Progress:      14/154 completed (9.1%)
```
