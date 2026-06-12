# Achievement System

<!-- FRAMEWORK: Reusable — achievement system pattern -->

> Read by AI at Step H (session end) and when student asks about achievements.
> Every achievement rewards UNDERSTANDING, not speed.

---

## Design Principle

Achievements must reward behaviors that align with genuine learning:
- Persistence over perfection
- Understanding over memorization
- Teaching over reciting
- Consistency over intensity

---

## Achievement Definitions

### 🎯 MILESTONES (6) — Progress-based

| ID | Name | Unlock Condition | Description |
|----|------|-----------------|-------------|
| M1 | First Steps | Complete Day 1 | 你踏出了第一步 |
| M2 | Framework Forged | Pass Phase 0 Gate | 你有了思考的框架 |
| M3 | Builder's Foundation | Pass Phase 1 Gate | 基礎建設完成 |
| M4 | Distributed Mind | Pass Phase 2 Gate | 分散式思維覺醒 |
| M5 | System Architect | Pass Phase 3 Gate | 你能設計完整系統了 |
| M6 | Ready for Anything | Pass Phase 4 Gate | 準備好面對任何挑戰 |

### ⚔️ MASTERY (5) — Understanding-based

| ID | Name | Unlock Condition | Description |
|----|------|-----------------|-------------|
| C1 | First Blood | Pass first Feynman Gate (both Recall + Transfer) | 第一次用自己的話解釋成功 |
| C2 | Flawless Session | All chunks in a session pass Feynman Gate on first attempt | 全部一次過 |
| C3 | Gate Crasher | Pass a Phase Gate on first attempt (attempt 1) | Phase Gate 一次過 |
| C4 | Comeback Kid | Resolve a 🔴 ❌ Unresolved mistake from Mistake Registry | 克服了卡住的地方 |
| C5 | Myth Buster | Student brings back a finding from cross-verification (Step G) that differs from what was taught | 你比教材更敏銳 |

### 📚 COLLECTION (4) — Knowledge accumulation

| ID | Name | Unlock Condition | Description |
|----|------|-----------------|-------------|
| K1 | One-Liner ×10 | One-Liner Library in progress.md reaches 10 entries | 面試快答庫初具規模 |
| K2 | One-Liner ×30 | One-Liner Library reaches 30 entries | 面試快答庫豐富了 |
| K3 | Encyclopedia | One-Liner Library reaches 61 entries (complete) | 完整的面試百科 |
| K4 | Bug Squasher ×5 | 5 mistakes resolved (❌→✅) in Mistake Registry | 錯誤是最好的老師 |

### 🔥 CONSISTENCY (4) — Habit building

| ID | Name | Unlock Condition | Description |
|----|------|-----------------|-------------|
| S1 | Three-peat | 3 consecutive days with sessions (day-based, not session-based) | 連續三天學習 |
| S2 | Weekly Warrior | Complete one Weekly Review | 完成週常回顧 |
| S3 | Streak: 7 | 7 consecutive days with sessions | 一週不中斷！ |
| S4 | Iron Will | Complete a session where Feynman Gate failed ≥ 3 times on any chunk | 撐過最難的時刻 |

### 🌟 EXCELLENCE (3) — Depth

| ID | Name | Unlock Condition | Description |
|----|------|-----------------|-------------|
| E1 | Perfect Drill | Score 100% on any Interview Drill (3/3, 5/5, or 7/7 depending on phase) | 面試模擬滿分 |
| E2 | Deep Diver | Complete a Full PoC (Go + Docker Compose) | 真正動手寫了完整的 PoC |
| E3 | The Mentor | Phase 2+: Student correctly answers a question Yuki asked | 教會別人才是真的懂 |

### 🎭 STORY (3) — Narrative

| ID | Name | Unlock Condition | Description |
|----|------|-----------------|-------------|
| R1 | 小杰's Nightmare | In a story context, student identifies and explains why 小杰's shortcut approach is wrong | 修好小杰闖的禍 |
| R2 | Karen's Hero | Complete a Phase 3 SD problem design (= delivered the feature Karen requested) | 達成 Karen 的需求 |
| R3 | 小球's Pride | Phase 3+: Student makes an independent design decision without 小球's prompting (小球 steps back and lets student lead) | 小球認可你了 |

---

## Display Rules

### On Unlock (during session)

```
🏆 Achievement Unlocked: [Name]
   「[Description]」
```

AI may add 1 line of personalized encouragement related to what the student did.
小球 may react in character if the moment fits naturally.

### In RPG Dashboard

```
🏆 Achievements: X/25
  Latest: [most recent unlock]
  Next closest: [closest to unlocking + progress indicator]
```

### Multiple Unlocks in Same Session

Show each one sequentially. Don't batch them into a single message.
Order: Milestones first, then Mastery, then others.

---

## Checking Logic (for AI at Step H)

At the end of each session, check these conditions against progress.md:

1. **Milestones (M1-M6):** Did a Phase Gate pass this session? Did Day 1 complete?
2. **Mastery (C1-C5):** Track Feynman Gate results during session. C5 requires student to have brought something from cross-verification.
3. **Collection (K1-K4):** Count One-Liner Library and Mistake Registry ✅ entries.
4. **Consistency (S1-S4):** Check streak value. S4 requires session-level Feynman failure tracking.
5. **Excellence (E1-E3):** Check scorecard result, PoC tier completed, Yuki interaction result.
6. **Story (R1-R3):** R1 triggered by story interaction. R2 triggered by Phase 3 problem completion. R3 triggered when student independently leads a design decision in Phase 3+ without needing 小球's guidance.

Only check achievements that are still 🔒. Skip already unlocked ones.
