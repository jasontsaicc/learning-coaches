# Day 08-09: Database Selection

> Status: ✅ 完成（Day 8 Chunk 1-6 + Day 9 Chunk 1-5 + PoC）

---

## 📝 One-liner

Database selection 不是 SQL vs NoSQL 二選一，而是根據 access pattern（read-heavy? write-heavy?）、data structure（fixed schema? flexible?）、consistency requirement 來選最適合的工具。

## ⚖️ Trade-off

- SQL vs NoSQL：SQL 提供 ACID + JOIN + strong consistency，適合關聯性資料；NoSQL 提供 flexible schema + horizontal scaling，適合 high write throughput 和 variable structure
- B-tree vs LSM-tree：B-tree read-optimized（in-place update, random I/O write 慢）；LSM-tree write-optimized（sequential write to memtable → SSTable，但 read 要查多層 + compaction overhead）
- Normalization vs Denormalization：Normalization 減少重複但需要 JOIN（latency 高）；Denormalization 允許重複以減少 JOIN（低 latency 但維護成本高、storage 大）

## 📈 Scale trigger

- Read latency 成瓶頸 → 加 Read Replicas 分散 read traffic
- Write throughput 超過單機上限 → Sharding（按 partition key 分散到多台）
- Schema 頻繁變動或 data structure 不固定 → 考慮 NoSQL（如 MongoDB）

## 🔧 DevOps angle

- RDS 監控重點：replication lag、connection count、IOPS、storage usage
- Read replica lag 超過閾值 → alert（可能影響 read-your-writes consistency）
- Connection pooling（如 PgBouncer）避免 connection exhaustion（Postgres 每個 connection 約 10MB memory）

---

## 核心概念

### SQL vs NoSQL — Decision Framework

| | SQL (PostgreSQL, MySQL) | NoSQL (MongoDB, DynamoDB) |
|---|---|---|
| **Data model** | Fixed schema, tables + rows | Flexible schema, documents/KV |
| **Query** | SQL + JOIN | Document query, no JOIN |
| **Consistency** | Strong (ACID) | Eventual (tunable) |
| **Scaling** | Vertical 為主（read replica 可分散讀） | Horizontal（built-in sharding） |
| **適合** | 關聯性強、需要 transaction | Schema 變動大、write-heavy、需要 horizontal scale |

**選擇關鍵不是「資料量大小」，是 access pattern + data relationship：**
- 資料之間關聯性強（需要 JOIN）→ SQL
- 資料結構不固定、每筆 document 結構不同 → NoSQL
- 需要 ACID transaction → SQL
- Write-heavy + horizontal scale → NoSQL

### Indexing: B-tree vs LSM-tree

| | B-tree | LSM-tree |
|---|---|---|
| **寫入** | Random I/O（in-place update 到 disk page）→ 慢 | Sequential write（先寫 memtable → flush to SSTable）→ 快 |
| **讀取** | 直接從 B-tree index 找 → 快 | 可能要查 memtable + 多層 SSTable → 慢 |
| **適合** | Read-heavy（如 PostgreSQL） | Write-heavy（如 Cassandra, RocksDB） |
| **維護** | Page split | Compaction（合併 SSTable，回收空間） |

**B-tree 像書的目錄**：翻到對的頁碼直接看，很快。但如果要「加新頁」要重新排版（random I/O）。

**LSM-tree 像先寫在便條紙（memtable），累積一疊再整理歸檔（flush to SSTable）**：寫入超快，但找東西要翻好幾疊便條紙。

### Normalization vs Denormalization

**Normalization（正規化）：**
- 不存重複資料，用 foreign key + JOIN 關聯
- 優點：data consistency（改一個地方就好）、storage 小
- 缺點：讀取需要 JOIN → latency 高、不利 horizontal scaling

**Denormalization（反正規化）：**
- 允許存重複資料，把常用的 JOIN 結果直接存在同一 row/document
- 優點：read 快（不用 JOIN）、適合 read-heavy
- 缺點：update 時要改多個地方（maintenance 高）、storage 大

### Sharding 入門

把資料依 **partition key** 分散到多台 DB，解決單機容量/throughput 上限。

- **Partition key 選擇很重要**：不均勻 → hot partition（某台負載爆表）
- 常見策略：hash-based（均勻但 range query 難）、range-based（range query 方便但可能不均勻）

### Connection Pooling

DB connection 是昂貴的（每個 ~10MB memory），高併發時容易用完。

- 用 PgBouncer 等 connection pool → 重複使用 connection
- 避免 "too many connections" error

---

## Day 9 進階概念

### WAL (Write-Ahead Log)

每筆寫入先寫到 WAL（append-only log），再寫到 data file。

- **Why**：如果 DB crash，可以從 WAL replay 恢復未完成的寫入
- **Trade-off**：多一次寫入（WAL + data file），但換來 durability
- 類比：先在草稿紙記下要做什麼，做完才劃掉。crash 了看草稿紙就知道做到哪

### Read Replicas

Leader 處理所有 write，replica 處理 read → 分散 read 負載。

```
Client write → Leader DB → WAL → Replication → Replica 1
                                              → Replica 2
Client read → Replica 1 or 2 (load balanced)
```

- **Replication lag**：replica 的資料可能比 leader 慢幾毫秒到幾秒
- 影響：剛寫完馬上讀 replica → 可能讀到舊值

### Consistency Trade-offs（三種 consistency model）

