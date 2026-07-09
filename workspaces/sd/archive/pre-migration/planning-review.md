# SD Curriculum Planning Review Notes

> Date: 2026-02-10 (original), 2026-02-11 (v2 adjustments)
> Reviewer: Senior DevOps perspective
> Status: Review complete, v4 adjustments applied (9 + 2 + 3 issues fixed)

---

## Review Summary

### Overall Score: 9/10

Original curriculum was well-structured with solid foundations. V1-V4 fixed content completeness; V5 fixed internal consistency. Key improvements made:

---

## Changes Made

### 1. Phase -1 Go Refresher — Timeline Fix

| Before | After | Why |
|--------|-------|-----|
| Day 0.1-0.5 (half-day) | Day -5 to Day -1 (5 days) | Concurrency + HTTP Server alone need 2-3 hours each |

- Go refresher is now a **prep week** before the 60-day main schedule
- Each topic gets a full day (1 hour focused learning)

### 2. Phase 2 — Added Missing Distributed Concepts

| Added | Why |
|-------|-----|
| **Bloom Filter** | Used in Web Crawler (URL dedup), cache, spell checker |
| **Gossip Protocol** | How Cassandra/DynamoDB detect failures and share state |
| **Distributed Transactions overview** | Foundation for Payment System (SAGA, 2PC) |

- Observability compressed from 2 days → 1 day (DevOps background = already know this)
- Freed 1 day for advanced distributed concepts

### 3. Phase 2 — Rate Limiter Scope Clarification

| Phase | Scope | Focus |
|-------|-------|-------|
| Phase 2 (Day 23-24) | **Algorithms** (local, single-node) | Token Bucket, Sliding Window implementation |
| Phase 3 (Day 31-32) | **System Design** (distributed, multi-node) | Redis-backed service, race conditions, Lua scripts |

### 4. Phase 3 — Tier System

#### Tier 1: Must Do (8 problems, 19 days)

```
Concept Coverage Matrix:

Concept / Topic →      URL  ID  Rate Noti Chat Feed Cache Pay
──────────────────────────────────────────────────────────────
Hashing/Encoding        ●        ●                    ●
Database Sharding       ●   ●                  ●            ●
Caching                 ●                      ●      ●
Message Queue                         ●        ●  ●        ●
WebSocket/Real-time                        ●
Fan-out Strategies                             ●  ●
Consistent Hashing                                    ●
Idempotency                  ●   ●                          ●
Distributed Locking              ●                          ●
Async Processing                      ●        ●           ●
Rate Limiting                    ●   ●
Ranking/Sorting                           ●    ●
```

Key insight: 8 problems cover 90% of SD concepts. Each concept hit by 2-3 problems = reinforcement.

#### Tier 2: Should Do (4 problems, 8 days)

- Metrics & Logging — **DevOps advantage topic** (strongest scoring opportunity)
- Search Autocomplete — Google favorite
- Web Crawler — Google classic (uses Bloom Filter from Day 26)
- Proximity Service — Uber/Maps type interviews

#### Tier 3: Deprioritized

| Dropped | Reason | Concepts Covered By |
|---------|--------|-------------------|
| Video Streaming | Domain-specific | CDN (caching) + async (notification) |
| Cloud Storage | Domain-specific | Consistency (distributed cache) + dedup (crawler) |
| Task Scheduler | Overlap | Notification (queue) + Payment (locking) |
| Ticket/Booking | Overlap | Payment (idempotency) + Rate Limiter (counting) |

### 5. New Topics Added

| Topic | Why Added | Interview Frequency |
|-------|-----------|-------------------|
| **Unique ID Generator** | Sub-problem in EVERY other design (Snowflake) | Very High |
| **Web Crawler** | Google classic, uses Bloom Filter | High |
| **Proximity Service** | Uber/Maps interviews, Geohash/QuadTree | High |

### 6. Checkpoint Mocks Added

| When | Format | Purpose |
|------|--------|---------|
| Day 16 (after Phase 1) | 15-min mini-mock | Test building block articulation |
| Day 26 (after Phase 2) | 30-min mid-mock | Test complete system design |
| Phase 4 (Day 56-61) | Full 45-min mocks | Interview simulation |

### 7. Interview Language Template

Every notes file should now include:

| Element | Format |
|---------|--------|
| **One-liner** | "X is a system that..." |
| **Trade-off** | "We chose X over Y because..." |
| **Scale trigger** | "At N scale, we need..." |
| **DevOps angle** | "In production, I'd monitor..." |
| **Capacity** | "We expect N DAU, N QPS, N GB/day..." |
| **Security** | "Main abuse vector is X; countermeasure is Y" |

### 8. DevOps Differentiator Strategy

Key topics where DevOps background = competitive advantage:

| Topic | DevOps Angle |
|-------|-------------|
| Load Balancer | ALB/NLB real-world, target group health checks |
| Caching | ElastiCache operational concerns |
| Message Queue | SQS FIFO vs Standard, DLQ in CloudWatch |
| Observability | Prometheus/Grafana/ELK, SLO-based alerting |
| Distributed Cache | ElastiCache cluster ops, failover |
| Metrics & Logging | **YOUR TERRITORY** — real production experience |
| Any system | Multi-AZ, DR, blue-green deployment |

---

## Final Day Count

```
Phase -1: 5 days (prep week, separate from 61-day count)
Phase 0:  3 days  (Day 1-3)
Phase 1:  13 days (Day 4-16)  — +1 day for Security & Auth
Phase 2:  10 days (Day 17-26)
Phase 3:  27 days (Day 27-53) — Tier 1: 19 days + Tier 2: 8 days
Phase 4:  8 days  (Day 54-61)
─────────────────────────────────────
Total:    61 days + 5 prep days
```

