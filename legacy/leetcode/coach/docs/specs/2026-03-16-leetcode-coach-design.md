# LeetCode Coach — Design Spec

> ⚠️ **Historical (v1, 2026-03-16).** This spec describes the original teaching-pipeline design
> (9-step A→I flow, phase gates, 7-table progress). The skill was redesigned in June 2026 into a
> retrieval-first "interview gym" (Drill / Learn / Cold Solve / Mock modes, 3-block progress) — see
> the current `SKILL.md` for the live design. Kept here as a record of the original rationale.

> A Claude Code skill for structured LeetCode interview preparation, using Feynman + Simon learning methods.
> Based on the SD Coach framework with LeetCode-specific adaptations.

**Target user:** DevOps engineer preparing for coding interview rounds.
**Problem set:** NeetCode 150 (Easy + Medium only) + high-frequency interview extras.
**Language:** Python.
**Pace:** 1 problem/day, with support for study group topic insertion.

---

## Decision Registry

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Fork SD Coach framework (Approach A) | Fastest path; proven teaching mechanics; YAGNI over shared framework extraction |
| D2 | NeetCode 150 Easy + Medium only | DevOps interviews rarely test Hard; Hard skipped but supported via jump-to mode |
| D3 | Add interview-common problems beyond NeetCode 150 | Real interviews draw from broader pool; ★ marks extra problems |
| D4 | Python as default language | User's background + interview speed advantage over Go |
| D5 | 4 Phases (not 18 categories) | Cleaner Phase Gates; categories are teaching units within Phases |
| D6 | 9-step Teaching Flow (A→I) | SD Coach's 8 steps + new Step E (optimal solution) |
| D7 | Brute → Optimal progressive solving | Core coding interview skill not needed in SD interviews |
| D8 | Complexity analysis as first-class citizen | Every solution requires Time + Space Big-O; integral to Steps D and E |
| D9 | Try-first-then-guide solving mode | Student attempts 5 min solo before Coach hints; most interview-realistic |
| D10 | Phase Gate = unseen problem, timed | Closest to real interview conditions |
| D11 | Feynman Transfer = variation + constraint change | Both types tested per problem |
| D12 | Study group jump-to mode | Not a separate mode; just router path to any specific problem |
| D13 | Problem Log in progress tracking | Per-problem record of approach, complexity, notes; SD Coach doesn't need this |
| D14 | Bilingual mode (English + Traditional Chinese) | User is non-native English speaker; bilingual for Feynman explanations, English Polish for interview prep |

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    LEETCODE COACH SKILL                       │
│                                                              │
│  Session Start                                               │
│    │                                                         │
│    ▼                                                         │
│  Read progress.md ──→ Breakpoint? ──Y──→ Resume              │
│    │                        │                                │
│    │ N                      │                                │
│    ▼                        │                                │
│  Quick Start Router         │                                │
│    ├── New student ──→ Warm-Up ──→ Phase 0 Problem 1         │
│    ├── Returning ──→ Next problem / Weekly Review             │
│    ├── Jump-to ──→ "Study group: need to learn XX" ──→ Teach │
│    └── Mock only ──→ Mock Interview mode                     │
│                                                              │
│  Teaching Flow (A → I) — per problem                         │
│    A. Review (Mistake Registry + yesterday's Pattern recall) │
│    B. Read Problem (understand + edge cases)                 │
│    C. Pattern Teaching (analogy + core template)             │
│    D. Brute Force (try solo → hint if stuck → code → O(?))  │
│    E. Optimal Solution (find bottleneck → optimize → O(?))   │
│    F. Feynman Gate (Recall + Transfer: variation + constraint)│
│    G. Mock Interview (timed + think aloud + Scorecard)       │
│    H. Notes (Pattern summary + mistakes + interview phrasing)│
│    I. Progress Update (mastery + Problem Log + breakpoint)   │
│                                                              │
│  Gates                                                       │
│    ├── Feynman Gate: per problem (Recall → Transfer)         │
│    │   └── Failure: re-explain → check prereqs → split       │
│    └── Phase Gate: per Phase                                 │
│        └── Unseen problem, timed, Scorecard threshold        │
│                                                              │
│  Weekly Review (every 7 sessions)                            │
│  Progress Report (heatmap + Pattern mastery + trends)        │
└──────────────────────────────────────────────────────────────┘
```

---

## Teaching Flow (A → I)

### A. Review (3 min)

- Skip for the very first session
- Read `progress.md` → check **Mistake Registry** for ❌ Unresolved items
- "What Pattern did we cover yesterday? Summarize in one sentence."
- If unresolved mistakes → "Last time you struggled with [X]. Can you explain it now?"
- If `session_count - last_weekly_review >= 7` → run Weekly Review instead

### B. Read Problem (3 min)

- Display the problem: number, title, description, examples, constraints
- Guide student to identify: input/output types, constraints, edge cases
- "Before looking at any solution, what Pattern does this remind you of?"
- If student identifies correctly → acknowledge and move to C
- If wrong → don't correct yet, let them discover during Steps D-E

### C. Pattern Teaching (5 min)

- Explain the Pattern behind this problem using an analogy
  - Example: "Sliding Window is like a train window sliding across scenery — you only see what's inside the frame"
- Show the Pattern's **Python template** (pseudocode with blanks)
- Chunk Map: list 3-5 key concepts for this Pattern
- For each chunk → **lightweight Feynman check** (Recall only, no formal pass/fail): "Can you explain this in your own words?"
- Note: This is NOT the formal Feynman Gate. Step F is the formal gate with both Recall + Transfer + failure escalation.

### D. Brute Force (10 min) — NEW

- **Student tries solo for 5 minutes.** Coach does NOT intervene.
- If stuck → Coach gives ONE hint (not the answer)
  - Hint escalation: conceptual hint → example walkthrough → partial pseudocode
- Student describes approach in plain language FIRST → then translates to code
- Run through example cases to verify
- **Complexity analysis** (mandatory):
  - "What's the time complexity? Walk me through why."
  - "What's the space complexity?"
  - If wrong → guide to correct answer, don't just state it

### E. Optimal Solution (10 min) — NEW

- "Where's the bottleneck in your brute force? Which step is slowest?"
- Guide student to discover the optimization direction
- Student writes optimal solution code
- **Complexity analysis** (mandatory): Time O(?) + Space O(?)
- "Why does this Pattern reduce the complexity? What's the key insight?"
- If the brute force IS already optimal → skip this step, acknowledge it

### F. Feynman Gate (5 min)

**Stage 1 — Recall:** "Explain in your own words: what Pattern did this problem use and why?"
- Pass criteria: Captures the core idea, not just restating the solution

**Stage 2 — Transfer (BOTH types):**
1. **Variation:** "What if the problem changed to [variation]?"
   - Example: Valid Anagram → "What if you need to find ALL anagram starting indices in a string?"
2. **Constraint change:** "What if [constraint changes]?"
   - Example: "What if input is Unicode instead of lowercase English letters?"
- Pass criteria: Student can adapt their approach to the new scenario

**Failure Escalation (3 levels):** Same as SD Coach:
- Attempt 1-2: Reteach with different angle
- Attempt 3: Check prerequisites
- Attempt 4: Split into sub-concepts, mark 🔴

### G. Mock Interview (10 min)

- Coach gives a **related unseen problem**, timed
  - Source: Claude generates a variation of the current problem (similar pattern, different constraints/data types). NOT drawn from curriculum to avoid spoiling future problems.
- Student must think aloud + write code
- Feedback using **Tiered Scorecard** (see below)
- **Interviewer Follow-Up Preview:**
  ```
  In a real interview, they might ask:
    - "[specific follow-up about edge case]"
    - "[what if we change the constraint to X]"
  Think about these — I'll ask you next session.
  ```

### H. Notes (5 min)

- Write notes using Notes Template (read `references/notes-template.md`)
- Save to `notes/patternXX-problem-name.md`
- **Required sections:**
  - Pattern one-liner → sync to One-Liner Library
  - 🔴 Mistakes & Misconceptions (mandatory, challenge if student says "none")
  - 🎤 Interview Phrasing ("I'd approach this by...")
  - Complexity quick-ref: Brute O(?) → Optimal O(?)
- **Cross-Verification:** "After the session, look up this problem on NeetCode or LeetCode discussions. If you find a different approach, bring it up next session."

### I. Progress Update (2 min)

- Update `progress.md`:
  1. Update Topic Mastery (per Pattern) based on Gate + Drill performance
  2. Add entry to Problem Log (problem, approach, complexity, notes)
  3. Add scorecard result to Scorecard History
  4. Sync 🔴 mistakes to Mistake Registry
  5. Add one-liner to Pattern One-Liner Library
  6. Increment session count
  7. Clear Breakpoint section (session completed)
  8. Check if `session_count - last_weekly_review >= 7` → flag next session
- Preview tomorrow's problem
- If student leaves mid-session → write Breakpoint with current position

---

## Curriculum Structure

### Phase 0: Foundation Patterns

**Categories:** Arrays & Hashing, Two Pointers, Sliding Window, Stack
**Problem count:** TBD — exact count determined when building curriculum.md by filtering NeetCode 150 Easy+Medium per category + interview extras. Category numbers in parentheses below are total NeetCode 150 counts (including Hard).

Phase Gate 0 → 1: One unseen Easy problem, 15 min, must produce working code. (Phase 0 does not require complexity analysis — that starts in Phase 1.)

### Phase 1: Core Data Structures

**Categories:** Binary Search, Linked List, Trees, Heap/Priority Queue
**Problem count:** TBD (Easy + Medium from NeetCode 150 + interview extras)

Phase Gate 1 → 2: One unseen Medium problem, 25 min, Scorecard ≥ 3/5.

### Phase 2: Advanced Algorithms

**Categories:** Backtracking, Tries, Graphs, Advanced Graphs
**Problem count:** TBD (Easy + Medium from NeetCode 150 + interview extras)

Phase Gate 2 → 3: One unseen Medium problem, 25 min, Scorecard ≥ 3/5.

### Phase 3: Optimization Techniques

**Categories:** 1-D DP, 2-D DP, Greedy, Intervals, Math & Geometry, Bit Manipulation
**Problem count:** TBD (Easy + Medium from NeetCode 150 + interview extras)

Final Gate: Mock interview — 2 Medium problems, 45 min, both Scorecard ≥ 5/7.

### Phase Gate Failure Protocol

```
Attempt 1: Fail
  → Identify 2-3 weakest Patterns from the attempt
  → Run targeted drill on each (Feynman Gate + practice problem)
  → Retry gate with a DIFFERENT unseen problem

Attempt 2: Fail
  → Run a full Weekly Review covering all Patterns in the Phase
  → Focus extra time on previously weak areas
  → Retry gate with a DIFFERENT unseen problem

Attempt 3: Fail
  → Show Progress Report to identify systemic weakness
  → Offer: "We can continue to the next Phase with a 🟡 flag on these
     Patterns, and I'll revisit them during Weekly Reviews. Or we can
     spend more time here. What do you prefer?"
  → Student decides — record choice in progress.md Phase Gate Results
```

### Prerequisites (per category)

```
Arrays & Hashing → (entry point)
Two Pointers → Arrays & Hashing
Sliding Window → Arrays & Hashing, Two Pointers
Stack → Arrays & Hashing
Binary Search → Arrays & Hashing
Linked List → (entry point)
Trees → Linked List (recursion concepts)
Heap → Arrays & Hashing, Trees
Backtracking → Trees (recursion)
Tries → Trees, Arrays & Hashing
Graphs → Trees, Heap
Advanced Graphs → Graphs
1-D DP → Arrays & Hashing, Binary Search
2-D DP → 1-D DP
Greedy → Arrays & Hashing, Sliding Window
Intervals → Arrays & Hashing, Greedy
Math & Geometry → Arrays & Hashing
Bit Manipulation → (entry point)
```

### curriculum.md Format (per category)

```markdown
### Sliding Window

**Core concept:** Maintain a dynamic window sliding across an array/string
**Prerequisites:** Arrays & Hashing, Two Pointers
**Template:** Fixed-size window / Dynamic-size window

| # | Problem | Difficulty | Source | Focus |
|---|---------|-----------|--------|-------|
| 1 | Best Time to Buy and Sell Stock | Easy | NeetCode 150 | Single pass |
| 2 | Longest Substring Without Repeating | Medium | NeetCode 150 | HashMap + window |
| ★ | Maximum Average Subarray I | Easy | Interview Freq | Fixed window intro |
```

---

## Tiered Scorecard

### Phase 0 Scorecard (/3)

```
📊 Interview Drill Scorecard (Phase 0)
┌───────────────────────────────┬───────┐
│ Think Aloud                   │ ✅/❌ │
│ Identified correct Pattern    │ ✅/❌ │
│ Code runs (passes examples)   │ ✅/❌ │
└───────────────────────────────┴───────┘
Score: X/3
```

### Phase 1 Scorecard (/5)

```
📊 Interview Drill Scorecard (Phase 1)
┌───────────────────────────────┬───────┐
│ Think Aloud                   │ ✅/❌ │
│ Identified correct Pattern    │ ✅/❌ │
│ Code runs (passes examples)   │ ✅/❌ │
│ Correct complexity analysis   │ ✅/❌ │
│ Edge cases handled            │ ✅/❌ │
└───────────────────────────────┴───────┘
Score: X/5
```

### Phase 2-3 Scorecard (/7)

```
📊 Interview Drill Scorecard (Phase 2-3)
┌───────────────────────────────┬───────┐
│ Think Aloud                   │ ✅/❌ │
│ Identified correct Pattern    │ ✅/❌ │
│ Code runs (passes examples)   │ ✅/❌ │
│ Correct complexity analysis   │ ✅/❌ │
│ Edge cases handled            │ ✅/❌ │
│ Wrote optimal (not just brute)│ ✅/❌ │
│ Explained WHY not other Pattern│ ✅/❌ │
└───────────────────────────────┴───────┘
Score: X/7
```

After every scorecard:
```
💡 Top improvement: [one specific, actionable suggestion]
🌟 Best moment: [one thing they did well]
```

Pass threshold: ≥ 60% (2/3, 3/5, 5/7).

---

## Progress Tracking (progress-template.md)

### Student Info

| Field | Value |
|-------|-------|
| Start date | YYYY-MM-DD |
| Current phase | Phase 0 / 1 / 2 / 3 |
| Current pattern | e.g., Sliding Window |
| Language | Python |
| Session count | N |
| Last weekly review | Session #N (YYYY-MM-DD) |
| Problems solved | X / TBD |

### Current Session (Breakpoint)

| Field | Value |
|-------|-------|
| Pattern | e.g., Sliding Window |
| Problem | e.g., Longest Substring Without Repeating |
| Step | A / B / C / D / E / F / G / H / I |
| Next action | e.g., Student stuck on brute force, give hint next |

### Topic Mastery (per Pattern)

| Pattern | Problems Done | Mastery | Phase Gate | Notes |
|---------|--------------|---------|------------|-------|
| Arrays & Hashing | 3/9 | 🟡 | — | HashMap solid, sorting weak |
| Two Pointers | 0/5 | ⬜ | — | |

> Mastery levels: ⬜ Not started │ 🔴 Needs work │ 🟡 Developing │ 🟢 Solid

### Problem Log

| Session | Problem | Difficulty | Pattern | Solved? | Brute | Optimal | Notes |
|---------|---------|-----------|---------|---------|-------|---------|-------|
| 1 | Contains Duplicate | Easy | Arrays | ✅ | O(n²) | O(n)/O(n) | HashSet |
| 2 | Valid Anagram | Easy | Arrays | ✅ | O(n log n) | O(n)/O(1) | Counter, forgot edge case |

### Scorecard History

| Session | Problem | Pattern | Score | Details |
|---------|---------|---------|-------|---------|
| | | | /3 or /5 or /7 | |

### 🔴 Mistake Registry

| Session | Problem | Pattern | Mistake | Status |
|---------|---------|---------|---------|--------|
| | | | | ❌ Unresolved / ✅ Resolved |

### 🎯 Pattern One-Liner Library

| Pattern | One-Liner |
|---------|-----------|
| Sliding Window | Maintain a dynamic window over sequence, tracking state inside the frame |

### Phase Gate Results

| Phase | Date | Problem Used | Score | Result | Weak spots |
|-------|------|-------------|-------|--------|------------|
| | | | | ✅ Pass / ❌ Retry | |

---

## Weekly Review

### Trigger

Auto-triggered when Step A detects `session_count - last_weekly_review >= 7`.
Also triggered manually: "weekly review", "let's review", "recall drill".
Replaces normal session when triggered.

### Flow

1. **Pick 3 Patterns**: 1 from this week + 2 from past weeks (prioritize 🔴 and 🟡)
2. **Blind Recall**: Student explains each Pattern's key idea + template without notes
3. **Problem Recall**: Pick one solved problem from each Pattern → student walks through approach
4. **Mistake Registry Review**: Test all ❌ Unresolved. Resolved → ✅. Still stuck → re-drill.
5. **Quick Drill**: Re-drill the weakest Pattern
6. **Update progress.md**: Set last_weekly_review, update mastery levels

---

## Language Configuration

Ask the student their language preference at first session start.

| Mode | Behavior |
|------|----------|
| **English** (default) | All teaching in English. Technical terms in English. |
| **Bilingual** | English for technical content, student's native language for Feynman-style plain explanations. Student can respond in either language. |

If bilingual mode is active:
- After each student response, provide a brief **English Polish**: a natural, interview-ready version of what they said
- Format: `💬 English Polish: "[polished version]"`
- Don't explain grammar — just show the improved version
- Especially valuable for non-native speakers preparing for English-language interviews

---

## Progress Report

### Trigger

- Student asks: "my progress", "how am I doing", "progress report"
- Automatically shown when passing a Phase Gate
- Shown during Weekly Review (abbreviated version)

### Format

Generate from `progress.md` data:

```
📊 LeetCode Interview Prep Report
═══════════════════════════════════════════

Progress: Problem X/TBD (Phase N)  ████████░░░░░░░░░░░░ XX%

Pattern Mastery Heatmap:
  Phase 0 Foundation:
  Arrays & Hashing    ████████████████████ 🟢 (7/9)
  Two Pointers        ████████████████░░░░ 🟡 (3/5)
  Sliding Window      ████████░░░░░░░░░░░░ 🔴 (1/6)
  Stack               ░░░░░░░░░░░░░░░░░░░░ ⬜ (0/6)

Interview Drill Trend:
  Phase 0 avg: X.X/3 → X.X/3 📈/📉

Complexity Accuracy:
  Last 10 problems: X/10 correct on first try

Top Unresolved Mistakes:
  1. [mistake from Mistake Registry]
  2. [mistake from Mistake Registry]

💪 Strength: [strongest Pattern]
🎯 Focus area: [weakest Pattern]
📋 Patterns summarized: X/18
```

---

## Quick Start Router

When this skill activates:

**First, read `progress.md`** (if it exists).

### Routing

1. **No progress file** → New student. Ask language preference (confirm Python), run warm-up (solve a simple problem to gauge level), start Phase 0.
2. **Progress file has Breakpoint** → Resume. "Last time we stopped at [Step X] of [Problem]. Let's pick up there."
3. **Progress file, no breakpoint** → Returning student. Check Weekly Review trigger. If not due → next problem.
4. **Student says "I need to prepare [specific problem]"** → Jump to that problem. Follow normal A→I flow. Mark as jump-to in Problem Log.
5. **Student asks for mock interview** → Mock Interview mode.

### New Student Warm-Up

> "Before we start, let me see where you are. Can you solve this: Given an array of integers, return true if any value appears at least twice. Take 3 minutes."

Based on response:
- **Strong** (optimal approach, explains complexity) → skip first Easy problem per category in Phase 0, go straight to Mediums
- **Medium** (brute force, some structure) → follow Phase 0 curriculum as written
- **Struggles** (doesn't know where to start) → reassure, add extra Easy problems from interview extras pool before Mediums

---

## Notes Template (notes-template.md)

```markdown
# Day XX — [Problem Name] ([Pattern])

## Pattern One-Liner
> [One sentence summary of the Pattern]

## Approach
- **Brute Force:** [description] — Time O(?), Space O(?)
- **Optimal:** [description] — Time O(?), Space O(?)
- **Key Insight:** [why optimal works]

## 🔴 My Mistakes & Misconceptions
| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| | | |

## 🎤 How to Say It in Interview
**Opening:** "I'd approach this with [Pattern] because..."
**Optimization:** "The brute force is O(?), but we can do O(?) by..."
**Edge cases:** "I'd handle [edge case] by..."

## Sync to Progress File
1. Add 🔴 Mistakes to Mistake Registry
2. Add Pattern one-liner to One-Liner Library
3. Update Topic Mastery
4. Add to Problem Log
```

---

## Pattern Cheatsheet (pattern-cheatsheet.md)

Quick reference for all 18 Patterns with Python templates. Example:

```markdown
### Sliding Window

**When to use:** Subarray/substring problems with contiguous elements
**Key signal:** "maximum/minimum subarray", "longest substring", "window of size k"

**Fixed-size template:**
def fixed_window(arr, k):
    window_sum = sum(arr[:k])
    best = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        best = max(best, window_sum)
    return best

**Dynamic-size template:**
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

## Eval Scenarios (evals.json)

20 eval cases covering all core paths:

| ID | Category | Scenario |
|----|----------|----------|
| 1 | quick-start | New student begins |
| 2 | quick-start | Returning student continues |
| 3 | quick-start | Jump-to: "Tomorrow I present Valid Anagram" |
| 4 | quick-start | Request mock interview |
| 5 | feynman-gate | Recall passes → must do Transfer |
| 6 | feynman-gate | Recall fails → escalation level 2 (check prereqs) |
| 7 | feynman-gate | Transfer with variation problem |
| 8 | feynman-gate | Transfer with constraint change |
| 9 | teaching-flow | Brute force → guide to optimal (don't give answer) |
| 10 | teaching-flow | Complexity analysis wrong → guide to correct |
| 11 | teaching-flow | Student stuck → give hint not answer |
| 12 | teaching-flow | Brute IS optimal → skip Step E |
| 13 | phase-gate | Phase Gate triggers with unseen problem |
| 14 | phase-gate | Phase Gate fails → failure protocol |
| 15 | progress | Weekly Review triggers (7 sessions) |
| 16 | progress | Breakpoint save + resume |
| 17 | progress | Progress Report generation |
| 18 | adversarial | Student asks for direct answer → refuse, guide |
| 19 | adversarial | Student asks SD question → redirect to SD Coach |
| 20 | adversarial | Student memorized answer but can't explain → detect, reteach |

---

## SKILL.md Frontmatter

```yaml
---
name: leetcode-coach
description: LeetCode interview coaching skill using Feynman + Simon learning methods. Guides students through NeetCode 150 (Easy + Medium) with pattern-based teaching, progressive brute-to-optimal solving, and mock interviews. Use PROACTIVELY when the user mentions LeetCode, coding interview prep, algorithm practice, NeetCode, data structures and algorithms, or wants to practice any coding pattern (sliding window, two pointers, dynamic programming, etc.). Also trigger when the user asks to review algorithms, solve coding problems, or prepare for technical coding interviews.
---
```

---

## Step Mapping (SD Coach → LeetCode Coach)

For maintainers working on both skills:

```
SD Coach              LeetCode Coach         Notes
────────              ──────────────         ─────
Step A (Review)    →  Step A (Review)        Same
Step B (Intro)     →  Step B (Read Problem)  Adapted: concept intro → problem reading
Step C (Teaching)  →  Step C (Pattern)       Adapted: topic chunks → pattern template
Step D (PoC)       →  Step D (Brute Force)   NEW content: hands-on PoC → brute force solving
—                  →  Step E (Optimal)       NEW: no SD Coach equivalent
Step E (Simon)     →  (merged into Step F)   Simon drill merged into Feynman Gate
Step F (Interview) →  Step G (Mock)          Same concept, shifted letter
Step G (Notes)     →  Step H (Notes)         Same concept, shifted letter
Step H (Progress)  →  Step I (Progress)      Same concept, shifted letter
```

---

## File Structure

```
leetcode-coach/
├── SKILL.md                      # Core — teaching methods, gates, flow
├── references/
│   ├── curriculum.md             # NeetCode 150 (E+M) + interview extras
│   ├── progress-template.md      # Student progress tracking format
│   ├── notes-template.md         # Per-problem notes format
│   └── pattern-cheatsheet.md     # Pattern one-liners + Python templates
├── evals/
│   └── evals.json                # 20 test cases
└── docs/
    └── specs/
        └── 2026-03-16-leetcode-coach-design.md  # THIS FILE
```

---

## What's NOT in Scope

| Item | Rationale |
|------|-----------|
| Hard problems | DevOps interviews don't test Hard; supported via jump-to only |
| Go language support | User chose Python for interviews; Go coach is a separate project |
| Automated LeetCode submission | Skill runs in Claude Code, not a browser extension |
| Framework extraction | YAGNI — extract when building third skill, not now |
| Spaced repetition algorithm | Weekly Review is sufficient; SRS adds complexity without proven benefit |
| Multi-user support | Single student tracking only |

## What Already Exists (Reused from SD Coach)

| Component | Reuse Level |
|-----------|------------|
| Session Router | Direct copy, change routing options |
| Feynman Gate (Recall + Failure Escalation) | Direct copy |
| Feynman Gate Transfer | Modified: variation + constraint change (was: compare/scenario/apply/counter) |
| Phase Gate structure | Direct copy, change exam format |
| Progress Tracking (Breakpoint, Mastery, Session Count) | Direct copy + add Problem Log |
| Mistake Registry | Direct copy |
| One-Liner Library → Pattern One-Liner Library | Rename + adapt |
| Weekly Review trigger + flow | Direct copy |
| Progress Report | Direct copy, add Pattern-level heatmap |
| Tiered Scorecard structure | Direct copy, change criteria |
| Notes Template structure | Direct copy + add complexity section |
| Teaching Flow (A→H) | Modified: 8→9 steps, add Steps D(brute) and E(optimal) |
| PoC Tiers → removed | Not applicable to LeetCode |
| Observability Mini → removed | SD-specific, not needed |
| 4-Step SD Framework → removed | Replaced by brute→optimal flow |

## New Patterns (Not in SD Coach)

| Pattern | Purpose |
|---------|---------|
| Brute → Optimal progressive solving | Core coding interview skill: find bottleneck, optimize, justify |
| Complexity analysis as first-class citizen | Every solution step requires Time + Space Big-O analysis |
| Problem Log | Per-problem tracking of approach, complexity, notes |
| Pattern Cheatsheet | Python templates for each of 18 patterns |
| Try-first-then-guide | 5 min solo attempt before Coach intervenes |
