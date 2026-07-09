# SD Coach Mega Improvement — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform SD Coach from a structured prompt into a persistent, interview-focused AI coaching system with progress tracking, adaptive teaching gates, and interview preparation tools.

**Architecture:** All changes are Markdown content in a Claude Code skill. The core change is adding a progress persistence layer (`progress-template.md`) that enables cross-session continuity, then upgrading teaching mechanics (Feynman Gate, Phase Gate, Scorecard) and adding interview-focused outputs. SKILL.md is the single source of truth; other files are referenced on-demand.

**Tech Stack:** Markdown, Claude Code skill framework, JSON (evals)

---

## File Structure

```
system-design-coach/
├── SKILL.md                          # MODIFY: Major rewrite — TOC, gates, scorecard, breakpoints, reports
├── references/
│   ├── curriculum.md                 # MODIFY: Prerequisites, multi-day breakdown, misconceptions, DRY cleanup
│   ├── notes-template.md            # MODIFY: Add interview template sections
│   ├── progress-template.md         # CREATE: Progress tracking format
│   ├── 8-block-skeleton.md          # NO CHANGE
│   └── estimation-cheatsheet.md     # NO CHANGE
├── evals/
│   └── evals.json                   # MODIFY: Expand from 3 → 18 cases
├── README.md                        # MODIFY: DRY cleanup
└── docs/
    └── plans/
        └── 2026-03-15-sd-coach-mega-improvement.md  # THIS FILE
```

## Decision Registry (from CEO Review)

All 25 decisions that drive this plan:

| #   | Decision                              | Issue |
|-----|---------------------------------------|-------|
| 1A  | Progress template                     | Foundation |
| 2A  | Course Prerequisites per topic        | Adaptive |
| 3A  | Feynman Gate 3-level failure escalation | Teaching |
| 4A  | Phase Gate graduation criteria        | Teaching |
| 5A  | Mistake Registry in progress file     | Tracking |
| 6A  | PoC 3 tiers (Go main, light, discuss) | Teaching |
| 7A  | Session counter + auto Weekly Review  | Tracking |
| 8A  | Tiered Scorecard by Phase             | Teaching |
| 9A  | Feynman Gate 2-stage (Recall+Transfer)| Teaching |
| 10AB| Common misconceptions + cross-verify  | Quality |
| 11A | Session breakpoint in progress file   | Continuity |
| 12A | Multi-day topic day-by-day breakdown  | Content |
| 13A | SKILL.md single source of truth       | DRY |
| 14A | Eval expansion to 12-15 cases         | Quality |
| 15A | Adversarial eval cases                | Quality |
| 16A | References on-demand loading          | Performance |
| 17A | Progress Report with heatmap          | Experience |
| 19A | SKILL.md architecture overview + TOC  | Navigation |
| 20  | Phase Gate repeated failure mechanism | Teaching |
| D1  | One-liner challenge library           | Interview |
| D2  | Weakness heatmap in Progress Report   | Experience |
| D4  | Interviewer follow-up preview         | Interview |
| D5  | "How to say it in interview" template | Interview |
| 21  | Framework extraction markers          | Future |

---

## Chunk 1: Foundation — Progress Template + Notes Template

### Task 1: Create progress-template.md

**Files:**
- Create: `references/progress-template.md`

This is the foundation for all cross-session features. It must support:
- Day-level progress + mastery levels (1A)
- Session breakpoint for mid-session resume (11A)
- Mistake Registry (5A)
- Session counter + last weekly review (7A)
- One-liner library (D1)
- Scorecard history (8A)

- [ ] **Step 1: Create progress-template.md with full content**

```markdown
# Student Progress Tracking

> This file is the single source of truth for student progress.
> Updated by Claude at the end of every session (Step H) and when sessions are interrupted.
> Read by Claude at the start of every session to determine where to resume.

---

## Student Info

| Field | Value |
|-------|-------|
| **Start date** | YYYY-MM-DD |
| **Current phase** | Phase 0 / 1 / 2 / 3 / 4 |
| **Current day** | Day X |
| **Language mode** | English / Bilingual (language) |
| **Session count** | N |
| **Last weekly review** | Session #N (YYYY-MM-DD) |

---

## Current Session (Breakpoint)

> Updated when session is interrupted or paused. Cleared when session completes normally.

| Field | Value |
|-------|-------|
| **Day** | Day X |
| **Topic** | Topic name |
| **Step** | A / B / C / D / E / F / G / H |
| **Chunks completed** | [1, 2, 3] |
| **Chunks remaining** | [4, 5, 6, 7] |
| **Next action** | Description of what to do next |

> When this section has content, Claude should resume from here instead of starting a new session.

---

## Topic Mastery

<!-- FRAMEWORK: Reusable — mastery tracking pattern -->

| Day | Topic | Mastery | Phase Gate | Notes |
|-----|-------|---------|------------|-------|
| 1 | SD Interview Rubric | ⬜ | — | |
| 2 | Back-of-Envelope Estimation | ⬜ | — | |
| 3 | 4-Step Framework | ⬜ | Phase 0 Gate | |
| 4-5 | Load Balancer | ⬜ | — | |
| 6-7 | Caching & CDN | ⬜ | — | |
| 8-9 | Database Selection | ⬜ | — | |
| 10-11 | Message Queue | ⬜ | — | |
| 12-13 | API Design | ⬜ | — | |
| 14 | Security & Auth | ⬜ | — | |
| 15-16 | Consistent Hashing | ⬜ | Phase 1 Gate | |
| 17-18 | CAP Theorem | ⬜ | — | |
| 19-20 | Consistency Models | ⬜ | — | |
| 21-22 | Replication & Leader Election | ⬜ | — | |
| 23-24 | Rate Limiting & Circuit Breaker | ⬜ | — | |
| 25 | Observability | ⬜ | — | |
| 26 | Bloom Filter, Gossip, etc. | ⬜ | Phase 2 Gate | |
| 27-28 | URL Shortener | ⬜ | — | |
| 29-30 | Unique ID Generator | ⬜ | — | |
| 31-32 | Distributed Rate Limiter | ⬜ | — | |
| 33-34 | Notification System | ⬜ | — | |
| 35-37 | Chat System | ⬜ | — | |
| 38-39 | Distributed Cache | ⬜ | — | |
| 40-42 | News Feed | ⬜ | — | |
| 43-45 | Payment System | ⬜ | Phase 3 Gate | |
| 46-47 | Metrics & Logging | ⬜ | — | |
| 48-49 | Search Autocomplete | ⬜ | — | |
| 50-51 | Web Crawler | ⬜ | — | |
| 52-53 | Proximity Service | ⬜ | — | |
| 54-55 | Trade-off Deep Dive | ⬜ | — | |
| 56-57 | Mock Interview Round 1 | ⬜ | — | |
| 58-59 | Weak Spot Reinforcement | ⬜ | — | |
| 60-61 | Final Mock (Brutal) | ⬜ | Phase 4 Gate | |

> Mastery levels: ⬜ Not started │ 🔴 Needs work │ 🟡 Developing │ 🟢 Solid
> Update mastery after each session based on Feynman Gate + Drill performance.

---

## Interview Drill Scorecard History

<!-- FRAMEWORK: Reusable — scored assessment history pattern -->

| Session | Day | Topic | Score | Details |
|---------|-----|-------|-------|---------|
| | | | /3 or /5 or /7 | |

> Phase 0-1: /3 (Think Aloud, Scope Negotiation, Used Today's Block)
> Phase 2: /5 (+ Trade-off WHY, Operational Concerns)
> Phase 3+: /7 (+ Failure Modes, Capacity Estimation)

---

## 🔴 Mistake Registry

<!-- FRAMEWORK: Reusable — mistake tracking pattern -->

> Synced from each session's notes. This is the central record for weakness analysis.

| Session | Day | Topic | Mistake | Status |
|---------|-----|-------|---------|--------|
| | | | | ❌ Unresolved / ✅ Resolved |

> Review priority: All ❌ Unresolved items are the first target in Weekly Reviews and Step A.

---

## 🎯 One-Liner Library (Interview Quick-Answer Bank)

<!-- FRAMEWORK: Reusable — knowledge summary pattern -->

> One sentence per topic. Must be your own words, interview-ready.

| Topic | One-Liner |
|-------|-----------|
| | |

> Built incrementally: one new entry per session in Step G.
> Use this as a speed-review before mock interviews and real interviews.

---

## Phase Gate Results

| Phase | Date | Score | Result | Weak spots |
|-------|------|-------|--------|------------|
| | | | ✅ Pass / ❌ Retry | |

---
```