---

## V2 Adjustments (2026-02-11)

### Issues Found & Fixed

| # | Issue | Fix | Impact |
|---|-------|-----|--------|
| 1 | CDN had no dedicated section | Expanded Caching → "Caching & CDN Strategies" with CDN deep dive | No extra days |
| 2 | Security/Auth missing entirely | Added Day 14: Security & Authentication Patterns | **+1 day** |
| 3 | Tier 1 difficulty too steep (Chat→News Feed back-to-back ★★★★) | Reordered: Chat → **Dist Cache** (breather) → News Feed → Payment | No extra days |
| 4 | Dependency Map: BF→PAY was wrong | Fixed to DT (Distributed Transactions) → PAY | No extra days |
| 5 | DNS not mentioned anywhere | Added DNS fundamentals to Load Balancer (Day 4-5) | No extra days |
| 6 | No diagramming guidance | Added to Phase 0 Day 3 + Daily Routine (5 min practice) | No extra days |
| 7 | SSE not mentioned as WebSocket alternative | Added WebSocket vs SSE vs Long Polling comparison to Chat System | No extra days |
| 8 | DB missing pooling/WAL/replicas | Added connection pooling, WAL, read replicas to Day 8-9 | No extra days |
| 9 | Go context.Context not covered | Added to Phase -1 Day -2 HTTP Server | No extra days |

### Net Impact

- Total days: 60 → **61** (+1 for Security & Auth)
- Prep days: 5 (unchanged)
- Tier 1 reordered for better difficulty pacing
- Additional enrichments (not numbered): Observability Mini for all Phase 1 topics, PoC Production Hooks, Data Model Design Template, Distributed Systems Kill Pack, ID Generator clock challenges, Rate Limiter multi-tenant design, Search Autocomplete extended pipeline, Trade-off specific scenarios, Mock interview recording + self-review, Voice drill in Daily Routine, Capacity + Security in Interview Language Template

---

## V3 Adjustments (2026-02-11)

| # | Issue | Fix | Impact |
|---|-------|-----|--------|
| 1 | 無複習機制，後期易遺忘早期內容 | 加入 Weekly Review（每週六 30 min） | 每週 +30 min |
| 2 | Dependency Map SEC 無 outgoing edge | 加 SEC→CHAT, SEC→PAY | 純圖表修正 |

---

## V4 Adjustments (2026-02-11)

| # | Issue | Fix | Impact |
|---|-------|-----|--------|
| 1 | 缺乏「設計陷阱 → 優雅轉彎」練習 | Phase 4 加入 Trap & Pivot Drills（Day 54-55 + Mock 場景） | 無額外天數 |
| 2 | Weekly Review 偏被動（翻閱 notes） | 升級為 Active Recall 三步驟（Blind Recall → Gap Check → Quick Drill） | 同樣 30 min |
| 3 | AI 教學無標準流程，筆記不記錄錯誤 | 新建 `SD/CLAUDE.md`：7 步驟教學流程 + Mistakes section + 進度更新規範 | 每次教學自動遵守 |

---

## V5 Adjustments (2026-02-11) — 整體一致性修復

> V1-V4 每輪迭代新增功能（Weekly Review、Notes Template、Teaching Flow、Simon Drill）之間沒有對齊。
> V5 聚焦於讓整個系統**自洽**，不增加天數或時間。

| # | Issue | Fix | Impact |
|---|-------|-----|--------|
| 1 | Daily Routine vs Teaching Flow 時間不對齊（複習 10 min vs 2-3 min，Simon Drill 缺席） | CLAUDE.md 重寫 A-H 時間預算（5+3+12+20+5+10~15+5+5=65-70 min），CURRICULUM.md Daily Routine 同步對齊 | 時間加總一致 |
| 2 | Notes Template 放在 Phase 3 裡面，但所有 Phase 都要用；Interview Language Template 重疊 | Notes Template 移到 Phase 3 之前，分三層（基礎/進階/完整）；Interview Language Template 合併進去 | Single source of truth |
| 3 | Weekly Review 6/6 計分在 Phase 0-2 不成立（Security/Capacity 還沒學） | 改為 phase-aware 計分表（Phase 0: 2/2, Phase 1: 4/4, Phase 2: 5/5, Phase 3+: 6/6） | 消除假警報 |
| 4 | 進度追蹤有三個地方（頂部表格 + checkbox + roadmap）遲早脫 sync | 刪除 CURRICULUM.md 頂部 Progress Tracker 表格，保留 checkbox + roadmap 兩處 | 簡化為兩層 |
| 5 | CLAUDE.md 沒有 Weekly Review 流程，AI 不知道週六怎麼進行 | 新增 Weekly Review Flow section（挑題 → Blind Recall → 計分 → Gap Check → Quick Drill） | AI 有章可循 |
| 6 | planning-review.md 分數停在 8/10 | 更新為 9/10 + 新增 V5 section | 紀錄完整 |

### Design Principles
- **不增加天數或時間** — 純結構對齊
- **Single source of truth** — 每個概念只定義在一個地方
- **Progressive complexity** — Template 和計分隨 Phase 成長

---

## Next Steps

- [ ] Start Phase -1 Go Refresher
- [ ] Set up `projects/` and `notes/` directory structure
- [ ] Begin Day -5: Go Fundamentals