| Model | 保證 | 適合 | 代價 |
|---|---|---|---|
| **Strong Consistency** | 讀到的一定是最新值 | 金融轉帳、庫存 | Latency 高（要等 replica sync） |
| **Read-Your-Writes** | 同一個 user 寫完後讀一定是最新值，其他人可能稍慢 | Social media（自己發文後馬上看到） | 需要 session stickiness 或 read from leader |
| **Eventual Consistency** | 最終會一致，但讀的時候可能是舊值 | Analytics、推薦系統 | 最低 latency，但要容忍 stale data |

**面試關鍵：不要只說「選 eventual consistency」，要說明 WHY 和 acceptable staleness window。**

### Data Model Design Template

設計 data model 的 6 步驟：
1. **Entities** — 有哪些實體？
2. **Access patterns** — 最常怎麼查？
3. **Partition key** — 按什麼分？
4. **Secondary index** — 還需要什麼查詢？
5. **Hot partition risk** — 會不會某些 key 特別熱？
6. **Backfill strategy** — 舊資料怎麼遷移？

### 📡 Observability Mini

| Element | What to monitor |
|---|---|
| **SLIs** | Query latency (P50/P99), replication lag, connection pool utilization, error rate |
| **SLO target** | P99 < 100ms, replication lag < 1s, connection utilization < 80% |
| **Alerts** | Replication lag > 5s, connection pool > 90%, disk usage > 85% |
| **Dashboards** | 3 graphs: query latency distribution, replication lag, active connections |

### PoC: SQL vs NoSQL Comparison

**Architecture：**
```
Go App → PostgreSQL (SQL, fixed schema + JSONB for flexible attrs)
       → MongoDB (NoSQL, flexible document)
```

**Key observation：**
- Structured query（`category='electronics' AND price < 1000`）：兩者都 OK
- Flexible attribute query（`brand = 'Apple'`）：
  - PG 需要 JSONB operator `attributes->>'brand'`（不自然）
  - Mongo 直接 `attributes.brand`（natural dot notation）
- **Trade-off**：PG 用 JSONB 可以「混合」fixed + flexible，但查詢語法較複雜

**Code：** `projects/day09-db-compare/main.go`

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| Btree is write random IO so is slow but read fast, LSM-tree is store in memory fast is write fast, read slow | B-tree uses random I/O for writes which makes it slow, but reads are fast since it goes directly to the right page. LSM-tree buffers writes in memory first making writes fast, but reads are slower because they may need to check multiple SSTables. |
| Normalization 是不存儲重複的資料以及要用 join, Denormalization 是可以允許存重複的資料但是可以減少 join 會增加空間的使用以及維護 | Normalization avoids storing duplicate data and relies on JOINs to link related tables. Denormalization allows data duplication to eliminate JOINs, trading increased storage and maintenance cost for faster reads. |
| eventual consistency 最終會一致, Read Your Writes 至少同一個使用者寫完之後再讀時不該看到舊值 | Eventual consistency guarantees data will converge across replicas over time. Read-your-writes ensures the same user always sees their own latest write — they should never read a stale value after writing. |

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| LSM-tree 是 read-optimized，B-tree 是 write-optimized | **反過來**：B-tree 是 read-optimized（直接查 index），LSM-tree 是 write-optimized（sequential write to memtable） | 搞反了。記住：LSM = Log-Structured **Merge** → 先 log 再 merge，所以寫快讀慢 |
| Denormalization 就是 Normalization | 完全相反：Normalization 消除重複（用 JOIN），Denormalization 允許重複（減少 JOIN） | 把兩個概念搞混，沒注意到 "De-" prefix 代表「反」 |
| Consistency Trade-offs — 完全空白 | 三種 model：Strong（金融）、Read-Your-Writes（社群）、Eventual（分析） | 上課時沒有真正理解應用場景，只是聽過名詞 |
| Interview Drill 看到「大量資料」就選 NoSQL | 資料量大小不是選 SQL vs NoSQL 的關鍵，access pattern 和 data relationship 才是。SQL 加 sharding 也能處理大量資料 | 被「大量資料 = NoSQL」的刻板印象誤導，沒有先分析 access pattern |
| Interview Drill 忘了 Scope Negotiation | 4-Step Framework 第一步就是 Clarify Requirements + Scope Negotiation，跳過這步是面試大忌 | 緊張時直接跳到設計，沒有養成先 clarify 的習慣 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "I'd categorize databases into SQL and NoSQL. SQL uses schema-on-write with ACID guarantees; NoSQL uses schema-on-read with flexible data structures. SQL trades flexibility and horizontal scaling for strong consistency, ACID transactions, and rich JOIN support. NoSQL trades JOIN support and strong consistency for schema flexibility and easier horizontal scaling."

**When asked to go deeper:**
> Q: "How would you decide between SQL and NoSQL for this system?"
> A: "I'd evaluate three things: first, how relational is the data — does it need many JOINs? If yes, SQL. Second, is the schema fixed or frequently changing? Changing schema favors NoSQL. Third, is the workload read-heavy or write-heavy, and what consistency level do we need? Write-heavy with eventual consistency leans NoSQL; strong consistency with transactions leans SQL."

**Showing production depth:**
> "In production, I'd monitor query latency P50/P99, replication lag, and connection pool utilization. The failure mode I'd watch most closely is replication lag causing stale reads — a user writes data but reads from a lagging replica and sees an outdated value, breaking read-your-writes consistency."
