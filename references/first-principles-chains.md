# First-Principles Derivation Chains

> **How to use this file:** Each chain defines physical constraints (the anchors) and a derivation direction (the arrows). 小球 uses these as reference material to guide the student naturally — NOT as a script to read verbatim. Present the constraints, ask the launch question, and let the student's reasoning determine the path.

## Chain Format

```
Physical constraints → Launch question → Derivation direction → Expected insight
基礎層: single-constraint, straight-line derivation
進階層: multi-constraint, trade-off analysis
Micro-exercise (Build): ASCII/pseudocode/mental-model task
Transfer question (Teach): Feynman Gate question for Yuki
```

---

## Concept Dependency Graph

```
Phase 1 (independent entry points — teach in curriculum order):

  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │Load Bal. │   │ Caching  │   │ Database │   │ Msg Queue│
  │(Day 4-5) │   │(Day 6-7) │   │(Day 8-9) │   │(Day10-11)│
  └──────────┘   └──────────┘   └──────────┘   └──────────┘
  CPU/mem limit   Latency gap    Read/write      Cascade
                                 patterns        failure

  ┌──────────┐   ┌──────────┐   ┌──────────────┐
  │API Design│   │ Security │   │Consistent Hash│
  │(Day12-13)│   │ (Day 14) │   │ (Day 15-16)  │
  └──────────┘   └──────────┘   └──────┬───────┘
  Client needs   Plaintext risk        │
                                       │ builds on
                               ┌───────┴──────────┐
                               ▼                   ▼
Phase 2:                 ┌─────────┐        ┌──────────┐
                         │   CAP   │        │Consistency│
                         │(Day17-18)│       │ (Day19-20)│
                         └────┬────┘        └─────┬────┘
                              │                   │
                              └─────────┬─────────┘
                                        ▼
                                 ┌──────────────┐
                                 │ Replication  │
                                 │ (Day 21-22)  │
                                 └──────────────┘

  ┌────────────┐   ┌──────────┐   ┌──────────┐
  │Rate Limiting│  │Observ.   │   │Bloom/Goss│
  │(Day 23-24) │  │(Day 25)  │   │(Day 26)  │
  └────────────┘  └──────────┘   └──────────┘
  System capacity  Distributed    Sub-linear
  limits           debugging      membership
```

> **Note:** This graph shows *conceptual* dependencies between derivation chains (which physical concepts build on which). Teaching order follows `curriculum.md` prerequisites.

---

# Phase 1 Chains

---

## 推導鏈 #1: Load Balancer (Day 4-5)

**Physical constraints:**
- 單機 CPU 核心數有限（典型 8-64 cores）
- 單機記憶體有限（典型 16-256 GB）
- 單機網路頻寬有限（典型 1-10 Gbps）
- 單一 process 的 concurrent connection 有上限（C10K problem: ~10K connections）

**Launch question:**
「一台伺服器最多能處理多少 request？如果流量超過這個上限，怎麼辦？」

### 基礎層

**Derivation direction:**
單機有物理上限 → 流量超過上限時服務降級或崩潰 → 必須用多台機器分攤 → 需要一個「分配器」決定每個 request 去哪台 → 這就是 Load Balancer

**Expected insight:** LB 的存在不是為了「好的架構」，而是因為單機硬體有物理極限。

### 進階層

**Additional constraints:**
- L4 (TCP) 只看 IP/port，每秒可處理 ~百萬連線
- L7 (HTTP) 需解析 header/body，每秒 ~十萬連線但能做 content-based routing
- Session state: 某些請求需要回到同一台（sticky session vs stateless design）

**Derivation direction:**
L4 快但笨 → L7 慢但聰明 → 選擇取決於「是否需要看請求內容」 → sticky session 是 LB 的反模式（為什麼？）

**Micro-exercise (Build):**
小球畫出以下骨架，學生填入 `???`：
```
Client → [LB: ??? algorithm] → Server A (CPU intensive)
                              → Server B (CPU intensive)
                              → Server C (idle)
Q: 用 Round Robin 還是 Least Connections？為什麼？
```

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 sticky session 會破壞 Load Balancer 的初衷？」

---

## 推導鏈 #2: Caching (Day 6-7)

