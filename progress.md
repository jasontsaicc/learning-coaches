# Student Progress Tracking

> This file is the single source of truth for student progress.
> Updated by Claude at the end of every session (Step H) and when sessions are interrupted.
> Read by Claude at the start of every session to determine where to resume.

---

## Student Info

| Field | Value |
|-------|-------|
| **Start date** | 2026-03-04 |
| **Current phase** | Phase 2 🌐 |
| **Current day** | Day 23-24 done (S28) → next: Day 25 Observability |
| **Language mode** | Bilingual — S27 切回繁中為主（學生英文閱讀疲勞），術語保留英文 |
| **Session count** | 28 |
| **Last weekly review** | 25 |

---

## 🎚️ Learning Mode (Active — set Session 23)

**Mode: 問題錨定 + 深度天花板 (Problem-anchored + Depth Ceiling)**

Reason: 學生在純理論主題(consistency models、consistent hashing 的 vnodes 數學)磨太久,
公式/形式化的深度對面試零回報,導致進度緩慢 + 學習痛苦。

Rules going forward:
1. **深度天花板三問** — 碰到一個主題往下鑽時問:(a) 面試官會問嗎? (b) 這層深度能讓我的回答更好嗎? (c) 我卡住是缺地基還是想完美? 任一題答「不會/不能/想完美」→ park 到 Curiosity Branches,繼續走。
2. **壓縮理論期** — Day 15-22 building block 改「概念 + 一句話 + 一個 trade-off」快速模式,PoC 降級為 Light/Discussion,不追完整 Full PoC。
3. **題目驅動 (pull)** — 用 **Design a Distributed Cache** 當錨,把 CAP(Day 17-18)、Consistency Models(Day 19-20)、Replication & Leader Election(Day 21-22)折進這個設計題,理論在設計需要時才 just-in-time 拉進來,capped 在面試深度。
4. 面試考的是 breadth of mental models + trade-off reasoning,**不是** CS 理論深度(linearizability 形式證明、consistency 數學模型 = PhD 範圍,不學)。

---

## Current Session (Breakpoint)

✅ **無中斷 — Session 28 (Day 23-24 Rate Limiting & Circuit Breaker) 正常完成全流程 A→H。**

**Pending PoC(park):** Circuit Breaker PoC + 分散式 Redis rate limiter → Day 31-32 Distributed Rate Limiter。Replication lag + Consistent hashing 獨立 PoC + distributed cache 完整實作 → Day 38-39。

**Pending review(下次帶到):** Consistency Models（Box 1, 6/4 到期）S28 Step A recall **沒完全過** — 光譜答成 CAP（已劃界線：光譜=latency 預算 vs CAP=partition 二選一）+ W+R>N 缺「重疊/鴿籠」關鍵字（已補）。**留 Box 1，下次快速複習鞏固**。

**Phase 2 進度:** [21-22]✅ [23-24]✅ 剩 [25] Observability、[26] Bloom/Gossip → **Phase 2 Gate（設計分散式 KV store, ≥3/5）**。

---

## Topic Mastery