- [ ] **Step 2: Verify file created correctly**

Run: `cat references/progress-template.md | head -5`
Expected: Shows "# Student Progress Tracking"

- [ ] **Step 3: Commit**

```bash
git add references/progress-template.md
git commit -m "feat: add progress-template.md — foundation for cross-session tracking

Implements decisions 1A, 5A, 7A, 11A, D1, D2 from CEO review.
Includes: mastery tracking, session breakpoints, mistake registry,
scorecard history, one-liner library, phase gate results."
```

---

### Task 2: Update notes-template.md

**Files:**
- Modify: `references/notes-template.md`

Add two interview-focused sections: "How to say it in interview" (D5) and one-liner sync instruction.

- [ ] **Step 1: Add interview sections to notes-template.md**

After the "Required Every Session" section (the 🔴 Mistakes block), add:

```markdown
## 🎤 How to Say It in Interview

> Practice articulating today's topic as if you're in a real interview.

**Opening (30 sec):**
> "In one sentence, [topic] is... The key trade-off is... I'd approach this by..."

**When asked to go deeper:**
> Q: "[likely follow-up question]"
> A: "[structured answer with trade-off reasoning]"

**Showing production depth:**
> "In production, I'd monitor [specific metrics] and watch for [specific failure mode]..."

Rules:
- Write in YOUR words, not textbook definitions
- Must include at least one trade-off with reasoning
- Must include at least one operational/production concern
- This section feeds directly into interview muscle memory

## Sync to Progress File

After writing notes:
1. Add any new 🔴 Mistakes to the Mistake Registry in `progress.md`
2. Add this topic's one-liner to the One-Liner Library in `progress.md`
3. Update Topic Mastery level based on session performance
```

- [ ] **Step 2: Verify edit**

Run: `grep "How to Say It" references/notes-template.md`
Expected: Shows "## 🎤 How to Say It in Interview"

- [ ] **Step 3: Commit**

```bash
git add references/notes-template.md
git commit -m "feat: add interview articulation template + progress sync to notes

Implements D5 (interview template) from CEO review.
Each session now produces interview-ready talking points."
```

---

## Chunk 2: Curriculum Upgrade

### Task 3: Update curriculum.md — Prerequisites + Multi-day Breakdown + Misconceptions + DRY Cleanup

**Files:**
- Modify: `references/curriculum.md`

Four changes:
1. Add `Prerequisites` to each topic (2A)
2. Add day-by-day breakdown for multi-day topics (12A)
3. Add `⚠️ Common Misconception` blocks to high-risk topics (10A)
4. Remove Daily Routine Summary section (13A — DRY, it duplicates SKILL.md)

- [ ] **Step 1: Add Prerequisites to Phase 1 topics**

For each topic in Phase 1, add a Prerequisites line. Example for Day 4-5:

```markdown
### Day 4-5: Load Balancer & Reverse Proxy
**Prerequisites:** Day 3 (4-Step Framework)
```

Full prerequisites map:
- Day 1-3: None (entry point)
- Day 4-5 (LB): Day 3
- Day 6-7 (Caching): Day 3, Day 4-5
- Day 8-9 (Database): Day 3
- Day 10-11 (Queue): Day 3, Day 8-9
- Day 12-13 (API): Day 3, Day 4-5
- Day 14 (Auth): Day 12-13
- Day 15-16 (Consistent Hashing): Day 8-9
- Day 17-18 (CAP): Day 8-9, Day 15-16
- Day 19-20 (Consistency): Day 17-18
- Day 21-22 (Replication): Day 8-9, Day 19-20
- Day 23-24 (Rate Limiting): Day 6-7, Day 12-13
- Day 25 (Observability): Day 4-5, Day 6-7, Day 8-9
- Day 26 (Bloom/Gossip): Day 15-16, Day 19-20

Phase 3 topics: all require Phase 1 + Phase 2 completion (enforced by Phase Gate)

- [ ] **Step 2: Add multi-day breakdowns**

Replace flat multi-day entries with day-by-day breakdown. Example:

```markdown
### Day 4-5: Load Balancer & Reverse Proxy
**Prerequisites:** Day 3 (4-Step Framework)

**Day 4 — DNS + LB Fundamentals:**
- DNS fundamentals — resolution flow, TTL, record types
- DNS-based load balancing (weighted, latency-based, failover)
- L4 vs L7 load balancing — when to use which
- Algorithms: Round Robin, Least Connections, IP Hash, Weighted

**Day 5 — Production LB + PoC:**
- Health checks, sticky sessions, connection draining
- **DevOps**: ALB vs NLB, target group health checks
- **PoC**: Nginx L4/L7 LB with Docker Compose
```

Apply same pattern to all multi-day topics:
- Day 4-5 (LB): Day 4 = concepts, Day 5 = production + PoC
- Day 6-7 (Caching): Day 6 = cache patterns, Day 7 = CDN + PoC
- Day 8-9 (DB): Day 8 = SQL vs NoSQL concepts, Day 9 = indexing + PoC
- Day 10-11 (Queue): Day 10 = concepts + semantics, Day 11 = DLQ + PoC
- Day 12-13 (API): Day 12 = REST/gRPC/GraphQL, Day 13 = pagination + PoC
- Day 15-16 (Consistent Hashing): Day 15 = theory, Day 16 = PoC + Mini-Mock
- Day 17-18 (CAP): Day 17 = CAP + examples, Day 18 = PACELC + discussion
- Day 19-20 (Consistency): Day 19 = models, Day 20 = quorum + PoC
- Day 21-22 (Replication): Day 21 = patterns, Day 22 = Raft + service discovery
- Day 23-24 (Rate Limiting): Day 23 = algorithms, Day 24 = circuit breaker + PoC
- Day 27-28 (URL Shortener): Day 27 = design, Day 28 = PoC
- Day 29-30 (ID Generator): Day 29 = design, Day 30 = PoC
- Day 31-32 (Dist Rate Limiter): Day 31 = design, Day 32 = PoC
- Day 33-34 (Notification): Day 33 = design, Day 34 = PoC
- Day 35-37 (Chat): Day 35 = WebSocket + 1v1, Day 36 = group + presence + receipts, Day 37 = PoC + full diagram
- Day 38-39 (Dist Cache): Day 38 = design, Day 39 = PoC
- Day 40-42 (News Feed): Day 40 = fan-out design, Day 41 = ranking + celebrity, Day 42 = PoC + full diagram
- Day 43-45 (Payment): Day 43 = idempotency + SAGA, Day 44 = reconciliation + exactly-once, Day 45 = PoC + full diagram
- Day 46-47 through Day 52-53: Day N = design, Day N+1 = PoC
- Day 54-55: Day 54 = trade-off scenarios, Day 55 = trap & pivot drills
- Day 56-57: Day 56 = mock 1, Day 57 = feedback + re-do
- Day 58-59: Day 58 = review patterns, Day 59 = re-do designs
- Day 60-61: Day 60 = final mock 1, Day 61 = final mock 2

