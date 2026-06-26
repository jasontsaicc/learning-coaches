# Day 27 — URL Shortener Interview Drill + Bloom/Cache 補強 (S34)

> 本場 = Bloom+Cache 組合重講(S33 學生點名模糊) + Day 27 URL Shortener Drill(Phase 3 Bar Raiser, 8/9)。

---

## Part 1 — Bloom + Cache 組合(穿透防禦)

### 讀路徑(誰守什麼)

```
請求 key → [Bloom Filter] → [Cache/Redis] → [Database]
            守「不存在的key」  守「存在且熱的key」  真相來源
```

- **Cache = 正向倉庫**:只記「有什麼」。結構上**擋不住**不存在的 key — 不存在 = 永遠 miss = 永遠放行到 DB。
- **Bloom = 反向門神**:敢拍胸脯說「這個**一定**沒有」,直接擋。
- penetration 攻擊打的是「不存在的 key」→ **只有敢說『沒有』的元件能擋** → Bloom 必須在 cache 前面。

### 為什麼 Bloom 敢直接擋(bit 層)

- **寫入** = 把 key 對應幾格 bit **設 1,永不歸零**。
- 查真實 key → 那幾格一定還是 1 → 只能說「possibly in」,**不可能說沒有**。
- 唯一說「沒有」的情況 = 至少一格是 0 = **從沒寫進去過**。
- → **錯誤單向**:真實 key 絕不誤殺(no false negative);不存在 key 偶爾誤放(false positive,白跑一趟,可調又罕見)。

### Cache 失效三件套

| 問題 | 是什麼 | 解法 |
|---|---|---|
| 穿透 penetration | 狂打**不存在**的 key | **Bloom filter** 前置 |
| 擊穿 stampede | 單一**熱門 key 過期**,大量併發重建 | 鎖 / request coalescing |
| 雪崩 avalanche | **大量 key 同時過期** | TTL 加隨機 jitter |

---

## Part 2 — URL Shortener Drill

### One-liner
極度讀多(100:1)的 KV 系統;短碼用 **counter + base62** 無碰撞生成(非 hash),存 **NoSQL KV** 做點查,前面掛 **cache(免 invalidation,mapping 不可變)** + **Bloom(擋穿透)**。

### Capacity → 短碼長度
- 100M/月 → 1.2B/年 → ×5 = **約 6B 組合**。
- **估算訣竅:62 ≈ 64 = 2⁶;2³⁰ ≈ 10⁹(十億)**。base62 n 碼 ≈ 2^(6n)。
  - 6 碼 ≈ 2³⁶ ≈ **640 億** → 已是需求 10 倍 → **6 碼就夠**。
  - 7 碼 ≈ 4 兆 → 保險頭寸,非必要。

### Generation(生碼)
| 做法 | 評價 |
|---|---|
| hash(url) | 要避碰撞 + 加 salt,還要查重 ❌ |
| **counter + base62** | **消滅**碰撞 + **免查重** ✅。代價:多一台 counter 要維護 + 是潛在瓶頸/SPOF |

### Storage
- **NoSQL KV(DynamoDB)** — 依據 **access pattern**(無 join、無交易、純短碼→長網址點查),**不是**「資料量大」。
- **真相來源 = durable DB**;**Redis = cache only**(重啟會掉資料 → 不能當 source of truth)。

### 讀路徑(完整 trace)
```
User 點 abc123
  → DNS → [LB]最前面分流 → API server
  → [Bloom] 一定沒有→擋(回404) / 可能有↓
  → [Redis] hit→回長網址跳轉 / miss↓
  → [DynamoDB] 找到→回寫cache再回傳 / 沒有→404
```

