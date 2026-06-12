# System Design Interview Curriculum

> Target: Big tech SD interviews (FAANG, AWS, Google, etc.)
> Pace: ~1 hour/day, deep learning over memorization
> Approach: Discussion → PoC → Notes → Reflect

---

## Phase 0: Thinking Framework (Day 1-3)

### Day 1: What SD Interviews Actually Test
**Prerequisites:** None (entry point)
- The 4 scoring dimensions: Problem Navigation, Design, Technical Depth, Trade-offs
- Analyze good vs bad answers for the same question
- **Discussion**: Deconstruct a real SD interview rubric

### Day 2: Back-of-Envelope Estimation
**Prerequisites:** Day 1
- Powers of 2, latency numbers every engineer should know
- Practice: Estimate YouTube daily storage, Twitter QPS
- **Exercise**: Build an estimation cheat sheet you actually understand

### Day 3: Your SD Answer Framework (4-Step Method)
**Prerequisites:** Day 1, Day 2
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

**Day 4 — DNS + LB Fundamentals:**
- DNS fundamentals — resolution flow, TTL, record types
- DNS-based load balancing (weighted, latency-based, failover)
- L4 vs L7 load balancing — when to use which
- Algorithms: Round Robin, Least Connections, IP Hash, Weighted

**Day 5 — Production LB + PoC:**
- Health checks, sticky sessions, connection draining
- **DevOps**: ALB vs NLB, target group health checks
- **PoC**: Nginx L4/L7 LB with Docker Compose

### Day 6-7: Caching & CDN Strategies
**Prerequisites:** Day 3, Day 4-5 (LB)

⚠️ **Common Misconception:** "More cache = always better." No — cache invalidation bugs can cause stale data, and large caches increase memory cost and cold-start time. Cache is a trade-off between speed and freshness.

**Day 6 — Cache Patterns:**
- Cache levels: Browser → CDN → App → DB
- Patterns: Cache-Aside, Write-Through, Write-Behind, Read-Through
- Eviction: LRU, LFU, TTL
- Cache invalidation — the hard problem

**Day 7 — CDN + PoC:**
- CDN: Edge caching, Pull vs Push, cache invalidation strategies
- **DevOps**: ElastiCache cluster mode, CloudFront behaviors, cache hit ratio
- **PoC**: Redis cache layer, measure latency with/without cache

### Day 8-9: Database Selection
**Prerequisites:** Day 3

**Day 8 — SQL vs NoSQL Concepts:**
- SQL vs NoSQL vs NewSQL — decision framework
- Indexing: B-tree (read-optimized) vs LSM-tree (write-optimized)
- Denormalization, sharding intro, connection pooling

**Day 9 — Storage Engine + PoC:**
- WAL, read replicas, consistency trade-offs
- **Data Model Design Template**: Entities → Access patterns → Partition key → Secondary index → Hot partition risk → Backfill strategy
- **PoC**: Same problem with SQL vs NoSQL, compare trade-offs

### Day 10-11: Message Queue & Async Processing
**Prerequisites:** Day 3, Day 8-9 (Database)

⚠️ **Common Misconception:** "Kafka has exactly-once delivery." Kafka has idempotent producers + transactional consumers, which achieves effectively-once processing. True exactly-once in distributed systems requires end-to-end idempotency — the broker alone cannot guarantee it.

**Day 10 — Queue Concepts + Semantics:**
- Why async? Decoupling, buffering, peak handling
- SQS vs Kafka vs RabbitMQ — positioning
- Delivery semantics: at-least-once, at-most-once, exactly-once

**Day 11 — DLQ + PoC:**
- Dead letter queue, retry strategies
- **DevOps**: SQS FIFO vs Standard, DLQ monitoring
- **PoC**: Producer-consumer with failures simulation

### Day 12-13: API Design
**Prerequisites:** Day 3, Day 4-5 (LB)

**Day 12 — API Styles:**
- REST vs gRPC vs GraphQL — trade-off matrix
- Pagination: Offset vs Cursor
- Versioning strategies, idempotency