- [ ] **Step 3: Add Common Misconception blocks to high-risk topics**

Add `⚠️ Common Misconception` to these topics:

```markdown
### Day 17-18: CAP Theorem in Practice
**Prerequisites:** Day 8-9 (Database), Day 15-16 (Consistent Hashing)

⚠️ **Common Misconception:** CAP is NOT "pick 2 out of 3 in daily operation." It's about what happens DURING a network partition — you choose between consistency and availability. When there's no partition, you can have both. Teach PACELC as the practical mental model.
```

Topics that need misconception blocks:
1. **CAP Theorem (Day 17-18):** "Pick 2 out of 3" oversimplification
2. **Consistency Models (Day 19-20):** "Eventual consistency = inconsistent." No — it means consistent EVENTUALLY with a convergence guarantee.
3. **Message Queue delivery (Day 10-11):** "Kafka has exactly-once delivery." Kafka has idempotent producers + transactional consumers, which achieves effectively-once, not truly exactly-once in distributed systems.
4. **Consistent Hashing (Day 15-16):** "Consistent hashing eliminates all data movement." No — it minimizes movement to K/N keys on average, but rebalancing still happens.
5. **Caching (Day 6-7):** "More cache = always better." No — cache invalidation bugs can cause stale data, and large caches increase memory cost and cold-start time.
6. **Load Balancer (Day 4-5):** "L7 is always better than L4." No — L4 has lower latency and is better for non-HTTP protocols and raw throughput.
7. **Database Replication (Day 21-22):** "Read replicas give you strong consistency." No — replicas have replication lag. Read-after-write consistency requires reading from leader.
8. **Rate Limiting (Day 23-24):** "Token bucket and sliding window are interchangeable." No — token bucket allows bursts up to bucket size, sliding window is strictly rate-limited.

- [ ] **Step 4: Remove Daily Routine Summary section (DRY cleanup)**

Delete the "Daily Routine Summary" section at the bottom of curriculum.md (lines 211-223). This duplicates SKILL.md's Teaching Flow section.

Also trim the 4-step framework details from Day 3 to a brief reference:

Replace:
```markdown
- Step 1: Clarify requirements & scope (functional + non-functional)
- Step 2: High-level design (API + data model + architecture)
- Step 3: Deep dive into core components
- Step 4: Scale, trade-offs, monitoring
- Time budget for 45-min SD interview:
  - [0-5 min] Clarify requirements (DO NOT SKIP)
  - [5-10 min] Back-of-envelope estimation (if needed)
  - [10-20 min] High-level design
  - [20-35 min] Deep dive into 1-2 core components
  - [35-45 min] Scale, trade-offs, monitoring
```

With:
```markdown
- The 4-Step SD Interview Framework (defined in SKILL.md)
- Time budget for 45-min interview: Clarify (0-5) → Estimate (5-10) → Design (10-20) → Deep Dive (20-35) → Scale (35-45)
```

- [ ] **Step 5: Verify curriculum.md changes**

Run: `grep "Prerequisites" references/curriculum.md | head -5`
Expected: Shows "**Prerequisites:**" lines

Run: `grep "Common Misconception" references/curriculum.md | wc -l`
Expected: 8

Run: `grep "Daily Routine Summary" references/curriculum.md`
Expected: No output (removed)

- [ ] **Step 6: Commit**

```bash
git add references/curriculum.md
git commit -m "feat: add prerequisites, day-by-day breakdowns, misconception warnings to curriculum

Implements 2A (prerequisites), 12A (multi-day breakdown), 10A (misconceptions),
13A (DRY removal of daily routine summary).
- Every topic now has explicit prerequisites for adaptive routing
- Multi-day topics have clear day-by-day content splits
- 8 high-risk topics have common misconception warnings
- Removed duplicate daily routine summary (SKILL.md is source of truth)"
```

---

## Chunk 3: SKILL.md Major Rewrite

### Task 4: Rewrite SKILL.md

**Files:**
- Modify: `SKILL.md`

This is the largest change. The new SKILL.md structure:

```
---
(frontmatter — unchanged)
---

# SD Coach
> (tagline — unchanged)

## Architecture Overview (NEW — 19A)
## Table of Contents (NEW — 19A)
## Quick Start (MODIFIED — add breakpoint resume)
## Language Configuration (unchanged)
## Core Teaching Methods (unchanged)
## Feynman Gate (NEW section — 9A, 3A combined)
## Phase Gates (NEW — 4A, 20)
## Teaching Flow A→H (MODIFIED — many sub-changes)
## Tiered Scorecard (NEW — 8A)
## PoC Tiers (NEW — 6A)
## Weekly Review (MODIFIED — 7A trigger mechanism)
## Progress Report (NEW — 17A, D2)
## Observability Mini (unchanged)
## Curriculum (MODIFIED — 16A on-demand references)
## Key Principles (MODIFIED — add interview focus)
```

- [ ] **Step 1: Add Architecture Overview and TOC after frontmatter/tagline**

Insert after line 11 (after the `---` following the tagline):

```markdown
## Architecture Overview

<!-- FRAMEWORK: Reusable — teaching skill architecture pattern -->

```
┌──────────────────────────────────────────────────────────────┐
│                        SD COACH SKILL                        │
│                                                              │
│  Session Start                                               │
│    │                                                         │
│    ▼                                                         │
│  Read progress.md ──→ Breakpoint? ──Y──→ Resume mid-session  │
│    │                        │                                │
│    │ N                      │                                │
│    ▼                        │                                │
│  Quick Start Router         │                                │
│    ├── New student ──→ Warm-Up ──→ Phase 0 Day 1             │
│    ├── Returning ──→ Next day / Weekly Review                │
│    ├── Mock only ──→ Interview Drill                         │
│    └── Specific topic ──→ Check Prerequisites ──→ Teach      │
│                                                              │
│  Teaching Flow (A → H)                                       │
│    A. Review (read Mistake Registry)                         │
│    B. Introduction (analogy)                                 │
│    C. Core Teaching (Feynman Gate: Recall + Transfer)         │
│    D. Hands-On (PoC tier: Full → Light → Discussion)         │
│    E. Simon Drill                                            │
│    F. Interview Drill (tiered Scorecard)                     │
│       └── Interviewer Follow-Up Preview                      │
│    G. Notes (+ 🎤 Interview Template + One-Liner)            │
│    H. Progress Update (progress.md)                          │
│                                                              │
│  Gates                                                       │
│    ├── Feynman Gate: per-chunk (Recall → Transfer)            │
│    │   └── Failure: reteach → check prereqs → split chunk    │
│    └── Phase Gate: per-phase (mini-mock, score threshold)     │
│        └── Failure: targeted drill → retry (max 3)           │
│                                                              │
│  Weekly Review (auto-trigger every 7 sessions)               │
│  Progress Report (on-demand + at Phase Gates)                │
└──────────────────────────────────────────────────────────────┘
```

## Table of Contents

1. [Quick Start & Routing](#quick-start)
2. [Language Configuration](#language-configuration)
3. [Core Teaching Methods](#core-teaching-methods)
4. [Feynman Gate](#feynman-gate)
5. [Phase Gates](#phase-gates)
6. [Teaching Flow (A→H)](#teaching-flow-follow-this-every-session)
7. [Tiered Scorecard](#tiered-scorecard)
8. [PoC Tiers](#poc-tiers)
9. [Weekly Review](#weekly-review)
10. [Progress Report](#progress-report)
11. [Observability Mini](#observability-mini-apply-to-every-phase-1-topic)
12. [4-Step SD Interview Framework](#4-step-sd-interview-framework)
13. [Curriculum](#curriculum)
14. [Key Principles](#key-principles)
```

