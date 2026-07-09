# Day 06-07: Caching & CDN Strategies

> Status: ✅ 完成（Chunk 1-10 + PoC）

---

## 📝 One-liner

Cache 把常用的資料放在更快、更近的儲存層（如 Redis），擋住大部分 request 不用打到 DB，大幅降低 latency 和 DB 負載。

## ⚖️ Trade-off

- Cache-Aside write 時「刪除」而不是「更新」cache：避免 race condition 導致 cache 和 DB 不一致
- Write-Through vs Write-Behind：一致性 vs 寫入速度。資料不能丟用 Write-Through，高寫入量可容忍短暫遺失用 Write-Behind
- 先寫 DB 再刪 cache vs 先刪 cache 再寫 DB：先寫 DB 再刪 cache 比較安全，反過來有 race condition 風險

## 📈 Scale trigger

當 DB query latency 成為瓶頸（P99 > 50ms）或 QPS 超過單機 DB 上限 → 加 Redis cache layer，目標 hit ratio > 90%。

## 🔧 DevOps angle

- ElastiCache (Redis) 監控重點：cache hit ratio、eviction rate、memory usage
- Cache hit ratio 突然下降 > 10% → 可能是 key pattern 改變或 deploy 導致 cold start
- CloudFront 的 cache hit ratio 可在 CloudWatch 看到

---

## 核心概念

### Cache 為什麼有效？

靠 **locality of access（存取局部性）**：
- **Temporal locality**：最近存取的資料很可能很快再被存取
- **80/20 rule**：80% 的 request 打 20% 的資料（hot data）
- 如果每個 request 都存取不同資料，cache 就沒用了

**Effective Latency 公式：**
```
Effective Latency = (Hit Rate × Cache Latency) + (Miss Rate × DB Latency)

Example: 90% hit rate, cache 1ms, DB 20ms
= (0.9 × 1) + (0.1 × 20) = 2.9ms  ← vs 20ms without cache
```

### Cache Levels（由快到慢）

```
Browser Cache → CDN → App Cache (Redis) → DB Query Cache → DB Disk
   ← faster, smaller                              slower, bigger →
```

| Level | Where | Latency | 適合 |
|---|---|---|---|
| **Browser** | Client 端 | 0ms | Static assets, `Cache-Control` header |
| **CDN** | Edge server | 1-10ms | 圖片、CSS/JS、public static content |
| **App Cache** | Redis/Memcached | 0.5-2ms | User profile, session, feed data |
| **DB Cache** | DB 內建 | 1-5ms | Query result cache |
| **DB Disk** | Storage | 5-50ms | 所有資料 |

**判斷原則：**

| | Static / Public | Dynamic / Per-user |
|---|---|---|
| 變動頻率 | 低 | 高 |
| 最佳 cache level | **CDN + Browser** | **Redis (App cache)** |
| 例子 | 大頭貼、圖片、CSS | Feed、cart、session |

### Caching Patterns — 讀取策略

#### Cache-Aside（Lazy Loading）— 最常用

App 自己管 cache，DB 和 cache 之間沒有直接連結。

**Read flow：**
```
App → Cache (hit?) → Yes → 回傳
                   → No (miss) → App → DB → App → 寫回 Cache → 回傳
```

**Write flow：**
```
App → 寫 DB → 刪除 Cache key
```

- 寫入時**刪除**而不是更新：避免兩個 thread 同時更新造成 race condition
- **順序很重要：先寫 DB 再刪 cache**（反過來有 race condition 風險）
- 優點：只 cache 真正被讀的資料（lazy），不浪費記憶體
- 缺點：第一次 read 一定 miss（cold start）

#### Read-Through

Cache 自己管 DB 讀取，App 只跟 Cache 說話。

```
App → Cache (hit?) → Yes → 回傳
                   → No (miss) → Cache → DB → Cache (store) → 回傳
```

