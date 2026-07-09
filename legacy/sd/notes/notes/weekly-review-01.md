# Weekly Review #1 — Recall Gaps & Improvement Plan

> Status: ✅ Session 10
> Topics reviewed: Database Selection, Load Balancer, Caching & CDN

---

## 📊 Recall Scores

| Topic | Score | Before → After |
|-------|-------|----------------|
| Database Selection | 3/4 | 🟡 → 🟡 |
| Load Balancer | 1/4 | 🟢 → 🟡 |
| Caching & CDN | 0/4 | 🟢 → 🔴 |

---

## 🔴 My Mistakes & Misconceptions

### Database Selection

| What I Said | Correct Answer | How to Fix |
|---|---|---|
| "SQL is read-heavy, NoSQL is write-heavy" | 這是 **storage engine**（B-tree vs LSM-tree）的差別，不是 SQL vs NoSQL 的差別。SQL vs NoSQL 的關鍵是 data model + query pattern + consistency | 記住兩條獨立的軸：① SQL vs NoSQL = data relationship + schema flexibility ② B-tree vs LSM-tree = read vs write optimization。不要混在一起 |
| Interview Drill 看到大量資料就選 NoSQL（改善中） | 資料量大不代表要選 NoSQL。SQL 加 sharding 也能處理。要先分析 access pattern | 面試時先問自己：「資料之間有沒有關聯？需要 JOIN 嗎？需要 ACID 嗎？」再決定 |

### Load Balancer

| What I Said | Correct Answer | How to Fix |
|---|---|---|
| One-liner: "protect and hide server" | LB 的三大功能：**High Availability、Horizontal Scalability、Zero-Downtime Deployment** | 背口訣：**HA + HS + ZD**。"Protect and hide" 是 reverse proxy 的功能，不是 LB 的核心價值 |
| Trade-off: 只描述 L4/L7 是什麼 | 要說 trade-off：**L4 = lower latency + higher throughput（不解析 HTTP）；L7 = content-based routing 但多了 HTTP parsing overhead** | 面試回答公式：「我會選 X over Y，because [gain]，代價是 [cost]」 |
| LB algorithms: 說成 "Latency" | **RWLI** = Round Robin, Weighted RR, **Least Connections**, IP Hash | L = **L**east Connections（不是 Latency）。記法：RWLI，第三個是 Least |
| DevOps 完全空白 | Health check interval + unhealthy threshold、Connection draining timing、NLB 支援 Elastic IP（固定 IP）、Route 53 canary | 背四個關鍵字：**Health / Drain / EIP / Canary** |
| Sticky session vs Redis 解釋模糊 | Sticky session = 用 cookie 把 user pin 在同一台 server（**stateful**，server 掛了 session 就沒了）。Redis external store = 所有 server 共用 Redis 存 session（**stateless**，任何 server 都能服務任何 user） | 關鍵區別：sticky = stateful（綁 server），Redis = stateless（綁 store）。面試要說清楚這是「相反的策略」 |

### Caching & CDN

| What I Said | Correct Answer | How to Fix |
|---|---|---|
| One-liner: 說成 CDN/CloudFront | Caching = 把常用資料放在**更快的儲存層**（如 Redis）擋在 DB 前面，降低 latency + DB load | CDN 只是 caching 的其中一層。面試被問 "What is caching?" 要從 Redis/app cache 開始講，不是從 CDN 開始 |
| Trade-off: 只描述 Cache-Aside / Write-Through 機制 | 要說 **when/why**：Write-Through = 資料一致性要求高 + read-heavy（如 user profile）；Write-Behind = 高寫入量 + 可容忍短暫 data loss（如 game score）；Cache-Aside = 最通用，lazy loading | 面試公式：「I'd pick X **when** [scenario], **because** [reason], the cost is [trade-off]」 |
| Scale trigger: "save DB and more fast" | 具體數字：**DB P99 > 50ms** 或 **QPS 超過單機 DB 上限** → 加 Redis，目標 **hit ratio > 90%** | 面試要給數字，不要只說「比較快」 |
| DevOps: 空白 | **3 metrics**: cache hit ratio、eviction rate、memory usage。Alert: hit ratio drop > 10% in 5min | 背三個字：**Hit / Evict / Mem** |

---

