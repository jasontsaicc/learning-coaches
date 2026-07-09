# Day 23-24: Rate Limiting & Circuit Breaker

> Sessions 28（教學 S28 完成）。Phase 2 🌐。問題錨定 + 深度天花板模式。

---

## One-Liner

**Rate Limiting**：限制單位時間內請求數量，保護後端不被流量打垮 + 確保公平性；核心選型是 burst 容忍度（Token Bucket 容許突發 vs Sliding Window 嚴格封頂）。

**Circuit Breaker**：偵測下游故障時「快速失敗（fail fast）」不再硬打，避免一個下游掛掉拖垮整條鏈路（雪崩）。

---

## Core Concepts（7 chunks 全過 at interview depth）

### 1. Token Bucket（令牌桶）

- 桶容量 = capacity，每秒補 `refillRate` 顆 token，每個請求拿 1 顆，沒 token 就 **reject**（不是 queue，queue 是 leaky bucket）
- **容許 burst**：攢著的 token 可一次用掉 → 平常閒置、偶爾爆量的場景友善
- 類比：AWS T-series CPU credits（閒置時攢 credit，需要時爆發）

### 2. Lazy Refill（懶惰補充）⭐ PoC 核心

- **不開背景 goroutine 每秒幫每個桶 +token**，而是「有人呼叫 `Allow()` 那一刻才回頭算這段空窗該補多少」，一次補齊
- **為什麼重要**：100 萬個 user 各一個桶，Eager 方案要掃 100 萬次/秒（99% 浪費在閒置桶）；Lazy 只算「真的有流量」的桶 → **計算成本跟著流量走，不跟著桶數量走**
- Lazy vs Eager 是 CS 根本二分法（lazy loading / lazy evaluation 同源思維）

### 3. Sliding Window（滑動視窗）

- 任意時間窗內**嚴格不超過 N** → 適合下游有硬上限（DB 每秒只扛 1000 QPS，超過就掛）
- boundary burst 問題：固定視窗在交界處可能瞬間 2x（sliding window 解這個）

### 4. TB vs SW trade-off（⚠️ misconception 已打通）

| | Token Bucket | Sliding Window |
|---|---|---|
| 行為 | 容許 burst | 嚴格封頂 |
| 用在 | 偶爾爆量可接受 | 下游硬上限不能超 |
| 本質 | 彈性 | 可預測性 |

### 5. 分散式 Rate Limiting（local counter 失效）

- 3 台機器各跑 in-memory 桶 → 實際上限變 **N × limit**（每台只看到 1/3 流量，無全局視野）
- 解法：計數**集中**到 Redis（共享儲存）
- **三個代價**：latency（多一次網路往返）、bottleneck（Redis 成熱點）、SPOF（Redis 掛 → fail-open 還 fail-close？）

### 6. Circuit Breaker 三狀態

| 狀態 | 運作 |
|------|------|
| **Closed**（正常） | 請求通過，統計失敗率 |
| **Open**（斷開） | 失敗率超閾值 → fail fast，不再打下游，給它喘息 |
| **Half-Open**（試探） | cooldown 後放少量請求探路，成功→Closed，失敗→退回 Open |

- 核心價值：**fail fast** 釋放卡死的連線，防雪崩
- Half-Open 的「少量試探」避免「一恢復就全量灌爆再次打掛」（= thundering herd）

### 7. Observability（fail-open vs fail-close）

- Rate limiter / Redis 掛掉時：**fail-open**（放行，保可用性）vs **fail-close**（擋住，保安全）→ 看業務性質

---

## 🔗 縱深防禦（Defense in Depth）⭐ 面試金句

> **Rate Limiter 在入口擋過量（預防）+ Circuit Breaker 在出口偵測下游死掉就止血（fail fast）**。一個防「太多進來」，一個防「下游死了還硬打」。

兩層限速最佳實踐：**per-user 擋單一濫用者（公平性）+ global 封頂保底（保護 DB）**。

---

## Scale Trigger

- 單機 → 多機：local in-memory counter 失效（N×limit），需集中到 Redis
- 流量遠超下游容量（50K QPS vs DB 1000 QPS）：global 嚴格封頂 + Circuit Breaker 防雪崩

## DevOps Angle（監控 3 指標）

