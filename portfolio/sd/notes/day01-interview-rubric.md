# Day 01: What SD Interviews Actually Test

> Status: ✅ Completed

---

## 📝 One-liner

SD 面試不是考你背答案，而是考你怎麼思考 — 用 4 個維度評分：問需求、畫架構、講深度、比優缺。

---

## Key Concepts

### SD 面試的 4 個評分維度

口訣：**問 → 畫 → 深 → 比**

| # | Dimension | 一句話 | 比喻 |
|---|---|---|---|
| 1 | **Problem Navigation** | 問對的問題來釐清需求和 scope | 廚藝比賽先問幾人份、有沒有食材限制 |
| 2 | **System Design** | 畫出合理的 high-level 架構圖 | 先畫藍圖再蓋房子 |
| 3 | **Technical Depth** | 深入解釋 component 的選擇（why + how + 限制） | 不只說「用烤的」，要說為什麼烤比煎好 |
| 4 | **Trade-off Analysis** | 分析方案的優點、缺點、什麼條件下改選別的 | 烤的少油但不脆，要脆就改煎 |

### 每個 Dimension 的好 vs 壞回答

| Dimension | ❌ Bad | ✅ Good |
|---|---|---|
| Problem Navigation | 聽到題目就畫架構圖 | 先花 3-5 分鐘問 requirements |
| System Design | 一口氣畫超複雜架構 | 先 high-level，再逐步深入 |
| Technical Depth | 「用 Redis 做 cache」就沒了 | 解釋 why Redis（in-memory, < 1ms latency, TTL） |
| Trade-off Analysis | 只講優點 | 同時講優點、缺點、什麼條件下改選別的 |

### 重要心態

- **問問題 ≠ 承諾你都會**：問「一對一還是群聊？」是展示你知道複雜度不同，不是說你群聊也會做
- **不需要每個技術都有生產經驗**：理解原理就夠 — 知道它解決什麼問題、跟替代方案的差異、它的限制
- **Dimension 1 是 Dimension 2 的地基**：沒有需求的架構圖就是亂猜

---

## 📋 Exercise: URL Shortener 回答分析（✅ 完成）

### 題目：Design a URL Shortener

**回答 A**（差）：用 server + MySQL，接收長網址、存 DB、redirect。

**回答 B**（好）：先問 QPS/過期/自訂短碼 → NoSQL + Base62 (7位) + Redis cache → 分析 Base62 vs random hash trade-off。

### 4 Dimensions 評分

| Dimension | 回答 A | 回答 B |
|---|---|---|
| Problem Navigation | 完全沒問需求 ❌ | 問了 QPS、過期、自訂短碼 ✅ |
| System Design | 只有 server + MySQL，沒有層次 ❌ | App Service + NoSQL + Redis cache，有層次 ✅ |
| Technical Depth | 「存到資料庫」就沒了 ❌ | 解釋 Base62 為什麼 7 位夠用（62^7 計算）✅ |
| Trade-off Analysis | 完全沒有 ❌ | Base62 不碰撞但可預測 vs random hash 安全但多 DB write ✅ |

**重點：回答 A 的架構也能動，但面試不是看能不能動，是看思考過程。**

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 問問題會暴露自己不會的東西，所以不敢問 | 問問題是展示思考能力，面試官通常會幫你縮小範圍 | 把「問問題」誤解為「承諾都會」，其實是展示你知道複雜度不同 |
| 沒有實際工作經驗的技術（如 WebSocket）講不出深度 | 理解原理就夠：知道它解決什麼問題、跟替代方案差異、限制 | 以為 Technical Depth = 生產經驗，其實是理解 what/why/downsides |
| 4 Dimensions 學完馬上被問卻回想不出來 | 需要口訣輔助記憶：問 → 畫 → 深 → 比 | 只是聽過一遍，沒有主動整理記憶點 |
| 分析好壞回答時只說「B 比較完整」 | 要逐個 Dimension 對比，說明每個維度具體差在哪 | 停在整體感覺，沒有用 framework 拆解分析 |
