# Day 25 — Observability（可觀測性）

> Phase 2 · Session 29 · 2026-06-15
> Mode: 問題錨定 + 深度天花板（理論壓縮，capped 在面試深度）

---

## One-liner

> Observability 用三根支柱回答系統的三個問題 —— **Metrics（多少/哪台異常）、Logs（什麼/為什麼出錯）、Traces（在哪/請求卡第幾跳）**，靠 correlation ID 把一個請求跨服務串成一條時間軸，讓你在數千節點裡不用逐台 ssh 就能定位問題。

## Trade-off

- **三支柱缺一不可**：各有盲區，互相補。Metrics 看不到原因、Logs 串不起跨服務、Traces 看不到那一跳的細節。
- **SLO 一定比 SLA 嚴格**：給自己留 buffer，內部告警先響，在「違約賠錢」之前有時間補救。
- **Trace 100% 覆蓋 vs 組織成本**：全員都要埋 trace-id，一個團隊偷懶 → 鏈斷在那 → 下游全消失。

## Scale trigger

- 數十～數千節點、一個請求跨 5-20 個服務 → 無法逐台 ssh → 必須集中式可觀測性。
- Log/Trace 量隨流量線性成長 → 全量存太貴 → 需要 **sampling**（head-based vs tail-based）。＊park，面試深度不需細節
- Metrics 高 cardinality（每個 user_id 一條 → 百萬 time series）→ 需聚合。＊park

## DevOps angle

- **Debug 動線（口訣）**：**Metrics 報警 → Traces 指路 → Logs 挖根因**。
- Production 我會定義 SLO（如 P99 < 200ms），用 metrics 設 burn-rate 告警、traces 定位慢的那一跳、logs 挖根因。
- **SLI 要用 P99/P95 不用平均** —— 平均會被超慢的尾巴拉平，dashboard 綠燈但用戶在哀號（tail latency）。

---

## 🔑 三支柱盲區對照表（精華）

| 工具 | 能看到 | 看不到 | 回答的問題 |
|------|--------|--------|-----------|
| **Metrics** | 數字趨勢、dashboard、哪台不健康 | 出事原因、單一請求（只有聚合平均）| 多少？哪台？ |
| **Logs** | 單一事件、error、出錯原因 | 整體趨勢、跨服務串聯、卡哪一跳 | 什麼？為什麼？ |
| **Traces** | 請求完整旅程、卡第幾跳、每跳耗時 | 那一跳為何慢的細節、且常是 sampling | 在哪？第幾跳？ |

## 🔑 SLI / SLO / SLA（考試比喻）

| 縮寫 | 是什麼 | 考試比喻 | 例子 |
|------|--------|----------|------|
| **SLI** Indicator | 實際量到的數字 | 實際考 85 分 | P99 = 150ms |
| **SLO** Objective | 內部目標 | 要考 90 分 | P99 < 200ms |
| **SLA** Agreement | 對客戶的合約 + 罰則 | 考不到 80 分沒收手機 | 99.9% 否則退費 |

- 自檢法：**「客戶會在乎這個數字嗎？」** 在乎（快不快/會不會壞）→ SLI；不在乎（CPU%）→ 內部 metric。
- SLI 三類：**Latency（快不快）、Availability/Error rate（會不會壞）、Throughput（撐不撐得住）**。

## Correlation ID 機制

1. **產生**：入口（API gateway / 第一個服務）生成唯一 trace ID
2. **傳遞**：每次呼叫下游，把 ID 放進 **HTTP header** 帶下去
3. **記錄**：每個服務 log 都帶上這個 ID → `grep <id>` 串起全程

```go
traceID := r.Header.Get("X-Trace-Id")
if traceID == "" {
    traceID = uuid.New().String() // 入口才生成；有就沿用
}
req.Header.Set("X-Trace-Id", traceID) // 往下游傳，斷一個鏈就斷
```

---

## 🔗 Derivation Insight

