# Day 31: Distributed Rate Limiter

> Session 37 · Phase 3 · 2026-07-03
> 把 Day 23-24 的 Rate Limiting building block 拉進真實設計題。故事：Karen 要開放第三方 API 給廠商，需要限流。

---

## One-Liner

> A distributed rate limiter keeps each user's counter in a shared store like **Redis**; to stop multiple servers racing on read-modify-write (**race condition**) it makes check-and-update **atomic** — a single atomic command for a simple counter, or a **Lua script** for multi-step logic; algorithm-wise it uses a **sliding window** over a **fixed window** to close the 2× boundary-burst hole.

---

## 核心因果鏈（大半自己推出來的）

```
單機限流器複製到 100 台，各記各的 counter
        │  每台是一座孤島,台北不知道倫敦放了多少
        ▼
惡意 user 實際能打 N × limit = 100×100 = 10,000  ← 限流被 scale 倍數架空
        │  修法方向:不要孤島 → 一個共享 counter
        ▼
共享 counter 放 Redis,100 台都讀寫同一個數字
        │  新坑:動作分兩步(先看有沒有滿 → 再決定加一)
        ▼
RACE CONDITION:兩台同時 GET 到同一個舊值 → 都以為沒滿 → 都放行 → 超額
        │  解藥:把「看+改」縮成一個切不開的動作(atomic)
        ▼
單一原子操作 DECR / INCR (Redis 單執行緒,一次跑一個命令,無空檔)
        │  counter 怎麼每分鐘重置?
        ▼
TTL / EXPIRE:key 裡塞「當前分鐘」+ 設 60s 過期 → 每分鐘天生一把新 key,舊的自動燒掉
        │  = Fixed Window Counter。但有破綻...
        ▼
邊界 2 倍破綻:12:00:59 打100 + 12:01:00 打100 = 1秒內 200 個(攻擊者能預測整點歸零)
        │  改用「從現在往回看 60 秒」的移動窗口
        ▼
SLIDING WINDOW:窗口跟著 now 移動,沒有固定交界可鑽;12:01:00 往回看仍記得 12:00:59 那批
        │  但 sliding window 要好幾個 Redis 命令(清舊/數量/加新/TTL)
        ▼
多步 → RACE CONDITION 重演(第2步數量、第3步加新,中間有縫)
        │  單一命令原子性不夠了
        ▼
LUA SCRIPT:整段腳本在 Redis 上「一個命令一次跑完」,中間不准插隊 → 多步變回原子 → 收口
```

---

## Trade-offs（面試要講的判斷）

| 決策 | 選擇 | 為什麼 / 反面代價 |
|---|---|---|
| counter 放哪 | 共享 Redis,非本地 | 本地 = N 座孤島 = N×limit 破功;共享 = 單一真相 |
| 統一在哪一層 | 統一「計數器」(B),非統一「限流機器」(A) | A 那台 = SPOF + bottleneck(Snowflake/DB auto-inc 同款病);B 讓 100 台各自算、只共享數字 |
| counter 重置 | 被動 TTL 過期,非主動背景 job 補 | 幾百萬 user → 定時 job 會漏跑/塞車/半夜掛;TTL 是 Redis 內建、零維護 |
| 演算法 | Sliding Window(嚴格封頂) | Fixed Window 邊界能爆 2 倍;Token Bucket 允許 burst。要不要容忍瞬間爆量 = 選型關鍵 |
| 多步原子性 | Lua script | 單一 DECR 天生原子;多步(sliding window)要 Lua 把好幾個命令捆成一個原子單位 |

---

## 🔑 一整天其實只有一個主題:原子性(atomicity)

- **單一動作** → 用內建原子命令(`DECR`/`INCR`),免費就是切不開的動作。
- **多步動作** → 用 **Lua** 把多步**捆成**一個切不開的動作。
- 同一種病(race condition = 根據「看完就過期的數字」做決定),同一種藥(把「看+改」縮成一個原子單位),規模從 1 步變 N 步。
- 遷移:庫存扣減、秒殺、搶紅包、分散式鎖 —— 全是這一題的變形。

## DevOps / 生產角度