### Scale & 失效(Step 4)
- **counter 不變單點**:多台發號 + **range allocation(KGS)**。
- **中央配號器**:每台一次領一大段(如 100 萬),本地全速發完才回去領 → **每個 block 才打配號器一次,非 per-request** → 不是瓶頸,且可 HA。
- **機器掛在 block 中間**:剩下號碼**丟掉變空洞 = 完全 OK**(640 億碼,短碼不需連續/無洞)。range allocation 的 trade-off = 用「容許空洞」換「免每筆協調 = 快又抗故障」。

---

## 🔗 Capacity 估算 Insight
- **物理約束**:base62 每碼 62 種,n 碼 = 62ⁿ;需求 6B 組合。
- **我的推導**:100M/月 →年→5年 = 6B → 62≈2⁶,2³⁰≈10億 → 6 碼 = 640 億 → 夠。
- **意外**:本來反射答「7 碼」(背的),實際算完 6 碼就有 10 倍餘裕;7 是保險不是需求。

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| LB 放在 redis 跟 db 中間 | LB 站**最前面**(DNS 後、API 前),邊緣分流到多台 API server | 忘了 LB 職責是「分散進來的流量」,不是內部元件 |
| 不存在的短碼回 **401** | 回 **404 Not Found**(401=沒登入/沒授權,403=沒權限,404=東西不存在) | 把「找不到」誤當「權限問題」 |
| 用 **Redis 當 source of truth** | Redis 是記憶體型,重啟掉資料 → 只能當 cache;真相來源要 durable DB(回退 S32 老錯,被質疑後自己修回) | 把「讀多需快取」跟「資料庫」混在一起 |
| 62ⁿ 不會算(預設 7 碼) | 62≈2⁶,2³⁰≈10億 → 心算 base62 任意位數 | 沒有 powers-of-2 估算錨 |
| 配號器怎麼領範圍 / 機器掛掉剩號碼怎辦 | 中央配號器每 block 領一次;掛掉剩號丟掉變空洞=OK | 知識邊界,沒想過(本場補上) |

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| 先檢查名單就是 bloom filter 再去 cache 沒有就到 DB | "First it checks the guest list, the Bloom filter; then the cache; if it's not there, it falls through to the DB." |
| cache 只會存實際有的 key,惡意打不存在的還是會爆 DB | "A cache only stores keys that exist, so a flood of non-existent keys all miss and crush the DB." |
| 100M/月,一年 1.2B,5 年 6B,base62 用 6 碼 | "100M a month is 1.2B a year, ~6B over five years; since 62≈2^6, six base62 chars give ~64B, about 10x headroom." |
| 沒 join 沒交易只是短碼查長網址,所以 NoSQL KV | "No joins, no transactions, just a single-key point lookup, so I'd pick a NoSQL KV store, driven by the access pattern not data volume." |
| Redis 重啟掉資料所以是 cache,真相來源用 durable DB | "Redis is in-memory, so a restart wipes it; it's only the cache, the source of truth needs a durable store." |
| 多開幾台用號碼分段,一台壞不影響整體 | "I'd run multiple ID generators, each owning a distinct number range, so they never collide and one failing doesn't stop the others." |

---

## 🎤 How to Say It in Interview

**穿透防禦(30 sec):**
> "That's a cache penetration attack. I'd add a Bloom filter up front to reject keys that definitely don't exist before they touch the cache or DB. It's safe because a Bloom filter has no false negatives, so a real key is never wrongly blocked, worst case is a rare false positive wasting one lookup."

**追問:counter 發號怎麼不變瓶頸?**
> "Generators grab blocks from a central allocator that's only hit once per block, not per request, so it's not a bottleneck and can be made HA. If a generator crashes mid-block, the leftover IDs are just lost as gaps, which is fine since codes don't need to be sequential."

**Production:**
> "I'd monitor cache hit rate (alert if it drops below ~90%), redirect P99 latency, ID-allocator availability, and the Bloom filter's false-positive rate."

> ⚠️ **頭號弱點提醒**:第一次開口就講足「選什麼 + why + 反面代價」,別等被追問。Step 4 收尾固定講「怎麼監控」。