- 比喻：Cache-Aside 是自己去超市買，Read-Through 是叫管家去買
- App code 更簡潔，但需要 cache library 支援（如 Guava Cache, AWS DAX）

### Caching Patterns — 寫入策略

#### Write-Through（同步寫兩邊）

```
App → Cache (write) → Cache → DB (write) → 回傳 success
```

- 優點：Cache 和 DB **永遠一致**
- 缺點：write latency 高（要等兩邊都寫完）、可能 cache 了沒人讀的資料
- 適合：資料一致性要求高、讀多寫少

#### Write-Behind / Write-Back（先寫 cache，異步批次寫 DB）

```
App → Cache (write) → 回傳 success（馬上！）
      Cache → (async batch) → DB（之後再寫）
```

- 優點：write latency 極低、batch write 減少 DB 壓力
- 缺點：**Cache 掛了 → 未 flush 的資料遺失**
- 適合：高寫入量、可容忍短暫遺失（如 game score、analytics、page view counter）

### 寫入策略比較

| Pattern | 寫入流程 | Latency | 一致性 | 風險 |
|---|---|---|---|---|
| **Cache-Aside** | App → DB → 刪 cache | 中 | 最終一致 | Cold read after write |
| **Write-Through** | App → Cache → DB（同步） | 高 | 強一致 | Write slow |
| **Write-Behind** | App → Cache → DB（異步） | 低 | 弱一致 | Data loss on crash |

### Read-Through + Write-Through 搭配

兩者搭配 → App 完全不碰 DB，只跟 Cache 互動：
- Read-Through 管讀：miss 時 cache 自動從 DB 載入
- Write-Through 管寫：寫入時 cache 同步寫到 DB
- 例：AWS DAX (DynamoDB Accelerator)

### Eviction Policies

Cache 記憶體有限，滿了要踢掉資料。

| Policy | 踢誰 | 適合 |
|---|---|---|
| **LRU** (Least Recently Used) | 最久沒被用的 | **最常用**，通用場景（Redis 預設） |
| **LFU** (Least Frequently Used) | 被用最少次的 | 有明確 hot data 不想被偶爾 cold request 洗掉（如熱門商品頁） |
| **TTL** (Time To Live) | 過期的 | 資料有明確過期時間 |

- LRU 看「最後一次」存取時間，LFU 看「總共」存取次數
- LFU 問題：過去很熱門但現在沒人用的 key 會一直留著 → 解法：加 decay 衰減 count
- Redis 預設：`maxmemory-policy allkeys-lru`

### Cache Invalidation — The Hard Problem

三種策略：

| Strategy | 做法 | 優缺點 |
|---|---|---|
| **TTL-based** | 設過期時間，自動刪 | 最簡單，但 TTL 內可能 stale |
| **Event-based** | 資料變更時主動刪 cache | 即時一致，但實作複雜 |
| **Version-based** | key 帶版本號 `user:123:v5` | 不用刪舊的，但 key 膨脹 |

**最常見組合：TTL + Event-based** — event 主動刪 + TTL 當 safety net。

**TTL trade-off：**
- 短 TTL (30s) → 資料新，但 hit ratio 低 → DB 壓力大
- 長 TTL (24hr) → hit ratio 高，但資料 stale 久

**Cache Stampede（驚群效應）：**
```
Hot key TTL 到期 → 1000 個 request 同時 cache miss → 全部打 DB → DB 爆了
```

解法：
1. **Lock**：第一個 miss 拿 lock 查 DB，其他人等
2. **隨機 TTL**：`TTL = 300s + random(0-60s)` 分散過期
3. **Stale-while-revalidate**：先回舊資料，背景更新

### CDN Deep Dive

CDN 把 static content 放到全球 edge server，user 從最近節點拿資料。

**Pull CDN vs Push CDN：**

