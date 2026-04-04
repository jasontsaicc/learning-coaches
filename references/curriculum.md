# System Design Interview Curriculum

> Target: Big tech SD interviews (FAANG, AWS, Google, etc.)
> Pace: progress by **content units**, not by clock or calendar. Each "Day" is one Learning Unit
>   that may span several work-gaps. **63 learning units ≠ 63 calendar days**, expect 12-14 weeks
>   for a working engineer studying in spare time. Deep learning over memorization.
> Approach: Discussion → PoC → Notes → Reflect

---

## Phase 0: Thinking Framework (Day 1-3)

### Day 1: What SD Interviews Actually Test
**Prerequisites:** None (entry point)
**Story:** 你的第一天。認識團隊。（角色：小球、小杰、Karen）
**Story beats:** 1. 小球帶你參觀辦公室，介紹團隊 2. 小杰隨口問「你會設計系統嗎？」你愣住 3. 小球安慰：「沒關係，這就是我們要一起學的」
- The 4 scoring dimensions: Problem Navigation, Design, Technical Depth, Trade-offs
- Analyze good vs bad answers for the same question
- **Discussion**: Deconstruct a real SD interview rubric

### Day 2: Back-of-Envelope Estimation
**Prerequisites:** Day 1
**Story:** 被問到容量估算問題，答不出來。（角色：Karen）
**Story beats:** 1. Karen 問「新功能需要多少儲存空間？」你算不出來 2. 小杰隨口猜一個數字，被小球指出差了 100 倍 3. 小球教你「工程師估算不是猜，是有方法的」
- Powers of 2, latency numbers every engineer should know
- Practice: Estimate YouTube daily storage, Twitter QPS
- **Exercise**: Build an estimation cheat sheet you actually understand
- **📖 Cross-verify**: Jeff Dean's "Latency Numbers Every Programmer Should Know" — compare with the cheatsheet, note any numbers that differ

### Day 3: Your SD Answer Framework (4-Step Method)
**Prerequisites:** Day 1, Day 2
**Story:** 學習框架，為明天的實戰做準備。（角色：小球）
**Story beats:** 1. 小球拿出白板：「每次面試都從這四步開始」 2. 用 URL Shortener 做 dry run，小球扮面試官 3. 結束後小球說：「明天開始，我們真正動手建東西」
- The 4-Step SD Interview Framework (defined in SKILL.md)
- Time budget for 45-min interview: Clarify (0-5) → Estimate (5-10) → Design (10-20) → Deep Dive (20-35) → Scale (35-45)
- Standard Whiteboard Diagram Template — the 8-block skeleton (see `8-block-skeleton.md`)
- Practice: Answer "Design URL Shortener" using the framework (dry run)

### Phase 0 Gate
> Answer a simple SD question using the 4-step framework. Must complete all 4 steps with reasonable structure.

---

## Phase 1: Core Building Blocks (Day 4-16)

> Apply the **Observability Mini** to every topic:
> SLIs → SLO target → Alerts → Dashboards

### Day 4-5: Load Balancer & Reverse Proxy
**Prerequisites:** Day 3 (4-Step Framework)

⚠️ **Common Misconception:** "L7 is always better than L4." No — L4 has lower latency and is better for non-HTTP protocols and raw throughput. L7 gives you content-based routing but adds processing overhead.

**Story:** 流量暴增，服務中斷。小杰提出了錯誤解法。（角色：小杰、小球）
**Story beats:** 1. Karen 衝進來：「用戶回報網站掛了！」 2. 小杰說「加 RAM 就好」，小球搖頭 3. 小球問你：「一台機器的極限是什麼？超過了怎麼辦？」
**Derivation:** ✅ 推導鏈 #1 — 單機硬體上限 → Load Balancer

**Day 4 — DNS + LB Fundamentals:**
- DNS fundamentals — resolution flow, TTL, record types
- DNS-based load balancing (weighted, latency-based, failover)
- L4 vs L7 load balancing — when to use which
- Algorithms: Round Robin, Least Connections, IP Hash, Weighted

**Day 5 — Production LB + PoC:**
- Health checks, sticky sessions, connection draining
- **DevOps**: ALB vs NLB, target group health checks
- **PoC**: Nginx L4/L7 LB with Docker Compose
- **📖 Cross-verify**: AWS docs on ALB vs NLB — check if the L4/L7 distinction matches what we covered, especially around WebSocket support

### Day 6-7: Caching & CDN Strategies
**Prerequisites:** Day 3, Day 4-5 (LB)

⚠️ **Common Misconception:** "More cache = always better." No — cache invalidation bugs can cause stale data, and large caches increase memory cost and cold-start time. Cache is a trade-off between speed and freshness.