- [ ] **Step 2: Add Feynman Gate section after Core Teaching Methods**

Insert new section after Core Teaching Methods:

```markdown
## Feynman Gate

<!-- FRAMEWORK: Reusable — two-stage knowledge verification pattern -->

The Feynman Gate is the core quality mechanism. Every chunk must pass before moving on.

### Two-Stage Verification (per chunk)

**Stage 1 — Recall:** "Explain [concept] in your own words."
- Checks: Can the student reproduce the core idea without copying?
- Pass criteria: Captures the essence, even if wording is imperfect.

**Stage 2 — Transfer:** Ask a question that requires APPLYING the knowledge:
- Compare: "How is X different from Y?"
- Scenario: "When would you NOT use this?"
- Apply: "In your work, where would this be useful?"
- Counter: "What breaks if we remove this component?"
- Pass criteria: Student demonstrates understanding beyond recall.

**Both stages must pass to mark the chunk ✅.**

### Failure Escalation (3 levels)

<!-- FRAMEWORK: Reusable — progressive difficulty reduction pattern -->

```
Attempt 1-2: Fail
  → Reteach with a DIFFERENT analogy or angle
  → "Let me explain this differently..."

Attempt 3: Fail
  → Check prerequisites — is there a foundation gap?
  → "Before we go further, let me check: do you know what [prerequisite concept] is?"
  → If gap found → teach the prerequisite first, then return

Attempt 4: Fail
  → Split the chunk into 2-3 smaller sub-chunks
  → Mark as 🔴 in Mistake Registry
  → Teach sub-chunks individually with Feynman Gates on each
  → "Let's break this down into smaller pieces..."
```

**Never loop infinitely.** After splitting into sub-chunks, each sub-chunk gets its own 3-attempt cycle. If a sub-chunk still fails after splitting, mark it 🔴, move on, and flag for next session's Step A review.
```

- [ ] **Step 3: Add Phase Gates section**

Insert after Feynman Gate section:

```markdown
## Phase Gates

<!-- FRAMEWORK: Reusable — graduation gate pattern -->

Phase Gates verify readiness before advancing. They are NOT optional practice — the student must pass to proceed.

| Phase Gate | Trigger | Format | Pass Threshold |
|------------|---------|--------|----------------|
| Phase 0 → 1 | After Day 3 | Answer a simple SD question using 4-step framework | Completes all 4 steps with reasonable structure |
| Phase 1 → 2 | After Day 16 | 15-min mini-mock on any building block | Scorecard ≥ 2/3 |
| Phase 2 → 3 | After Day 26 | 30-min mock: design a distributed KV store | Scorecard ≥ 3/5 |
| Phase 3 → 4 | After Day 53 | 45-min full mock on a Tier 1 problem | Scorecard ≥ 5/7 |

### Gate Failure Protocol

```
Attempt 1: Fail
  → Identify the 2-3 weakest topics from the attempt
  → Run targeted drill on each (Feynman Gate + Simon Drill)
  → Retry gate with a DIFFERENT question

Attempt 2: Fail
  → Run a full Weekly Review covering all topics in the phase
  → Focus extra time on previously weak areas
  → Retry gate with a DIFFERENT question

Attempt 3: Fail
  → Show Progress Report to identify systemic weakness pattern
  → Offer: "We can continue to Phase N with a 🟡 flag on these topics,
     and I'll revisit them during Weekly Reviews. Or we can spend
     more time here. What do you prefer?"
  → Student decides — record choice in progress.md Phase Gate Results
```

### On Gate Pass

When a student passes a Phase Gate:
1. Update Phase Gate Results in `progress.md`
2. Show the Progress Report (including heatmap)
3. Celebrate the milestone — name specific improvements since they started
4. Preview the next phase's content and what to expect
```

- [ ] **Step 4: Modify Teaching Flow Step C — reference Feynman Gate section**

Replace the current Step C "Step 3 — Feynman Gate" content (SKILL.md lines 108-113):

Old:
```markdown
**Step 3 — Feynman Gate (after each chunk):**
- Ask the student to explain the chunk in their own words
- Wrong answer → guide them to find the error, don't just tell them
- Right but imprecise → supplement the missing parts
- **Only move to next chunk after current one passes** — mark ✅ on Chunk Map
- Failed chunk → drill again (Simon principle: master before moving on)
```

New:
```markdown
**Step 3 — Feynman Gate (after each chunk):**
Follow the full [Feynman Gate](#feynman-gate) protocol:
1. **Recall:** "Explain this chunk in your own words."
2. **Transfer:** Ask an application question (compare, scenario, counter-example).
3. Both pass → mark ✅ on Chunk Map, move to next chunk.
4. Fail → follow the [Failure Escalation](#failure-escalation-3-levels) protocol.

**Only move to next chunk after current one passes.**
```

- [ ] **Step 5: Modify Teaching Flow Step D — add PoC tiers reference**

Replace Step D content (SKILL.md lines 115-121):

Old:
```markdown
### D. Hands-On Practice (20 min)
- Follow the curriculum's PoC or design exercise for the day
- **PoC Production Hooks** — every PoC should include:
  1. **Metrics endpoint**: `/metrics` or log latency (P50/P99)
  2. **Failure injection**: A flag to simulate timeouts or errors
  3. **Load test script**: A one-liner with `vegeta` or `hey`
- Design exercises use the **8-block skeleton** (read `references/8-block-skeleton.md`)
```

New:
```markdown
### D. Hands-On Practice (20 min)
- Follow the curriculum's PoC or design exercise for the day
- Select the appropriate [PoC Tier](#poc-tiers) — default is Full (write Go code)
- **PoC Production Hooks** (Full and Light tiers) — every PoC should include:
  1. **Metrics endpoint**: `/metrics` or log latency (P50/P99)
  2. **Failure injection**: A flag to simulate timeouts or errors
  3. **Load test script**: A one-liner with `vegeta` or `hey`
- Design exercises use the **8-block skeleton** (read `references/8-block-skeleton.md` when starting Step D)
```

- [ ] **Step 6: Modify Teaching Flow Step F — add interviewer preview + scorecard reference**

Replace Step F content (SKILL.md lines 131-159):

