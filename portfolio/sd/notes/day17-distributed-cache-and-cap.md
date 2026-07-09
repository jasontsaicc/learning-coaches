# Day 17 — Design a Distributed Cache（problem-anchored）+ CAP Theorem

> 本節用「設計分散式 cache」當錨，把 CAP / Replication 用 just-in-time 方式拉進來。
> 同時擔任 **Phase 1 → Phase 2 Gate mini-mock**（3/3 PASS）。

---

## One-Liner

> A distributed cache spreads data across multiple nodes using **consistent hashing** to route keys, with **replicas** for availability. The key trade-off is favoring **AP over CP** — because the source of truth is the DB and TTL makes staleness self-healing.

## Trade-off（核心取捨）

- **Sharding 機制**：consistent hashing over mod N（節點變動時只搬 ~1/N，不是全部）
- **路由位置**：client-side（smart client）vs proxy 層 → 選 client-side，因為 **延遲優先**（少一跳），代價是 membership propagation（節點變了要通知所有 client，靠 gossip 解）
- **一致性**：partition 時選 **AP**（可用但可能舊）over CP（一致但拒絕服務）

## Scale Trigger（什麼規模逼出什麼設計）

| 數字 | 逼出的設計 |
|---|---|
| 100 GB hot data > 32 GB/node | **必須 sharding**（consistent hashing） |
| node 年故障率 2~10% | **必須 replication**（掛一台 ≠ 資料消失） |
| 500K reads/s, P99 < 5ms | client-side routing（少一跳）+ in-memory |
| 熱門 key 同時 miss | **request coalescing**（防 thundering herd） |

## DevOps Angle（production 要監控什麼）

- **SLI**：cache hit ratio、P99 latency、per-node 記憶體用量、replica lag
- **Alert**：hit ratio 驟降（可能是某 shard 掛了）、單節點記憶體飽和、DB QPS 突增（stampede 前兆）
- **Dashboard**：throughput per shard、latency 分佈、miss rate 趨勢

---

## Capacity Estimation（back-of-envelope）

```
資料量:   50M keys × 2KB ≈ 100 GB
單機可用: ~32 GB
裝得下:   100 / 32 ≈ 3.2 → 至少 4 台（容量）
實務起步: + headroom + replicas → ~6 台
讀寫比:   10:1（讀多寫少 → 適合 cache-aside）
```

---

## 🔗 Derivation Insight（CAP 是被問題拉出來的）

- **Physical constraint**：兩複本間的網路**一定會斷**（partition 不是「萬一」是「遲早」）；硬體年故障率 2~10%。
- **My derivation**：node 掛 → 那 1/N 的 key 消失 → reads 全變 miss → 全砸 DB → **cache stampede / cascading failure**。為了救它 → 每個 shard 存多份(replication) → 一個 key 有多份複本 → 更新時「等同步完才回(慢但一致)」vs「不等(快但舊)」→ 這就是 **CAP**。
- **Surprise**：原來 CAP 不是「教材第幾天的定理」，是順著「node 會掛」自然推出來的。而且 cache 選 AP 的理由超直覺（源頭是 DB + TTL 自癒）。

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 路由邏輯放 client 還是 proxy「不確定」 | 兩者都行，是 trade-off：**client-side 快但節點變動要通知所有人**；**proxy 集中好維護但多一跳 + 自己要 HA** | 沒建立「沒有對錯、只有取捨」的反射，遇到開放題會卡住 |
| 不清楚 partition 是什麼 | partition = 機器**都活著但彼此網路失聯**，各自繼續收 request 導致資料分歧。**≠ 機器掛掉** | 把「node 死」和「node 失聯」混為一談 |
| `hash mod N` 搬移比例講「75%」 | 不是固定比例，是「**幾乎全部**」（4→5 台約 80%）；consistent hashing 壓到 ~1/N | 記成一個具體數字，反而不準 |
| One-liner 需要提示才串得起來 | headline-first：先講「是什麼」再講「trade-off + why」 | 還沒形成「一句話打包」的口說肌肉 |
| clarify 時偏向「問 AI 要答案」 | 面試要**主動斷言並圈定範圍**：「I'll focus on X, assume Y for now」 | 舊習慣（S8 也曾忘 Scope Negotiation）|

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "A distributed cache shards data across nodes with consistent hashing and replicates each shard for availability. For a cache I'd choose AP over CP, because the DB is the source of truth and TTL makes stale data self-healing."

**When asked to go deeper — "What happens when a node dies?":**
> "Its shard's keys vanish, so all reads for them miss and hit the DB at once — a cache stampede that can cascade into an outage. I'd prevent that with replication so a replica takes over, plus request coalescing so concurrent misses on a hot key share one DB lookup."

**When asked "CAP — pick 2 of 3?":**
> "That framing is misleading. Without a partition you get both C and A. CAP only forces a choice *during* a partition: consistency (refuse stale answers) or availability (serve possibly-stale). And the choice can be per-feature — browsing AP, checkout/inventory CP."

**Showing production depth:**
> "I'd monitor cache hit ratio and per-shard P99; a sudden hit-ratio drop usually means a shard is down, and a DB QPS spike is the early warning of a stampede."

---

## 🌍 CAP in the Real World（建立畫面）

**心法：給錯資料會不會直接損失金錢或安全？會 → CP；不會 → AP。**

| 系統 / 場景 | 選 | 為什麼 |
|---|---|---|
| DNS | AP | 永遠答得出，靠 TTL 容忍舊值 |
| Cassandra / DynamoDB（預設） | AP | 目錄、動態、購物車：能用 > 完美 |
| Amazon 購物車 | AP | 寧可讓你繼續買，衝突後合併 |
| 銀行轉帳 / 付款 | CP | 餘額算錯 = 賠錢 |
| 限量最後一件庫存 | CP | 超賣 = 真實損失 |
| ZooKeeper / etcd | CP | leader 選舉必須全體一致 |

> 同一電商：瀏覽/評論 → AP，結帳/扣款/扣庫存 → CP。

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| consistent hashing can solve node change... mod N every change will move 75% data so not good, use ring and vnode better | "Consistent hashing solves nodes joining or leaving. With `hash mod N`, changing N forces nearly all keys to be remapped — too expensive. Mapping keys and nodes onto a ring, plus virtual nodes, means only ~1/N of keys move." |
| one node redis not enough, need 水平擴張, support get/set/delete? TTL? latency? | "A single Redis node isn't enough, so we need horizontal scaling. Should it support get/set/delete? Do we need TTL, and what's the latency target?" |
| miss 回去 db 查詢 回寫 redis | "On a cache miss, the app reads from the DB, writes the value back into the cache, then returns it — the cache-aside pattern." |
| if wait data sync to master and replica is slow | "Waiting for the write to sync to both primary and replica is consistent but slow; not waiting is fast but the replica may serve stale data." |
| 我會選 AP, 源頭是 DB, redis can set TTL | "For a cache I'd choose AP: the DB is the source of truth, so slight staleness is acceptable, and TTL makes it self-healing — and a cache that refuses to answer defeats its purpose." |

---

## Cross-Verification（下次帶回來）

> 查證 **「Amazon Dynamo 論文裡的購物車為什麼選 AP」**（Dynamo paper / DDIA Ch.5）。看它怎麼用 vector clock 處理「加購物車」的衝突合併。下次跟我說你發現了什麼。
