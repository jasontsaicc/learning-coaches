# LeetCode Coach Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code skill that coaches DevOps engineers through NeetCode 150 (Easy + Medium) using Feynman + Simon methods, with progressive brute-to-optimal solving, pattern-based teaching, and mock interviews.

**Architecture:** All changes are Markdown content in a Claude Code skill. SKILL.md is the single source of truth for teaching mechanics. Reference files (curriculum, progress template, notes template, pattern cheatsheet) are loaded on-demand. Evals validate skill behavior.

**Tech Stack:** Markdown, Claude Code skill framework, JSON (evals)

**Spec:** `docs/specs/2026-03-16-leetcode-coach-design.md`

---

## File Structure

```
leetcode-coach/
├── SKILL.md                          # CREATE: Core skill — full teaching flow, gates, scorecards
├── references/
│   ├── curriculum.md                 # CREATE: NeetCode 150 (E+M) + interview extras, 18 categories, 4 Phases
│   ├── progress-template.md          # CREATE: Student progress tracking format
│   ├── notes-template.md             # CREATE: Per-problem notes format
│   └── pattern-cheatsheet.md         # CREATE: 18 Pattern one-liners + Python templates
├── evals/
│   └── evals.json                    # CREATE: 20 eval test cases
├── .gitignore                        # CREATE: Standard ignores
├── README.md                         # CREATE: Install + overview
└── docs/
    ├── specs/
    │   └── 2026-03-16-leetcode-coach-design.md  # EXISTS
    └── plans/
        └── 2026-03-16-leetcode-coach-implementation.md  # THIS FILE
```

---

## Chunk 1: Foundation — Progress Template + Notes Template

### Task 1: Create progress-template.md

**Files:**
- Create: `references/progress-template.md`

This is the foundation for all cross-session features. It must support: mastery tracking, session breakpoints, mistake registry, scorecard history, one-liner library, problem log, phase gate results.

- [ ] **Step 1: Create progress-template.md with full content**

Write the file with content exactly matching the spec's "Progress Tracking" section (spec lines 329-391). Include all sections:
- Student Info table (start date, current phase, current pattern, language, session count, last weekly review, problems solved)
- Current Session (Breakpoint) table
- Topic Mastery table (all 18 patterns with ⬜ initial state, Phase Gate markers at correct positions)
- Problem Log table (with Brute and Optimal complexity columns)
- Scorecard History table
- 🔴 Mistake Registry table
- 🎯 Pattern One-Liner Library table
- Phase Gate Results table

Key differences from SD Coach's progress-template.md:
- "Day" column → removed (LeetCode tracks by problem, not day)
- "Topic" → "Pattern" everywhere
- Add "Problem Log" section (new, not in SD Coach)
- Mastery table has 18 pattern rows (not 30 topic rows)
- Problem Log columns: Session, Problem, Difficulty, Pattern, Solved?, Brute, Optimal, Notes

- [ ] **Step 2: Verify file created**

Run: `head -5 references/progress-template.md`
Expected: Shows "# Student Progress Tracking"

- [ ] **Step 3: Commit**

```bash
git add references/progress-template.md
git commit -m "feat: add progress-template.md — foundation for cross-session tracking"
```

---

### Task 2: Create notes-template.md

**Files:**
- Create: `references/notes-template.md`

- [ ] **Step 1: Create notes-template.md**

Write the file with content exactly matching the spec's "Notes Template" section (spec lines 497-525). Includes:
- Pattern One-Liner section
- Approach section (Brute Force + Optimal + Key Insight, each with Time/Space complexity)
- 🔴 My Mistakes & Misconceptions table
- 🎤 How to Say It in Interview section (Opening, Optimization, Edge cases)
- Sync to Progress File checklist

- [ ] **Step 2: Verify**

Run: `grep "How to Say It" references/notes-template.md`
Expected: Shows "## 🎤 How to Say It in Interview"

- [ ] **Step 3: Commit**

```bash
git add references/notes-template.md
git commit -m "feat: add notes-template.md — per-problem notes with complexity + interview phrasing"
```

---

## Chunk 2: Pattern Cheatsheet + Curriculum

