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