| | Pull CDN | Push CDN |
|---|---|---|
| 運作 | 第一次請求時 edge 去 origin 拿 | 主動上傳到所有 edge |
| 第一次請求 | 慢（回 origin） | 快（已在 edge） |
| 適合 | 流量大、內容多 | 內容少、可預測（CSS/JS） |
| 維護 | 簡單，CDN 自動管 | 複雜，要管上傳邏輯 |

**Origin Shield：** Edge 和 Origin 中間的共用 cache 層，避免多個 Edge 同時打 Origin（類似 cache stampede 概念）。

```
User → Edge (miss) → Origin Shield (shared cache) → Origin Server
```

### CDN Cache Invalidation — 3 Strategies

| Strategy | 做法 | 速度 | 費用 |
|---|---|---|---|
| **TTL-based** | 設 `Cache-Control: max-age`，等過期 | 慢（小時） | 免費 |
| **Purge (Invalidation API)** | 呼叫 API 刪除所有 edge 上的特定 path | 快（5-15 分鐘） | **$$**（CloudFront: 前 1000 次/月免費，之後 $0.005/path） |
| **Versioned URLs** | 檔名帶 hash（`style.a1b2c3.css`） | **即時** | 免費 |

**Best Practice 組合：**
- Static assets (CSS/JS/images)：**Versioned URLs + 長 TTL（1 年）**
  - build tool 產生 hash filename → 新版本 = 新 URL → 不用 invalidate
- HTML pages：**短 TTL (60s) + Purge 當 fallback**
  - HTML 裡引用新 asset URL，所以 user 自動拿到新檔案

**為什麼 Versioned URLs 優於 Purge？**
1. 即時生效（Purge 要 5-15 分鐘 propagation）
2. 免費（Purge 要付錢）
3. 保證不會拿到舊版（新 filename = 不可能 cache hit 到舊的）

**CloudFront Invalidation API：**
```bash
aws cloudfront create-invalidation \
  --distribution-id E1234 \
  --paths "/*"    # wildcard 算 1 path，省錢
```

### ElastiCache — Cluster Mode vs Non-Cluster Mode

| | Non-Cluster Mode | Cluster Mode |
|---|---|---|
| Sharding | ❌ 單一 shard | ✅ 最多 500 shards |
| Max data | ~100GB | 理論上無限 |
| Scale writes | ❌ | ✅（資料分散到不同 shard） |
| Multi-key ops | ✅ 任意 keys | ⚠️ keys 必須同 slot（用 `{hash_tag}`） |
| 適合 | 中小型 cache | 大規模、高吞吐量 |

**Operational gotcha：** Cluster mode 的 `MGET`/`MSET` — keys 分散在不同 shard 會 error。解法：用 hash tag `{user:123}:profile`, `{user:123}:settings` 確保同 user 的 keys 在同 shard。

### 📡 Observability Mini

| Element | What to monitor |
|---|---|
| **SLIs** | Cache hit ratio, origin latency, eviction rate |
| **SLO target** | Hit ratio > 90%, P99 < 50ms |
| **Alerts** | Hit ratio drop > 10% in 5min, eviction spike, memory > 80% |
| **Dashboards** | 3 graphs: hit/miss ratio, eviction rate, memory usage |

### PoC: Redis Cache Layer

**Architecture：**
```
Client → Go App (:8085) → Redis (cache hit?) → Yes → return
                                              → No → simulateDB (50ms) → write Redis (TTL 30s) → return
```

**測試結果：**
- Cache enabled: 1st request miss, 2nd request hit → hit ratio 50%
- Cache disabled (`CACHE_DISABLED=true`): 所有 request 都 miss → hit ratio 0%
- Graceful degradation：Redis 掛了 app 不 crash，只是每個 request 都打 DB（變慢）