### Task 3: Create pattern-cheatsheet.md

**Files:**
- Create: `references/pattern-cheatsheet.md`

This file is loaded during Step C (Pattern Teaching) to show the student the Pattern's Python template.

- [ ] **Step 1: Create pattern-cheatsheet.md with all 18 patterns**

For each of the 18 NeetCode 150 categories, write:
- Pattern name
- **When to use:** (1 sentence)
- **Key signal:** (keywords that indicate this pattern)
- **Python template(s):** working Python code template

The 18 patterns in curriculum order:

1. **Arrays & Hashing** — HashMap/HashSet for O(1) lookups. Template: frequency counter with `collections.Counter`.
2. **Two Pointers** — Two indices moving toward each other or same direction. Template: left/right converging on sorted array.
3. **Sliding Window** — Fixed or dynamic window over contiguous elements. Templates: fixed-size and dynamic-size (as shown in spec lines 539-559).
4. **Stack** — LIFO for matching/nesting problems. Template: monotonic stack for next-greater-element.
5. **Binary Search** — Halving search space on sorted data. Template: `left, right = 0, len(arr)-1` with `while left <= right`.
6. **Linked List** — Pointer manipulation. Templates: fast/slow pointer (cycle detection), reverse linked list.
7. **Trees** — Recursive traversal. Templates: DFS (inorder/preorder/postorder), BFS (level-order with deque).
8. **Heap / Priority Queue** — Top-K problems. Template: `heapq.nlargest/nsmallest`, min-heap with `heapq`.
9. **Backtracking** — Explore all candidates, prune invalid. Template: recursive with `path.append()` / `path.pop()`.
10. **Tries** — Prefix-based string search. Template: TrieNode class with `children` dict + `is_end` flag.
11. **Graphs** — BFS/DFS traversal. Templates: adjacency list + BFS with deque, DFS with recursion + visited set.
12. **Advanced Graphs** — Dijkstra, topological sort, union-find. Templates: Dijkstra with heapq, topological sort with indegree, Union-Find class.
13. **1-D Dynamic Programming** — Overlapping subproblems in 1D. Template: `dp = [0] * (n+1)` with bottom-up iteration.
14. **2-D Dynamic Programming** — Grid/two-sequence DP. Template: `dp = [[0]*(m+1) for _ in range(n+1)]`.
15. **Greedy** — Local optimal → global optimal. Template: sort + iterate with greedy choice.
16. **Intervals** — Sorting by start/end, merge/overlap detection. Template: sort by start, merge overlapping.
17. **Math & Geometry** — Modular arithmetic, matrix operations. Template: varies by problem.
18. **Bit Manipulation** — XOR, AND, OR, bit shifts. Template: XOR for single number, bit mask operations.

- [ ] **Step 2: Verify pattern count**

Run: `grep -c "^### " references/pattern-cheatsheet.md`
Expected: 18

- [ ] **Step 3: Commit**

```bash
git add references/pattern-cheatsheet.md
git commit -m "feat: add pattern-cheatsheet.md — 18 patterns with Python templates"
```

---

### Task 4: Create curriculum.md

**Files:**
- Create: `references/curriculum.md`

This is the largest reference file. It lists every problem in NeetCode 150 (Easy + Medium only), organized by Phase and category, with prerequisites and interview extras.

- [ ] **Step 1: Create curriculum.md header + Phase 0**