**Physical constraints:**
- DRAM: ~100ns 存取延遲
- SSD: ~100μs（比 DRAM 慢 1000x）
- Network round-trip: ~1ms（比 DRAM 慢 10000x）
- DRAM 價格 ~$5/GB，SSD ~$0.10/GB（DRAM 貴 50x）

**Launch question:**
「DRAM 比 SSD 快 1000 倍，比網路快 10000 倍。如果某些資料被反覆讀取，你會怎麼做？」

### 基礎層

**Derivation direction:**
延遲差距巨大 → 常讀資料放到快的儲存層可省 999x+ 延遲 → 但 DRAM 貴 50x，不能全放 → 只放「常用的」 → 需要淘汰策略（LRU/LFU） → 需要一致性策略（TTL/invalidation）

**Expected insight:** Cache = 讓常用資料待在快的儲存層。淘汰和一致性是 cache 容量有限的直接後果。

### 進階層

**Additional constraints:**
- 讀寫比：95:5 vs 50:50 對 cache 效益影響巨大
- Hit rate 99% → 95%：miss 量增加 5 倍
- 分散式環境：cache invalidation 變成分散式一致性問題

**Derivation direction:**
讀寫比決定 cache 策略 → write-heavy 時 write-through 成本高 → hit rate 微降 = miss 量暴增（非線性） → 多節點 cache 的 invalidation 是分散式一致性問題的子集

**Micro-exercise (Build):**
「讀寫比 95:5 的系統 vs 50:50 的系統，分別適合什麼 cache 策略？為什麼？用 1-2 句話描述每個選擇。」

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 cache hit rate 從 99% 掉到 95% 會讓延遲暴增？」

---

## 推導鏈 #3: Database Selection (Day 8-9)

**Physical constraints:**
- B-tree 索引：讀取 O(log N)，寫入需維護索引（寫放大）
- LSM-tree：寫入 O(1) amortized（append-only），讀取需合併多層（讀放大）
- 行式儲存：整行一起讀，適合 OLTP（讀一筆完整紀錄）
- 列式儲存：同欄位連續存放，適合 OLAP（掃描某欄位聚合）

**Launch question:**
「如果你的系統每秒寫入 10 萬筆資料但很少讀，跟每秒讀取 10 萬筆但很少寫，底層的儲存結構會一樣嗎？」

### 基礎層

**Derivation direction:**
讀寫模式不同 → 最佳儲存結構不同 → 讀多寫少：B-tree/RDBMS → 寫多讀少：LSM-tree/NoSQL → 沒有「最好的資料庫」，只有「最適合這個 workload 的資料庫」

**Expected insight:** 資料庫選擇不是信仰（SQL vs NoSQL），而是從 workload 的讀寫模式推導出最佳儲存結構。

### 進階層

**Additional constraints:**
- ACID 事務：強一致性但需要 lock，限制 throughput
- 關聯查詢：RDBMS 的 JOIN vs NoSQL 的 denormalization
- Schema 彈性：fixed schema vs schema-less 的開發速度 vs 資料品質 trade-off

**Derivation direction:**
一致性需求 → ACID 的成本 → 是否值得付這個成本取決於業務需求 → 什麼時候 denormalization 比 JOIN 更好？

**Micro-exercise (Build):**
小球畫出以下骨架，學生填入 `???`：
```
用戶 Profile (讀多寫少, 需要 JOIN) → DB: ???
用戶行為 Log (寫多讀少, append-only) → DB: ???
理由: ???
```

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 Instagram 用 PostgreSQL 存貼文但用 Cassandra 存 feed？」

---

## 推導鏈 #4: Message Queue (Day 10-11)

**Physical constraints:**
- 同步呼叫：caller 必須等待 callee 回應（耦合）
- 如果 callee 掛了：caller 也跟著 timeout/失敗（級聯故障）
- 處理時間差異：某些任務需要 100ms，某些需要 10 分鐘
- 流量尖峰：黑五流量可能是平時的 100x

**Launch question:**
「如果服務 A 同步呼叫服務 B，而 B 掛了 30 秒，會發生什麼事？如果同時有 100 個服務都依賴 B 呢？」