## ✅ Mistakes Resolved This Session

| Topic | Mistake | How I Proved It |
|---|---|---|
| Database | LSM-tree 讀寫搞反 | Correctly answered: B-tree = read-optimized, LSM-tree = write-optimized |
| Load Balancer | DNS-based LB limitations | Correctly answered: TTL stale IP + no real-time health check |

---

## 🎤 How to Say It in Interview — 改進版

### Load Balancer

**Opening (30 sec):**
> "A Load Balancer distributes traffic across multiple backend servers to achieve three things: high availability, horizontal scalability, and zero-downtime deployments. The key trade-off is L4 vs L7 — L4 gives lower latency and higher throughput because it doesn't parse HTTP, while L7 enables content-based routing like path-based routing for microservices, at the cost of parsing overhead."

**DevOps depth:**
> "In production, I'd configure health checks on a `/health` endpoint with a 30-second interval, set connection draining to 30 seconds for fast APIs, and use NLB if I need static Elastic IPs. For canary deployments, I'd use Route 53 weighted routing with a 90/10 split."

### Caching

**Opening (30 sec):**
> "Caching places a faster store like Redis in front of a slower store like a database to reduce latency and DB load. I'd add a cache layer when DB query P99 exceeds 50ms or QPS hits the single-node limit, targeting a hit ratio above 90%. The main trade-off is freshness vs speed — Cache-Aside is the most common pattern for read-heavy workloads with lazy loading."

**DevOps depth:**
> "In production, I'd monitor cache hit ratio, eviction rate, and memory usage. A sudden hit ratio drop over 10% in 5 minutes usually means a key pattern change or a cold start after deployment."

---

## 📝 Recall Cheatsheet（下次 session 前複習）

| Topic | 記住這些 |
|---|---|
| **LB One-liner** | HA + Horizontal Scalability + Zero-Downtime |
| **LB Algorithms** | RWLI = Round Robin, Weighted, **Least Connections**, IP Hash |
| **LB DevOps** | Health / Drain / EIP / Canary |
| **Cache One-liner** | Faster store in front of slower store → reduce latency + DB load |
| **Cache Trade-off** | Write-Through = consistency, Write-Behind = speed, Cache-Aside = 通用 |
| **Cache Scale** | P99 > 50ms or QPS > single DB → Redis, hit ratio > 90% |
| **Cache DevOps** | Hit / Evict / Mem |
| **DB 兩條軸** | ① SQL vs NoSQL = data model ② B-tree vs LSM = storage engine |

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| database selection is process of choosing the right database type based on you'r system patterns consistency or scale query requirements | Database selection is the process of choosing the right database type — SQL, NoSQL, or NewSQL — based on your system's access patterns, consistency needs, and scalability requirements. |
| SQL vs NoSQL the trade-off is SQL is good for read heavy NoSQL is write heavy and SQL have ACID | The key trade-off is about data model and query patterns: SQL excels with relational data, JOINs, and ACID transactions; NoSQL excels with flexible schemas, simple access patterns, and horizontal scaling. |
| LBs can protect and hide server and distributing traffic | A Load Balancer distributes traffic across multiple backend servers to achieve high availability, horizontal scalability, and zero-downtime deployments. |
| L7 like nlb tcp or udp L7 is ALB http or https path base so if use microservice use alb | L4, like NLB, operates at the TCP/UDP level with lower latency and higher throughput. L7, like ALB, operates at HTTP/HTTPS with path-based routing — ideal for microservices, but at the cost of HTTP parsing overhead. |
| caching is CDN in aws is cloudfront can in edge location do cache | Caching places frequently accessed data in a faster store — like Redis in front of a database — to reduce latency and DB load. CDN is just one caching layer, specifically for static content at edge locations. |
| cache-aside is app hit cache and cache hit db and write cache, write-through is write data cache first and than write db | Cache-Aside means the app checks cache first; on a miss, it reads from DB and lazily writes back to cache. Write-Through synchronously writes to both cache and DB, ensuring strong consistency but with higher write latency. |
| nosql is good because activity log is write heavy and usually see recent log | For activity logs, NoSQL could be a good fit because the workload is write-heavy and we typically query only recent data — but I'd also evaluate whether PostgreSQL with time-based partitioning could handle the load before committing. |