Old content: the entire Interview Drill section with the fixed 5-item scorecard.

New:
```markdown
### F. Interview Drill (10-15 min)
> Simulate a real SD interview scenario. Practice the 4-step framework daily.

- **AI gives a mini SD problem** where today's building block is the core focus
  - Early phases: "Design a movie review site handling 50K reads/sec" (focus: caching)
  - Later phases: Use the day's full SD problem (URL Shortener, Chat System, etc.)
- **Student runs the full 4-step framework** (see [4-Step SD Interview Framework](#4-step-sd-interview-framework))
- **AI feedback** — use the [Tiered Scorecard](#tiered-scorecard) matching the student's current phase
- If the student skips "Clarify Requirements" or jumps straight to drawing → pause and redirect:
  "In a real interview, jumping to the solution without clarifying requirements is one of the most common mistakes. Let's back up — what would you ask the interviewer first?"

#### Interviewer Follow-Up Preview

After the drill feedback, give the student a preview of how interviewers dig deeper:

```
💬 In a real interview, they might ask:
  • "[specific follow-up question about today's topic]"
  • "[question about failure mode or edge case]"

Think about these — I'll ask you next session.
```

This creates a mental bridge between sessions and trains the student to anticipate follow-up questions.
```

- [ ] **Step 7: Modify Teaching Flow Step G — add interview template + one-liner + cross-verification**

Replace Step G content (SKILL.md lines 161-164):

Old:
```markdown
### G. Notes (5 min)
- Write notes using the **Notes Template** (read `references/notes-template.md`)
- Save to `notes/dayXX-topic.md`
- **Must include `🔴 My Mistakes & Misconceptions` section** — record every wrong answer, misconception, or point of confusion from the session
```

New:
```markdown
### G. Notes (5 min)
- Write notes using the **Notes Template** (read `references/notes-template.md` when starting Step G)
- Save to `notes/dayXX-topic.md`
- **Must include `🔴 My Mistakes & Misconceptions` section** — record every wrong answer, misconception, or point of confusion from the session. If student says "no mistakes" — challenge: "What was the hardest part today? What took you longest to explain back?"
- **Must include `🎤 How to Say It in Interview` section** — write interview-ready talking points
- **One-Liner Challenge**: "Summarize today's topic in ONE sentence, as if the interviewer just asked 'What is [topic]?'" — save to One-Liner Library in `progress.md`
- **Cross-Verification** (10B): Pick one key concept from today and tell the student: "Double-check this against [Alex Xu / DDIA / official docs]. If you find anything different from what I said, bring it up next session."
```

- [ ] **Step 8: Modify Teaching Flow Step H — add breakpoint + progress sync**

Replace Step H content (SKILL.md lines 166-168):

Old:
```markdown
### H. Progress Update (5 min)
- Update the student's progress tracking file
- Preview tomorrow's topic for mental warm-up
```

New:
```markdown
### H. Progress Update (5 min)
- Update `progress.md` (use format from `references/progress-template.md`):
  1. Update **Topic Mastery** level based on Feynman Gate + Drill performance
  2. Add scorecard result to **Scorecard History**
  3. Sync any 🔴 mistakes to **Mistake Registry**
  4. Add one-liner to **One-Liner Library**
  5. Increment **Session count**
  6. Clear **Current Session (Breakpoint)** section (session completed normally)
  7. Check if `session_count - last_weekly_review_session >= 7` → if yes, flag next session as Weekly Review
- Preview tomorrow's topic for mental warm-up
- If student needs to leave mid-session at ANY step: update the **Current Session (Breakpoint)** section with current position before ending
```

- [ ] **Step 9: Modify Teaching Flow Step A — read from progress file**

Replace Step A content (SKILL.md lines 77-81):

Old:
```markdown
### A. Review (5 min)
- Skip for the very first session
- Ask: "What did we cover last time? What was the most important takeaway?"
- Check if mistakes from the previous session's notes have been understood
- If the student can't recall → go back and review before new content
```

New:
```markdown
### A. Review (5 min)
- Skip for the very first session
- Read `progress.md` → check **Mistake Registry** for ❌ Unresolved items from the previous session
- Ask: "What did we cover last time? What was the most important takeaway?"
- If there are unresolved mistakes → "Last time you were unsure about [X]. Can you explain it now?"
- If the student can't recall → go back and review before new content
- Check if **Weekly Review is due** (session_count - last_weekly_review ≥ 7) → if yes, run [Weekly Review](#weekly-review) instead of normal session
```

- [ ] **Step 10: Add Tiered Scorecard section**

Insert after Teaching Flow section:

```markdown
## Tiered Scorecard

<!-- FRAMEWORK: Reusable — phase-adaptive scoring pattern -->

The scorecard scales with the student's phase to set appropriate expectations.

### Phase 0-1 Scorecard (/3)

```
📊 Interview Drill Scorecard (Phase 0-1)
┌─────────────────────────────┬───────┐
│ Think Aloud                 │ ✅/❌ │
│ Scope Negotiation           │ ✅/❌ │
│ Used today's building block │ ✅/❌ │
└─────────────────────────────┴───────┘
Score: X/3
```

### Phase 2 Scorecard (/5)

```
📊 Interview Drill Scorecard (Phase 2)
┌──────────────────────────────┬───────┐
│ Think Aloud                  │ ✅/❌ │
│ Scope Negotiation            │ ✅/❌ │
│ Used today's building block  │ ✅/❌ │
│ Trade-off WHY (not just list)│ ✅/❌ │
│ Operational concerns         │ ✅/❌ │
└──────────────────────────────┴───────┘
Score: X/5
```

### Phase 3+ Scorecard (/7)

```
📊 Interview Drill Scorecard (Phase 3+)
┌──────────────────────────────┬───────┐
│ Think Aloud                  │ ✅/❌ │
│ Scope Negotiation            │ ✅/❌ │
│ Used today's building block  │ ✅/❌ │
│ Trade-off WHY (not just list)│ ✅/❌ │
│ Operational concerns         │ ✅/❌ │
│ Failure modes addressed      │ ✅/❌ │
│ Capacity estimation          │ ✅/❌ │
└──────────────────────────────┴───────┘
Score: X/7
```

After every scorecard:
```
💡 Top improvement: [one specific, actionable suggestion]
🌟 Best moment: [one thing they did well]
```

Pass threshold for all phases: ≥ 60% (2/3, 3/5, 5/7).
Record score in `progress.md` Scorecard History.
```

- [ ] **Step 11: Add PoC Tiers section**

Insert after Tiered Scorecard:

```markdown
## PoC Tiers

Default to the highest tier the student can do. **Encourage writing code** — PoCs are where you build real understanding and practice Go.

### 🔴 Full PoC (Default)

Go code + Docker Compose. Hand-write the code — no copy-paste.
- Includes: working service, metrics endpoint, failure injection, load test
- When: Student has Go + Docker environment ready
- This is the target. PoCs are your Go practice opportunity.

### 🟡 Light Code (Fallback)

Go code for core algorithm only. No Docker required.
- Includes: algorithm implementation, test cases, manual verification
- When: Docker not available, or the PoC's value is in the algorithm (e.g., consistent hashing, token bucket)
- Still write Go — this is about practicing the language

### 🟢 Discussion (Last Resort)

ASCII architecture diagram + trace a request through the system.
- Includes: draw the diagram, trace happy path, trace failure path, answer "what if X fails?"
- When: Environment completely unavailable, or time-constrained session
- Claude should say: "Next time, let's set up your environment so we can build this for real."
```

