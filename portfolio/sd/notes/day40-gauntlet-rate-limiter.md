# S40 — Drill Gauntlet #1: Distributed Rate Limiter + 逾期複習清倉

> execution-heavy 場。前半換情境冷測清 4 筆逾期複習,後半 L3 bar-raiser drill。
> 重點不在分數(~3/9 訓練場),在**暴露輸出習慣**:第一句永遠裸結論。

---

## Distributed Rate Limiter — 全鏈設計(drill 自產)

**題目**:公開 API 防濫用,每 user 100 次/分,50 台 server 多區域,尖峰 500K RPS。

### 推導鏈(一句一環)
1. **本地 counter 壞掉** → 一個 user 被 LB 打散到 50 台,每台各放 100 → `100×50 = 5000/min`,破表 50 倍
2. **修法 = 共享 Redis counter** → 50 台讀寫**同一個真相來源**,count 才是全域的
   - cost(禁用「低」):① 每個請求多一次 **network hop** ② Redis 變 **critical dependency**(要 HA)③ throughput 要驗證
3. **capacity** → 一台 Redis ~10 萬 ops/sec,`500K / 100K = 5 台 shard`
4. **怎麼 shard** → **by user_id**(hash),同 user 所有請求落同一台,counter 不再散開(= consistent hashing 落地)
5. **心臟 = 並發不是計數** → counter=99,兩請求同時讀 99、都判斷「<100 放行」、都寫 100 → **超賣**(搶票比喻)
   - 難的不是 `+1` 算術,是**多請求爭搶同一份共享可變狀態**
6. **解 = 原子性** → Redis 單執行緒
   - **簡單計數 → 一個 `INCR` 就夠**(單一命令天生原子,回傳新值直接判斷,沒有「先讀再寫」的縫)
   - **多步邏輯(sliding window)→ 非 Lua 不可**(刪舊+數+加 三步捆成一包)

### Clarify 檢查表(rate limiter 專用,面試該問的)
| 維度 | 要 clarify |
|------|-----------|
| Functional | 限流單位(user/IP/API-key)、超限**回 429 拒絕不排隊**、是否分級 |
| Non-functional | **精準 vs 效能**(近似可接受?)、延遲預算(夾每個請求→用記憶體)、**限流器掛了 fail-open/closed** |

### 多區域全球限流(park,改天專練)
- A. 單一全球 counter:準,但跨區延遲 + 全球 SPOF
- B. 本地限流 + 非同步對帳:快,但近似(短暫超額)→ **近似可接受時選 B**

### 3AM page test(收尾儀式,第 5 步)
Redis 掛(fail-open?)/ reject 率暴衝(被攻擊 or 誤擋?)/ Redis P99 延遲升高。SLI = reject rate / Redis P99 / Redis 可用性。

---

## 逾期複習清倉(換情境冷測)

- **Bloom**:FP=浪費一次查詢[可接受] / FN=弄丟真資料[災難]。守門員**只會誤放不會誤殺**(真 key 每個 bit 都是 1,必全中)。SSTable:**每檔配一個 Bloom**,說「一定不在」就跳過**讀硬碟**(省的是 disk I/O,不是查 DB;SSTable 就是資料本體無兜底)。
- **CB 三狀態**(配電箱):Closed=電路通=正常放行+數失敗 / Open=跳閘=快速失敗防雪崩 / Half-Open=試推開關放幾個試探(防剛復活的服務被 retry storm 再打死)。
- **Consistent Hashing**:換 `%11` → 幾乎全 remap → 99% miss → DB 過載雪崩。**ring**=加一台只動 1/N(只偷鄰居一段弧);**vnode**=撒很多點讓負載均勻(兩根不同軸)。
- **LB**:sticky session(狀態留 server 釘住人,往內壓)vs Redis store(狀態搬出 server 無狀態,往外拉)= **方向相反**。忙閒不均用 **Least Connections**(不是 latency)。

---

## 🔴 My Mistakes & Misconceptions

1. **Step 1 跳過 clarify 直接報解法** + 把剛複習的 LB 演算法亂套進 rate limiter(recency bias)。→ 面試官還沒聽到思路就在報菜名 = no-hire 開場。
2. **"cost is low"** = 初階 tell。cost 格是證明「營運過」的地方,禁用低/高/還好,一律換具體會咬你的東西。
3. **"because it fixes the problem"** = 循環論證,沒講機制(單一真相來源)。
4. **第 5 次沒主動收尾監控**(unprompted-ops 掛蛋)。3AM page test 焊成第 5 步硬關卡。
5. **兩次要「參考高手答案」** = 逃避持球(#4 弱點)。→ 自己頂回去後推得出 5000/min = 知識本來就在。
6. Bloom SSTable 一開始又漏「每檔配一個」+ 搬「DB 兜底」進 LSM(軸摺疊);CB 三狀態一度忘;Least Connections 英文名想不起。

**共同診斷**:知識全在,病灶 100% 在「壓力下第一句只倒有把握的結論,把沒把握的推導吞回去」。面試官買推導不買結論。

---

## 🎤 How to Say It in Interview

- **開場先 clarify,別跳解法**:「Before I design, let me clarify: are we limiting per-user or per-IP? Is approximate counting acceptable, or must it be exact? And if the limiter itself goes down, do we fail open or closed?」
- **每個決策帶 cost**:「I'd use a centralized Redis counter because all servers share one source of truth — the cost is a network hop per request and Redis becoming a critical dependency I must make HA.」
- **收尾自己丟監控**:「On the ops side, the things that'd page me at 3am are Redis going down, a spike in reject rate, and Redis P99 latency creeping up.」

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| use redis because can fix N server × M user problem, cost is low | I'd use a **centralized counter in Redis** instead of local counters, **because** all servers share one source of truth — a user's count is global, not per-server. The **cost** is a network round-trip per request plus Redis becoming a critical dependency. |
| 會有 race condition 要原子性,用 Redis 單執行緒 Lua | This is a race condition on shared state — I need **atomicity**. For a simple counter a single **INCR** is already atomic; I'd only reach for a **Lua script** when the logic is multi-step, like a sliding window. |
| 每個 SSTable 搭配一個 因為需要知道是哪個 | One Bloom filter **per SSTable** — I need to know *which* file might hold the key, so a "maybe" doesn't force me to read every file from disk. |
