# Notes Template

Use this template for every session's notes. Save as `notes/dayXX-topic.md`.

---

## Basic Elements (All Phases)

| Element | Format | Example |
|---------|--------|---------|
| **One-liner** | "X is a system that..." | "A URL shortener maps long URLs to short codes for sharing" |
| **Trade-off** | "We chose X over Y because..." | "We chose base62 over MD5 because we need shorter URLs and can handle collisions" |
| **Scale trigger** | "At N scale, we need..." | "At 10K writes/sec, we need database sharding" |
| **DevOps angle** | "In production, I'd monitor..." | "I'd set up alarms on 4xx/5xx rates and P99 latency" |

## Advanced Elements (Phase 1+ PoC Topics)

- **Capacity & cost estimation**:
  - Traffic assumptions: DAU, peak QPS, payload size
  - Storage growth: Daily new data (GB), yearly total (TB)
  - Cost top 2: Compute vs storage vs data transfer — who's biggest, why, how to cut 30%

## Full Elements (Phase 3+)

- **Failure modes** (address at least 3):
  - Dependency down, latency spike, partial outage
  - Message duplication, data corruption, thundering herd

- **Abuse & security** (list at least 3 attack vectors + countermeasures):
  - Credential stuffing, replay attack, spam/bot abuse
  - Data exfiltration, DDoS/resource exhaustion

## Required Every Session

```markdown
## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| (original wrong understanding) | (correct understanding) | (why the misconception happened) |
```

Rules:
- Record every wrong answer, misconception, or confusion point from the session
- "What I Thought" must contain the actual wrong understanding, not be blank
- If genuinely no mistakes → write "No mistakes this session" (this should be rare)
- This section is the priority target for review sessions

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