| Day | Topic | Mastery | Phase Gate | Notes |
|-----|-------|---------|------------|-------|
| -5 to -1 | Go Refresher | 🟢 | — | 5 days complete |
| 1 | SD Interview Rubric | 🟢 | — | |
| 2 | Back-of-Envelope Estimation | 🟢 | — | |
| 3 | 4-Step Framework | 🟢 | Phase 0 Gate | |
| 4-5 | Load Balancer | 🟢 | — | WR3 (S25) recall 4/5 大回血。Weighted RR 老錯 resolved，補回 RR + Least Connections 基礎，L4/L7 最強。Upgraded 🟡→🟢. |
| 6-7 | Caching & CDN | 🟡 | — | WR3 (S25) recall 3.5/5 大躍進 (WR1 是 0/4)。核心穩,補上 cache invalidation 主動同步 (寫時刪 cache 而非更新)。Scale trigger 補強 (read-heavy+熱點)。Upgraded 🔴→🟡. |
| 8-9 | Database Selection | 🟡 | — | Weekly Review 3/4 recall. B-tree/LSM resolved. Trade-off axis confusion persists. |
| 10-11 | Message Queue | 🟢 | — | WR2 Part 2: 3 mistakes resolved (delivery semantics, why-async 3 reasons, FR/NFR/Scope definitions). Now confident on core concepts. Recall 2/4 → notes patched gap. Upgraded from 🟡. |
| 12-13 | API Design | 🟢 | — | WR2 Part 2: 5 mistakes resolved (GET/POST data location, JWT in header, pagination, idempotency 3rd state, SLI/SLO hierarchy). Notes patched with Scale Trigger + DevOps Angle sections. Upgraded from 🟡. |
| 14 | Security & Auth | 🟢 | — | Sessions 19-21. All 8 chunks ✅. OAuth Q2/Q3 resolved, Auth Code Flow, Observability Mini, Scale Trigger, JWT PoC, Simon Drill passed. |
| 15-16 | Consistent Hashing | 🟢 | — | S22-23. 所有 chunk ✅ at interview depth。Strong self-recall。S24 在 distributed cache 設計中當 sharding 機制實際應用。vnode 統計證明 + 獨立 PoC parked → Day 38-39。|
| 17-18 | CAP Theorem | 🟢 | — | S24 problem-anchored。自己推出 cache stampede → replication → C vs A 矛盾。AP 選擇給出教科書級三理由(DB=truth, TTL 自癒, cache 天職是答得出)。partition 定義一開始不清→當場補。業界 CAP 對照表 + 「給錯=賠錢→CP」心法。PACELC 未深入(park)。|
| — | Distributed Cache (design) | 🟢 | **Phase 1 Gate ✅** | S24. 問題錨定設計，3/3 PASS = Phase 1→2 Gate。涵蓋 clarify→sharding→cache-aside→client vs proxy routing→replication→CAP→thundering herd/request coalescing。完整 PoC park 到 Day 38-39。|
| 19-20 | Consistency Models | 🟢 | — | S26 Day 19。7 chunk 全過 at interview depth。自推 strong=同步=等待=慢。光譜表(Strong/Causal/RYW/Eventual)+ Quorum W+R>N(鴿籠重疊)。Eventual≠不一致(收斂保證)misconception 打通。Vector clock(Day 20)park。Drill 4/5。|
| 21-22 | Replication & Leader Election | 🟢 | — | S27。7 chunk 全過 at interview depth。核心因果鏈打通(硬體壞→多份→ordering→election→split-brain→lag→監控)。Single-leader=唯一 ordering 免衝突、過半票防腦裂(鴿籠)、read replica≠strong(lag) 三大點都能在設計題情境自然調用。Interview Drill 5/5 滿分。Raft 細節/Service Discovery/PoC park。|
| 23-24 | Rate Limiting & Circuit Breaker | 🟢 | — | S28。7 chunk 全過 at interview depth (一次過沒卡)。Token Bucket(+自連 AWS T-series credits)、lazy refill(成本跟流量走不跟桶數)、Sliding Window 嚴格封頂、分散式 local counter 失效(N×limit→Redis 3代價)、Circuit Breaker Closed/Open/Half-Open(fail fast 防雪崩)。Light PoC 手打 lazy refill 驗證 rate=refillRate×time。Interview Drill「惡意爬蟲攻擊 API」5/5 滿分,自推 per-user+global 兩層+SW 護 DB+CB 防雪崩。lazy 概念當場補。CB PoC park。|
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
| 18 | WR2 | Weekly Review (API/Cache/MQ) — Mistake Review | 8 resolved | Single-session record. API Design 5 + MQ 3 mistakes fixed. Found notes-gap pattern (Scale Trigger / DevOps Angle missing from API Design notes). |
| 24 | Gate | **Phase 1 Gate** — Distributed Cache design (problem-anchored) | **3/3 ✅ PASS** | ✅ Think Aloud, ✅ Scope Negotiation, ✅ Used building block. 自己推出 stampede + cascading failure (Phase 2 級反應)。Improvement: clarify 時更早明確圈定範圍。Gate crashed on attempt 1. |
| 25 | WR3 | Weekly Review (Caching/LB/CAP) | Caching 3.5/5, LB 4/5, CAP 3/5 | Caching 🔴→🟡 (補 invalidation), LB 🟡→🟢 (Weighted RR 老錯 resolved). CAP 本週剛學已衰退 (英文字母+stampede 術語掉,核心判斷在). |
| 26 | 19 | Consistency Models (Interview Drill) | 4/5 | ✅ Think Aloud, ✅ Scope Negotiation (主動 clarify 開場), ✅ Used spectrum, ✅ Trade-off WHY (老問題改善). ❌ Operational concerns (漏 replication lag 監控收尾). 社群三功能各選對等級。|
| 27 | 21-22 | Replication & Leader Election (Interview Drill) | **5/5 滿分** | 「設計訂單資料層,機器掛掉不掉訂單」。全 5 項過: ✅ Think Aloud, ✅ Scope(收斂 create/read order), ✅ 用 replication+election, ✅ Trade-off WHY(C→sync), ✅ Operational(補回 lag/election 監控,Day 19 弱點收斂). read-after-write 一口氣列三解法無提示。改善點: 選 C 時主動講反面代價(partition 下不了單也賠錢)。|
| 28 | 23-24 | Rate Limiting & Circuit Breaker (Interview Drill) | **5/5 滿分** | 「惡意爬蟲攻擊 API,DB 1000 QPS 上限 vs 50K 攻擊」。全 5 項過: ✅ Think Aloud, ✅ Scope(開場三問+主動提 WAF), ✅ 用 Rate Limiter+Circuit Breaker 雙主角, ✅ Trade-off WHY(global→per-user 被 challenge 後自修正+SW 護硬上限), ✅ Operational(reject數/CB狀態/P99). 改善點: 第一次答常太精簡(「global 一個桶」),被追問才展開,可主動把 why+反面代價一次講完。|

