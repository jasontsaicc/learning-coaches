# Phase 4 — Trap Scenarios & Pivot Drills

> Reference material for Phase 4 sessions (Day 54-61).
> These are examples and patterns, not scripts. AI should adapt, remix, and create new traps based on the student's weakness profile from `progress.md`.

---

## Trap Scenarios

A trap is a design prompt that looks simple but contains a hidden assumption or constraint that invalidates the obvious approach. The student must recognize the trap and pivot gracefully.

### Pattern: The Hidden Write-Heavy System

**Setup:** "Design a simple read-heavy leaderboard for a mobile game."
**Trap:** The game has 50M DAU and scores update every match (~10 matches/day per user). That's 500M writes/day. It's actually write-heavy.
**What to watch:** Does the student ask about write frequency, or assume read-heavy and jump to caching?

### Pattern: The Scale Cliff

**Setup:** "Design a notification system for a B2B SaaS with 10K companies."
**Trap:** One enterprise customer has 500K employees. Fan-out to that single tenant dwarfs all others combined.
**What to watch:** Does the student handle the tenant-size skew, or design for uniform distribution?

### Pattern: The Consistency Trap

**Setup:** "Design a collaborative document editor. Users need to see each other's changes in real-time."
**Trap:** "Real-time" + "consistent" at global scale is extremely expensive. The student needs to recognize CRDT or OT, not just "use WebSocket."
**What to watch:** Does the student identify the conflict resolution problem, or stop at the transport layer?

### Pattern: The Cost Bomb

**Setup:** "Design a video transcoding pipeline. Budget is not a concern."
**Trap:** Budget is always a concern. If the student doesn't bring up cost estimation, the interviewer reveals: "Actually, we process 1M videos/day at 4K. What does that cost?" Estimated: ~$50K/day in compute alone.
**What to watch:** Does the student volunteer cost analysis, or only think about architecture?

### Pattern: The Requirement Flip

**Setup:** "Design a URL shortener." (Student starts designing.)
**Mid-interview pivot:** "Actually, we also need analytics — click counts by country, device, and time window, queryable in real-time."
**What to watch:** Can the student integrate analytics into their existing design without starting over? Do they identify that this changes the system from simple CRUD to an analytics pipeline?

---

## Pivot Drills

A pivot drill trains the student to gracefully change direction when the interviewer redirects. The core skill: acknowledge the pivot, adjust the design, explain what changes and what stays.

### Drill Format

1. Student starts a design (5 min to get to high-level architecture)
2. Interviewer drops a constraint change or new requirement
3. Student must: (a) acknowledge, (b) identify what in the current design breaks, (c) propose the adjustment, (d) explain trade-offs of the pivot

### Example Pivots

| Original Design | Pivot | What Changes |
|----------------|-------|-------------|
| Chat system with single-region DB | "We're expanding to Asia-Pacific" | Replication strategy, consistency model, message routing |
| Rate limiter using Redis | "Redis is down. What's your fallback?" | Local in-memory rate limiting, degraded mode, eventual sync |
| News feed with fan-out-on-write | "We just signed a celebrity with 50M followers" | Hybrid fan-out, celebrity exception path |
| Payment system with sync processing | "Merchants complain about 5s latency" | Async processing with webhooks, optimistic UI |
| Search with Elasticsearch | "Search index is 2 hours stale" | Near-real-time indexing, change data capture, cache invalidation |

### Double Pivot (Day 61 — Brutal Mode)

Chain two pivots in sequence without letting the student fully stabilize:
1. Start: "Design a ticket booking system"
2. Pivot 1: "We need to handle 100K concurrent users during a flash sale" (→ queue + rate limiting)
3. Pivot 2: "The payment provider has a 30-second timeout during flash sales" (→ reservation pattern, idempotency under timeout)

The student must maintain composure and build incrementally rather than restarting.

---

## Interviewer Behavior in Phase 4

In Phase 4, 小球 shifts from teacher to tough interviewer:
- **No hints.** If the student is stuck, wait silently for 30 seconds before offering a nudge.
- **Redirect aggressively.** If the student spends too long on one component, say "Let's move on to X."
- **Challenge weak points.** Read the student's Mistake Registry — ask about their historically weak areas.
- **Time pressure.** Enforce the 45-minute limit strictly. Announce "You have 10 minutes left" at the 35-minute mark.

But after the drill, 小球 returns to mentor mode for detailed feedback.
