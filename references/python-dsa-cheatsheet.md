# Python for LeetCode — Quick Reference

> Read this during Phase 0 Session 3, then use as a reference throughout.

---

## Core Data Structures

### List (Dynamic Array)
```python
# Creation
arr = [1, 2, 3]
arr = [0] * n              # n zeros
arr = [[0] * cols for _ in range(rows)]  # 2D array (NOT [[0]*cols]*rows!)

# Operations                    Time
arr.append(x)                 # O(1) amortized
arr.pop()                     # O(1) — remove last
arr.pop(i)                    # O(n) — remove at index
arr.insert(i, x)              # O(n)
arr[i]                        # O(1) — access
arr[i:j]                      # O(j-i) — slice
len(arr)                      # O(1)
x in arr                     # O(n) — use set for O(1) lookup!
arr.sort()                    # O(n log n) — in-place
sorted(arr)                   # O(n log n) — returns new list
arr.reverse()                 # O(n) — in-place
arr[::-1]                     # O(n) — returns new list
```

### Dict (Hash Map)
```python
# Creation
d = {}
d = {'a': 1, 'b': 2}

# Operations                    Time
d[key] = value                # O(1)
d[key]                        # O(1) — KeyError if missing
d.get(key, default)           # O(1) — returns default if missing
key in d                     # O(1)
del d[key]                    # O(1)
d.keys()                      # O(1) to create view
d.values()                    # O(1) to create view
d.items()                     # O(1) to create view
```

### Set
```python
# Creation
s = set()
s = {1, 2, 3}

# Operations                    Time
s.add(x)                      # O(1)
s.remove(x)                   # O(1) — KeyError if missing
s.discard(x)                  # O(1) — no error if missing
x in s                       # O(1) ← this is why you use sets!
s1 & s2                       # intersection
s1 | s2                       # union
s1 - s2                       # difference
```

### collections Module
```python
from collections import defaultdict, Counter, deque

# defaultdict — dict with default value
d = defaultdict(list)         # d[key] auto-creates []
d = defaultdict(int)          # d[key] auto-creates 0
d = defaultdict(set)          # d[key] auto-creates set()

# Counter — count frequencies
c = Counter([1, 1, 2, 3])    # Counter({1: 2, 2: 1, 3: 1})
c.most_common(k)              # top k frequent
c[item]                       # frequency of item (0 if missing)

# deque — double-ended queue (for BFS, sliding window)
q = deque()
q.append(x)                   # O(1) — add to right
q.appendleft(x)               # O(1) — add to left
q.pop()                       # O(1) — remove from right
q.popleft()                   # O(1) — remove from left
```

### heapq (Min-Heap)
```python
import heapq

# Python has MIN-heap only! For max-heap, negate values.
heap = []
heapq.heappush(heap, x)       # O(log n)
heapq.heappop(heap)            # O(log n) — removes smallest
heap[0]                        # O(1) — peek smallest (don't pop)
heapq.heapify(arr)             # O(n) — convert list to heap

# Max-heap trick: push -x, pop gives -x (negate back)
heapq.heappush(heap, -x)
val = -heapq.heappop(heap)

# Top K pattern
heapq.nlargest(k, arr)        # O(n log k)
heapq.nsmallest(k, arr)       # O(n log k)
```

## Common Patterns

### Sorting
```python
arr.sort()                         # in-place, returns None
arr.sort(key=lambda x: x[1])      # sort by second element
arr.sort(key=lambda x: -x)        # descending
sorted(arr)                        # returns new sorted list
sorted(arr, reverse=True)          # descending

# Custom sort: sort by multiple keys
arr.sort(key=lambda x: (x[0], -x[1]))  # asc by first, desc by second
```

### String Operations
```python
s = "hello"
s[i]                          # access char
s[i:j]                        # slice
s[::-1]                       # reverse
''.join(list_of_chars)        # join chars into string
s.split(',')                  # split by delimiter
ord('a')                      # 97 — char to ASCII
chr(97)                       # 'a' — ASCII to char
s.isalnum()                   # alphanumeric check
s.lower()                     # lowercase
```

### Common Tricks
```python
# Infinity
float('inf')                  # positive infinity
float('-inf')                 # negative infinity

# Integer division
7 // 2                        # 3 (floor division)
-7 // 2                       # -4 (floors toward negative!)
int(-7 / 2)                   # -3 (truncates toward zero — usually what you want)

# Swap without temp
a, b = b, a

# Enumerate
for i, val in enumerate(arr):

# Zip
for a, b in zip(arr1, arr2):

# List comprehension
squares = [x**2 for x in range(10)]
filtered = [x for x in arr if x > 0]

# Dictionary comprehension
d = {k: v for k, v in items}
```

## Gotchas

| Gotcha | Wrong | Right |
|--------|-------|-------|
| 2D array creation | `[[0]*3]*3` (shared refs!) | `[[0]*3 for _ in range(3)]` |
| Mutable default arg | `def f(arr=[])` | `def f(arr=None): arr = arr or []` |
| String immutability | `s[0] = 'H'` (error!) | `s = 'H' + s[1:]` or use list |
| Integer division | `-7 // 2 = -4` | `int(-7 / 2) = -3` |
| No integer overflow | Python has arbitrary precision | Note this vs other languages! |
| Shallow copy | `b = a` (same reference) | `b = a[:]` or `b = a.copy()` |
