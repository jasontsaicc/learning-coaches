# SD Coach Response — Returning Student, Day 12, Phase 1

## Context

The student says they have an existing `progress.md` from "before the RPG update" with sections: Student Info, Topic Mastery, Scorecard History, Mistake Registry, One-Liner Library, and Phase Gate Results — but no "RPG Profile" or "Achievements" sections. They are on Day 12, Phase 1.

## How the Main Branch Skill Handles This

The main branch skill has **no RPG features whatsoever**. It does not know what an "RPG Profile" or "Achievements" section is. The skill simply reads `progress.md` at session start and routes based on what it finds.

The student's existing `progress.md` structure (Student Info, Topic Mastery, Scorecard History, Mistake Registry, One-Liner Library, Phase Gate Results) **exactly matches** the `progress-template.md` defined in the main branch references. There is nothing missing, nothing to migrate, and nothing to add.

---

## Full Coach Response

Welcome back! I've read your `progress.md`. Here's what I see:

**Your current status:**

| Field | Value |
|-------|-------|
| Current phase | Phase 1 |
| Current day | Day 12 |
| Topics mastered | LB 🟢, Caching 🟢, Database 🟡, Queue 🟡 |
| Scorecard entries | 3 |
| Unresolved mistakes | 5 |
| Phase Gate | Phase 0 passed ✅ |

You mentioned something about an "RPG update" — I'm not sure what you mean by that. Your progress file looks exactly as expected. Everything is in order.

Now, let's get into today's session.

---

### Step A — Review

You have **5 unresolved mistakes** in your Mistake Registry. Before we start new content, I need to check on those.

Looking at your Topic Mastery, **Database** and **Queue** are both at 🟡 (Developing). Let me test whether you've solidified those since our last sessions.

1. **Message Queue check:** Last time we covered delivery semantics. Can you explain the difference between at-least-once and exactly-once delivery in your own words? And why is "exactly-once" considered misleading in distributed systems?

2. I also want to revisit your unresolved mistakes from previous sessions. Let me go through them one by one — for each one, try to explain it back to me. If you've got it now, we mark it ✅ Resolved. If not, we drill it.

Let's also check: your session count minus your last weekly review — are we due for a Weekly Review? (I'll check the numbers in your progress file.) If `session_count - last_weekly_review >= 7`, we'll do a Weekly Review instead of the normal session today.

**Assuming no Weekly Review is due**, today is **Day 12: API Design — API Styles**.

---

### Step B — Introduction (if proceeding to Day 12)

Today we're covering **API Design**, specifically the different styles: REST, gRPC, and GraphQL.

Think of it this way: imagine you're at a restaurant. REST is like ordering from a fixed menu — each dish is a specific URL endpoint, and you get exactly what's listed. GraphQL is like a buffet where you tell the chef exactly which items you want on your plate — no more, no less. gRPC is like a kitchen-to-kitchen intercom in a large restaurant chain — fast, efficient, but requires both sides to speak the same protocol.

Each has trade-offs. By the end of today, you'll know when to pick which one in an interview and why.

---

### Step C — Core Teaching (Chunk Map)

Here are today's core chunks:

```
☐ 1. REST — resource-oriented, HTTP verbs, stateless
☐ 2. gRPC — protobuf, HTTP/2, streaming, when to use
☐ 3. GraphQL — query language, over/under-fetching, when to use
☐ 4. Trade-off matrix: REST vs gRPC vs GraphQL
☐ 5. Pagination: Offset vs Cursor — trade-offs
☐ 6. API Versioning strategies (URL, header, query param)
☐ 7. Idempotency — why it matters, idempotency keys
☐ 8. Observability Mini — SLIs, SLO targets, Alerts, Dashboards for APIs
```

We'll go through each chunk one at a time. After each one, I'll ask you to explain it back (Feynman Gate). Ready?

Let's start with **Chunk 1: REST**.

---

*[Session continues with the standard A→H teaching flow as defined in the skill]*

---

## Analysis: What the Main Branch Skill Does NOT Do

1. **No mention of RPG features** — the skill has no concept of RPG Profile, Achievements, XP, levels, or any gamification.
2. **No migration logic** — there is nothing to migrate. The student's progress.md already conforms to the expected template.
3. **No special handling for "old" formats** — the skill reads whatever sections exist in progress.md and uses them. If a section is missing, it would create it using the template. But in this case, all expected sections are present.
4. **Acknowledges confusion, moves on** — the coach briefly notes it doesn't understand the "RPG update" reference, confirms the progress file is fine, and proceeds with the session.

The main branch skill treats this as a straightforward **returning student** scenario (Quick Start routing case #3: "Progress file, no breakpoint → Returning student").