### 基礎層

**Derivation direction:**
同步呼叫 = 命運綁定 → 一個慢 = 全部慢（級聯故障） → 需要「解耦」機制 → 放一個中間人暫存訊息 → caller 送完就走，callee 自己的節奏消化 → 這就是 Message Queue

**Expected insight:** MQ 的核心價值是「時間解耦」和「故障隔離」，不只是「非同步」。

### 進階層

**Additional constraints:**
- At-most-once vs at-least-once vs exactly-once 語義的實現成本差異
- 順序保證：全局順序 vs 分區順序 vs 無序
- Consumer group：多個消費者如何分攤 workload 又不重複處理

**Derivation direction:**
exactly-once 需要 producer 冪等 + consumer 事務 → 代價很高 → 大多數場景用 at-least-once + 冪等消費者 → 順序保證的代價是什麼？

**Micro-exercise (Build):**
小球畫出兩個場景，學生指出差異：
```
場景 A (無 MQ): 訂單服務 --同步呼叫--> 庫存服務 (100x 流量湧入)
場景 B (有 MQ): 訂單服務 --> [???] --> 庫存服務 (100x 流量湧入)
Q: 庫存服務掛了 30 秒，A 和 B 各發生什麼事？
```

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 Kafka 說的 "exactly-once" 其實是 "effectively-once"？」

---

## 推導鏈 #5: API Design (Day 12-13)

**Physical constraints:**
- 不同客戶端（手機、網頁、IoT）有不同資料需求和頻寬限制
- 手機：頻寬有限、電量有限 → 每次 request 都是成本
- 網頁：可以大量請求但使用者期望 <100ms 回應
- API 一旦發布，改動成本極高（breaking change 影響所有客戶端）

**Launch question:**
「手機 app 只需要用戶名稱和頭像，但 API 回傳了完整的用戶資料（50 個欄位）。這有什麼問題？」

### 基礎層

**Derivation direction:**
不同客戶端需要不同資料 → over-fetching 浪費頻寬 → under-fetching 需要多次 request → 需要一種方式讓客戶端「點菜」→ REST（固定菜單）vs GraphQL（自選菜單）各有適用場景

**Expected insight:** API 設計的核心矛盾是「通用性 vs 效率」。REST 和 GraphQL 不是新舊替代，而是不同 trade-off。

### 進階層

**Additional constraints:**
- 版本管理：URL versioning vs header versioning vs GraphQL schema evolution
- Rate limiting 在 API 層的實現
- gRPC：binary protocol，延遲低但瀏覽器支援差（適合 service-to-service）

**Derivation direction:**
外部 API → REST（通用、可 cache） → 內部微服務 → gRPC（快、type-safe） → 前端密集互動 → GraphQL（彈性） → 選擇取決於「誰在呼叫、頻率多高、資料多複雜」

**Micro-exercise (Build):**
「Social media 的手機版 feed 只需要 title + thumbnail，網頁版 dashboard 需要完整資料。用 REST（固定 endpoint）還是 GraphQL（自選欄位）？列出你的選擇和理由。」

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 Netflix 對外用 REST 但對內用 gRPC？」

---

## 推導鏈 #6: Security & Auth (Day 14)

**Physical constraints:**
- HTTP 是明文傳輸 → 網路上任何節點都能看到內容
- 密碼如果明文存資料庫 → 一次 breach 洩漏所有用戶密碼
- 每個 request 都需要驗證身份 → 不能每次都查 DB（太慢）
- Token 有效期越長越方便，但被盜用的風險也越大

**Launch question:**
「如果你在咖啡廳用公共 WiFi 登入銀行帳戶，HTTP 明文傳輸的話會發生什麼？」

### 基礎層

**Derivation direction:**
明文可被竊聽 → 需要加密（HTTPS/TLS） → 密碼不能明文存 → 需要 hash（bcrypt） → 每次 request 查 DB 驗身份太慢 → 需要 token（JWT） → token 是「自包含的身份證明」

**Expected insight:** 每一層安全機制都是對應一個具體的物理/網路威脅，不是「最佳實踐清單」。

### 進階層

