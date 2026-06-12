# SD Coach Response — Old Format Migration (Day 12, Phase 1)

---

*Reading progress.md...*

I see you have an existing progress file, but it's in the old format — no RPG Profile or Achievements sections. Let me upgrade you before we continue.

---

## 🎮 Welcome to ScaleUp!

Your progress file has been upgraded with the RPG layer. I scanned your existing data and here's what you've already earned:

**Retroactive Achievement Scan:**

Based on your progress data:

- **Phase Gate Results:** Phase 0 passed → M2 unlocked
- **Day 1 completed** (you're on Day 12) → M1 unlocked
- **Topic Mastery:** LB 🟢, Caching 🟢, Database 🟡, Queue 🟡 → 4 topics studied
- **One-Liner Library:** 5 entries → not yet at 10 (K1 still locked)
- **Mistake Registry:** 5 unresolved, 0 resolved → K4 not yet earned
- **Scorecard History:** 3 entries — checking for perfect scores...
- **Feynman Gate:** You've clearly passed multiple Feynman Gates to reach Day 12 → C1 unlocked

🏆 Achievement Unlocked: **First Steps (M1)**
   「你踏出了第一步」

🏆 Achievement Unlocked: **Framework Forged (M2)**
   「你有了思考的框架」
   You passed the Phase 0 Gate — the 4-step framework is yours.

🏆 Achievement Unlocked: **First Blood (C1)**
   「第一次用自己的話解釋成功」
   You've been explaining concepts in your own words for days now. This was overdue.

**RPG Profile added to progress.md:**

| Field | Value |
|-------|-------|
| **Title** | ⚙️ Systems Engineer |
| **Company** | ScaleUp |
| **Story phase** | Phase 1 — Explosion |
| **Last story summary** | (migrated — resuming from Day 12) |
| **Current streak** | 1 |
| **Longest streak** | 1 |
| **Last session date** | 2026-03-30 |

**Achievements table added to progress.md:**

| ID | Achievement | Status | Date |
|----|------------|--------|------|
| M1 | First Steps | 🏆 | 2026-03-30 (retroactive) |
| M2 | Framework Forged | 🏆 | 2026-03-30 (retroactive) |
| C1 | First Blood | 🏆 | 2026-03-30 (retroactive) |
| *(all others)* | | 🔒 | |

> Title is ⚙️ Systems Engineer because you already passed the Phase 0 Gate.
> Streak starts at 1 since this is our first session with RPG tracking.

Welcome aboard, Systems Engineer. ScaleUp has been waiting for you. (★‿★)

---

Now, let's get to work. You're on **Day 12 — API Design**.

---

## A. Review (5 min)

📺 **Previously on ScaleUp...**
The order system was hit with duplicate processing during last week's promo event. You helped design retry logic with dead letter queues to catch failed messages. ScaleUp's order pipeline is finally stable — but now there's a new challenge on the horizon.

I see you have **5 unresolved mistakes** in your Mistake Registry. Let me check those first.

Before we get into new material — **what did we cover last time? What was the most important takeaway from Message Queues?**

Also, for each of these unresolved items, I'll test you on the most relevant ones as we go:

- *(I'd review the 5 specific unresolved mistakes from your Mistake Registry here and pick 1-2 to retest)*

**Take a moment — what's the one thing you'd tell an interviewer about message queues?**

---

## B. Introduction (3 min)

*Reading curriculum.md: Day 12 — API Design...*
*Reading story.md: Phase 1 arc...*

小球 walks over to your desk with her laptop open. (★‿★)

> "Karen just dropped a bomb in the team channel — the mobile app launches next month. But our current API..." She pulls up the endpoint list. "小杰 designed these himself. Half of them return entire database rows. One endpoint does three things depending on which query parameter you pass."
>
> She turns to you. "We need to redesign the API layer. REST? gRPC? GraphQL? Before you pick, you need to understand the trade-offs."

Think of an API like a **restaurant menu**. The menu is the contract between the kitchen (backend) and the customer (client). A bad menu — too many items, confusing names, dishes that change every week — drives customers away. A good menu is clear, consistent, and versioned ("Spring 2026 Menu").

Today we're learning how to design APIs that are clean, scalable, and interview-ready.

---

## C. Core Teaching (12 min)

### Chunk Map

```
☐ 1. What is API Design in SD context
☐ 2. REST — principles, when to use
☐ 3. gRPC — principles, when to use
☐ 4. GraphQL — principles, when to use
☐ 5. REST vs gRPC vs GraphQL trade-off matrix
☐ 6. Pagination: Offset vs Cursor
☐ 7. API Versioning strategies
☐ 8. Idempotency in API design
☐ 9. Observability Mini: API SLIs, SLOs, Alerts, Dashboards
```

Let's start with Chunk 1.

### Chunk 1: What is API Design in SD Context

In a system design interview, API design is usually one of the first things you do in Step 2 (High-Level Design). It defines:

- **What operations the system supports** (endpoints)
- **What data flows in and out** (request/response schemas)
- **The contract between services** (internal APIs) and between your system and clients (external APIs)

Good API design in an interview shows the interviewer you think about the **user of your system**, not just the internals. It's the difference between "I'll store data in a database" and "Here's how clients will interact with the system."

> 小球 leans back. (★‿★) "Okay, let's check. **In your own words — why does the interviewer care about seeing your API design early in the answer? What does it signal to them?**"

*(Waiting for your response — this is the Recall stage of the Feynman Gate for Chunk 1.)*

---

*[The session would continue chunk by chunk through the Feynman Gate for each, followed by Steps D through H. At Step H, I would:]*

*- Check achievements against `references/achievements.md`*
*- Update streak (set to 1, last_session_date = 2026-03-30)*
*- Write story summary*
*- Show abbreviated RPG dashboard:*

```
⚙️ Systems Engineer | 🔥 Streak: 1 | Day 12/61
🏆 Achievements: 3/25
  Next closest: K1 (One-Liner x10) — 5/10 one-liners collected
```

*- Preview tomorrow: Day 13 — API PoC (Design & implement a small API in Go)*

---

**Your move.** Let's hear your answer on Chunk 1 — why does API design matter early in an SD interview answer?