**Day 13 — API PoC:**
- **PoC**: Design & implement a small API in Go

### Day 14: Security & Authentication
**Prerequisites:** Day 12-13 (API Design)
- JWT vs Session-based authentication
- OAuth 2.0 flow basics
- API Key management, HTTPS, encryption
- **DevOps**: Cognito, OIDC integration, secrets rotation

### Day 15-16: Consistent Hashing & Data Partitioning
**Prerequisites:** Day 8-9 (Database)

⚠️ **Common Misconception:** "Consistent hashing eliminates all data movement." No — it minimizes movement to K/N keys on average when a node joins/leaves, but rebalancing still happens and virtual nodes affect distribution uniformity.

**Day 15 — Theory:**
- Why simple hash mod N fails
- Consistent hashing with virtual nodes
- Range-based vs Hash-based partitioning

**Day 16 — PoC + Checkpoint:**
- **PoC**: Implement consistent hashing from scratch in Go

### Phase 1 Gate
> 15-minute mini-mock: Explain any building block using the 4-step framework. Scorecard ≥ 2/3.

---

## Phase 2: Distributed Systems Core (Day 17-26)

### Day 17-18: CAP Theorem in Practice
**Prerequisites:** Day 8-9 (Database), Day 15-16 (Consistent Hashing)

⚠️ **Common Misconception:** CAP is NOT "pick 2 out of 3 in daily operation." It's about what happens DURING a network partition — you choose between consistency and availability. When there's no partition, you can have both. Teach PACELC as the practical mental model.

**Day 17 — CAP + Examples:**
- CAP is about network partitions, not a daily choice
- Real-world examples: DynamoDB (AP), Zookeeper (CP)

**Day 18 — PACELC + Discussion:**
- PACELC model as a more practical framework
- Discussion: classify real-world systems on the CAP/PACELC spectrum

### Day 19-20: Consistency Models
**Prerequisites:** Day 17-18 (CAP)

⚠️ **Common Misconception:** "Eventual consistency = inconsistent." No — eventual consistency means the system WILL converge to a consistent state given enough time with no new writes. It has a convergence guarantee, unlike "no consistency" which has none.

**Day 19 — Models:**
- Strong, Eventual, Causal, Read-your-writes
- Quorum: W + R > N

**Day 20 — Conflict Resolution + PoC:**
- Vector clocks, conflict resolution
- **PoC**: Simulate eventual consistency

### Day 21-22: Replication & Leader Election
**Prerequisites:** Day 8-9 (Database), Day 19-20 (Consistency)

⚠️ **Common Misconception:** "Read replicas give you strong consistency." No — replicas have replication lag (milliseconds to seconds). Read-after-write consistency requires reading from the leader, or using techniques like session stickiness or synchronous replication.

**Day 21 — Replication Patterns:**
- Single-leader, multi-leader, leaderless
- Raft consensus algorithm (simplified)

**Day 22 — Service Discovery:**
- Service Discovery: Consul, Kubernetes DNS, Cloud Map

### Day 23-24: Rate Limiting & Circuit Breaker
**Prerequisites:** Day 6-7 (Caching), Day 12-13 (API Design)

⚠️ **Common Misconception:** "Token bucket and sliding window are interchangeable." No — token bucket allows bursts up to the bucket size (good for bursty traffic), while sliding window enforces a strict rate limit (better for steady rate enforcement). Choose based on your traffic pattern.

**Day 23 — Algorithms:**
- Token Bucket, Sliding Window, Fixed Window

**Day 24 — Circuit Breaker + PoC:**
- Circuit Breaker pattern (Closed → Open → Half-Open)
- Bulkhead pattern
- **PoC**: Token Bucket + Circuit Breaker implementation in Go

### Distributed Systems Kill Pack (Reference)
- **Idempotency Key**: scope, TTL, storage, behavior
- **Deduplication**: message ID, dedup window, consumer vs infra side
- **Distributed Lock**: lease-based, fencing token, failure modes