- **Redis 是這個設計的 SPOF + 熱點** → 要 replica / cluster;Redis 掛了要決定 fail-open(放行,保可用)還是 fail-closed(全擋,保後端)。
- 監控:reject 率、每個 user 的 counter 打滿率、Redis 延遲 P99、Lua script 執行時間。
- **「讓資料自己過期」永遠比「派排程主動清理」可靠** —— cache/session/限流通用心法。

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 「使用一個統一的限流器嗎?」(用問句、沒 commit、沒說哪一層) | 要 commit + 講清楚統一的是「計數器」不是「限流機器」;後者 = SPOF+bottleneck | 頭號主線:給結論不給論證 + 不敢 commit 先問 AI(S8→S37) |
| counter 扣到 0 後,用 INCR 手動加回去 | 不要主動補,讓 key TTL 自動過期,每分鐘天生新 key。被動 > 主動 | 直覺想到「加回去」,沒想到「讓它自己消失」這個方向 |
| (推導卡點) fixed window 的破綻講不出時間點,只說「2 倍」 | 12:00:59 打100 + 12:01:00 打100 = 1 秒 200 個 | 給結論(2倍)沒給論證(哪兩秒);後補上 |

> 註:本場多次「有點亂/什麼意思」是節奏被塞太多所致(非真的不懂),退小步+比喻後都通。概念本身掌握紮實。

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "A distributed rate limiter keeps each user's counter in a shared store like Redis. The hard part isn't the limiting — it's concurrency: multiple app servers racing on the same counter. So I make check-and-update atomic, and I pick a sliding window over a fixed window to avoid the 2× boundary burst."

**Q: "為什麼不能每台 app server 各自限流就好?"**
> A: "每台的 counter 是一座孤島,100 台就等於放大到 N×limit —— 規則寫 100,實際能打進 10,000。所以計數必須放共享的地方,例如 Redis。"

**Q: "共享 counter 之後還有什麼問題?"**
> A: "Race condition。如果是『先 GET 看有沒有滿、再 INCR』兩步,兩台會同時讀到同一個舊值、都以為沒滿、都放行。解法是把它變原子:簡單計數用單一 DECR;sliding window 那種多步邏輯,用 Lua script 把整段包成一個原子單位。"

**Q: "fixed vs sliding window 怎麼選?"**
> A: "Fixed window 在整點歸零,攻擊者可以卡 12:00:59 和 12:01:00 各打滿,1 秒內灌 2 倍。Sliding window 永遠看『從現在往回 60 秒』,窗口跟著移動、沒有固定交界可鑽,代價是要存每次的時間戳、比較耗空間。"

**Showing production depth:**
> "In production, Redis is my SPOF and hot spot — I'd run it clustered with replicas, and decide fail-open vs fail-closed if it dies. I'd monitor reject rate, per-user saturation, Redis P99, and Lua execution time."

---

## 現實怎麼落地 (Production Reality)

**核心認知:現實裡多半「不自己寫」限流** —— 我們推的 Redis+Lua+sliding window 全是真的,但生產環境它住在**邊緣/閘道/mesh 層**,用設定檔開啟,不寫進 app code。

| 住在哪一層 | 實際用什麼 | 機制 |
|---|---|---|
| 反向代理(單機) | Nginx `limit_req` | Leaky bucket, per-node(跨機要接 Redis: OpenResty + `lua-resty-limit-traffic`) |
| K8s Ingress | `nginx-ingress` annotation `limit-rps`/`limit-rpm` | YAML 加一行就開(我的 EKS 世界) |
| Service Mesh | Envoy global rate limit filter → ratelimit service(Lyft OSS) → Redis | **就是本題的生產版** |
| CDN/邊緣 | Cloudflare rate limiting / AWS WAF rate-based rule | 近似 sliding window, per-IP |
| 雲 API 層 | AWS API Gateway usage plan throttling | Token bucket, per-API-key |
| App 內(少數) | Stripe 自寫 middleware / `redis-cell` module | Redis + GCRA token bucket |

**真實演算法 vs 我們教的:**
- Sliding window log(存每個 timestamp 的 ZSET)= 精確但吃記憶體 → 高 QPS 下 Redis 爆。
- **Sliding window counter(近似)= Cloudflare 做法**:只留「上一窗數量 + 這一窗數量」加權平均,省記憶體夠準。
- **GCRA token bucket = Stripe / `redis-cell`**:只存一個時間戳(TAT)就有 token bucket 效果,`CL.THROTTLE` 一命令搞定(內建原子)。