**Additional constraints:**
- JWT 是 stateless（不用查 DB）但無法主動撤銷 → refresh token 機制
- OAuth2：委託第三方驗證身份 → 信任鏈的概念
- RBAC vs ABAC：權限粒度 vs 管理複雜度

**Derivation direction:**
stateless token 無法撤銷 → 短效 access token + 長效 refresh token → OAuth2 的核心是「信任委託」而非「登入按鈕」→ 權限模型取決於業務複雜度

**Micro-exercise (Build):**
小球畫出以下流程，學生填入 `???`：
```
1. 用戶登入 → Server 回傳 [???] + [???]
2. 用戶存取 API → 帶上 [???]，Server 驗證（需要查 DB 嗎？???）
3. [???] 過期 → 用 [???] 去換新的
4. 用戶被停權 → 如何讓已發出的 token 失效？???
```

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 JWT 不能只設 24 小時過期就好，還需要 refresh token？」

---

## 推導鏈 #7: Consistent Hashing (Day 15-16)

**Physical constraints:**
- hash(key) mod N：當 N（節點數）改變時，幾乎所有 key 都要重新分配
- 分散式系統中節點增減是常態（擴容、故障、維護）
- 資料搬遷有成本：網路頻寬、時間、期間的不一致狀態

**Launch question:**
「你有 4 台 cache server，用 hash(key) mod 4 分配。現在要加第 5 台，會發生什麼事？」

### 基礎層

**Derivation direction:**
mod N 的問題：改 N → ~100% 資料重分配 → 需要一種「改 N 時只搬少量資料」的方法 → 把 hash space 變成環 → 每個節點佔環上一段 → 增減節點只影響相鄰區段 → 平均只搬 K/N 的資料

**Expected insight:** Consistent Hashing 解決的不是「怎麼分配」，而是「怎麼在節點變動時少搬資料」。

### 進階層

**Additional constraints:**
- 節點能力不均：虛擬節點（virtual nodes）讓強機器佔更多點
- 熱點問題：某些 key 特別熱門 → 即使均勻分配也可能單節點過載
- 環上相鄰節點同時故障 → 資料可用性問題

**Derivation direction:**
實體節點不均勻 → virtual nodes 改善 → 但增加 routing table 大小 → 熱點需要額外機制（replication/splitting） → 沒有完美分配，只有「可接受的不均勻」

**Micro-exercise (Build):**
小球畫出以下 hash ring，學生回答問題：
```
        Node A (v1, v2, v3)
       /                    \
  Node D                  Node B
  (v1, v2, v3)            (v1, v2, v3)
       \                    /
        Node C (v1, v2, v3)

Q1: key "user:123" hash 到 Node B-v2 和 Node C-v1 之間，資料在哪？
Q2: Node C 掛了，它的資料搬去哪？搬多少？
```

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 DynamoDB 和 Cassandra 都用 consistent hashing 而不是 mod N？」

---

# Phase 2 Chains

---

## 推導鏈 #8: CAP Theorem (Day 17-18)

**Physical constraints:**
- 光速有限：跨資料中心通訊有不可壓縮的延遲（地球兩端 ~150ms RTT）
- 網路 partition 是事實，不是「萬一」（海底電纜斷裂、路由故障、雲端 AZ 隔離）
- 一致性（所有節點看到相同資料）需要等待同步完成

**Launch question:**
「兩個資料中心之間的光纖斷了。你的系統還能同時保證『所有人看到一樣的資料』和『所有人都能繼續操作』嗎？」

### 基礎層

**Derivation direction:**
partition 不可避免（物理事實） → partition 發生時必須選擇 → 等同步完再回應（Consistency，犧牲 Availability） → 不等同步直接回應（Availability，犧牲 Consistency） → 「三選二」是誤導 → 真正的選擇是「partition 發生時，選 C 還是 A？」

**Expected insight:** CAP 不是日常選擇題，而是「網路分區時的緊急決策」。平時可以同時有 C 和 A。