### Day 25: Observability Consolidation
**Prerequisites:** Day 4-5 (LB), Day 6-7 (Caching), Day 8-9 (Database)
- Metrics, Logs, Traces — three pillars
- Distributed tracing, SLI/SLO/SLA formalization
- Structured logging, correlation IDs
- How to discuss monitoring in SD interviews

### Day 26: Bloom Filter, Gossip Protocol & Advanced Concepts
**Prerequisites:** Day 15-16 (Consistent Hashing), Day 19-20 (Consistency)
- Bloom Filter: probabilistic membership testing
- Gossip Protocol: node discovery and state sharing
- Distributed Transactions overview (2PC/3PC)

### Phase 2 Gate
> 30-minute mock: Design a distributed key-value store. Scorecard ≥ 3/5.

---

## Phase 3: Classic SD Problems (Day 27-53)

> All Phase 3 topics require completion of Phase 1 + Phase 2 (enforced by Phase Gate).
> Format: Day 1 = Discussion & Design | Day 2 = PoC + Diagram + Notes
> Complex problems get 3 days.

### Tier 1: Must Do (Day 27-45)

#### Day 27-28: URL Shortener ★★☆
**Key Concepts:** Hashing, base62, read-heavy

**Day 27 — Design:**
- Requirements clarification (read:write ratio, URL length, analytics)
- High-level design: API → ID generator → DB → Cache
- Deep dive: base62 encoding, collision handling, custom aliases

**Day 28 — PoC + Diagram:**
- **PoC**: URL shortener service in Go
- Full architecture diagram with 8-block skeleton
- Notes with interview template

#### Day 29-30: Unique ID Generator ★★☆
**Key Concepts:** Snowflake, clock sync, coordination-free

**Day 29 — Design:**
- Requirements: uniqueness, ordering, performance
- Approaches: UUID, DB auto-increment, Snowflake, ULID
- Deep dive: Snowflake bit layout, clock skew handling

**Day 30 — PoC + Diagram:**
- **PoC**: Snowflake ID generator in Go
- Full architecture diagram
- Notes with interview template

#### Day 31-32: Distributed Rate Limiter ★★★
**Key Concepts:** Distributed sliding window, Redis Lua, race conditions

**Day 31 — Design:**
- Single-node vs distributed: new challenges
- Redis-based sliding window with Lua scripts
- Race conditions and how to handle them

**Day 32 — PoC + Diagram:**
- **PoC**: Distributed rate limiter with Redis in Go
- Full architecture diagram
- Notes with interview template

#### Day 33-34: Notification System ★★★
**Key Concepts:** Push/Pull, priority queue, multi-channel

**Day 33 — Design:**
- Multi-channel: push notification, SMS, email
- Priority queue for urgent vs batch notifications
- Delivery guarantees and retry logic

**Day 34 — PoC + Diagram:**
- **PoC**: Notification dispatcher in Go
- Full architecture diagram
- Notes with interview template

#### Day 35-37: Chat System ★★★★
**Key Concepts:** WebSocket, presence, read receipts, group chat

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

#### Day 38-39: Distributed Cache ★★★
**Key Concepts:** Consistent hashing, invalidation at scale, thundering herd

**Day 38 — Design:**
- Distributed cache architecture (consistent hashing for sharding)
- Cache invalidation at scale: TTL, event-driven, versioning
- Thundering herd: locking, request coalescing

**Day 39 — PoC + Diagram:**
- **PoC**: Distributed cache with consistent hashing in Go
- Full architecture diagram
- Notes with interview template

#### Day 40-42: News Feed ★★★★
**Key Concepts:** Fan-out on write/read, ranking, celebrity problem

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

#### Day 43-45: Payment System ★★★★
**Key Concepts:** Idempotency, SAGA, exactly-once, reconciliation

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

### Tier 2: Should Do (Day 46-53)

