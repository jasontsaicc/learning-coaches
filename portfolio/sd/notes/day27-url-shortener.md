# Day 27: URL Shortener (Design)

> Session 32 ｜ Phase 3 第一題 ｜ build-type，Day 28 接 Full PoC (base62 + KGS)

## One-Liner

A URL shortener maps long URLs to short codes for sharing. 核心是極度 read-heavy 的雙向映射；難點全在 scale（生碼不撞、十億級儲存、讀放大）。

---

## Core Design Summary (這場推出的答案)

| 決策 | 選擇 | 為什麼 |
|---|---|---|
| 生碼法 | Counter/KGS + base62（非 hash 截斷）| 「設計掉碰撞」勝過「處理碰撞」，省掉每次寫入查重 |
| 短碼長度 | 7 位 base62 | 62^7 ≈ 3.5 兆 >> 5 年 ~2000 億；base10 要 12 位太長 |
| 唯一號來源 | 分散式（號碼段 / Snowflake）| 單一 counter = SPOF + bottleneck |
| 儲存 | NoSQL KV (DynamoDB/Cassandra) | access pattern 是 point lookup 無關聯；好水平 sharding（理由不是「資料量大」）|
| 讀路徑 | Redis cache 先擋 → miss → read replica → leader | read-heavy；mapping immutable 所以 cache 無 invalidation 煩惱 |
| 點擊分析 | async 經 Message Queue | 拆掉「每讀必寫」，redirect 維持快 |

---

## Architecture Diagram (自己重畫一次，再對答案)

先蓋住下面，自己畫「寫入 / 讀取 / 分析」三條路徑，再核對。

```
[寫入 ~1k/s]
Client → DNS → LB → API Server → ID Gen (Snowflake/KGS) → base62 → NoSQL KV DB
                                  (拿全域唯一號，無碰撞)            (存 short_code↔long_url)

[讀取 / redirect ~10k/s]
Client → DNS → LB → API Server → Redis Cache ── hit ──→ 回 301 redirect
                                      │
                                  (miss)
                                      ↓
                                 Read Replica → NoSQL KV DB → 回填 cache → 301

[點擊分析，不拖慢讀取]
API Server ── async ──→ Message Queue → Analytics Worker → 統計寫 DB
```

每塊存在的理由（面試要能一句話講出）：

| Block | 一句話理由 |
|---|---|
| ID Gen (Snowflake/KGS) | counter 法天生唯一 → 短碼天生唯一 → 不用查重 |
| NoSQL KV DB | durable 真相來源（redis 掛了不會全站 404）；point lookup 無關聯 → KV 最順 |
| Redis Cache | read-heavy 第一防線；immutable mapping → 無 invalidation 痛點 |
| Read Replica | cache miss 分流；代價 = replication lag → read-after-write 可能短暫 404 |
| Message Queue | 點擊統計走 async，redirect 不被寫入拖慢 |

> 301 vs 302：要點擊分析就用 **302 (temporary)**，瀏覽器每次都回來打 server 才記得到點擊；不需要分析、只要最快就用 **301 (permanent)**，瀏覽器會 cache 跳轉、不再經過你。

---

## My Answer vs Google SRE (L6) — 逐段對照

> 用法：先看「我這場」，再看「SRE 版」和面試官 OS，把差距記進腦。SRE 特別吃：真實容量數字 (NALSD)、SLO/error budget、failure mode、可降級。

### 1. Clarify Requirements

**🟦 我這場：** 認出 read-heavy → 要 cache；問 QPS；scope 圈 create + read 不做 edit；問用戶數和 URL 數。analytics 需求一開始漏掉，被提示才抓回。讀寫比給 10:1~100:1，但理由一開始連到「每天產生量」（偏弱）。

**🟩 Google SRE (L6) 會這麼答：**
> 「先確認幾件事。規模：DAU、每天新增多少條短碼？讀寫比多少，這決定整個架構往讀傾斜。要不要點擊分析，這影響我選 301 還是 302。短碼長度有上限嗎、要支援自訂 alias 嗎？我先假設不做修改和刪除，需要再加回。最後一個 SRE 會問的：redirect 的可用性目標訂多少？我假設 99.95%，這是錢的等級，因為 redirect 掛掉等於全站連結死掉。」

**🎙️ 面試官 OS：** 每個 clarify 都連到一個設計決策（讀寫比→cache、analytics→301/302、規模→是否分片），這叫 requirements-driven design。主動宣告「不做刪除」是 scope 管理。問可用性目標 = SRE 把 SLO 當設計輸入，不是事後補。

