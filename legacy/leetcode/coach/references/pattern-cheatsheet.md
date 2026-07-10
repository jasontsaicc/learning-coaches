# Pattern Cheatsheet

> Quick reference for all 18 NeetCode 150 patterns with Python templates.
> The ~8-10 core skeletons here are what Drill mode is built on. Read this when drilling a
> pattern's skeleton or when teaching a pattern's template in Learn mode.

---

### Arrays & Hashing

**When to use:** Problems requiring O(1) lookups, counting frequencies, or detecting duplicates
**Key signal:** "find duplicates", "frequency", "two sum", "group by"

```python
# Frequency counter
from collections import Counter
freq = Counter(arr)  # {element: count}

# HashMap for complement lookup
seen = {}
for i, num in enumerate(arr):
    complement = target - num
    if complement in seen:
        return [seen[complement], i]
    seen[num] = i
```

---

### Two Pointers

**When to use:** Sorted arrays, pair/triplet problems, palindrome checks
**Key signal:** "sorted array", "pair that sums to", "palindrome", "remove duplicates"

```python
# Converging pointers on sorted array
left, right = 0, len(arr) - 1
while left < right:
    total = arr[left] + arr[right]
    if total == target:
        return [left, right]
    elif total < target:
        left += 1
    else:
        right -= 1
```

---

### Sliding Window

**When to use:** Subarray/substring problems with contiguous elements
**Key signal:** "maximum/minimum subarray", "longest substring", "window of size k"

```python
# Fixed-size window
def fixed_window(arr, k):
    window_sum = sum(arr[:k])
    best = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        best = max(best, window_sum)
    return best

# Dynamic-size window
def dynamic_window(s):
    left = 0
    seen = set()
    best = 0
    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        best = max(best, right - left + 1)
    return best
```

---

### Stack

**When to use:** Matching/nesting problems, next greater/smaller element, expression evaluation
**Key signal:** "valid parentheses", "next greater", "evaluate expression", "monotonic"

```python
# Monotonic stack (next greater element)
def next_greater(arr):
    result = [-1] * len(arr)
    stack = []  # indices
    for i, num in enumerate(arr):
        while stack and arr[stack[-1]] < num:
            result[stack.pop()] = num
        stack.append(i)
    return result
```

---

### Binary Search

**When to use:** Sorted data, search space that can be halved, "minimum/maximum that satisfies"
**Key signal:** "sorted array", "find target", "minimum speed/capacity", "search in rotated"

```python
# Standard binary search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Binary search on answer (e.g., minimum speed)
def min_speed(piles, h):
    left, right = 1, max(piles)
    while left < right:
        mid = (left + right) // 2
        if can_finish(piles, mid, h):
            right = mid
        else:
            left = mid + 1
    return left
```

---

### Linked List

**When to use:** Pointer manipulation, cycle detection, reversal, merge
**Key signal:** "reverse linked list", "detect cycle", "merge lists", "middle of list"

```python
# Fast/slow pointer (cycle detection)
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Reverse linked list
def reverse(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

---

### Trees

**When to use:** Hierarchical data, recursive problems, level-order processing
**Key signal:** "binary tree", "BST", "depth", "level order", "path sum"

```python
# DFS (recursive)
def dfs(node):
    if not node:
        return 0
    left = dfs(node.left)
    right = dfs(node.right)
    return 1 + max(left, right)

# BFS (level-order with deque)
from collections import deque
def bfs(root):
    if not root:
        return []
    queue = deque([root])
    result = []
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

---

### Heap / Priority Queue

**When to use:** Top-K problems, scheduling, stream median, merge K sorted
**Key signal:** "kth largest", "top k", "merge k sorted", "schedule tasks"

```python
import heapq

# Min-heap (default in Python)
heap = []
heapq.heappush(heap, val)
smallest = heapq.heappop(heap)

# Max-heap (negate values)
heapq.heappush(heap, -val)
largest = -heapq.heappop(heap)

# Top K frequent
def top_k(nums, k):
    freq = Counter(nums)
    return heapq.nlargest(k, freq.keys(), key=freq.get)
```