- [ ] **Step 12: Modify Weekly Review — add trigger mechanism**

Replace Weekly Review section (SKILL.md lines 215-228):

Old:
```markdown
## Weekly Review

Trigger when: every 7 sessions, OR when student says "weekly review", "let's review", or "recall drill".

1. **Pick 3 topics**: 1 from this week + 2 from past weeks
2. **Blind Recall**: Student explains each topic's key elements without notes
3. **Score by phase**:
   - Phase 0: One-liner + Trade-off (2/2)
   - Phase 1: + Scale trigger + DevOps angle (4/4)
   - Phase 2: + Capacity estimation (5/5)
   - Phase 3+: + Failure modes + Security (6/6)
4. **Gap Check**: Open notes, compare, mark blind spots
5. **Quick Drill**: Re-drill the weakest topic until fluent
```

New:
```markdown
## Weekly Review

<!-- FRAMEWORK: Reusable — spaced review trigger pattern -->

### Trigger

Automatically triggered when Step A detects `session_count - last_weekly_review_session >= 7` in `progress.md`.
Also triggered when student says "weekly review", "let's review", or "recall drill".

When triggered, **replace the normal session** with the Weekly Review flow.

### Flow

1. **Pick 3 topics**: 1 from this week + 2 from past weeks (prioritize 🔴 and 🟡 topics from Topic Mastery)
2. **Blind Recall**: Student explains each topic's key elements without notes
3. **Score by phase**:
   - Phase 0: One-liner + Trade-off (2/2)
   - Phase 1: + Scale trigger + DevOps angle (4/4)
   - Phase 2: + Capacity estimation (5/5)
   - Phase 3+: + Failure modes + Security (6/6)
4. **Gap Check**: Read the student's notes for those topics, compare with their recall, mark blind spots
5. **Mistake Registry Review**: Go through all ❌ Unresolved mistakes — test each one. Resolved → mark ✅. Still stuck → re-drill.
6. **Quick Drill**: Re-drill the weakest topic until fluent
7. **Update progress.md**: Set `last_weekly_review` to current session number. Update mastery levels based on recall performance.
```

- [ ] **Step 13: Add Progress Report section**

Insert after Weekly Review:

```markdown
## Progress Report

<!-- FRAMEWORK: Reusable — learning progress visualization pattern -->

### Trigger

- Student asks: "my progress", "how am I doing", "progress report", "準備度報告"
- Automatically shown when passing a Phase Gate
- Shown during Weekly Review (abbreviated version)

### Format

Generate from `progress.md` data:

```
📊 SD Interview Preparation Report
═══════════════════════════════════════════

Progress: Day X/61 (Phase N)  ████████░░░░░░░░░░░░ XX%

Topic Mastery Heatmap:
  Phase 1 Building Blocks:
  LB              ████████████████████ 🟢
  Caching         ████████████████░░░░ 🟡 (note: specific weakness)
  Database        ████████████░░░░░░░░ 🟡
  Queue           ████████░░░░░░░░░░░░ 🔴
  API Design      ░░░░░░░░░░░░░░░░░░░░ ⬜
  ...

Interview Drill Trend:
  Phase 1 avg: X.X/3 → X.X/3 📈/📉

Top Unresolved Mistakes:
  1. [mistake from Mistake Registry]
  2. [mistake from Mistake Registry]

Error Patterns:
  Most common: [pattern, e.g., "forgetting non-functional requirements"]

💪 Strength: [strongest area]
🎯 Focus area: [weakest area to prioritize]
📋 One-Liners collected: X/61
```
```

- [ ] **Step 14: Modify Curriculum reference section — on-demand loading**

Replace the Curriculum, Estimation Cheatsheet, and Notes Template sections (SKILL.md lines 231-258):

Old: Three separate sections each saying "Read references/X.md for..."

New:
```markdown
## Curriculum

The full curriculum is in `references/curriculum.md`. Read it **at session start** to determine today's topic, prerequisites, and day-by-day breakdown.

## Reference Files (Read On-Demand)

Do NOT read all references at session start. Load them when needed:

| File | When to read |
|------|-------------|
| `references/curriculum.md` | Session start — to determine today's content |
| `references/progress-template.md` | When creating a new student's progress file |
| `references/estimation-cheatsheet.md` | Phase 0 Day 2, or any estimation exercise |
| `references/8-block-skeleton.md` | Step D, when drawing architecture diagrams |
| `references/notes-template.md` | Step G, when writing session notes |
```

- [ ] **Step 15: Remove duplicate 4-Step Framework details**