**差距：** 你的方向對，但（a）讀寫比要連到「每條 URL 一生被讀幾次」的用戶行為，不是每天產量；（b）開場就主動丟 SLO 目標（99.95% redirect 可用性）；（c）analytics 要自己想到不靠提示。

---

### 2. High-Level Design / Capacity

**🟦 我這場：** 算對 write 1000/s、read 10000/s（懶人估算法）。讀重 → 先想到 replica，cache 是被追問才補上順序。

**🟩 Google SRE (L6) 會這麼答：**
> 「先攤數字。寫入 1 億/天 ≈ 1.2k QPS、尖峰 ×3 ≈ 3.6k。讀按 10:1 是 ~12k、尖峰 ~36k。每條 ~500 bytes，5 年 ~2000 億條 ≈ 100TB 級。這些數字告訴我三件事：寫入很小，單一發號邏輯綽綽有餘，不要過度設計；讀很大且是純 KV 查，cache hit 可做到 95%+，所以 cache 是主力不是配角；儲存要 sharding 但 access pattern 單純，KV store 就夠。所以讀路徑 client→CDN/LB→service→Redis→replica→DB，寫路徑走獨立發號。」

**🎙️ 面試官 OS：** 畫圖前先攤數字，每個架構決策都引用一個數字當理由。「寫入小所以不過度設計」特別加分，知道哪裡不需要複雜的人，比一直堆元件的人少見。

**差距：** 你算出了數字但沒「用數字驅動決策」。練習：每講一個元件，後面接「因為（某個數字）」。cache 要主動先講（read-heavy 第一防線），不要等被問。

---

### 3. Deep Dive: 短碼生成

**🟦 我這場：** 一開始把 hash(A) 和 counter(B) 混在一起（「加 salt 用 A 再加 B 減少碰撞」）。經教學後抓到 B = 發號碼牌，天生唯一、不用查重。SPOF + bottleneck 自己答對。

**🟩 Google SRE (L6) 會這麼答：**
> 「兩條路線比一下。Hash 截斷：無狀態、同網址天然去重，但會碰撞，要查庫探測再加 salt 重試，寫入多一次往返，且 DB 越滿碰撞越多。發號器 + base62：全域 counter 編碼，無碰撞、不查重，但 counter 中心化要顧可用性，且循序 ID 可被遍歷（安全問題）。我選發號器：用號碼段分發解可用性（每個實例一次領 10 萬個號，counter 掛了還能撐一陣子），用混淆打亂輸出解遍歷。理由是寫入才 3.6k QPS，hash 查庫的額外成本不划算，且 99% 不需要去重。」

**🎙️ 面試官 OS：** 回答結構正是想看的：選項 A 代價、選項 B 代價、我的選擇、為什麼在這個 context 選它。主動講「循序 ID 可被遍歷」這個安全面，多數題解沒有。號碼段「掛了還能撐一陣子」是 operational 思維。

**差距：** 你最終懂了 B，但面試要能**一口氣**講「A 代價 / B 代價 / 我選 B / 為什麼」，不要被引導才拼出來。再補兩個高分點：循序 ID 的**安全遍歷風險**、號碼段的**降級存活**。

---

### 4. Scale & Trade-offs

**🟦 我這場：** 講到 replica 分流、cache 擋熱門。Operational 監控沒主動展開。

**🟩 Google SRE (L6) 會這麼答：**
> 「三個具體點。一，DB 分片：shard key 用短碼本身，唯一查詢就是 by 短碼，hash 分佈天然均勻不會 hot partition。二，真正的風險是熱 key：一條短碼被瘋傳打爆單一 cache 節點，我在 service 層加 local cache（毫秒 TTL）扛尖峰，代價是極短不一致窗口，redirect 完全可接受。三，SLO 與監控：redirect 可用性 99.95%、P99 < 50ms 當 SLI，cache hit ratio 掉到 90% 以下告警（代表 DB 流量要翻倍），加上號碼段餘量告警。一句 trade-off 總結：我用最終一致換讀取效能，新建短碼可能一兩秒查不到，business 上沒人在乎。」

**🎙️ 面試官 OS：** 三點全是這題專屬：shard key 有理由、熱 key 是真實事故、監控講到 hit ratio 和號段餘量這種粒度。最後用業務語言衡量一致性代價，這是 strong hire 段落。

**差距：** 你還沒到「主動收尾講 trade-off + SLI + 降級」。Phase 3 起每場 drill 結尾練：一句話總結「用什麼換什麼」+ 兩個要監控的 SLI。

---

## Key Trade-offs