---

### Backtracking

**When to use:** Generate all combinations/permutations/subsets, constraint satisfaction
**Key signal:** "all combinations", "all permutations", "subsets", "generate", "word search"

```python
def backtrack(candidates, target, start, path, result):
    if target == 0:
        result.append(path[:])
        return
    for i in range(start, len(candidates)):
        if candidates[i] > target:
            break
        path.append(candidates[i])
        backtrack(candidates, target - candidates[i], i, path, result)
        path.pop()  # undo choice
```

---

### Tries

**When to use:** Prefix-based search, autocomplete, word dictionaries
**Key signal:** "prefix", "word dictionary", "starts with", "search words"

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```

---

### Graphs

**When to use:** Connected components, shortest path, cycle detection, traversal
**Key signal:** "number of islands", "course schedule", "clone graph", "connected components"

```python
from collections import deque

# BFS
def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# DFS (recursive)
def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

---

### Advanced Graphs

**When to use:** Weighted shortest path, minimum spanning tree, topological ordering, union-find
**Key signal:** "cheapest path", "network delay", "minimum cost", "course order", "redundant connection"

```python
import heapq

# Dijkstra's shortest path
def dijkstra(graph, start):
    dist = {start: 0}
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float('inf')):
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist

# Topological sort (Kahn's algorithm)
from collections import deque
def topo_sort(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for u, v in prerequisites:
        graph[v].append(u)
        indegree[u] += 1
    queue = deque(i for i in range(num_courses) if indegree[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)
    return order if len(order) == num_courses else []

# Union-Find with path compression
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

---

### 1-D Dynamic Programming

**When to use:** Overlapping subproblems in one dimension, optimal substructure
**Key signal:** "climbing stairs", "house robber", "coin change", "longest increasing"

```python
# Bottom-up 1D DP
def climb_stairs(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# Space-optimized (only need prev two)
def climb_stairs_opt(n):
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
```

---

### 2-D Dynamic Programming

**When to use:** Grid paths, two-sequence comparison, knapsack with 2D state
**Key signal:** "unique paths", "longest common subsequence", "edit distance", "interleaving"

```python
# Grid DP
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]

# Two-sequence DP (LCS)
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
```

---

### Greedy

**When to use:** Local optimal choice leads to global optimal, scheduling, interval selection
**Key signal:** "maximum subarray", "jump game", "gas station", "partition labels"

```python
# Kadane's algorithm (maximum subarray)
def max_subarray(nums):
    max_sum = curr_sum = nums[0]
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum
```

---

### Intervals

**When to use:** Overlapping intervals, scheduling, merge/insert intervals
**Key signal:** "merge intervals", "meeting rooms", "insert interval", "non-overlapping"

```python
# Merge overlapping intervals
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

---

### Math & Geometry

**When to use:** Matrix manipulation, number theory, modular arithmetic
**Key signal:** "rotate image", "spiral matrix", "power", "happy number"

```python
# Fast exponentiation
def my_pow(x, n):
    if n < 0:
        x, n = 1 / x, -n
    result = 1
    while n:
        if n % 2:
            result *= x
        x *= x
        n //= 2
    return result

# Rotate matrix 90° clockwise
def rotate(matrix):
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse each row
    for row in matrix:
        row.reverse()
```

---

### Bit Manipulation

**When to use:** XOR tricks, bit counting, power of 2, single number problems
**Key signal:** "single number", "number of 1 bits", "missing number", "reverse bits"

```python
# XOR to find single number (all others appear twice)
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result

# Count set bits (Hamming weight)
def hamming_weight(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

# Check/set/clear bit
def get_bit(n, i):   return (n >> i) & 1
def set_bit(n, i):   return n | (1 << i)
def clear_bit(n, i): return n & ~(1 << i)
```