```markdown
# LeetCode Interview Curriculum (NeetCode 150 — Easy + Medium)

> Target: DevOps coding interviews + general tech interviews
> Pace: ~1 problem/day, pattern-based deep learning
> Language: Python

---

## Phase 0: Foundation Patterns

> Build the core problem-solving patterns. Every category here is an entry point or builds on basics.

### Arrays & Hashing

**Core concept:** Use HashMaps/HashSets for O(1) lookups to avoid nested loops
**Prerequisites:** None (entry point)

| # | Problem | Difficulty | Source | Focus |
|---|---------|-----------|--------|-------|
| 1 | Contains Duplicate | Easy | NeetCode 150 | HashSet basics |
| 2 | Valid Anagram | Easy | NeetCode 150 | Frequency counter |
| 3 | Two Sum | Easy | NeetCode 150 | HashMap complement |
| 4 | Group Anagrams | Medium | NeetCode 150 | Sorted key + HashMap |
| 5 | Top K Frequent Elements | Medium | NeetCode 150 | Bucket sort / Counter |
| 6 | Encode and Decode Strings | Medium | NeetCode 150 | Delimiter design |
| 7 | Product of Array Except Self | Medium | NeetCode 150 | Prefix/suffix arrays |
| 8 | Longest Consecutive Sequence | Medium | NeetCode 150 | HashSet + sequence start |
| ★ | Move Zeroes | Easy | Interview Freq | Two pointer variant |
| ★ | Merge Sorted Array | Easy | Interview Freq | In-place merge |
```

Continue with Two Pointers, Sliding Window, Stack for Phase 0. Include Phase 0 Gate at the end.

