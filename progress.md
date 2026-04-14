# Student Progress Tracking

> This file is the single source of truth for student progress.
> Updated by Claude at the end of every session (Step H) and when sessions are interrupted.
> Read by Claude at the start of every session to determine where to resume.

---

## Student Info

| Field | Value |
|-------|-------|
| **Start date** | 2026-03-04 |
| **Current phase** | Phase 1 |
| **Current day** | Day 12 |
| **Language mode** | Bilingual (繁中 + English) |
| **Session count** | 18 |
| **Last weekly review** | 10 |

---

## Current Session (Breakpoint)

| Field | Value |
|-------|-------|
| **Day** | Weekly Review #2 (Session 18) |
| **Step** | Blind Recall complete, Gap Check next |
| **Position** | Round 1 API Design: 2/4 (One-liner ✅, Trade-off ✅, Scale trigger ❌, DevOps ❌). Round 2 Caching: 4/4 (all ✅, huge improvement from 0/4). Round 3 MQ: 2/4 (One-liner ✅, Trade-off ✅, Scale trigger ❌, DevOps ❌). Parked: MQ long polling question. |
| **Topics** | 1. API Design (2/4) 2. Caching & CDN (4/4) 3. Message Queue (2/4) |
| **Remaining** | Gap Check → Mistake Registry Review → Quick Drill → Update progress |

---

## Topic Mastery

| Day | Topic | Mastery | Phase Gate | Notes |
|-----|-------|---------|------------|-------|
| -5 to -1 | Go Refresher | 🟢 | — | 5 days complete |
| 1 | SD Interview Rubric | 🟢 | — | |
| 2 | Back-of-Envelope Estimation | 🟢 | — | |
| 3 | 4-Step Framework | 🟢 | Phase 0 Gate | |
| 4-5 | Load Balancer | 🟡 | — | Weekly Review 1/4 recall. 5 unresolved mistakes. Downgraded from 🟢. |
| 6-7 | Caching & CDN | 🔴 | — | Weekly Review 0/4 recall. Drill partial recovery. Downgraded from 🟢. |
| 8-9 | Database Selection | 🟡 | — | Weekly Review 3/4 recall. B-tree/LSM resolved. Trade-off axis confusion persists. |
| 10-11 | Message Queue | 🟡 | — | Concepts understood with guidance. Interview Drill 3/3 but needed help with requirements framework, inventory placement, idempotency architecture. |
| 12-13 | API Design | 🟡 | — | Chunks all passed. Interview Drill 3/3. But many endpoint design mistakes (singular nouns, path params, security), pagination naming confusion, HTTP body basics gap. |
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

---

## Interview Drill Scorecard History

| Session | Day | Topic | Score | Details |
|---------|-----|-------|-------|---------|
| 8 | 8-9 | Database Selection | 2/3 | ❌ Scope Negotiation, initially chose NoSQL based on data volume (wrong reasoning) |
| 10 | WR1 | Weekly Review (DB/LB/Cache) | DB 3/4, LB 1/4, Cache 0/4 | First weekly review. LB 🟢→🟡, Cache 🟢→🔴. 2 mistakes resolved (DNS limits, LSM-tree). |
| 13 | 10 | Message Queue (Interview Drill) | 3/3 | ✅ Think Aloud, ✅ Scope Negotiation, ✅ Used MQ. Needed guidance on requirements framework and idempotency placement. |
| 17 | 12 | API Design (Interview Drill) | 3/3 | ✅ Think Aloud, ✅ Scope Negotiation, ✅ Used API Design. Fixed endpoint mistakes mid-drill. Strong idempotency deep dive. |

---

## 🔴 Mistake Registry

