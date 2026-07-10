# Student Progress

> Single source of truth for where the student is. Read at session start; written at
> mode boundaries (start of a problem, after a gate, end of session) — not every micro-step.
> Three blocks only. We track what changes a decision, nothing more.

`notes_lang: mixed`  ·  `language: bilingual`  ·  `started: YYYY-MM-DD`  ·  `sessions: 0`

---

## 1. Resume

> Where we pick up next time. Clear/overwrite at the end of each session.

| Field | Value |
|-------|-------|
| **Pattern / problem** | e.g., Sliding Window — Longest Substring |
| **Mode** | Drill / Learn / Cold Solve / Mock |
| **Next action** | e.g., stuck filling the window-shrink line; resume at fill-in-the-blank |

---

## 2. Mistake Registry  🔴

> The most valuable block. Every wrong answer, misconception, or 手感 slip goes here.
> Append-only — add rows, don't restructure. These drive what to re-drill.

| Date | Pattern / problem | The mistake | Status |
|------|-------------------|-------------|--------|
| | | | ❌ open / ✅ resolved |

---

## 3. Pattern Fluency

> Measures what the student can write COLD, not how many problems they've seen.
> A pattern hits the **bar** when both are true: (a) cold 0-bug skeleton, and
> (b) solved one unseen problem in it (Cold Solve). This replaces phase gates.

| Pattern | Cold reps (0-bug) | Last cold pass | Cold Solve cleared? | At bar? |
|---------|-------------------|----------------|---------------------|---------|
| Arrays & Hashing | 0 | — | no | ⬜ |
| Two Pointers | 0 | — | no | ⬜ |
| Sliding Window | 0 | — | no | ⬜ |
| Stack | 0 | — | no | ⬜ |
| Binary Search | 0 | — | no | ⬜ |
| Linked List | 0 | — | no | ⬜ |
| Trees | 0 | — | no | ⬜ |
| Heap / Priority Queue | 0 | — | no | ⬜ |
| Backtracking | 0 | — | no | ⬜ |
| Tries | 0 | — | no | ⬜ |
| Graphs | 0 | — | no | ⬜ |
| 1-D DP | 0 | — | no | ⬜ |
| 2-D DP | 0 | — | no | ⬜ |
| Greedy | 0 | — | no | ⬜ |
| Intervals | 0 | — | no | ⬜ |
| Bit Manipulation | 0 | — | no | ⬜ |

> At bar: ⬜ not yet │ 🟡 skeleton cold but no Cold Solve │ 🟢 both cleared
> Add `+1` to Cold reps only on a next-day, crutches-off, 0-bug reproduction.