1. **Rate limiter reject 數**（擋了多少 → 知道攻擊規模 + 是否誤殺正常 user）
2. **Circuit Breaker 當前狀態**（Open = 下游正在掛）
3. **下游 DB P99 latency**（飆高 = 即將觸發斷路器）

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 不清楚 lazy 是什麼 | Lazy = 有人用才算（敲門才補 token），對比 Eager = 背景一直算 | 沒接觸過 lazy/eager 這組 CS 概念 |
| Interview Drill：global 一個桶就好 | global 保護 DB ✅ 但會被爬蟲吸乾、餓死正常 user（公平性 ❌）→ 要 per-user + global 兩層 | 只想到「保護 DB」單一目標，漏了「公平性」第二目標 |
| Circuit Breaker 講得出概念但沒講出三狀態名稱 | Closed / Open / Half-Open 是術語，面試要講出來才專業 | 概念懂、術語還不熟（recall 已補） |
| （PoC）method 簽名斷成兩行 `Allow\n()` | Go 自動分號：識別字在行尾會補 `;`，`{` 必須同行 | Go ASI 規則還不熟 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "Rate limiting protects the backend from overload and ensures fairness. The key choice is Token Bucket — which allows bursts — versus Sliding Window, which strictly caps. I'd layer per-user limits for fairness plus a global cap to protect the DB, and add a Circuit Breaker on downstream calls to fail fast and prevent cascading failure."

**When asked to go deeper:**
> Q: "How do you rate-limit across multiple servers?"
> A: "In-memory counters break because each machine only sees a fraction of traffic, so the effective limit becomes N times the intended one. I'd centralize the count in Redis — at the cost of added latency, a potential bottleneck, and a single point of failure that forces a fail-open vs fail-close decision."

> Q: "The DB starts timing out — how do you stop the whole service from collapsing?"
> A: "A Circuit Breaker. When failure rate crosses a threshold it trips to Open and fails fast instead of waiting on timeouts, releasing connections. After a cooldown it goes Half-Open, letting a few test requests through before fully recovering — which also avoids a thundering herd on recovery."

**Showing production depth:**
> "I'd monitor three things: rate-limiter reject count, Circuit Breaker state, and downstream DB P99 latency."

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| 每次都要調整100萬桶 | "With the eager approach, you'd update all 1M buckets every second, even idle ones. Lazy refill only computes on an actual request, so cost scales with traffic, not bucket count." |
| Token Bucket 容許 burst，Sliding Window 嚴格封頂 | "Token Bucket allows bursts by spending accumulated tokens, while Sliding Window enforces a strict cap within any window." |
| 如果每台都有自己的計數器，實際可能 N×100 | "If each machine keeps its own counter, the effective limit becomes N times the intended one, because each machine only sees a fraction of the traffic." |
| 兩層疊加，per-user 限速 + global 封頂保底 | "I'd layer two limiters: per-user to stop any single abuser and keep things fair, plus a global cap as a backstop to protect the DB." |
| Sliding Window，因為要嚴格封頂不能讓 burst 超過 DB 上限 | "I'd use Sliding Window for the global cap, because the DB has a hard ceiling — Token Bucket bursts could momentarily exceed it and crash the DB." |
| 要設定後面服務掛掉就不要繼續打，或減量先測試後端正常沒 | "I'd add a Circuit Breaker: when failures cross a threshold it trips Open and fails fast; after a cooldown it goes Half-Open to test recovery with a few requests." |

---

## PoC

`projects/day23-rate-limiter/main.go` — Light Code Token Bucket（lazy refill）。
- 學生手打練語法，自己抓 5 個 typo + Go ASI 簽名問題
- 驗證：120 req → ~100 allowed；sleep 1s → refill 10 → ~10 allowed ✅（證明 rate = refillRate × time）
- **Park**：Circuit Breaker PoC + 分散式 Redis rate limiter → Day 31-32

---

## Cross-Verification（下次帶來）

對照 **Alex Xu Vol.1 Ch.4 (Design a Rate Limiter)** — 確認 Token Bucket / Sliding Window Log / Sliding Window Counter 的差異，看 Alex Xu 怎麼講「Redis 集中計數 + race condition（Lua script 原子操作）」這一塊。