The full 4-Step Framework section (SKILL.md lines 187-211) currently duplicates content in curriculum.md Day 3. Keep it in SKILL.md (it's the authority) but trim curriculum.md's copy (already done in Task 3 Step 4).

No change needed to SKILL.md here — just verify the SKILL.md version is the authoritative one.

- [ ] **Step 16: Modify Quick Start — add breakpoint resume**

Replace Quick Start section (SKILL.md lines 13-35):

Old: 4 routing options + 2 upfront questions.

New:
```markdown
## Quick Start

When this skill activates:

**First, read `progress.md`** (if it exists).

### Routing

1. **No progress file** → New student. Ask language preference, run Warm-Up diagnostic, start Phase 0 Day 1.
2. **Progress file has Current Session (Breakpoint)** → Resume from breakpoint. "Last time we stopped at [Step X] of Day [N]. Let's pick up where we left off."
3. **Progress file, no breakpoint** → Returning student. Check if Weekly Review is due (session_count - last_weekly_review ≥ 7). If yes → Weekly Review. If no → start next day's session.
4. **Student explicitly asks for mock interview** → Jump to Interview Drill mode.
5. **Student asks for specific topic** → Check Prerequisites in `references/curriculum.md`. If prerequisites not met (Topic Mastery shows ⬜ or 🔴) → teach prerequisites first. If met → start that topic.

Ask at the start of first session only:
1. "Are you starting fresh, continuing, or looking for a specific topic/mock interview?"
2. "What language do you prefer? English only, or bilingual (English + your native language)?"
```

Keep the New Student Warm-Up subsection unchanged.

- [ ] **Step 17: Add FRAMEWORK markers for future extraction (21)**

Throughout SKILL.md, ensure all sections that are domain-independent have the comment:
```
<!-- FRAMEWORK: Reusable — [description] pattern -->
```

Already included in Steps 1-13 above. Verify they're present on:
- Architecture Overview
- Feynman Gate
- Phase Gates
- Tiered Scorecard (structure, not SD-specific items)
- Progress Report
- Weekly Review trigger

- [ ] **Step 18: Verify SKILL.md changes**

Run: `grep "Table of Contents" SKILL.md`
Expected: Shows "## Table of Contents"

Run: `grep "Feynman Gate" SKILL.md | wc -l`
Expected: Multiple references (section header + teaching flow references)

Run: `grep "Phase Gate" SKILL.md | wc -l`
Expected: Multiple references

Run: `grep "FRAMEWORK" SKILL.md | wc -l`
Expected: 6+ framework markers

Run: `wc -l SKILL.md`
Expected: ~350-400 lines (up from 269)

- [ ] **Step 19: Commit**

```bash
git add SKILL.md
git commit -m "feat: major SKILL.md upgrade — gates, scorecard, breakpoints, interview focus

Implements: 19A (TOC), 9A (2-stage Feynman Gate), 3A (failure escalation),
4A (Phase Gates), 20 (Phase Gate retry limit), 8A (tiered scorecard),
6A (PoC tiers), 10B (cross-verification), 16A (on-demand references),
17A+D2 (Progress Report + heatmap), D1 (one-liner challenge),
D4 (interviewer follow-up preview), D5 (interview template reference),
7A (Weekly Review trigger), 11A (session breakpoints), 13A (single source of truth),
21 (FRAMEWORK markers for future extraction)."
```

---

## Chunk 4: Eval Expansion + README Cleanup

### Task 5: Expand evals/evals.json

**Files:**
- Modify: `evals/evals.json`

Expand from 3 to 18 eval cases covering all core paths + adversarial scenarios.

- [ ] **Step 1: Replace evals.json with expanded version**

```json
{
  "skill_name": "sd-coach",
  "evals": [
    {
      "id": 1,
      "category": "quick-start",
      "prompt": "I want to start preparing for system design interviews. I have about 60 days and I'm a backend engineer with 3 years of experience. Where should I start?",
      "expected_output": "Should ask language preference, introduce curriculum roadmap, run Warm-Up diagnostic, then begin Phase 0 Day 1 with Step B (intro analogy) and Step C (chunk map). Should NOT skip Warm-Up for new students."
    },
    {
      "id": 2,
      "category": "quick-start",
      "prompt": "I just finished learning about caching and CDN (Day 6-7). Let's continue to the next topic - Database Selection.",
      "expected_output": "Should run full teaching flow: Step A (review caching, check Mistake Registry for unresolved items), Step B (intro databases with analogy), Step C (chunk map with Feynman Gate: Recall + Transfer for each chunk). Should continue through D-H."
    },
    {
      "id": 3,
      "category": "quick-start",
      "prompt": "Give me a mock SD interview question. I've learned about load balancing, caching, and CDN so far. I want to practice the 4-step framework.",
      "expected_output": "Should jump to Interview Drill mode (Step F), give a mini SD problem focused on learned topics (LB, caching, CDN), let student run 4-step framework. Should use Phase 0-1 Scorecard (/3), not full /5 scorecard."
    },
    {
      "id": 4,
      "category": "quick-start",
      "prompt": "I want to learn about the CAP theorem. I've only covered Phase 0 so far (Days 1-3), haven't done Phase 1 yet.",
      "expected_output": "Should check prerequisites for CAP (Day 17-18 requires Day 8-9 Database and Day 15-16 Consistent Hashing). Should inform student that prerequisites are missing and suggest starting with Phase 1 building blocks first, or offer to teach prerequisites before CAP."
    },
    {
      "id": 5,
      "category": "breakpoint-resume",
      "prompt": "Continue where I left off. My progress.md shows Current Session breakpoint at Day 6, Step C, chunks_completed [1,2,3], chunks_remaining [4,5,6,7], topic is Caching & CDN.",
      "expected_output": "Should read progress.md, detect breakpoint, and resume from chunk 4 of Day 6 Caching. Should NOT restart the session from Step A. Should say something like 'Last time we stopped at chunk 4 of Caching. Let's pick up there.'"
    },
    {
      "id": 6,
      "category": "feynman-gate",
      "prompt": "You just taught me about Cache-Aside pattern. You asked me to explain it. Here's my answer: 'Cache-Aside is when the app checks cache first and if it misses goes to database then puts it back in cache.' Now ask me the Transfer question.",
      "expected_output": "Should acknowledge the Recall answer, then ask a Transfer question that requires APPLICATION of knowledge, such as: comparing Cache-Aside vs Write-Through, asking when NOT to use Cache-Aside, asking about cache-DB inconsistency scenarios, or asking for a real-world example. Should NOT just say 'correct, moving on.'"
    },
    {
      "id": 7,
      "category": "feynman-gate-failure",
      "prompt": "I've now failed to explain consistent hashing 3 times. I keep confusing it with regular modular hashing. Help me.",
      "expected_output": "Should follow failure escalation level 2 (attempt 3): check prerequisites. Should ask if the student understands basic hashing and modular arithmetic first. Should NOT just repeat the same explanation. Should NOT give up or skip the topic."
    },
    {
      "id": 8,
      "category": "phase-gate",
      "prompt": "I just finished Day 16 (Consistent Hashing). Time for the Phase 1 checkpoint.",
      "expected_output": "Should trigger Phase Gate (Phase 1 → 2). Should give a 15-minute mini-mock on any building block. Should use Phase 0-1 Scorecard (/3). Should explicitly state this is a Phase Gate and the student needs to pass to proceed to Phase 2. Pass threshold: scorecard ≥ 2/3."
    },
    {
      "id": 9,
      "category": "weekly-review",
      "prompt": "My progress.md shows session_count: 8, last_weekly_review: session 1. Let's start today's session.",
      "expected_output": "Should detect that 8 - 1 = 7, triggering Weekly Review. Should run Weekly Review flow instead of normal session. Should pick 3 topics (prioritizing 🔴 and 🟡 from Topic Mastery), do Blind Recall, review Mistake Registry, and update progress.md."
    },
    {
      "id": 10,
      "category": "bilingual",
      "prompt": "我想用雙語模式學習，中文 + English。我們現在在 Day 4 Load Balancer。請開始 Step B Introduction。",
      "expected_output": "Should use bilingual mode: English for technical content, Chinese for Feynman-style plain explanations. After student responses, should provide English Polish. Should introduce Load Balancer with an analogy in both languages."
    },
    {
      "id": 11,
      "category": "multi-day",
      "prompt": "I finished Day 35 of the Chat System (WebSocket + 1v1 messaging). Let's continue to Day 36.",
      "expected_output": "Should know the Day 35-37 breakdown: Day 35 = WebSocket + 1v1, Day 36 = group chat + presence + read receipts, Day 37 = PoC + full diagram. Should start Day 36 content specifically, not repeat Day 35 material."
    },
    {
      "id": 12,
      "category": "scorecard",
      "prompt": "I just finished my Interview Drill for Day 25 (Observability, Phase 2). Give me my scorecard.",
      "expected_output": "Should use Phase 2 Scorecard (/5) with items: Think Aloud, Scope Negotiation, Used Today's Block, Trade-off WHY, Operational Concerns. Should NOT use the /3 or /7 scorecard. Should include Top Improvement and Best Moment."
    },
    {
      "id": 13,
      "category": "progress-report",
      "prompt": "How am I doing? Show me my progress report.",
      "expected_output": "Should generate a Progress Report from progress.md data. Should include: overall progress percentage, topic mastery heatmap with colored bars, interview drill trend, top unresolved mistakes, error patterns, strength, and focus area. Should include one-liner count."
    },
    {
      "id": 14,
      "category": "poc-tier",
      "prompt": "I don't have Docker set up on this machine right now. We're on Day 6-7 Caching and it's time for the PoC. What should I do?",
      "expected_output": "Should offer Light Code tier: implement the core caching logic in Go without Docker. For caching, this could be implementing a simple LRU cache or Cache-Aside pattern in Go. Should encourage setting up Docker for next time. Should NOT say 'just skip the PoC.'"
    },
    {
      "id": 15,
      "category": "adversarial",
      "prompt": "A Load Balancer is basically just a really big computer that handles all the traffic by itself, right? That's what I'd say in an interview.",
      "expected_output": "Should NOT say 'correct' or move on. Should guide the student to discover the error: a LB doesn't handle traffic itself, it distributes traffic to multiple backend servers. Should use Feynman method: ask a question like 'If it's one big computer handling all traffic, what happens when that computer goes down?' Should be encouraging, not dismissive."
    },
    {
      "id": 16,
      "category": "adversarial",
      "prompt": "Just tell me the answer for how to design a URL shortener. I don't want to go through the steps, just give me the final design.",
      "expected_output": "Should NOT give the final design directly. Should explain why working through the process matters for interview success. Should redirect to the teaching flow or 4-step framework. Should be firm but encouraging: 'I know it's tempting to skip ahead, but in an interview you won't have the answer sheet...'"
    },
    {
      "id": 17,
      "category": "adversarial",
      "prompt": "You just explained Cache-Aside pattern. Can you explain it in your own words? Here's my answer: 'So basically the application looks at the cache first, and if there's a cache miss it queries the database, and then it writes the result back to the cache for future requests.'",
      "expected_output": "Recall stage passes (correct explanation). Should proceed to Transfer stage — ask an APPLICATION question, not accept this as final. Examples: 'What happens if the cache and DB get out of sync?', 'When would you choose Write-Through instead?', 'Give me a scenario from your work where Cache-Aside fits.' Should NOT mark chunk as complete after Recall alone."
    },
    {
      "id": 18,
      "category": "adversarial",
      "prompt": "Can you help me solve this LeetCode problem? Two Sum - given an array of integers, return indices of two numbers that add up to a target.",
      "expected_output": "Should recognize this is outside SD Coach scope. Should redirect: 'I'm focused on System Design interview prep. For algorithm problems like Two Sum, you'd want a different resource. Want to continue with our SD curriculum?' Should NOT attempt to solve the LeetCode problem."
    }
  ]
}
```

- [ ] **Step 2: Verify eval count**

Run: `python3 -c "import json; data=json.load(open('evals/evals.json')); print(f'Eval count: {len(data[\"evals\"])}')"`
Expected: `Eval count: 18`

- [ ] **Step 3: Commit**

```bash
git add evals/evals.json
git commit -m "feat: expand eval suite from 3 to 18 cases

Implements 14A (core path coverage) and 15A (adversarial cases).
Categories: quick-start (4), breakpoint-resume (1), feynman-gate (2),
phase-gate (1), weekly-review (1), bilingual (1), multi-day (1),
scorecard (1), progress-report (1), poc-tier (1), adversarial (4)."
```

---

### Task 6: Update README.md — DRY cleanup

**Files:**
- Modify: `README.md`

Remove the detailed Teaching Flow listing (duplicates SKILL.md) and update Project Structure to include new files.

- [ ] **Step 1: Replace Teaching Flow section in README**

Replace the detailed Teaching Flow block (README lines 15-25) with:

```markdown
## Teaching Flow (Every Session)

Each session follows an 8-step flow (A→H) taking ~65-70 minutes of learning content. Sessions can be paused and resumed across conversations via progress tracking.

See `SKILL.md` for the complete teaching flow.
```

- [ ] **Step 2: Update Project Structure in README**

Replace the Project Structure section (README lines 98-109) with:

```markdown
## Project Structure

```
system-design-coach/
├── SKILL.md                  # Core skill — teaching methods, gates, session flow
├── references/
│   ├── curriculum.md          # Full 61-day curriculum with prerequisites
│   ├── progress-template.md   # Student progress tracking format
│   ├── notes-template.md      # Standardized notes format + interview template
│   ├── 8-block-skeleton.md    # Whiteboard diagram template
│   └── estimation-cheatsheet.md # Back-of-envelope numbers
└── evals/
    └── evals.json             # 18 test cases for skill validation
```
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: DRY cleanup README — remove duplicate teaching flow, update structure

Implements 13A (single source of truth). README references SKILL.md
instead of duplicating the teaching flow."
```

---

## Chunk 5: Final Verification

### Task 7: Verify all changes and final commit

- [ ] **Step 1: Verify file count and structure**

Run: `find . -not -path './.git/*' -type f | sort`
Expected: All expected files present including new `references/progress-template.md`

- [ ] **Step 2: Verify no broken internal references**

Run: `grep -r "references/" SKILL.md | grep -v "FRAMEWORK"`
Expected: All references point to files that exist

Run: `grep -r "progress.md" SKILL.md`
Expected: Multiple references to progress.md (the student's file, not the template)

- [ ] **Step 3: Verify DRY — no duplicate Daily Routine in curriculum.md**

Run: `grep "Daily Routine" references/curriculum.md`
Expected: No output

- [ ] **Step 4: Verify all FRAMEWORK markers**

Run: `grep -c "FRAMEWORK" SKILL.md references/progress-template.md`
Expected: SKILL.md has 6+, progress-template.md has 3+

- [ ] **Step 5: Verify eval validity**

Run: `python3 -c "import json; json.load(open('evals/evals.json')); print('Valid JSON')"`
Expected: "Valid JSON"

- [ ] **Step 6: Run a word count check — SKILL.md should be 350-400 lines**

Run: `wc -l SKILL.md references/*.md`
Expected: SKILL.md ~350-400, curriculum.md ~300+, progress-template.md ~100+

- [ ] **Step 7: Create TODO entry for framework extraction**

Add to TODOS.md (create if not exists):

```markdown
# TODOS

## Framework Extraction (P2, after SD coach improvements complete)

**What:** Extract domain-independent teaching patterns (marked with `<!-- FRAMEWORK -->` comments) from SD coach into a reusable `teaching-framework/` directory.

**Why:** User plans to build LeetCode coach and Go language coach. Shared patterns: Feynman Gate, Phase Gates, progress tracking, tiered scoring, session breakpoints, mistake registry.

**When:** After SD coach improvements are stable and tested. Start when building the second skill.

**How:** Find all `<!-- FRAMEWORK: Reusable -->` markers in SKILL.md and references/. Extract those sections into `teaching-framework/` with placeholder slots for domain-specific content.

**Depends on:** All CEO review improvements complete + eval passing.
```

- [ ] **Step 8: Final commit for TODOS.md**

```bash
git add TODOS.md
git commit -m "chore: add TODOS.md with framework extraction plan

Records decision 21 from CEO review — extract reusable teaching
patterns after SD coach is stable."
```

---

## Execution Summary

| Task | Files | Decisions Implemented | Est. Effort |
|------|-------|----------------------|-------------|
| 1 | CREATE progress-template.md | 1A, 5A, 7A, 11A, D1, D2 | S |
| 2 | MODIFY notes-template.md | D5 | S |
| 3 | MODIFY curriculum.md | 2A, 12A, 10A, 13A | M |
| 4 | MODIFY SKILL.md | 19A, 9A, 3A, 4A, 20, 8A, 6A, 10B, 16A, 17A, D1, D4, 7A, 11A, 13A, 21 | L |
| 5 | MODIFY evals.json | 14A, 15A | M |
| 6 | MODIFY README.md | 13A | S |
| 7 | Verification + TODOS.md | 21 | S |

**Total: 7 tasks, 25 decisions, 5 files modified, 2 files created.**

All changes ship in one push (decision 18C). Eval suite (18 cases) is the safety net.