- **Physical constraint:** 數十～數千節點、不能逐台 ssh、一個請求跨 5-20 個服務、問題常在「服務之間」。
- **My derivation:** 我先想到要看每個服務的 CPU/memory/latency（= Metrics）→ 被追問「為什麼慢」時想到看 log（= Logs）→ 想追蹤路徑時直覺講 traceroute（= 點到 Traces，只是工具層級錯了）。
- **Surprise:** traceroute 是 L3 網路層追路由器，distributed tracing 是應用層追「請求」跨服務 —— 但我的直覺方向（追路徑）是對的，tracing 就是「應用層的 traceroute」。

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 追蹤請求路徑用 traceroute | traceroute 追網路路由器（L3）；追請求跨服務要 distributed tracing（應用層）| 把「網路封包路徑」和「請求在服務間的旅程」混為一談 |
| Debug 先看 trace | 先看 **metrics**（告警/雷達指方向）→ 再 trace 定位 → 最後 log 挖根因 | 沒有「metrics 是雷達、先指路」的動線概念 |
| （drill）答案講太精簡「先看 trace」就停 | 面試要主動把 why + 取捨一次講足，不要等追問 | 老習慣：握不住球，傾向問面試官要參考答案（S8/S24 同根）|
| （複習）Consistency = read-your-write/strong/eventual 三個選項 | 是一條**光譜**：軸 = 新鮮度 vs 等待成本；Strong（最新但等同步=慢）↔ Eventual（快但 stale）| 只記名字、沒抓到「光譜的軸在量什麼」|

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> 「Observability 是用三根支柱回答系統健康的三個不同問題：Metrics 告訴我哪台、哪個指標異常；Traces 告訴我一個請求卡在第幾跳；Logs 告訴我那一跳為什麼出錯。關鍵是 correlation ID 把跨服務的訊號串成一條時間軸。」

**When asked to go deeper:**
> Q:「系統慢但 dashboard 綠燈，為什麼？」
> A:「dashboard 可能看的是平均延遲，會被超慢的尾巴拉平。我會看 P99/P95，1% 的百萬用戶就是上萬個怒吼的人。SLI 要看尾巴不看平均。」

**Showing production depth:**
> 「In production 我會定義 SLO，例如 P99 < 200ms，SLO 壓得比 SLA 嚴格留 buffer。告警用 metrics 設 burn-rate，出事時走 Metrics→Traces→Logs 動線定位，目標 10 分鐘內找到是哪一跳。」

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| if we have many service it's very hard to check all services, so need distributed tracing | "With many services, logs are scattered across machines and metrics only show per-service averages — neither can stitch one request's journey together. Distributed tracing tags each request with an ID so all hops form a single timeline, pinpointing which hop is slow." |
| 整個 chain 就中斷了，沒辦法繼續追查 | "The trace breaks at that hop — every service downstream of the one that dropped the header falls off the trace, leaving a blind spot exactly where you need visibility." |
| 1. SLI 2. SLA（分辨題）| "A measured P99 latency is an SLI; a guaranteed 99.9% availability with refund penalties is an SLA." |
| 平均可能會有人超級慢嚴重影響體驗 | "Averages hide tail latency — a small fraction of very slow requests gets masked by the fast majority, so I'd track P99/P95 instead of the mean." |
| （Consistency 複習）一定是最新的資料一定要全部 server 同步完成 | "Strong consistency is slower because every read must wait for all replicas to finish syncing to the latest value — you trade latency for freshness." |

---

## 📖 Cross-verify（下次帶來）

Google SRE Book Ch.6 的 **Four Golden Signals**（Latency, Traffic, Errors, Saturation）。
比對我們的 SLI 三類（Latency / Availability·Error / Throughput）—— 我們漏了哪個？
（提示：**Saturation** 飽和度，例如 disk/connection pool 快滿 —— 我們沒提到，想想它算 SLI 還是內部 metric。）