| Session | Day | Topic | Mistake | Status |
|---------|-----|-------|---------|--------|
| 4 | 4-5 | Load Balancer | Said "least robin" — confused RR and Least Connections names | ❌ Unresolved |
| 4 | 4-5 | Load Balancer | Thought Weighted RR is for different request processing times (it's for different server specs) | ❌ Unresolved |
| 4 | 4-5 | Load Balancer | Couldn't recall LB algorithm names during Simon Drill | ❌ Unresolved |
| 4 | 4-5 | Load Balancer | Forgot DNS-based LB limitations (TTL stale IP, no real-time health check) | ✅ Resolved (WR1) |
| 4 | 4-5 | Load Balancer | Thought 8.8.8.8 is ISP DNS (it's Google Public DNS) | ❌ Unresolved |
| 4 | 4-5 | Load Balancer | Confused sticky sessions and Redis external store as same approach (opposite strategies) | ❌ Unresolved |
| 4 | 4-5 | Load Balancer | Missed sticky session risk: uneven load distribution | ❌ Unresolved |
| 9 | 8-9 | Database Selection | LSM-tree 讀寫搞反（以為是 read-optimized） | ✅ Resolved (WR1) |
| 9 | 8-9 | Database Selection | Denormalization 跟 Normalization 搞混 | ✅ Resolved (S11) |
| 9 | 8-9 | Database Selection | Consistency Trade-offs 空白（不知道三種 model） | ❌ Unresolved |
| 9 | 8-9 | Database Selection | 看到「大量資料」就選 NoSQL（data volume ≠ DB 選擇關鍵） | ✅ Resolved (S11) |
| 9 | 8-9 | Database Selection | Interview Drill 忘了 Scope Negotiation | ❌ Unresolved |
| 12 | 10 | Message Queue | Simon Drill: Why Async 只記得 fast response，漏 decoupling/buffering | ❌ Unresolved |
| 12 | 10 | Message Queue | Simon Drill: delivery semantics 名稱講不完整 (most/least/excely) | ❌ Unresolved |
| 12 | 10 | Message Queue | 設計練習不知道怎麼起手（需要拆成小問題逐步推） | ❌ Unresolved |
| 13 | 10 | Message Queue | 忘了 Functional / Non-Functional / Scope 的定義（Step 1 基礎） | ❌ Unresolved |
| 13 | 10 | Message Queue | Inventory check 放 Queue 之後（沒考慮 user 等半天才知道沒貨的體驗） | ✅ Resolved (S14) |
| 13 | 10 | Message Queue | 把 Idempotency 當獨立 service（其實是 Order Service 裡的邏輯） | ❌ Unresolved |
| 13 | 10 | Message Queue | 把 Redis DECR（庫存 pre-check）跟 Idempotency check（防重複）搞混 | ❌ Unresolved |
| 13 | 10 | Message Queue | 說 at-least-once 是解決重複扣款的方法（at-least-once 是問題來源，idempotency 才是解法） | ✅ Resolved (S14) |
| 15 | 12 | API Design | gRPC recall 只說 "for service to service"，說不出 WHY（binary fast + strict contract） | ✅ Resolved (WR2) |
| 15 | 12 | API Design | GraphQL transfer 只說「可以用」沒解釋 HOW（client 寫 query 選 fields，burden 從 backend 移到 client） | ❌ Unresolved |
| 16 | 12 | API Design | Simon Drill: Pagination 完全忘記（Offset vs Cursor） | ❌ Unresolved |
| 16 | 12 | API Design | Versioning 說「修改不需要新版本」，但 rename field 是 breaking change | ❌ Unresolved |
| 16 | 12 | API Design | Observability: 又把 SLI/SLO/Dashboard 當成 metrics（正確是 Latency, Error rate, Throughput） | ❌ Unresolved |
| 16 | 12 | API Design | Interview Drill: REST endpoint 寫 `/v1/get/restaurants`，verb 塞進 URL（正確：`GET /v1/restaurants`） | ✅ Resolved (S17) |
| 17 | 12 | API Design | 不知道 GET data 放 URL (query string)、POST data 放 request body | ❌ Unresolved |
| 17 | 12 | API Design | REST path 用 singular noun + path param 寫成字面文字 | ✅ Resolved (S17, 當場修正) |
| 17 | 12 | API Design | Price/user_id 放 request body（沒想過 client 可以竄改） | ❌ Unresolved |
| 17 | 12 | API Design | Pagination 說成 "offline"（正確: offset），cursor 也靠提示才想起 | ❌ Unresolved |
| 17 | 12 | API Design | Idempotency record 只想到 exists/not exists，沒想到需要 processing 中間狀態 | ❌ Unresolved |

---

## 🎯 One-Liner Library (Interview Quick-Answer Bank)

| Topic | One-Liner |
|-------|-----------|
| Load Balancer | A Load Balancer distributes traffic across multiple backend servers to achieve high availability, horizontal scalability, and zero-downtime deployments. |
| Caching & CDN | Cache puts frequently-used data in a faster store like Redis in front of the DB, reducing latency and DB load by serving most requests without hitting the database. |
| Database Selection | Database selection is choosing the right storage engine — SQL, NoSQL, or NewSQL — based on access patterns, relationship complexity, and consistency requirements, so the database fits the workload rather than forcing the workload to fit the database. |
| Message Queue | A Message Queue decouples producers from consumers, enabling async processing, peak traffic buffering, and failure resilience through retry and dead letter queues — the key is pairing at-least-once delivery with idempotency to prevent duplicate processing. |
| API Design | API Design is about choosing the right style (REST, GraphQL, gRPC) based on who's calling, call frequency, and data complexity — the key trade-off is flexibility versus simplicity and cacheability. |

---

## RPG Profile

| Field | Value |
|-------|-------|
| **Title** | ⚙️ Systems Engineer |
| **Current streak** | 2 🔥 |
| **Longest streak** | 4 |
| **Last session date** | 2026-04-14 |
| **Last story summary** | API Design Interview Drill 完成 (3/3)。Food delivery API: 學會 REST endpoint 設計 (plural nouns, path params, resource nesting)、API security (不信任 client input)、cursor pagination 應用、idempotency crash recovery (中間狀態)。 |

---

## Achievements

| ID | Name | Status | Date |
|----|------|--------|------|
| M1 | First Steps | 🏆 | retroactive |
| M2 | Framework Forged | 🏆 | retroactive |
| C1 | First Blood | 🏆 | retroactive |
| C4 | Comeback Kid | 🏆 | retroactive |
| S2 | Weekly Warrior | 🏆 | retroactive |
| E1 | Perfect Drill | 🏆 | 2026-04-02 |
| S1 | Three-peat | 🏆 | 2026-04-02 |
| K4 | Bug Squasher ×5 | 🏆 | 2026-04-10 |

**Total: 8/25**

---

## Curiosity Branches

| Topic | Question | Status |
|-------|----------|--------|
| Message Queue | Long polling in MQ (長輪詢) | ⏸ Parked (likely relevant at Day 33-34 Notification System) |

---

## Phase Gate Results

| Phase | Date | Score | Result | Weak spots |
|-------|------|-------|--------|------------|
| Phase 0 | — | — | ✅ Pass (retroactive — completed Day 1-3) | |