**Code：** `projects/caching-poc/main.go`

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| caching is put more faster store like redis in slow store like DB frontend let less client hit DB can less latency | Caching places a faster store like Redis in front of a slower store like a DB, so fewer client requests hit the database, reducing overall latency. |
| cache memory usually more expensive then DB store, and have more limit but we can 分配 data like hot or cold data, hot data have more client use so can put in cache memory | Cache memory is more expensive and has limited capacity compared to DB storage. But we can classify data as hot or cold — hot data that's frequently accessed by many clients goes into cache, while cold data stays in the DB. |
| Cache-Aside is app manages cache, app will read cache if miss will read db and write cache use delete don't use update avoid race conditions | Cache-Aside means the app manages the cache. On a read miss, the app reads from DB and writes to cache. On writes, we delete the cache key instead of updating to avoid race conditions. |
| Read-Through is cache self manage data, app > cache if miss cache will read DB and write cache, app can more simple | Read-Through means the cache itself manages data loading. On a miss, the cache reads from DB and stores it — the app just talks to cache, keeping code simpler. |
| Write-Behind over Write-Through, if need very a lot write can use Write-Behind, like online game write cache first and batch to DB | When there's a very high volume of writes, I'd choose Write-Behind — like in an online game where player actions write to cache first, then batch flush to DB asynchronously. |
| risk is if cache shutdown will loss data | The risk is if the cache goes down before the batch write, we lose data that hasn't been persisted to DB yet. |
| LFU is least frequently use, so will count use, so if app usually use same data, can use LFU | LFU counts access frequency, so it keeps consistently popular data in cache. Choose LFU over LRU when you have clear hot data that shouldn't be evicted by occasional cold requests. |
| cache stampede is if hot key TTL 過期 many request read and miss will all request hit DB, DB will crush, so we can use lock only one request can hit DB, other wait and read cache. 2. TTL use random. 3. give old data and read DB get right data | Cache stampede happens when a hot key's TTL expires and many requests simultaneously cache miss, all hitting the DB at once. Solutions: 1) Use a lock so only one request queries DB while others wait. 2) Add random jitter to TTL to avoid simultaneous expiration. 3) Return stale data first while refreshing from DB in the background. |
| purge is call api to delete path let cache get new data, versioned URLs is static assets set redom name so if update version will change filename so will miss and get new data | Purge calls the CDN API to delete specific paths from all edge servers so they fetch new data on the next request. Versioned URLs embed a hash in the filename — when you deploy a new version, the filename changes, so it's automatically a cache miss and edges fetch the new file. |
| we prefer versioned URLs because speed is fast than other strategy | We prefer versioned URLs because they're instant, free, and guarantee no stale content — it's a new URL entirely, so there's nothing to invalidate. Purge is a fallback for content that can't change URLs, like index.html. |
| because if port is other prosses use just shut server so use log.Fatal, call os.exit | Because if the port is already in use by another process, the server can't start at all, so we use log.Fatal which calls os.Exit(1) to shut down the program. |

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 先刪 cache 再寫 DB 沒問題 | 先刪 cache 再寫 DB 有 race condition：刪完 cache 後、寫 DB 前，另一個 thread 可能讀到舊的 DB 值寫回 cache | 沒考慮到 concurrent read 在 delete 和 write 之間的時間窗口 |
| Write-Behind 的風險是 DB shutdown | 風險是 **Cache** shutdown — 資料先寫在 cache 還沒 flush 到 DB，cache 掛了資料就不見了 | 搞反了哪個元件掛掉才是危險的 |
| 不懂 `ctx` (context) 為什麼要傳給 Redis | `ctx` 是操作的「控制遙控器」— 因為 Redis 是網路呼叫，可能會卡住，ctx 讓你設 timeout 或取消。PoC 用 `context.Background()`（不設限），生產環境用 `context.WithTimeout` | 沒意識到 Redis call 是網路操作，需要超時控制機制 |
| Cache-aside 的 nested if/else 結構寫錯（少了內層 `if err == nil`） | 兩層 if：外層判斷 cache 開/關，內層判斷 hit/miss。漏掉內層 = hit 和 miss 的 code 沒有分開 | 不熟悉 Go 的 nested if/else 結構，把兩個判斷混在一起 |