**Depends on:** Consistent Hashing (#7) — 理解分散式資料分佈後才能理解為什麼 partition 影響一致性

### 進階層

**Additional constraints:**
- PACELC：即使沒有 partition，Latency 和 Consistency 也有 trade-off
- 不同操作可以有不同的 CAP 選擇（讀 CP、寫 AP 是合法的）

**Derivation direction:**
即使無 partition → latency vs consistency 仍存在 → PACELC 模型 → 每個操作獨立決策，不需要整個系統一刀切

**Micro-exercise (Build):**
「電商場景，partition 發生時：商品庫存選 CP 還是 AP？用戶評論選 CP 還是 AP？各用 1 句話說明理由。」

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼面試時說 "CAP 就是三選二" 是錯的？」

---

## 推導鏈 #9: Consistency Models (Day 19-20)

**Physical constraints:**
- 光速有限：寫入節點 A 後，節點 B 不可能瞬間知道
- 同步複製延遲 = 節點間 RTT（同 AZ ~0.5ms，跨 region ~50-150ms）
- 更強的一致性 = 更高的延遲 = 更低的 throughput

**Launch question:**
「你在台北寫了一筆資料，東京的用戶 1ms 後去讀，能讀到嗎？為什麼？」

### 基礎層

**Derivation direction:**
光速限制 → 跨節點同步需要時間 → 「馬上一致」的代價是等待 → 等待 = 延遲 → 不同業務能容忍不同程度的不一致 → Strong / Causal / Eventual 是不同「等多久」的選擇

**Expected insight:** 一致性模型不是「好壞」而是「延遲預算」。Eventual ≠ 不一致，而是「保證最終會一致，但不保證什麼時候」。

**Depends on:** CAP Theorem (#8) — 理解 partition 時的 C vs A 選擇後，才能理解平時的一致性光譜

### 進階層

**Additional constraints:**
- Linearizability 需要全局順序 → 通常需要 consensus protocol（Paxos/Raft），成本高
- Causal consistency：只要求因果順序，不要求全局順序 → 成本較低
- Read-your-writes：最常見的用戶期望（我寫的東西我馬上能看到）

**Derivation direction:**
全局順序太貴 → 大多數場景只需要因果順序或 read-your-writes → 實現方式：寫完讀同一節點 / version vector / 邏輯時鐘

**Micro-exercise (Build):**
小球列出三個操作，學生填入一致性等級：
```
1. 發文後看自己的 timeline → 需要 ??? consistency
2. 發文後朋友看 feed      → 需要 ??? consistency
3. 兩人同時編輯共用文件    → 需要 ??? consistency
理由: ???
```

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 "eventual consistency = 不一致" 是錯的？」

---

## 推導鏈 #10: Replication (Day 21-22)

**Physical constraints:**
- 硬碟年故障率 ~2-4%（AFR）
- 伺服器年故障率 ~2-10%
- 單點 = 單點故障（SPOF）
- 資料一旦丟失，可能無法恢復

**Launch question:**
「一台伺服器一年有 2-10% 的機率故障。如果這台機器存著你唯一的用戶資料，你能接受嗎？」

### 基礎層

**Derivation direction:**
硬體會壞（物理事實） → 單點 = 風險不可接受 → 資料必須存多份 → 存多份 = replication → 問題變成「多份資料怎麼保持一致？」

**Expected insight:** Replication 的動機是「硬體必然故障」，方案選擇取決於「對一致性和延遲的要求」。

**Depends on:** CAP (#8) + Consistency Models (#9) — replication 的核心問題就是「多份資料的一致性」

### 進階層

**Additional constraints:**
- 同步複製：一致但慢（寫入要等所有 replica 確認）
- 非同步複製：快但可能丟資料（primary 掛了，未複製的寫入丟失）
- 半同步：折中（等 1-2 個 replica 確認）
- Leader-based vs leaderless：寫入衝突處理的複雜度差異

**Derivation direction:**
同步太慢 → 非同步可能丟資料 → 半同步是常見折中 → leaderless 避免 leader 瓶頸但需要衝突解決 → 選擇取決於「能丟多少資料（RPO）、能停多久（RTO）」

**Micro-exercise (Build):**
小球畫出以下場景，學生回答問題：
```
Leader ──async──> Replica 1 (延遲 50ms)
       ──async──> Replica 2 (延遲 200ms)

Leader 在 t=0 收到一筆寫入，t=100ms 掛了。
Q1: Replica 1 和 2 各有沒有這筆資料？
Q2: 如果 Replica 2 被選為新 Leader，會發生什麼？
```

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 read replica 不等於 strong consistency？」

---

## 推導鏈 #11: Rate Limiting (Day 23-24)

**Physical constraints:**
- 任何系統都有處理能力上限（CPU、記憶體、DB connections 有限）
- 超過上限 → 服務降級或完全不可用
- 惡意流量（DDoS）和合法流量尖峰外觀相似
- 處理一個惡意 request 和處理一個正常 request 消耗相同資源

**Launch question:**
「你的 API server 最多能處理 10,000 req/s。如果突然來了 100,000 req/s，你有兩個選擇：全部接受（然後全部慢），或者只接受 10,000 個（其他拒絕）。哪個對用戶更好？」

### 基礎層

**Derivation direction:**
系統有上限 → 超過上限全部受影響 → 不如主動拒絕超額部分 → 保護 10,000 個正常請求 → 需要一個「閘門」計算速率 → 這就是 Rate Limiter

**Expected insight:** Rate Limiting 是「保護大多數人的服務品質」，不是「限制用戶」。

### 進階層

**Additional constraints:**
- Token Bucket：允許突發但限制平均速率
- Sliding Window：精確計數但記憶體成本高
- 分散式 Rate Limiting：多台 API server 需要共享計數（Redis）→ 增加延遲
- 不同粒度：per-user、per-IP、per-API-key → 各有適用場景

**Derivation direction:**
Token Bucket vs Sliding Window → 突發友好 vs 精確計數 → 分散式場景需要集中式計數器 → 集中式計數器本身成為瓶頸怎麼辦？→ local + global 的混合方案

**Micro-exercise (Build):**
「Token Bucket：bucket size=100, refill rate=10/s。兩個場景各發生什麼事？」
```
場景 A: 一次湧入 150 個 request
  → 前 ??? 個通過，剩下 ??? 個被 ???
場景 B: 穩定 5 req/s 持續 30 秒
  → bucket 狀態？會不會被限流？為什麼？
```

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 token bucket 和 sliding window 不能互換使用？」

---

## 推導鏈 #12: Observability (Day 25)

**Physical constraints:**
- 分散式系統有數十到數千個節點
- 不可能 ssh 到每台機器看 log（物理和權限上都不可行）
- 一個 request 可能跨越 5-20 個服務
- 問題往往在「服務之間」而非「服務之內」

**Launch question:**
「你的微服務系統有 50 個服務。用戶回報 "載入很慢"。你要從哪裡開始查？」

### 基礎層

**Derivation direction:**
無法逐台 ssh → 需要集中式的可見性 → 三根支柱：Logs（事件發生了什麼）、Metrics（數字趨勢）、Traces（一個 request 的完整旅程） → 三者缺一會有盲區

**Expected insight:** Observability 三支柱不是「功能清單」，而是回答三個不同問題的工具：Logs=什麼、Metrics=多少、Traces=流經哪裡。

### 進階層

**Additional constraints:**
- Log 量隨流量線性增長 → 全量存太貴 → 需要 sampling
- Metrics 的 cardinality 爆炸（每個 user_id 一條 metric → 百萬 time series）
- Trace propagation 需要所有服務配合（一個服務沒埋 → 斷鏈）

**Derivation direction:**
全量太貴 → sampling 策略（head-based vs tail-based） → 高 cardinality metrics 的解法（聚合 vs 預計算） → 100% trace 覆蓋率的組織挑戰

**Micro-exercise (Build):**
小球列出三種工具，學生填入能看到 / 看不到的東西：
```
情境: 用戶回報「載入很慢」，50 個微服務

| 工具    | 能看到          | 看不到          |
|---------|----------------|----------------|
| Logs    | ???            | ???            |
| Metrics | ???            | ???            |
| Traces  | ???            | ???            |
```

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼只有 logs 和 metrics 不夠，還需要 distributed tracing？」

---

## 推導鏈 #13: Bloom Filter & Gossip Protocol (Day 26)

**Physical constraints:**
- 精確成員查詢（「X 在不在集合裡？」）需要 O(N) 空間
- 百萬筆資料的精確查找 → 數 MB 到 GB 的記憶體
- 分散式系統中每個節點廣播狀態給所有其他節點 → O(N²) 訊息量
- 節點越多，全量廣播越不可行

**Launch question (Bloom):**
「你有 10 億筆黑名單。每次 request 都要查 "這個 IP 在不在黑名單裡"。全部存記憶體太貴，查 DB 太慢。怎麼辦？」

### 基礎層

**Derivation direction (Bloom):**
精確查詢太貴 → 如果接受「可能有 false positive 但絕不 false negative」→ 用多個 hash function 壓縮空間 → 10 億筆只需 ~1.2 GB（vs 精確查詢可能 >10 GB）→ trade-off：空間 vs 準確度

**Launch question (Gossip):**
「100 個節點需要知道彼此的狀態。全量廣播 = 100×99 條訊息。有沒有更省的方式？」

**Derivation direction (Gossip):**
全量廣播 O(N²) 不 scale → 模仿流言傳播：每個節點隨機告訴幾個鄰居 → O(N log N) 訊息量 → 最終所有人都知道 → trade-off：收斂速度 vs 訊息量

**Expected insight:** Bloom 和 Gossip 的核心思想相同 — 用「近似」或「最終」來換取巨大的效率提升。精確和即時是昂貴的。

### 進階層

**Additional constraints:**
- Bloom Filter 不支援刪除 → Counting Bloom Filter（增加空間）
- Gossip 的收斂時間 O(log N) 但常數可能很大 → 緊急消息可能需要直接廣播
- Bloom 的 false positive rate 和 hash function 數量、bit array 大小的數學關係

**Derivation direction:**
近似的代價：Bloom 不能刪除 → 解法增加複雜度 → Gossip 收斂慢 → 緊急場景需要 hybrid approach → 何時「近似夠好」vs「必須精確」的判斷

**Micro-exercise (Build):**
「10 億筆資料，可接受 1% false positive rate。用公式 m = -n·ln(p)/(ln2)² 估算需要多少 bit？換算大約幾 GB？這跟精確儲存 10 億筆 ID 比起來省了多少？」

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 Cassandra 用 Gossip Protocol 而不是中心化的 membership service？」

---

# Phase 3 Chains（新 archetype，Day 54-59）

---

## 推導鏈 #14: Inventory Consistency（Day 54-55 Ticket Booking）

**Physical constraints:**
- 一個 DB row 同一時刻只能被一個 transaction 修改（鎖 = 序列化點，吞吐上限 ~千 TPS/row）
- check 和 act 是兩個動作，中間的瞬間世界會變（TOCTOU: time-of-check to time-of-use）
- 網路請求可能在流程的任意一步之後失敗（部分完成是常態）

**Launch question:**
「庫存剩 1，兩個人同時讀到『1 > 0』，各自扣 1——最後庫存是多少？賣出了幾件？」

### 基礎層

**Derivation direction:**
並發下 check-then-act 兩人都通過 check → lost update / 超賣 → 必須把 check+act 變成一個原子動作 → 三條路線：鎖（悲觀）、CAS（樂觀）、單線程序列化（queue）→ 選擇取決於競爭激烈度

**Expected insight:** 超賣不是程式寫錯，是「檢查和動作之間有時間縫隙」這個物理事實；所有解法都是在消滅這個縫隙。

### 進階層

**Additional constraints:**
- 原子扣減只保護「單步」；下單流程跨多步（預扣 → 付款 → 確認），沒有跨步原子性
- 付款要等第三方，秒級延遲，期間庫存被佔用

**Derivation direction:**
扣減後 crash → 庫存漏（少賣）→ 預扣是租約不是所有權 → TTL 到期自動歸還 + 對帳兜底 → 「傾向少賣」是刻意選的偏向（連回 Payment 的 SAGA/補償思路）

**Micro-exercise (Build):**
小球給出偽碼，學生指出爆點在哪一行、怎麼修：
```go
stock := redis.GET("stock")   // A
if stock > 0 {                // B
    redis.DECR("stock")       // C
    db.CreateOrder(...)       // D
}
// Q1: 兩個 goroutine 同時跑，哪兩行之間出事？
// Q2: 就算 A-C 原子化了，C 和 D 之間 crash 會怎樣？
```

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼『先檢查庫存再扣』在並發下會超賣，就算程式邏輯完全正確？」

---

## 推導鏈 #15: Probabilistic Counting（Day 56-57 Top-K）

**Physical constraints:**
- 精確計數每個 key 需要一個獨立 counter → 記憶體 O(unique keys)
- 十億級 key 空間 × 每個 counter 幾十 bytes = 記憶體放不下
- hash 可以把任意大的 key 空間壓進固定大小的陣列（代價：碰撞）

**Launch question:**
「十億個不同的 URL，要統計每個被訪問幾次，只給你 100MB 記憶體——怎麼辦？」

### 基礎層

**Derivation direction:**
精確計數記憶體 O(N) 放不下 → 用精確度換空間 → hash 到固定格數的陣列累加 → 碰撞 = 多個 key 共享同一格 → 讀出來的數字只會偏大不會偏小 → 多組獨立 hash 各記一份、查詢取 min → Count-Min Sketch

**Expected insight:** CMS 是 Bloom Filter 的兄弟——同一招（hash 進固定陣列 + 接受單向誤差），Bloom 回答「在不在」，CMS 回答「大概幾次」。

### 進階層

**Additional constraints:**
- CMS 只能回答「這個 key 大概幾次」，不能回答「哪些 key 最大」（Top-K 要的是後者）
- 「最近一小時」的需求 vs CMS 不能減量（decrement 會破壞不低估性質）

**Derivation direction:**
Top-K = CMS（計數）+ min-heap（追蹤候選最大值）→ 時間窗需求 → 分桶 sketch、過期整桶丟 → 分散式：CMS 同參數逐格相加可合併（這是它比 exact 結構好合併的原因）

**Micro-exercise (Build):**
「3 組 hash、每組 4 格。key A 落在格 (0,1,2)，key B 落在格 (0,3,2)。A 出現 5 次、B 出現 3 次。畫出陣列內容，然後查詢 A——讀到多少？為什麼取 min 還是可能高估？」

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼 CMS 永遠不會低估、但可能高估？跟 Bloom Filter 的 no false negative 是什麼關係？」

---

## 推導鏈 #16: Geo Matching（Day 58-59 Ride Matching）

**Physical constraints:**
- 「附近」是 2D 概念，但索引本質是 1D 排序——經緯度兩個維度無法同時排序
- 移動物體的位置持續失效（每 4 秒一次心跳 = 讀到的永遠是幾秒前的世界）
- 一個司機同一時刻只能接一張單（互斥資源）

**Launch question:**
「10 萬個移動中的司機，怎麼在 100ms 內找出離乘客最近的 10 個？逐一算距離可以嗎？」

### 基礎層

**Derivation direction:**
暴力算距離 O(N) 太慢 → 需要空間索引 → geohash 把 2D 切成格子、前綴相同 = 空間相鄰（連回 Day 52-53）→ 查自己 + 8 個鄰格 → 候選集縮到幾十個 → 精排（真實距離/ETA）

**Expected insight:** 兩階段是關鍵——索引負責「粗篩候選」（可以 stale、可以近似），精排負責「準確決策」（查最新 KV）。

### 進階層

**Additional constraints:**
- 找到最近的 ≠ 派給他：多張訂單同時看到同一個「最近司機」
- 司機可以拒單/不回應（offer 不是指派）

**Derivation direction:**
候選集 → 互斥搶佔（司機狀態 CAS，本質 = 推導鏈 #14 的庫存問題，司機是庫存量 1 的 SKU）→ offer + timeout 狀態機 → 拒絕/超時釋放重派 → matching 從「查詢問題」升級成「資源分配問題」→ 批次配對優於逐單貪心

**Micro-exercise (Build):**
「畫出訂單狀態機：requested → matched → picked_up → completed。現在加入兩個並發事件：rider cancel 和 driver accept 同時到達——標出哪個轉移需要 CAS 保護、誰贏、輸的一方怎麼補償。」

**Transfer question (Teach):**
「向 Yuki 解釋：為什麼找出最近的司機之後，還不能直接把單派給他？」