**🔑 現實最大取捨(概念沒講到):local + global 兩層。** 每個 request 都打 Redis = 多一次 hop + Redis 全域熱點,大流量會痛。解法:
```
第 1 層  每台 app server 本地小 token bucket,先擋明顯超量
第 2 層  週期性/抽樣跟 Redis 對帳全域用量
結果    絕大多數 request 本地決定,不打 Redis;接受「一點點超額」換低延遲
```
→ massive scale 下**沒人做精確全域限流**(Cloudflare 幾百邊緣節點不可能每 request 同步)。接受近似 = 今天「主動 vs 被動」「精確 vs 成本」的延伸,同 distributed cache 選 AP 的判斷:能容忍就用最終一致換效能。

**被擋回什麼:** `429 Too Many Requests` + `Retry-After: 30` + `X-RateLimit-Limit/Remaining/Reset` headers(讓 client 自律)。

**🎤 一句話收斂:** 「限流放 gateway/mesh 層不寫進業務邏輯,Redis+Lua 做 sliding window 中等規模夠用;massive scale 退成 local+global 兩層近似,避免每 request 打 Redis;被擋回 429+Retry-After。」

### 圖解 + 場景（白板可直接畫）

**限流住在請求路徑的哪幾層（縱深防禦):**
```
Client
  │
  ▼
① Edge/CDN   (Cloudflare, AWS WAF)   per-IP、擋 DDoS/爬蟲、粗粒度、可近似
  │ 過了
  ▼
② Gateway/Ingress/Mesh (Envoy...)    per-user/per-API-key ← 主戰場、要精確
  │ 查/扣 counter
  ▼
③ Redis                              共享 counter，Lua sliding window（本題核心）
  │ 過了
  ▼
④ App servers                        業務邏輯，幾乎不自己做限流
```
> 擋攻擊放邊緣、擋濫用放閘道。放錯層 = 擋不住攻擊 或 誤傷正常人。

**兩種真實架構:**
```
A. 集中式 Redis（中等規模, 精確）
   [GW1][GW2][GW3] ──每 request──▶ [Redis](Lua)
   ✅精確  ❌每 request +1 hop、Redis 熱點+SPOF

B. Local + Global 兩層（海量, 近似）
   [node1 local bucket]┐
   [node2 local bucket]┼─每 100ms 對帳─▶ [Redis]
   [node3 local bucket]┘
   ✅低延遲、Redis 不爆  ❌短暫超額
   → 轉折點: 當「每 request 打 Redis 的延遲/成本」> 「精確的價值」就退到 B
```

**場景對照:**
| 場景 | 用什麼 | 為什麼 |
|---|---|---|
| 中型 SaaS API(Stripe/GitHub) 要精確 per-key | 架構 A: gateway + Redis + Lua sliding window / GCRA | 精確 > 延遲,一次 hop 可接受 |
| 全球邊緣抗 DDoS(Cloudflare/WAF) per-IP 海量 | 架構 B: 本地 + 近似聚合 | 幾百節點無法每 request 全域同步 |
| 微服務內部互打(Lyft) | Envoy sidecar + ratelimit service + Redis | mesh 層宣告式,不改業務碼 |
| 我的 EKS 保護內部 endpoint | `nginx-ingress` annotation `limit-rps` | 夠用就好,跨 pod 精確才上 Redis |

**壞流量走位(場景 A,第 101 個 request):**
```
Client(key=acme) ─▶ Envoy Gateway ─(Lua 原子: 清舊→數量→滿了)─▶ [Redis]
                       │
                       ◀─ 429 Too Many Requests + Retry-After:12 + X-RateLimit-Remaining:0
                       ✗ 根本沒碰到 app server → 後端零負載
```
> 限流的價值:壞流量在最前面彈掉,app + DB 完全無感。

---

## Pending（下次補）

- **Interview Drill(bar-raiser)** 壓力測試本題 —— 本場因節奏放慢略過,下次先補。
- **Day 32 PoC**:Redis-based distributed rate limiter in Go(可選,學生常跳 PoC)。
- Capacity estimation 沒做(老弱點,固定練)。