#### Day 46-47: Metrics & Logging System
**Key Concepts:** Time-series DB, aggregation, sampling

**Day 46 — Design:**
- Data ingestion pipeline: agents → collectors → storage
- Time-series DB selection (InfluxDB, Prometheus, TimescaleDB)
- Aggregation strategies and downsampling

**Day 47 — PoC + Diagram:**
- **PoC**: Metrics pipeline in Go
- Full architecture diagram
- Notes with interview template

#### Day 48-49: Search Autocomplete
**Key Concepts:** Trie, ranking, Elasticsearch

**Day 48 — Design:**
- Trie data structure for prefix matching
- Ranking: frequency-based, personalized
- Elasticsearch integration for full-text search

**Day 49 — PoC + Diagram:**
- **PoC**: Autocomplete service in Go
- Full architecture diagram
- Notes with interview template

#### Day 50-51: Web Crawler
**Key Concepts:** BFS/DFS, URL frontier, dedup (Bloom filter)

**Day 50 — Design:**
- Crawler architecture: URL frontier → fetcher → parser → storage
- BFS vs DFS crawling strategies
- Deduplication with Bloom filter, politeness (robots.txt, rate limiting)

**Day 51 — PoC + Diagram:**
- **PoC**: Web crawler in Go
- Full architecture diagram
- Notes with interview template

#### Day 52-53: Proximity Service
**Key Concepts:** Geohash, QuadTree, spatial indexing

**Day 52 — Design:**
- Geohash: encoding lat/lng into a string for range queries
- QuadTree: spatial partitioning for nearest-neighbor
- Trade-offs: Geohash (simple, DB-friendly) vs QuadTree (dynamic, memory)

**Day 53 — PoC + Diagram:**
- **PoC**: Proximity search service in Go
- Full architecture diagram
- Notes with interview template

### Phase 3 Gate
> 45-minute full mock on a Tier 1 problem. Scorecard ≥ 5/7.

### Tier 3: Nice to Have (Optional)

Video Streaming, Cloud Storage, Distributed Task Scheduler, Ticket/Booking System — concepts already covered by Tier 1/2.

---

## Phase 4: Advanced & Mock Interviews (Day 54-61)

### Day 54-55: Trade-off Analysis Deep Dive
**Prerequisites:** All Phase 1-3

**Day 54 — Trade-off Scenarios:**
- Practice specific trade-off scenarios (5 min each)
- Cost estimation for designs

**Day 55 — Trap & Pivot Drills:**
- Trap & Pivot Drills — practice graceful pivots when initial design hits a wall

### Day 56-57: Mock Interview Round 1
**Prerequisites:** All Phase 1-3

**Day 56 — Mock 1:**
- 45-minute strictly timed mock interview
- Detailed feedback on 4 dimensions

**Day 57 — Feedback + Re-do:**
- Practice thinking aloud, following interviewer hints
- Re-do weak sections from Day 56's mock

### Day 58-59: Weak Spot Reinforcement
**Prerequisites:** All Phase 1-3

**Day 58 — Review Patterns:**
- Review all notes, identify patterns in mistakes

**Day 59 — Re-do Designs:**
- Re-do 2-3 difficult designs
- Practice articulating trade-offs in 2-3 sentences

### Day 60-61: Final Mock Interview (Brutal Mode)
**Prerequisites:** All Phase 1-3

**Day 60 — Final Mock 1:**
- 45-minute interview with interruptions and requirement changes

**Day 61 — Final Mock 2:**
- 45-minute interview, double trap drills — chaining pivots without losing composure

### Phase 4 Gate
> 45-minute final mock (Day 60 or 61). Scorecard ≥ 5/7 on both final mocks.

---

## PoC Language & Tools

- **Default PoC Language**: Go (chosen for concurrency model and interview relevance)
  - Students can use any language they're comfortable with
- **Diagrams**: Mermaid + whiteboard practice
- **Infrastructure**: Docker Compose for local PoC environments
- **Notes**: Markdown