**Story:** 頁面載入極慢，用戶在抱怨。（角色：Karen）
**Story beats:** 1. Karen 秀出用戶投訴截圖：「載入要 8 秒！」 2. 你查了 DB query，發現同一筆熱門商品被讀了上萬次 3. 小球：「如果這筆資料就放在手邊呢？」
**Derivation:** ✅ 推導鏈 #2 — DRAM/SSD/Network 延遲差距 → Caching

**Day 6 — Cache Patterns:**
- Cache levels: Browser → CDN → App → DB
- Patterns: Cache-Aside, Write-Through, Write-Behind, Read-Through
- Eviction: LRU, LFU, TTL
- Cache invalidation — the hard problem

**Day 7 — CDN + PoC:**
- CDN: Edge caching, Pull vs Push, cache invalidation strategies
- **DevOps**: ElastiCache cluster mode, CloudFront behaviors, cache hit ratio
- **PoC**: Redis cache layer, measure latency with/without cache
- **📖 Cross-verify**: Redis official docs on eviction policies — check if LRU implementation is exact or approximate (it's approximate, and that matters)

### Day 8-9: Database Selection
**Prerequisites:** Day 3
**Story:** 新功能需要選 DB，團隊意見不一。（角色：小杰）
**Story beats:** 1. 小杰堅持用 MongoDB 因為「NoSQL 比較潮」 2. Karen 問：「哪個選擇不會讓我們半年後後悔？」 3. 小球：「不是哪個比較好，而是你的 workload 長什麼樣」
**Derivation:** ✅ 推導鏈 #3 — 讀寫模式決定最佳儲存結構 → Database Selection

**Day 8 — SQL vs NoSQL Concepts:**
- SQL vs NoSQL vs NewSQL — decision framework
- Indexing: B-tree (read-optimized) vs LSM-tree (write-optimized)
- Denormalization, sharding intro, connection pooling

**Day 9 — Storage Engine + PoC:**
- WAL, read replicas, consistency trade-offs
- **Data Model Design Template**: Entities → Access patterns → Partition key → Secondary index → Hot partition risk → Backfill strategy
- **PoC**: Same problem with SQL vs NoSQL, compare trade-offs
- **📖 Cross-verify**: DDIA Chapter 3 (Storage and Retrieval) — compare B-tree vs LSM-tree trade-offs with what we covered, especially write amplification numbers

### Day 10-11: Message Queue & Async Processing
**Prerequisites:** Day 3, Day 8-9 (Database)

⚠️ **Common Misconception:** "Kafka has exactly-once delivery." Kafka has idempotent producers + transactional consumers, which achieves effectively-once processing. True exactly-once in distributed systems requires end-to-end idempotency — the broker alone cannot guarantee it.

**Story:** 促銷活動，訂單處理異常。出現重複處理。（角色：Karen）
**Story beats:** 1. 促銷開始 5 分鐘，Karen 收到用戶反映「被扣了兩次款」 2. 小杰：「重啟消費者應該就好了吧？」結果更慘 3. 小球帶你看 log：「你看到問題了嗎？消費者處理太慢，rebalance 導致重複消費」
**Derivation:** ✅ 推導鏈 #4 — 同步呼叫的級聯故障 → Message Queue

**Day 10 — Queue Concepts + Semantics:**
- Why async? Decoupling, buffering, peak handling
- SQS vs Kafka vs RabbitMQ — positioning
- Delivery semantics: at-least-once, at-most-once, exactly-once

**Day 11 — DLQ + PoC:**
- Dead letter queue, retry strategies
- **DevOps**: SQS FIFO vs Standard, DLQ monitoring
- **PoC**: Producer-consumer with failures simulation
- **📖 Cross-verify**: Kafka docs on "exactly-once semantics" — check what guarantees are actually provided vs what's marketing. Compare with our "effectively-once" discussion

### Day 12-13: API Design
**Prerequisites:** Day 3, Day 4-5 (LB)
**Story:** 行動 App 要上線，API 需要重新設計。（角色：小球）
**Story beats:** 1. 行動端工程師抱怨：「一個 API call 回 50 個欄位，我只要 3 個」 2. 小杰：「那就多開幾個 endpoint 啊」小球皺眉 3. 小球：「有沒有辦法讓客戶端自己選要什麼？」
**Derivation:** ✅ 推導鏈 #5 — 不同客戶端的資料需求差異 → API Design

**Day 12 — API Styles:**
- REST vs gRPC vs GraphQL — trade-off matrix
- Pagination: Offset vs Cursor
- Versioning strategies, idempotency

**Day 13 — API PoC:**
- **PoC**: Design & implement a small API in Go
- **📖 Cross-verify**: Compare REST vs GraphQL maturity in your target company's tech stack — Google/Meta lean GraphQL, AWS/Stripe lean REST. Check if your understanding of trade-offs matches their published engineering blogs

### Day 14: Security & Authentication
**Prerequisites:** Day 12-13 (API Design)
**Story:** 資安稽核。發現安全漏洞。（角色：小杰）
**Story beats:** 1. 資安稽核報告出來，小杰臉色發白：「我把 API key 放在 URL query string 裡...」 2. 小球冷靜地說：「我們一個一個修」 3. 修復過程中發現 JWT token 沒設過期時間
**Derivation:** ✅ 推導鏈 #6 — HTTP 明文傳輸的物理風險 → Security & Auth

- JWT vs Session-based authentication
- OAuth 2.0 flow basics
- API Key management, HTTPS, encryption
- **DevOps**: Cognito, OIDC integration, secrets rotation
- **📖 Cross-verify**: OAuth 2.0 RFC 6749 Section 1.3 (Authorization Grant) — check if your understanding of the auth code flow matches the spec. Many tutorials oversimplify the redirect steps

### Day 15-16: Consistent Hashing & Data Partitioning
**Prerequisites:** Day 8-9 (Database)

⚠️ **Common Misconception:** "Consistent hashing eliminates all data movement." No — it minimizes movement to K/N keys on average when a node joins/leaves, but rebalancing still happens and virtual nodes affect distribution uniformity.

**Story:** 資料庫需要重新分片。搬移過程影響服務。（角色：小球）
**Story beats:** 1. 資料庫快撐不住，需要從 4 台擴到 5 台 2. 小杰做了 hash mod 5 的遷移，結果 80% 的資料要搬家 3. 小球：「有沒有一種方法，加一台只搬 20% 的資料？」
**Derivation:** ✅ 推導鏈 #7 — hash mod N 的資料重分配問題 → Consistent Hashing

**Day 15 — Theory:**
- Why simple hash mod N fails
- Consistent hashing with virtual nodes
- Range-based vs Hash-based partitioning

**Day 16 — PoC + Checkpoint:**
- **PoC**: Implement consistent hashing from scratch in Go
- **📖 Cross-verify**: DynamoDB paper (Dynamo: Amazon's Highly Available Key-value Store) Section 4.2 — check how Amazon implements virtual nodes and if the K/N rebalancing claim holds in practice

### Phase 1 Gate
> Mini-mock (scope-based, not timed): Explain any building block using the 4-step framework. Interviewer redirects after 2-3 exchanges. Scorecard ≥ 2/3.

---

## Phase 2: Distributed Systems Core (Day 17-26)

### Day 17-18: CAP Theorem in Practice
**Prerequisites:** Day 8-9 (Database), Day 15-16 (Consistent Hashing)

⚠️ **Common Misconception:** CAP is NOT "pick 2 out of 3 in daily operation." It's about what happens DURING a network partition — you choose between consistency and availability. When there's no partition, you can have both. Teach PACELC as the practical mental model.

**Story:** 海外用戶看到過時資料。（角色：Karen、Yuki 登場）
**Story beats:** 1. Karen：「日本用戶看到的商品價格跟台灣不一樣！」 2. Yuki 首次登場，從東京辦公室視訊加入：「我這邊看到的確實跟你們不同」 3. 小球：「當兩個資料中心之間的連線斷了，你只能選一邊」
**Derivation:** ✅ 推導鏈 #8 — 網路 partition 不可避免 → CAP Theorem

**Day 17 — CAP + Examples:**
- CAP is about network partitions, not a daily choice
- Real-world examples: DynamoDB (AP), Zookeeper (CP)

**Day 18 — PACELC + Discussion:**
- PACELC model as a more practical framework
- Discussion: classify real-world systems on the CAP/PACELC spectrum
- **📖 Cross-verify**: Martin Kleppmann (DDIA author) 的 blog post "Please stop calling databases CP or AP" — check if the "pick 2 out of 3" framing we debunked matches his critique

### Day 19-20: Consistency Models
**Prerequisites:** Day 17-18 (CAP)

⚠️ **Common Misconception:** "Eventual consistency = inconsistent." No — eventual consistency means the system WILL converge to a consistent state given enough time with no new writes. It has a convergence guarantee, unlike "no consistency" which has none.

**Story:** 跨區域資料不一致。（角色：Karen）
**Story beats:** 1. 用戶發文後刷新頁面看不到自己的貼文，氣到發客訴 2. Yuki：「eventual consistency 就是不一致吧？」（常見誤解，教學入口） 3. 小球帶大家看 replication lag 的 metrics：「差距只有 200ms，但用戶感受到了」
**Derivation:** ✅ 推導鏈 #9 — 光速有限，跨節點同步需要時間 → Consistency Models

**Day 19 — Models:**
- Strong, Eventual, Causal, Read-your-writes
- Quorum: W + R > N

**Day 20 — Conflict Resolution + PoC:**
- Vector clocks, conflict resolution
- **PoC**: Simulate eventual consistency
- **📖 Cross-verify**: DDIA Chapter 5 (Replication) on "Reading Your Own Writes" — check if the implementation techniques (read from leader, remember timestamp) match what we covered

### Day 21-22: Replication & Leader Election
**Prerequisites:** Day 8-9 (Database), Day 19-20 (Consistency)

⚠️ **Common Misconception:** "Read replicas give you strong consistency." No — replicas have replication lag (milliseconds to seconds). Read-after-write consistency requires reading from the leader, or using techniques like session stickiness or synchronous replication.

**Story:** 主資料庫故障。小杰的回應讓問題更嚴重。（角色：小杰）
**Story beats:** 1. 凌晨 3 點 on-call 警報：primary DB 掛了 2. 小杰 半夢半醒手動 promote replica，但選了 lag 最大的那台，丟了 30 秒資料 3. 小球事後覆盤：「如果有自動 failover + 正確的 replica 選擇策略，就不會發生這種事」
**Derivation:** ✅ 推導鏈 #10 — 硬體年故障率 2-10%，單點 = 單點故障 → Replication

**Day 21 — Replication Patterns:**
- Single-leader, multi-leader, leaderless
- Raft consensus algorithm (simplified)

**Day 22 — Service Discovery:**
- Service Discovery: Consul, Kubernetes DNS, Cloud Map
- **📖 Cross-verify**: Raft consensus paper (In Search of an Understandable Consensus Algorithm) Section 5 — compare with our simplified Raft explanation. Are there safety properties we glossed over?

### Day 23-24: Rate Limiting & Circuit Breaker
**Prerequisites:** Day 6-7 (Caching), Day 12-13 (API Design)

⚠️ **Common Misconception:** "Token bucket and sliding window are interchangeable." No — token bucket allows bursts up to the bucket size (good for bursty traffic), while sliding window enforces a strict rate limit (better for steady rate enforcement). Choose based on your traffic pattern.

**Story:** 被惡意爬蟲攻擊 API。（角色：小球）
**Story beats:** 1. 監控告警：某個 IP 每秒打 5000 次 API 2. 小球：「先擋住，再分析。但怎麼擋才不會誤殺正常用戶？」 3. 討論 per-IP vs per-user vs per-API-key 的粒度選擇
**Derivation:** ✅ 推導鏈 #11 — 系統處理能力有物理上限 → Rate Limiting

**Day 23 — Algorithms:**
- Token Bucket, Sliding Window, Fixed Window

**Day 24 — Circuit Breaker + PoC:**
- Circuit Breaker pattern (Closed → Open → Half-Open)
- Bulkhead pattern
- **PoC**: Token Bucket + Circuit Breaker implementation in Go
- **📖 Cross-verify**: Stripe's blog post on rate limiting — check if their approach (token bucket + Redis) matches our implementation, and note any production nuances they mention

### Distributed Systems Kill Pack (Reference)
- **Idempotency Key**: scope, TTL, storage, behavior
- **Deduplication**: message ID, dedup window, consumer vs infra side
- **Distributed Lock**: lease-based, fencing token, failure modes

### Day 25: Observability Consolidation
**Prerequisites:** Day 4-5 (LB), Day 6-7 (Caching), Day 8-9 (Database)
**Story:** 半夜事故，但缺少可觀測性。（角色：小球）
**Story beats:** 1. 半夜事故，花了 3 小時才找到問題：某個微服務的 latency spike 導致下游 cascade 2. 小球：「如果我們有 distributed tracing，10 分鐘就能定位」 3. 團隊決定建 observability stack，小球讓你主導
**Derivation:** ✅ 推導鏈 #12 — 無法逐台 ssh 到數千節點 → Observability

- Metrics, Logs, Traces — three pillars
- Distributed tracing, SLI/SLO/SLA formalization
- Structured logging, correlation IDs
- How to discuss monitoring in SD interviews
- **📖 Cross-verify**: Google SRE Book Chapter 6 (Monitoring Distributed Systems) — compare their "Four Golden Signals" with our SLI/SLO approach. Are we missing any signals?

### Day 26: Bloom Filter, Gossip Protocol & Advanced Concepts
**Prerequisites:** Day 15-16 (Consistent Hashing), Day 19-20 (Consistency)
**Story:** Sprint review。回顧整個 Phase 2。（角色：全員）
**Story beats:** 1. Sprint demo 日，全員到齊，你展示 Phase 2 學到的分散式系統知識 2. Karen 問了一個 practical 的問題讓你把 Bloom Filter 連結到真實場景 3. 小球：「Phase 2 結束了。準備好面對真正的設計題了嗎？」
**Derivation:** ✅ 推導鏈 #13 — 精確查詢 O(N) 太貴 + 全量廣播 O(N²) 不 scale → Bloom/Gossip

- Bloom Filter: probabilistic membership testing
- Gossip Protocol: node discovery and state sharing
- Distributed Transactions overview (2PC/3PC)
- **📖 Cross-verify**: Cassandra docs on Bloom Filter usage — check how they tune false positive rate per SSTable and if the formula from our derivation chain matches their implementation

### Phase 2 Gate
> Mock (scope-based, not timed): Design a distributed key-value store — full 4 steps, interviewer changes 1 requirement mid-way. Scorecard ≥ 4/6.

---

## Phase 3: Classic SD Problems (Day 27-53)

> All Phase 3 topics require completion of Phase 1 + Phase 2 (enforced by Phase Gate).
> Format: Day 1 = Discussion & Design | Day 2 = PoC + Diagram + Notes
> Complex problems get 3 days.

### Tier 1: Must Do (Day 27-45)

#### Day 27-28: URL Shortener ★★☆
**Key Concepts:** Hashing, base62, read-heavy
**Story:** 行銷需要短網址追蹤功能。（角色：Karen）
**Story beats:** 1. Karen 拿著行銷報表衝過來：「我需要追蹤每個連結的點擊數，但網址太長社群都不願意轉貼」 2. 你提出用 hash 產生短碼，Karen 追問：「如果兩個網址 hash 出一樣的怎麼辦？」 3. 你開始思考 base62 編碼 + 碰撞處理的方案

**Day 27 — Design:**
- Requirements clarification (read:write ratio, URL length, analytics)
- High-level design: API → ID generator → DB → Cache
- Deep dive: base62 encoding, collision handling, custom aliases

**Day 28 — PoC + Diagram:**
- **PoC**: URL shortener service in Go
- Full architecture diagram with 8-block skeleton
- Notes with interview template
- **📖 Cross-verify**: Alex Xu Vol 1 Ch 8 — check base62 vs base64 trade-offs

#### Day 29-30: Unique ID Generator ★★☆
**Key Concepts:** Snowflake, clock sync, coordination-free
**Story:** 訂單 ID 重複問題。（角色：Karen）
**Story beats:** 1. Karen 緊急通報：「兩筆不同訂單拿到同一個 ID，客戶帳單全亂了」 2. 你查了程式碼，發現用的是 DB auto-increment + 多台 DB，ID 撞車了 3. 小球提示：「有沒有方法讓每台機器獨立產生 ID，又保證全域唯一？」

**Day 29 — Design:**
- Requirements: uniqueness, ordering, performance
- Approaches: UUID, DB auto-increment, Snowflake, ULID
- Deep dive: Snowflake bit layout, clock skew handling

**Day 30 — PoC + Diagram:**
- **PoC**: Snowflake ID generator in Go
- Full architecture diagram
- Notes with interview template
- **📖 Cross-verify**: Alex Xu Vol 1 Ch 7 — compare Snowflake bit layout

#### Day 31-32: Distributed Rate Limiter ★★★
**Key Concepts:** Distributed sliding window, Redis Lua, race conditions
**Story:** 開放第三方 API，需要限流。（角色：小球）
**Story beats:** 1. 小球：「我們要開放 API 給外部合作夥伴，但你還記得之前被爬蟲打爆的事嗎？」 2. 你提出用 Day 23 學的 Token Bucket，小球追問：「單機版的 counter 在多台 API server 之間怎麼同步？」 3. 你意識到分散式限流需要共享狀態，開始探索 Redis + Lua 的方案

**Day 31 — Design:**
- Single-node vs distributed: new challenges
- Redis-based sliding window with Lua scripts
- Race conditions and how to handle them

**Day 32 — PoC + Diagram:**
- **PoC**: Distributed rate limiter with Redis in Go
- Full architecture diagram
- Notes with interview template
- **📖 Cross-verify**: Alex Xu Vol 1 Ch 4 — compare sliding window approaches

#### Day 33-34: Notification System ★★★
**Key Concepts:** Push/Pull, priority queue, multi-channel
**Story:** 通知系統問題：有人收不到，有人收太多。（角色：Karen）
**Story beats:** 1. Karen 列出客訴清單：「VIP 客戶的出貨通知沒收到，但有人一天被推播轟炸 20 次」 2. 你發現通知沒有優先級分類，全擠在同一條 queue 裡 3. Karen：「能不能讓重要通知一定送到，但也讓用戶控制頻率？」

**Day 33 — Design:**
- Multi-channel: push notification, SMS, email
- Priority queue for urgent vs batch notifications
- Delivery guarantees and retry logic

**Day 34 — PoC + Diagram:**
- **PoC**: Notification dispatcher in Go
- Full architecture diagram
- Notes with interview template
- **📖 Cross-verify**: Alex Xu Vol 1 Ch 10 — check priority queue implementation

#### Day 35-37: Chat System ★★★★
**Key Concepts:** WebSocket, presence, read receipts, group chat
**Story:** 新功能需求：即時客服聊天。（角色：Karen）
**Story beats:** 1. Karen：「客服回覆太慢，用戶流失率飆高。我們需要即時聊天功能」 2. 你提出用 HTTP polling，小球反問：「每秒打一次 API，十萬個用戶同時在線，伺服器撐得住嗎？」 3. 你開始研究 WebSocket 的雙向通道，Karen 追加：「還要支援群組聊天和已讀回條」

**Day 35 — WebSocket + 1v1 Messaging:**
- WebSocket vs long polling vs SSE
- 1v1 message flow: send → store → deliver
- Message ordering and offline delivery

**Day 36 — Group Chat + Presence + Read Receipts:**
- Group chat: fan-out strategies
- Presence service: heartbeat, status propagation
- Read receipts: per-message tracking

**Day 37 — PoC + Full Diagram:**
- **PoC**: Chat server with WebSocket in Go
- Full architecture diagram (all components)
- Notes with interview template
- **📖 Cross-verify**: Alex Xu Vol 1 Ch 12 — compare WebSocket vs SSE decision framework

#### Day 38-39: Distributed Cache ★★★
**Key Concepts:** Consistent hashing, invalidation at scale, thundering herd
**Story:** 商品頁效能問題。Cache 架構需要升級。（角色：小球）
**Story beats:** 1. 小球拿出 APM 報表：「商品頁 P99 latency 從 200ms 飆到 2 秒，Redis 單節點已經到極限了」 2. 你建議加 Redis replica，小球：「那 cache miss 時 100 個 request 同時打 DB 呢？」 3. 你發現需要 consistent hashing 做分片 + request coalescing 防 thundering herd

**Day 38 — Design:**
- Distributed cache architecture (consistent hashing for sharding)
- Cache invalidation at scale: TTL, event-driven, versioning
- Thundering herd: locking, request coalescing

**Day 39 — PoC + Diagram:**
- **PoC**: Distributed cache with consistent hashing in Go
- Full architecture diagram
- Notes with interview template
- **📖 Cross-verify**: Alex Xu Vol 1 Ch 6 — check thundering herd mitigation strategies

#### Day 40-42: News Feed ★★★★
**Key Concepts:** Fan-out on write/read, ranking, celebrity problem
**Story:** 社交動態牆功能。大帳號發文導致效能問題。（角色：Karen）
**Story beats:** 1. Karen：「我們要做社交動態牆，讓用戶看到朋友的動態」你開始設計 fan-out on write 2. 上線第一天就出事：一個百萬粉絲的 KOL 發文，write amplification 癱瘓了整個系統 3. 你被迫思考 hybrid 策略：普通用戶 fan-out on write，大帳號 fan-out on read

**Day 40 — Fan-out Design:**
- Fan-out on write vs fan-out on read
- Hybrid approach for celebrity accounts
- Feed storage and retrieval

**Day 41 — Ranking + Celebrity Problem:**
- Feed ranking algorithms (chronological vs ML-based)
- Celebrity problem: how to handle accounts with millions of followers
- Cache warming and precomputation

**Day 42 — PoC + Full Diagram:**
- **PoC**: News feed service in Go
- Full architecture diagram (all components)
- Notes with interview template
- **📖 Cross-verify**: Alex Xu Vol 1 Ch 11 — compare fan-out strategies for celebrity problem

#### Day 43-45: Payment System ★★★★
**Key Concepts:** Idempotency, SAGA, exactly-once, reconciliation
**Story:** 支付系統嚴重事故：用戶被重複扣款。（角色：小球、Karen）
**Story beats:** 1. Karen 臉色鐵青衝進來：「有用戶被扣了三次款，客訴電話接不完，法務說可能要賠償」 2. 小球帶你看 log：retry 邏輯沒有 idempotency key，每次 timeout retry 都真的扣了一次 3. 你意識到支付系統的核心不是「快」而是「正確」——開始設計 idempotency + SAGA 補償機制

**Day 43 — Idempotency + SAGA:**
- Payment flow: authorization → capture → settlement
- Idempotency keys for payment APIs
- SAGA pattern for distributed transactions

**Day 44 — Reconciliation + Exactly-once:**
- Double-entry bookkeeping
- Reconciliation: internal vs external (bank statements)
- Achieving exactly-once processing with idempotency

**Day 45 — PoC + Full Diagram:**
- **PoC**: Payment processing service in Go
- Full architecture diagram (all components)
- Notes with interview template
- **📖 Cross-verify**: Stripe engineering blog on idempotency — check idempotency key lifecycle

### Tier 2: Should Do (Day 46-53)

#### Day 46-47: Metrics & Logging System
**Key Concepts:** Time-series DB, aggregation, sampling
**Story:** 工程團隊需要自建 metrics 平台。（角色：小球）
**Story beats:** 1. 小球：「我們現在靠 CloudWatch 撐，但自訂 metrics 的查詢太慢、成本太高」 2. 你開始調研 time-series DB，發現 ingestion rate 和 query pattern 完全不同於 OLTP 3. 小球挑戰：「每秒百萬筆 metrics 進來，你怎麼存、怎麼查、過期的怎麼壓縮？」

**Day 46 — Design:**
- Data ingestion pipeline: agents → collectors → storage
- Time-series DB selection (InfluxDB, Prometheus, TimescaleDB)
- Aggregation strategies and downsampling

**Day 47 — PoC + Diagram:**
- **PoC**: Metrics pipeline in Go
- Full architecture diagram
- Notes with interview template
- **📖 Cross-verify**: Prometheus docs on data model — compare with our time-series approach

#### Day 48-49: Search Autocomplete
**Key Concepts:** Trie, ranking, Elasticsearch
**Story:** 搜尋體驗很差，自動完成太慢。（角色：Karen）
**Story beats:** 1. Karen：「用戶打了三個字要等兩秒才出建議，競品是即時的」 2. 你查了架構，發現每次 keystroke 都打一次 DB full-text search 3. 小球提示：「如果把熱門搜尋詞預先建好一棵樹呢？」你開始研究 Trie

**Day 48 — Design:**
- Trie data structure for prefix matching
- Ranking: frequency-based, personalized
- Elasticsearch integration for full-text search

**Day 49 — PoC + Diagram:**
- **PoC**: Autocomplete service in Go
- Full architecture diagram
- Notes with interview template
- **📖 Cross-verify**: Alex Xu Vol 1 Ch 13 — compare Trie optimization techniques

#### Day 50-51: Web Crawler
**Key Concepts:** BFS/DFS, URL frontier, dedup (Bloom filter)
**Story:** 需要爬取競品資料做分析。（角色：Karen）
**Story beats:** 1. Karen：「產品部需要競品的公開定價資料，目前是實習生手動抄的」 2. 你開始設計爬蟲，馬上遇到問題：重複 URL、無限迴圈、被網站封鎖 3. 你引入 Bloom Filter 做去重，加上 robots.txt 解析和 politeness delay

**Day 50 — Design:**
- Crawler architecture: URL frontier → fetcher → parser → storage
- BFS vs DFS crawling strategies
- Deduplication with Bloom filter, politeness (robots.txt, rate limiting)

**Day 51 — PoC + Diagram:**
- **PoC**: Web crawler in Go
- Full architecture diagram
- Notes with interview template
- **📖 Cross-verify**: Alex Xu Vol 1 Ch 9 — check politeness/robots.txt handling details

#### Day 52-53: Proximity Service
**Key Concepts:** Geohash, QuadTree, spatial indexing
**Story:** 新功能：附近取貨點。地理查詢需求。（角色：Karen）
**Story beats:** 1. Karen：「用戶想找最近的取貨點，但現在要手動輸入地址再按搜尋，體驗很差」 2. 你第一版用暴力算距離排序，結果掃了整張 table，P99 超過 5 秒 3. 小球：「地理資料有空間特性，能不能用編碼把『附近』變成『前綴相同』？」

**Day 52 — Design:**
- Geohash: encoding lat/lng into a string for range queries
- QuadTree: spatial partitioning for nearest-neighbor
- Trade-offs: Geohash (simple, DB-friendly) vs QuadTree (dynamic, memory)

**Day 53 — PoC + Diagram:**
- **PoC**: Proximity search service in Go
- Full architecture diagram
- Notes with interview template
- **📖 Cross-verify**: Alex Xu Vol 2 Ch 1 — compare Geohash precision levels

### Phase 3 Gate
> Full mock (scope-based, not timed) on a Tier 1 problem — all 4 steps + follow-ups pushed to the student's knowledge boundary. Scorecard ≥ 6/9.

### Tier 3: Nice to Have (Optional)

Video Streaming, Cloud Storage, Distributed Task Scheduler, Ticket/Booking System — concepts already covered by Tier 1/2.

---

## Phase 4: Advanced & Mock Interviews (Day 54-63)

### Day 54-55: Trade-off Analysis Deep Dive
**Prerequisites:** All Phase 1-3
**Story:** 回顧成長。準備面對最難的挑戰。（角色：小球）
**Story beats:** 1. 小球拿出你 Day 1 的筆記跟現在對比：「你看你走了多遠」 2. 但隨即嚴肅：「面試不考你會多少，考的是你能不能在壓力下做正確的取捨」 3. 小球開始用快節奏丟 trade-off 情境，不給你太多思考時間——這就是面試的節奏

**Day 54 — Trade-off Scenarios:**
- Practice specific trade-off scenarios (rapid-fire, a few exchanges each)
- Cost estimation for designs

**Day 55 — Trap & Pivot Drills:**
- Trap & Pivot Drills — practice graceful pivots when initial design hits a wall

### Day 56-57: Brownfield / Legacy Migration ★★★★
**Prerequisites:** All Phase 1-3
**Story:** ScaleUp 的單體訂單系統撐不住了，但不能停機重寫。（角色：小球、Karen）

> **為什麼這個主題：** 真實工作 90% 是改造既有系統，不是綠地設計。Senior+ 面試官也越來越愛問 migration 題，因為它考的是「在約束下把事做成」的成熟度，而不是空地上畫架構。

⚠️ **Common Misconception:** 「migration 就是把資料 copy 到新系統」。錯。難的是「遷移期間新舊系統並存、資料持續變動」下的一致性與可回滾性。

**Day 56 — Migration Strategy & Patterns:**
- Greenfield vs Brownfield：為什麼改造比新建難（不能停機、有舊資料、有既有依賴與呼叫方）
- **Strangler Fig**：用 proxy/router 逐步把流量從舊系統導到新系統，舊系統慢慢「被絞殺」
- **Dual-write + backfill**：新舊資料庫雙寫 + 回填歷史資料，怎麼保證一致、怎麼驗證
- **Shadow traffic / dark launch**：複製真實流量到新系統驗證，但不影響用戶
- **Cutover & rollback**：漸進切換（canary %）、出事怎麼安全退回
- **DevOps**：feature flag、藍綠/金絲雀部署、遷移期的雙重監控（新舊系統同時看）

**Day 57 — PoC + Design:**
- **Design exercise**：把 ScaleUp 的 monolith 訂單模組拆成獨立的 event-driven Order Service，零停機
- 畫出 migration 階段圖：strangler proxy → dual-write → backfill → shadow → cutover → decommission
- **PoC**：用 Go 寫一個 strangler proxy（依 feature flag / % 把請求路由到舊 or 新 handler）+ dual-write 範例
- Notes：每個階段的 failure mode 與 rollback 計畫
- **🔗 連回你的工作**：對照你現在維護的某個系統，這套手法哪一步用得上、哪一步最危險

### Day 58-59: Mock Interview Round 1
**Prerequisites:** All Phase 1-3
**Story:** 模擬面試。小球不再提示。（角色：小球）
**Story beats:** 1. 小球換了一種語氣，冷靜、禮貌但不給任何暗示——完全的面試官模式 2. 你中途卡住，習慣性看向小球求助，但他只是沉默等待 3. 結束後小球恢復正常：「你剛才有 30 秒的沉默，面試中這很致命。我們來練怎麼買時間」

**Day 58 — Mock 1:**
- Full scope-based mock interview (no clock — interviewer drives via turns, redirects, and follow-ups)
- Detailed feedback on 4 dimensions

**Day 59 — Feedback + Re-do:**
- Practice thinking aloud, following interviewer hints
- Re-do weak sections from Day 58's mock

### Day 60-61: Weak Spot Reinforcement
**Prerequisites:** All Phase 1-3
**Story:** 弱點補強衝刺。（角色：小球）
**Story beats:** 1. 小球拿出 Day 56 的 scorecard：「你的 trade-off 分析還是太淺，每次都只講優缺點，沒有量化」 2. 你回頭翻之前的筆記，發現有些概念以為懂了其實只記了表面 3. 小球：「離面試剩不到一週。現在不是學新東西的時候，是把會的磨到刀刃利」

**Day 60 — Review Patterns:**
- Review all notes, identify patterns in mistakes

**Day 61 — Re-do Designs:**
- Re-do 2-3 difficult designs
- Practice articulating trade-offs in 2-3 sentences

### Day 62-63: Final Mock Interview (Brutal Mode)
**Prerequisites:** All Phase 1-3
**Story:** 最終模擬。全力以赴。（角色：小球）
**Story beats:** 1. 小球：「今天我不是你的導師，我是 Google L5 面試官。準備好了嗎？」 2. 面試進行到一半，小球突然改需求：「剛剛說的日活從 10 萬變成 1 億，你的設計還撐得住嗎？」 3. 結束後小球笑了：「不管結果怎樣，你已經不是 Day 1 那個愣住的人了」

**Day 62 — Final Mock 1:**
- Full mock with interruptions and requirement changes (interviewer interrupts mid-thought, swaps a requirement, pushes follow-ups to the knowledge boundary)

**Day 63 — Final Mock 2:**
- Full mock, double trap drills — chaining pivots without losing composure

### Phase 4 Gate
> Full final mock (scope-based, not timed — Day 62 or 63). Scorecard ≥ 6/9 on both final mocks.

---

## PoC Language & Tools

- **Default PoC Language**: Go (chosen for concurrency model and interview relevance)
  - Students can use any language they're comfortable with
- **Diagrams**: Mermaid + whiteboard practice
- **Infrastructure**: Docker Compose for local PoC environments
- **Notes**: Markdown
