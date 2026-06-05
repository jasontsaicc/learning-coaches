# 4-Step Problem-Solving Framework

> Practice this framework on EVERY problem until it's muscle memory.
> In interviews, thinking aloud through these steps shows structured problem-solving.

---

## The Framework

### Step 1: Understand (1-2 min)
- Read the problem statement carefully — TWICE
- Identify: inputs, outputs, constraints
- Ask yourself:
  - What are the input types and ranges?
  - Are there duplicates? Negative numbers? Empty input?
  - What should I return if input is invalid?
- Write 2-3 test cases (including at least 1 edge case)
- In interviews: ask the interviewer clarifying questions

**Edge cases to always consider:**
| Input Type | Edge Cases |
|-----------|------------|
| Array | Empty [], single element [x], all same values, sorted/reverse sorted |
| String | Empty "", single char, all same chars, unicode |
| Integer | 0, negative, MAX_INT, MIN_INT |
| Linked List | None, single node, cycle |
| Tree | None, single node, skewed (all left or all right) |
| Graph | Disconnected, single node, cycle, self-loop |

### Step 2: Match (1-2 min)
- Which pattern(s) could apply? (refer to Pattern Map)
- WHY does this pattern fit? Explain the match:
  - "The input is sorted → Two Pointers or Binary Search"
  - "We need to find contiguous subarray → Sliding Window"
  - "We need O(1) lookup → Hash Map"
- What data structure(s) do I need?
- Estimate time/space complexity BEFORE coding

**Pattern Recognition Signals:**
| If you see... | Think... |
|---------------|----------|
| "Find pair/group" or "frequency" | Hash Map |
| Sorted array + find pair | Two Pointers |
| Contiguous subarray/substring | Sliding Window |
| "Valid parentheses" or LIFO | Stack |
| Sorted + find target/boundary | Binary Search |
| "Reverse" or "merge" linked list | Two Pointers on LL |
| Tree traversal | DFS (recursive) or BFS (queue) |
| Prefix matching | Trie |
| "K largest/smallest" | Heap |
| "All combinations/permutations" | Backtracking |
| Grid traversal / connected components | BFS/DFS on graph |
| "Shortest path" | BFS / Dijkstra |
| "How many ways" / "minimum cost" | Dynamic Programming |
| "Maximum/minimum with constraint" | DP or Greedy |
| Overlapping intervals | Sort + sweep |
| Bit-level operations | Bit Manipulation |

### Step 2.5: Narrate the approach in plain words (the anti-blank bridge)

> This step exists because of one specific failure: you understand the problem, you even know the pattern, but you put your hands on the keyboard and your mind goes blank. That blank is not a knowledge gap. It is a missing translation layer. You are trying to jump straight from a pattern name ("two pointers") to syntax, with nothing in between.

Before writing any code, hold a plain-language Q&A with yourself. Four questions cover almost every array / string / graph problem:

1. **What am I computing?** Name the quantity and how it is built. ("area = width × the shorter wall")
2. **What must I try, and what is the brute force?** Say the O(n²) / O(2^n) version out loud first, even if you will not use it. It anchors everything that follows.
3. **How do I shrink the work / move?** What pointer moves, what goes into the map, which branch the recursion takes. And WHY that move is safe (often: "the other move can never be better, so I drop it").
4. **When do I stop?** The exact termination condition.

The answers are plain sentences. The code is just their translation. The first line falls out of question 1 or 3 almost mechanically (`l, r = 0, len(a)-1`, `seen = {}`, `dq = deque([start])`). You are no longer generating code from nothing; you are transcribing decisions you already made in words.

**Drill these four questions until they are automatic.** They are the fixed checklist your brain runs the moment it hits a blank screen. The blank disappears once the first move comes from a sentence you just said, not from thin air.

### Step 3: Plan & Code (10-20 min)
- Write pseudocode or outline steps (3-5 bullet points)
- Implement in Python:
  - Use meaningful variable names (not `i`, `j` for everything)
  - Handle edge cases at the top
  - Write clean, readable code
- Think aloud as you code (interview habit):
  - "I'll start by creating a hash map to store..."
  - "This loop processes each element once, so it's O(n)..."

### Step 4: Verify (2-3 min)
- Trace through your test cases manually (dry run on paper/whiteboard)
- Check edge cases from Step 1
- Confirm time/space complexity matches your Step 2 estimate
- Ask yourself: "Can I do better?"
  - If yes: explain the optimization, decide if time allows implementing it
  - If no: state confidently "This is optimal because..."

---

## An articulable approach IS the deliverable (interview reframe)

You will almost never get a problem you have already solved. So the goal is NOT "recall the exact solution." The goal is: **produce a clear, discussable approach, out loud, even when you cannot fully solve it.**

Interviewers score the conversation, not just the final code:
- Stating the brute force and its complexity = points, always. Never skip it because it feels "too dumb."
- Naming the pattern and explaining WHY it fits = points.
- "Here is my plan; the part I am unsure about is X" = a strong signal, not a weakness. It turns a stuck moment into a collaboration with the interviewer.
- A correct approach with a small bug beats silence at a blank screen.

So train the Step 2.5 plain-language Q&A as a standalone skill, separate from typing solutions blind. They are two different abilities:
- **Approach articulation** → produce a discussable plan for an UNSEEN problem. Saves you when you have never met the problem (the common case).
- **Skeleton fluency** → type a KNOWN pattern cold, fast, bug-free.

Interviews need both. Practice them separately.

---

## Common Mistakes by Step

| Step | Mistake | Fix |
|------|---------|-----|
| 1 | Jump to coding immediately | Force yourself to write test cases first |
| 1 | Miss edge cases | Use the edge case table above |
| 2 | Pick wrong pattern | Explain WHY out loud — if you can't explain, reconsider |
| 2 | Skip complexity estimate | Always estimate BEFORE coding |
| 2.5 | Mind goes blank at the first line | Run the 4 plain-language questions; transcribe the answer, don't invent code |
| 3 | Write messy code | Use helper functions for complex logic |
| 3 | Silent coding | Practice talking while coding |
| 4 | Skip verification | Always trace at least 1 test case |
| 4 | Say "I think it works" | Prove it by tracing, don't guess |

---

## Example Walkthrough: Two Sum (LC #1)

**Step 1: Understand**
- Input: array of integers + target integer
- Output: indices of two numbers that add to target
- Constraints: exactly one solution, can't use same element twice
- Test cases: [2,7,11,15] target=9 → [0,1], [3,3] target=6 → [0,1]

**Step 2: Match**
- "Find pair" → Hash Map
- Why: need O(1) lookup for complement (target - current)
- Expected: O(n) time, O(n) space

**Step 2.5: Narrate in plain words**
- What am I computing? The two indices whose values add to `target`.
- Brute force? Check every pair, O(n²). Too slow.
- How to shrink? As I walk the array once, for each number ask "have I already seen its complement (`target - num`)?" That needs O(1) lookup → a hash map of value→index. First line writes itself: `seen = {}`.
- When to stop? The moment a complement is found, return; the problem promises exactly one answer.

**Step 3: Plan & Code**
```python
def twoSum(nums, target):
    seen = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

**Step 4: Verify**
- [2,7,11,15], target=9:
  - i=0: complement=7, seen={} → no match, seen={2:0}
  - i=1: complement=2, seen={2:0} → match! return [0,1] ✅
- Complexity: O(n) time, O(n) space ✅ matches estimate
