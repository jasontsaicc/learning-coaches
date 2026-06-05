# Big-O Complexity Reference

> Read this during Phase 0 Session 2, then use as a reference throughout.

---

## Common Complexities (fastest → slowest)

```
O(1)       → Constant      (hash map lookup, array access)
O(log n)   → Logarithmic   (binary search)
O(n)       → Linear        (single loop, two pointers)
O(n log n) → Linearithmic  (sorting)
O(n²)      → Quadratic     (nested loops)
O(2^n)     → Exponential   (subsets, backtracking without pruning)
O(n!)      → Factorial     (permutations)
```

For n = 1,000,000:
| Complexity | Operations | Feasible? |
|-----------|------------|-----------|
| O(1) | 1 | Yes |
| O(log n) | 20 | Yes |
| O(n) | 1,000,000 | Yes |
| O(n log n) | 20,000,000 | Yes |
| O(n^2) | 1,000,000,000,000 | No — too slow |
| O(2^n) | infinity | No |

**Rule of thumb:** LeetCode time limit is ~10^8 operations/second. If n <= 10^4, O(n^2) is OK. If n <= 10^5, need O(n log n). If n <= 10^6+, need O(n) or better.

## Data Structure Operations

| Structure | Access | Search | Insert | Delete | Notes |
|-----------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(1) append |
| Hash Map | — | O(1)* | O(1)* | O(1)* | *amortized |
| Hash Set | — | O(1)* | O(1)* | O(1)* | *amortized |
| Stack | O(n) | O(n) | O(1) | O(1) | push/pop |
| Queue | O(n) | O(n) | O(1) | O(1) | enqueue/dequeue |
| Heap | — | O(n) | O(log n) | O(log n) | peek: O(1) |
| BST (balanced) | — | O(log n) | O(log n) | O(log n) | |
| Linked List | O(n) | O(n) | O(1)* | O(1)* | *at known position |
| Trie | — | O(m) | O(m) | O(m) | m = key length |

## Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable? |
|-----------|------|---------|-------|-------|---------|
| Python sort (Timsort) | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) | O(log n) | No |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |

## Algorithm Pattern Complexities

| Pattern | Typical Time | Typical Space |
|---------|-------------|---------------|
| Two Pointers | O(n) | O(1) |
| Sliding Window | O(n) | O(k) window size |
| Binary Search | O(log n) | O(1) |
| BFS/DFS (graph) | O(V + E) | O(V) |
| BFS/DFS (grid) | O(m x n) | O(m x n) |
| Backtracking | O(2^n) or O(n!) | O(n) recursion depth |
| Dynamic Programming | O(n x m) varies | O(n x m) varies |
| Topological Sort | O(V + E) | O(V) |
| Union-Find | O(alpha(n)) approx O(1) | O(n) |
| Dijkstra | O(E log V) | O(V) |

## How to Analyze Your Solution

### Time Complexity
1. **Count nested loops:** 1 loop = O(n), 2 nested = O(n^2)
2. **Recursive calls:** draw the call tree, count total calls
3. **Built-in operations:** sorting = O(n log n), `in` on list = O(n)
4. **Multiple steps:** add them (O(n) + O(n log n) = O(n log n))

### Space Complexity
1. **What grows with input?** New arrays, hash maps, recursion stack
2. **Recursion depth:** each call uses stack space
3. **In-place vs copy:** modifying input = O(1) extra space
4. **Don't count input:** only count EXTRA space used

### Quick Checks
- "Is this fast enough?" → Check constraint: n <= 10^4 allows O(n^2)
- "Can I do better?" → Lower bound: sorting >= O(n log n), searching unsorted >= O(n)
- "Am I using extra space?" → Check if you created new data structures