For each category: follow the curriculum.md format from spec (lines 257-271). List all NeetCode 150 Easy + Medium problems. Add 1-2 ★ interview extras per category where relevant. Mark Hard problems from NeetCode 150 as SKIPPED (don't include them).

- [ ] **Step 2: Add Phase 1 (Binary Search, Linked List, Trees, Heap)**

Same format. Include Phase 1 Gate.

- [ ] **Step 3: Add Phase 2 (Backtracking, Tries, Graphs, Advanced Graphs)**

Same format. Include Phase 2 Gate.

- [ ] **Step 4: Add Phase 3 (1-D DP, 2-D DP, Greedy, Intervals, Math & Geometry, Bit Manipulation)**

Same format. Include Final Gate.

- [ ] **Step 5: Add prerequisites map at the bottom**

Copy the prerequisites map from spec lines 236-254.

- [ ] **Step 6: Verify curriculum structure**

Run: `grep "^### " references/curriculum.md | wc -l`
Expected: 18 (one per category)

Run: `grep "Phase.*Gate" references/curriculum.md | wc -l`
Expected: 4 (Phase 0, 1, 2, Final)

Run: `grep "^| ★" references/curriculum.md | wc -l`
Expected: At least 10 (interview extras)

- [ ] **Step 7: Commit**

```bash
git add references/curriculum.md
git commit -m "feat: add curriculum.md — NeetCode 150 E+M with 4 Phases and interview extras"
```

---

## Chunk 3: SKILL.md — Core Skill File

### Task 5: Create SKILL.md

**Files:**
- Create: `SKILL.md`

This is the main skill file. It contains ALL teaching mechanics. Structure:

```
---
(frontmatter)
---

# LeetCode Coach
> tagline

## Architecture Overview (ASCII diagram)
## Table of Contents
## Quick Start (router + warm-up)
## Language Configuration
## Core Teaching Methods (Feynman + Simon)
## Feynman Gate (2-stage + failure escalation)
## Phase Gates (4 gates + failure protocol)
## Teaching Flow A→I (9 steps, full detail)
## Tiered Scorecard (3 tiers)
## Weekly Review (trigger + flow)
## Progress Report (trigger + format)
## Curriculum & References (on-demand loading)
## Key Principles
```

- [ ] **Step 1: Write frontmatter + Architecture Overview + TOC**

Frontmatter from spec lines 596-599.
Architecture diagram from spec lines 36-72.
TOC linking to all sections.

- [ ] **Step 2: Write Quick Start + Language Configuration**

Quick Start from spec lines 472-493 (router + warm-up with concrete pacing outcomes).
Language Configuration from spec lines 413-426.

- [ ] **Step 3: Write Core Teaching Methods**

Feynman Method section (explain like I'm five, never ask "do you understand?", guide to find errors).
Simon Method section (5-10 chunks per pattern, each must pass Feynman Gate, concentrated effort).

Adapt from SD Coach SKILL.md lines 125-137. Change "topic" to "pattern", remove SD-specific examples, add LeetCode examples.

- [ ] **Step 4: Write Feynman Gate section**

From spec lines 125-140. Include:
- Two-stage verification (Recall + Transfer)
- Transfer types: variation problem + constraint change (with examples)
- Failure Escalation (3 levels): reteach → check prereqs → split chunks
- "Never loop infinitely" safety clause

- [ ] **Step 5: Write Phase Gates section**

From spec lines 183-232. Include:
- 4 Phase Gate table (trigger, format, pass threshold)
- Phase 0 does NOT require complexity analysis
- Gate Failure Protocol (3 attempts)
- On Gate Pass actions (update progress, show report, celebrate, preview)

- [ ] **Step 6: Write Teaching Flow A→I (all 9 steps)**

The largest section. From spec lines 77-179. Each step fully specified:

- Step A: Review (check Mistake Registry, Pattern recall, Weekly Review trigger)
- Step B: Read Problem (display, identify edge cases, pattern guess)
- Step C: Pattern Teaching (analogy, Python template from cheatsheet, lightweight Feynman checks — NOT the formal Gate)
- Step D: Brute Force — NEW (5 min solo, hint escalation, human-language-first, complexity analysis mandatory)
- Step E: Optimal Solution — NEW (find bottleneck, optimize, complexity analysis, skip if brute IS optimal)
- Step F: Feynman Gate (formal 2-stage: Recall + Transfer with both variation and constraint change)
- Step G: Mock Interview (Claude-generated variation problem, timed, Scorecard, Interviewer Follow-Up Preview)
- Step H: Notes (use notes-template.md, required sections, cross-verification)
- Step I: Progress Update (update all progress.md sections, breakpoint handling)

- [ ] **Step 7: Write Tiered Scorecard section**

From spec lines 275-325. Three tiers:
- Phase 0: /3 (Think Aloud, Pattern ID, Code runs)
- Phase 1: /5 (+ Complexity, Edge cases)
- Phase 2-3: /7 (+ Optimal, WHY not other Pattern)
- Pass threshold: ≥ 60%
- After every scorecard: Top improvement + Best moment

- [ ] **Step 8: Write Weekly Review section**

From spec lines 394-409. Include trigger mechanism + 6-step flow.

- [ ] **Step 9: Write Progress Report section**

From spec lines 430-468. Include trigger conditions + format template with heatmap.

- [ ] **Step 10: Write Curriculum & References + Key Principles**

On-demand loading table (which file, when to read).
Key Principles adapted from SD Coach:
1. Understanding over memorization
2. No skipping patterns — mastery before moving on
3. Brute first, then optimize — understand WHY
4. Interview muscle memory — daily mock practice
5. Honest mistake tracking
6. Everything serves the interview

- [ ] **Step 11: Verify SKILL.md**

Run: `grep "^## " SKILL.md | wc -l`
Expected: 12-14 sections

Run: `grep "Feynman Gate" SKILL.md | wc -l`
Expected: 5+ references

Run: `grep "Phase Gate" SKILL.md | wc -l`
Expected: 5+ references

Run: `wc -l SKILL.md`
Expected: ~500-600 lines

- [ ] **Step 12: Commit**

```bash
git add SKILL.md
git commit -m "feat: add SKILL.md — core LeetCode Coach skill with 9-step teaching flow"
```

---

## Chunk 4: Evals + README + Cleanup

### Task 6: Create evals.json

**Files:**
- Create: `evals/evals.json`

- [ ] **Step 1: Create evals.json with 20 eval cases**

From spec lines 564-590. Write all 20 cases with:
- `id` (1-20)
- `category` (quick-start, feynman-gate, teaching-flow, phase-gate, progress, adversarial)
- `prompt` (realistic student input)
- `expected_output` (specific behaviors the skill SHOULD and SHOULD NOT exhibit)

Key eval cases to get right:
- **Eval 3 (jump-to):** "Tomorrow I need to present Valid Anagram at our study group" → should follow normal A→I flow for that specific problem
- **Eval 9 (brute→optimal):** Student gives brute force → Coach should NOT give optimal directly, should ask "where's the bottleneck?"
- **Eval 12 (brute IS optimal):** Problem where brute force is already optimal → should skip Step E
- **Eval 17 (progress report):** Should generate formatted report with heatmap
- **Eval 20 (memorized answer):** Student recites solution but can't explain WHY → Coach should detect and re-teach pattern

- [ ] **Step 2: Verify eval count and JSON validity**

Run: `python3 -c "import json; data=json.load(open('evals/evals.json')); print(f'Eval count: {len(data[\"evals\"])}')"`
Expected: `Eval count: 20`

- [ ] **Step 3: Commit**

```bash
git add evals/evals.json
git commit -m "feat: add 20 eval cases covering all core paths + adversarial scenarios"
```

---

### Task 7: Create README.md + .gitignore

**Files:**
- Create: `README.md`
- Create: `.gitignore`

- [ ] **Step 1: Create .gitignore**

```
# Student files (created during sessions, not committed)
progress.md
notes/
```

- [ ] **Step 2: Create README.md**

Include:
- Title + description (LeetCode Coach for DevOps interview prep)
- What It Does (5 bullet points: NeetCode 150 E+M, pattern-based teaching, brute→optimal, mock interviews, progress tracking)
- Teaching Flow overview (A→I, ~55 min per problem)
- Curriculum overview (4 Phases table)
- Install instructions (same as SD Coach: npx, manual, temporary)
- Key Features (Feynman Method, Progressive Solving, Tiered Scorecard, Pattern Cheatsheet)
- Language Support (English + Bilingual)
- Project Structure (file tree)

Keep it DRY — reference SKILL.md for detailed teaching flow, don't duplicate.

- [ ] **Step 3: Commit**

```bash
git add .gitignore README.md
git commit -m "docs: add README.md and .gitignore"
```

---

## Chunk 5: Final Verification

### Task 8: Verify all files and push

- [ ] **Step 1: Verify file count and structure**

Run: `find /home/ubuntu/leetcode-coach -not -path '*/.git/*' -type f | sort`
Expected files:
- `.gitignore`
- `README.md`
- `SKILL.md`
- `docs/plans/2026-03-16-leetcode-coach-implementation.md`
- `docs/specs/2026-03-16-leetcode-coach-design.md`
- `evals/evals.json`
- `references/curriculum.md`
- `references/notes-template.md`
- `references/pattern-cheatsheet.md`
- `references/progress-template.md`

- [ ] **Step 2: Verify no broken internal references**

Run: `grep -r "references/" SKILL.md`
Expected: All references point to files that exist

Run: `grep -r "progress.md" SKILL.md`
Expected: Multiple references (to the student's file, not the template)

- [ ] **Step 3: Verify pattern count consistency**

Run: `grep -c "^### " references/pattern-cheatsheet.md`
Expected: 18

Run: `grep -c "^### " references/curriculum.md`
Expected: 18

These must match — every pattern in the cheatsheet has a curriculum section and vice versa.

- [ ] **Step 4: Verify eval JSON**

Run: `python3 -c "import json; json.load(open('evals/evals.json')); print('Valid JSON')"`
Expected: "Valid JSON"

- [ ] **Step 5: Verify SKILL.md line count**

Run: `wc -l SKILL.md references/*.md`
Expected: SKILL.md ~500-600, curriculum.md ~300+, pattern-cheatsheet.md ~200+, progress-template.md ~80+, notes-template.md ~40+

- [ ] **Step 6: Push to remote**

```bash
git push -u origin main
```

---

## Execution Summary

| Task | Files | Description | Est. Effort |
|------|-------|-------------|-------------|
| 1 | CREATE progress-template.md | Progress tracking format | S |
| 2 | CREATE notes-template.md | Per-problem notes format | S |
| 3 | CREATE pattern-cheatsheet.md | 18 patterns with Python templates | M |
| 4 | CREATE curriculum.md | NeetCode 150 E+M, 4 Phases, extras | L |
| 5 | CREATE SKILL.md | Core skill, 9-step flow, gates, scorecards | L |
| 6 | CREATE evals.json | 20 eval test cases | M |
| 7 | CREATE README.md + .gitignore | Docs + ignore patterns | S |
| 8 | Verification + push | Cross-file consistency checks | S |

**Total: 8 tasks, 9 files created, 5 chunks.**