- **Counter vs Hash 生碼**：選 counter，用「無碰撞 + 不查重」換「需要分散式發號機制」。
- **NoSQL KV vs SQL**：選 KV，用「放棄關聯能力」換「point lookup 順 + 易 sharding」。理由是 access pattern，不是 data volume。
- **Cache 一致性**：用「最終一致（新碼短暫查不到）」換「讀取效能」。因為 mapping immutable，這個代價趨近於零。
- **301 vs 302**：用「失去瀏覽器跳轉 cache（302 每次回來打 server）」換「能記到每次點擊」。

## Capacity (back-of-envelope)

```
寫 QPS = 100M/天 ÷ ~10萬秒 = ~1,000/s（尖峰 ×3 ≈ 3,000）
讀 QPS = 寫 ×10 = ~10,000/s（尖峰 ≈ 30,000）
短碼   = 5 年 ~2000 億條 → 7 位 base62 (62^7 ≈ 3.5 兆)
儲存   = ~2000 億 × ~500B ≈ 100TB 級 → 需 sharding
```

## Failure Modes (Phase 3 要求，至少 3)

| 故障 | 後果 | 應對 |
|---|---|---|
| Cache 熱 key 節點被打爆 | 單點過載、延遲飆 | service 層 local cache（毫秒 TTL）擋尖峰 |
| Read replica lag | 剛建的短碼讀到 404 (read-after-write) | 新寫入短時間讀 leader，或寫入後主動回填 cache |
| ID 發號器/counter 掛 | 無法建立新短碼 | 號碼段預領（本地還有號可發）+ Snowflake 去中心化 |
| Queue 積壓 | 點擊統計延遲（非關鍵路徑）| 可容忍；redirect 不受影響，補監控 queue lag |

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 讀寫比從「每天產生量」推 | 比例來自用戶行為：一條 URL 一生被讀幾次 | 把「產量」和「每條被讀次數」兩個軸混了 |
| hash(A) 加 salt 再加 B 來「減少」碰撞 | A 和 B 是兩條平行路線；B(counter) 是「消滅」碰撞不是減少 | 沒分清 salt 是 A 的「碰撞後重試」手段，不是預防 |
| 架構 ② 真相來源填 redis cache | ② 要 durable DB；redis 重啟會清空 → 全站短碼永久 404 | 把 cache（volatile）當成可以存唯一一份的真相來源 |
| ⑤ 點擊統計填「async」 | async 是性質，零件名是 Message Queue | 講了「怎麼做」沒講「用哪個元件」 |
| 卡住直接喊「提示我」 | 頭號習慣弱點：求助前要先丟一個答案 | Phase 3 起每場第一要求：先嘗試再求助 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "A URL shortener is an extremely read-heavy key-value system. The interesting parts are all about scale: generating short codes without collisions, storing billions of mappings, and absorbing a 10-to-1 read load. I'd start by clarifying the read:write ratio and the availability target, since both drive the whole architecture."

**When asked「兩個網址 hash 出同一個短碼怎麼辦」:**
> "I'd avoid that class of problem entirely by not hashing. Instead I generate a globally unique counter value and base62-encode it. Each number is unique by construction, so each code is unique, and I never have to check the DB for collisions. The trade-off moves to generating unique numbers without a single bottleneck, which I solve with number-range allocation or Snowflake."

**Showing production / SRE depth:**
> "My SLI is redirect availability at 99.95% and P99 under 50ms. The real-world failure mode is a hot key: one viral link overloads a single cache node. I'd add a short-TTL local cache at the service layer to absorb the spike, accepting a tiny inconsistency window that's fine for redirects. I'd alert on cache hit ratio dropping below 90%, because that signals DB load is about to double."

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| read more than write so cache is important, check QPS, focus create and check not edit | "Since reads far outnumber writes, caching is critical. I'd confirm the expected QPS and scope this to creation and redirects, not editing." |
| write 1000 qps read 10000, for one db is heavy so use replica | "Writes are ~1,000 QPS and reads ~10,000. That's a lot of read load for one DB, so I'd put a cache in front first, then add read replicas." |
| cache first can handle hot key, second replica but replica has sync delay | "A cache absorbs the hot keys first; read replicas then spread the remaining load, at the cost of replication lag." |
| base10 7 位只有 1000 萬不夠，要更多位，網址會變長 | "Base10 with 7 digits only covers 10 million, far too few. You'd need many more digits, which makes the URL longer. Base62 packs more per character, so 7 chars is enough." |
| 不用 join，看起來可以用 nosql | "There are no joins or cross-row transactions here, so a NoSQL key-value store fits this access pattern well." |

---

## Cross-Verify

📖 Alex Xu Vol 1 Ch 8: 對照 base62 vs base64 的 trade-off（為什麼不用 `+` `/` 這種非 URL-safe 字元），以及他的 KGS（Key Generation Service）離線預生 key 設計。下次帶一個發現回來。