---

## 🔴 Mistake Registry

| Session | Day | Topic | Mistake | Status |
|---------|-----|-------|---------|--------|
| 4 | 4-5 | Load Balancer | Said "least robin" — confused RR and Least Connections names | ❌ Unresolved |
| 4 | 4-5 | Load Balancer | Thought Weighted RR is for different request processing times (it's for different server specs) | ✅ Resolved (WR3-S25, 答對「新舊機混用→Weighted」) |
| 4 | 4-5 | Load Balancer | Couldn't recall LB algorithm names during Simon Drill | ✅ Resolved (WR3-S25, 補回 RR+Least Connections 5 演算法表) |
| 4 | 4-5 | Load Balancer | Forgot DNS-based LB limitations (TTL stale IP, no real-time health check) | ✅ Resolved (WR1) |
| 4 | 4-5 | Load Balancer | Thought 8.8.8.8 is ISP DNS (it's Google Public DNS) | ❌ Unresolved |
| 4 | 4-5 | Load Balancer | Confused sticky sessions and Redis external store as same approach (opposite strategies) | ❌ Unresolved |
| 4 | 4-5 | Load Balancer | Missed sticky session risk: uneven load distribution | ❌ Unresolved |
| 9 | 8-9 | Database Selection | LSM-tree 讀寫搞反（以為是 read-optimized） | ✅ Resolved (WR1) |
| 9 | 8-9 | Database Selection | Denormalization 跟 Normalization 搞混 | ✅ Resolved (S11) |
| 9 | 8-9 | Database Selection | Consistency Trade-offs 空白（不知道三種 model） | ✅ Resolved (S26 Day 19, Strong/Causal/RYW/Eventual 光譜全建立) |
| 9 | 8-9 | Database Selection | 看到「大量資料」就選 NoSQL（data volume ≠ DB 選擇關鍵） | ✅ Resolved (S11) |
| 9 | 8-9 | Database Selection | Interview Drill 忘了 Scope Negotiation | ❌ Unresolved |
| 12 | 10 | Message Queue | Simon Drill: Why Async 只記得 fast response，漏 decoupling/buffering | ✅ Resolved (WR2-S18) |
| 12 | 10 | Message Queue | Simon Drill: delivery semantics 名稱講不完整 (most/least/excely) | ✅ Resolved (WR2-S18) |
| 12 | 10 | Message Queue | 設計練習不知道怎麼起手（需要拆成小問題逐步推） | ❌ Unresolved |
| 13 | 10 | Message Queue | 忘了 Functional / Non-Functional / Scope 的定義（Step 1 基礎） | ✅ Resolved (WR2-S18) |
| 13 | 10 | Message Queue | Inventory check 放 Queue 之後（沒考慮 user 等半天才知道沒貨的體驗） | ✅ Resolved (S14) |
| 13 | 10 | Message Queue | 把 Idempotency 當獨立 service（其實是 Order Service 裡的邏輯） | ❌ Unresolved |
| 13 | 10 | Message Queue | 把 Redis DECR（庫存 pre-check）跟 Idempotency check（防重複）搞混 | ❌ Unresolved |
| 13 | 10 | Message Queue | 說 at-least-once 是解決重複扣款的方法（at-least-once 是問題來源，idempotency 才是解法） | ✅ Resolved (S14) |
| 15 | 12 | API Design | gRPC recall 只說 "for service to service"，說不出 WHY（binary fast + strict contract） | ✅ Resolved (WR2) |
| 15 | 12 | API Design | GraphQL transfer 只說「可以用」沒解釋 HOW（client 寫 query 選 fields，burden 從 backend 移到 client） | ❌ Unresolved |
| 16 | 12 | API Design | Simon Drill: Pagination 完全忘記（Offset vs Cursor） | ✅ Resolved (WR2-S18) |
| 16 | 12 | API Design | Versioning 說「修改不需要新版本」，但 rename field 是 breaking change | ❌ Unresolved |
| 16 | 12 | API Design | Observability: 又把 SLI/SLO/Dashboard 當成 metrics（正確是 Latency, Error rate, Throughput） | ✅ Resolved (WR2-S18) |
| 16 | 12 | API Design | Interview Drill: REST endpoint 寫 `/v1/get/restaurants`，verb 塞進 URL（正確：`GET /v1/restaurants`） | ✅ Resolved (S17) |
| 17 | 12 | API Design | 不知道 GET data 放 URL (query string)、POST data 放 request body | ✅ Resolved (WR2-S18) |
| 17 | 12 | API Design | REST path 用 singular noun + path param 寫成字面文字 | ✅ Resolved (S17, 當場修正) |
| 17 | 12 | API Design | Price/user_id 放 request body（沒想過 client 可以竄改） | ✅ Resolved (WR2-S18) |
| 17 | 12 | API Design | Pagination 說成 "offline"（正確: offset），cursor 也靠提示才想起 | ✅ Resolved (WR2-S18) |
| 17 | 12 | API Design | Idempotency record 只想到 exists/not exists，沒想到需要 processing 中間狀態 | ✅ Resolved (WR2-S18) |
| 20 | 14 | Security (JWT vs Session) | Scenario A trade-off 用「more mantion more infra」這種抽象詞，沒拆成 HA/failover/monitoring/backup | ✅ Resolved (S20, English Polish 補強) |
| 20 | 14 | Security (JWT vs Session) | Scenario B 直接跳到答案 (Hybrid)，沒先論證為什麼 base 是 JWT 不是 Session — WR2 老問題 (WHAT 知道 WHY 跳過) 重現 | ✅ Resolved (S20, 補上 centralized state 的 WHY) |
| 20 | 14 | Security (OAuth) | Q2「為什麼 Auth Server 跟 Resource Server 要分開」答「不同 api」— 描述現象沒講 blast radius separation | ✅ Resolved (S21) |
| 20 | 14 | Security (OAuth) | Q3「三個 disaster 對應 OAuth 解法」跳過沒答 — 還沒建立「設計每元件對應一個痛點」的對照感 | ✅ Resolved (S21) |
| 24 | 17-18 | Distributed Cache / CAP | 不清楚 network partition 是什麼（把「node 死」和「node 失聯但都活著」混為一談） | ✅ Resolved (S24, 當場補：partition = 都活著但網路斷、各自收 request) |
| 24 | 17-18 | Distributed Cache | client-side vs proxy routing 答「不確定」— 缺「開放題=trade-off 取捨、沒有對錯」的反射 | ❌ Unresolved |
| 24 | 17-18 | Distributed Cache | Clarify 時偏向「問 AI 要答案」而非主動斷言並圈定 scope（S8 Scope Negotiation 老問題變體） | 🟡 Improving (S26 Day 19 drill 主動 clarify 開場,但問的是容量題非一致性核心) |
| 26 | 19 | Consistency | CAP recall 說平時「拿到 CAP 三個」— P 不是選項,是「網路會不會斷」的物理事實,平時拿到的是 C+A | ❌ Unresolved |
| 26 | 19 | Consistency | 一開始推不出「instant/strong consistency 要付什麼代價」— 缺「同步=等待=慢」因果鏈 | ✅ Resolved (S26, 白板比喻當場通,後續自己推出) |
| 26 | 19 | Consistency | Quorum W+R>N 不懂為何保證讀到最新(卡兩次) | ✅ Resolved (S26, 杯子/位子鴿籠比喻+填空打通「重疊」) |
| 27 | 21-22 | Replication | Gate「為何 single-leader 免解衝突」答成「leader 是 bottleneck」— 把缺點誤當成原因,沒抓到「唯一 ordering」才是答案 | ✅ Resolved (S27, 用 Tokyo/London 同時寫比喻打通,後續自己遷移到設計題) |
| 28 | 23-24 | Rate Limiting | 不清楚 lazy 是什麼 — 沒有 lazy/eager(敲門才算 vs 背景一直算)這組 CS 概念 | ✅ Resolved (S28, 集點卡比喻+「成本跟流量走不跟桶數走」打通,後續 drill 自己答出 N×limit) |
| 28 | 23-24 | Rate Limiting | Interview Drill 選 global 一個桶 — 只想「保護 DB」漏「公平性」,沒想到爬蟲會吸乾全局桶餓死正常 user | ✅ Resolved (S28, 被 challenge 後自己推到 per-user+global 兩層) |
| 28 | 23-24 | Circuit Breaker | 概念懂但講不出三狀態術語名 (Closed/Open/Half-Open) | ✅ Resolved (S28, 補上術語對照表,白話對應正式名稱) |

---

## 🎯 One-Liner Library (Interview Quick-Answer Bank)

| Topic | One-Liner |
|-------|-----------|
| Load Balancer | A Load Balancer distributes traffic across multiple backend servers to achieve high availability, horizontal scalability, and zero-downtime deployments. |
| Caching & CDN | Cache puts frequently-used data in a faster store like Redis in front of the DB, reducing latency and DB load by serving most requests without hitting the database. |
| Database Selection | Database selection is choosing the right storage engine — SQL, NoSQL, or NewSQL — based on access patterns, relationship complexity, and consistency requirements, so the database fits the workload rather than forcing the workload to fit the database. |
| Message Queue | A Message Queue decouples producers from consumers, enabling async processing, peak traffic buffering, and failure resilience through retry and dead letter queues — the key is pairing at-least-once delivery with idempotency to prevent duplicate processing. |
| API Design | API Design is about choosing the right style (REST, GraphQL, gRPC) based on who's calling, call frequency, and data complexity — the key trade-off is flexibility versus simplicity and cacheability. |
| Security & Auth | Security in distributed systems means separating what can issue credentials from what can consume them — OAuth solves password-sharing disasters by introducing scoped, revocable access tokens exchanged through a trusted server-to-server flow. |
| Consistent Hashing | Consistent hashing maps both keys and nodes onto a ring, so adding or removing a node only remaps about 1/N of the keys instead of nearly all — and virtual nodes keep the load evenly spread. |
| Distributed Cache | A distributed cache spreads data across multiple nodes using consistent hashing to route keys, with replicas for availability — the key trade-off is favoring AP over CP, because the DB is the source of truth and TTL makes staleness self-healing. |
| CAP Theorem | CAP isn't "pick 2 of 3" — without a partition you get both C and A; CAP only forces a choice during a partition: stay consistent (refuse stale answers) or stay available (serve possibly-stale), and the choice can be made per-feature. |
| Replication & Leader Election | Replication stores data on multiple nodes to survive hardware failure; the key design question is who accepts writes — a single leader gives one total ordering so conflicts are impossible, while multi-leader/leaderless buys write availability at the cost of conflict resolution, and leader election uses majority quorum to prevent split-brain. |
| Consistency Models | Consistency is a spectrum, not on/off — a latency budget from Strong (everyone always sees the latest, most expensive) to Eventual (stale now but guaranteed to converge, cheapest); you tune it with quorums (W+R>N forces read/write overlap) and pick per-operation by how much staleness the business tolerates. |
| Rate Limiting & Circuit Breaker | Rate limiting protects the backend and ensures fairness — Token Bucket allows bursts while Sliding Window strictly caps, and you layer per-user limits for fairness plus a global cap to protect downstream; a Circuit Breaker complements it on outbound calls by failing fast when a dependency is down (Closed→Open→Half-Open) to prevent cascading failure. |

---

## RPG Profile

| Field | Value |
|-------|-------|
| **Title** | 🌐 Distributed Architect |
| **Current streak** | 1 🔥 (S28 2026-06-09, 距上次 6/5 隔 4 天 streak 重置) |
| **Longest streak** | 4 |
| **Last session date** | 2026-06-09 |
| **Last story summary** | Session 28 完成 (Day 23-24) — Karen 衝進來說 API 被惡意爬蟲打爆、DB 快撐不住。學生手打 token bucket lazy refill PoC(驗證 rate=refillRate×time),Simon Drill 3/3 無提示答出分散式 N×limit 陷阱。Interview Drill「設計 API 防護層」拿 5/5,從 global 一個桶被 challenge 後自推 per-user+global 兩層+Sliding Window 護 DB 硬上限+Circuit Breaker 防雪崩。Day 23-24 達成 🟢。|

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
| M3 | Builder's Foundation | 🏆 | 2026-05-29 (Pass Phase 1 Gate) |
| C3 | Gate Crasher | 🏆 | 2026-05-29 (Phase 1 Gate, attempt 1) |
| K1 | One-Liner ×10 | 🏆 | 2026-06-03 (S26, Consistency Models 補上第 10 條) |

**Total: 11/25**

---

## Review Schedule (Spaced Repetition)

> Box 1 → next day | Box 2 → 3 days | Box 3 → 7 days | Box 4 → 14 days → retired

| Topic | Box | Next Review |
|-------|-----|-------------|
| Security & Auth | 2 | 2026-05-18 (overdue — 下次帶到) |
| Consistent Hashing | 2 | 2026-06-05 |
| Distributed Cache + CAP | 2 | 2026-06-06 (S26 recall pass「partition 才選 CP/AP」,Box 1→2) |
| Caching & CDN | 2 | 2026-06-07 (S27 recall PASS「寫時刪 cache 不更新,避 race condition」,Box 1→2) |
| Load Balancer | 2 | 2026-06-05 (WR3 recall 4/5 pass, Box 1→2) |
| Consistency Models | 1 | 2026-06-04 (S26 新學,Box 1。S28 recall 未完全過,留 Box 1) |
| Replication & Leader Election | 1 | 2026-06-06 (S27 新學,Box 1) |
| Rate Limiting & Circuit Breaker | 1 | 2026-06-10 (S28 新學,Box 1) |

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
| Phase 1 | 2026-05-29 | 3/3 | ✅ Pass (attempt 1) — Distributed Cache design (problem-anchored mini-mock) | clarify 時更早明確圈定 scope |
