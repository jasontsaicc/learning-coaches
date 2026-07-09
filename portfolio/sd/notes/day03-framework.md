# Day 03: Your SD Answer Framework (4-Step Method)

> Status: ✅ Completed

---

## 📝 One-liner

SD 面試用 4-Step Framework 回答：Clarify → High-level Design → Deep Dive → Scale & Trade-offs，45 分鐘內每個 Step 都有固定時間分配。

---

## Key Concepts

### 4-Step Framework + 時間分配

```
[0-5 min]   Step 1: Clarify        → 問需求（Functional + Non-functional）
[5-10 min]  Estimation              → 估算 QPS / Storage（如果需要）
[10-20 min] Step 2: High-level     → API → Data Model → Architecture Diagram
[20-35 min] Step 3: Deep Dive      → 挑 1-2 個核心 component 深入
[35-45 min] Step 4: Scale & Trade  → 擴展 + 取捨 + 監控
```

對應 Day 1 的 4 Dimensions：

| Step | Dimension | 時間 |
|---|---|---|
| Step 1: Clarify | Problem Navigation | 5 min |
| Step 2: High-level Design | System Design | 10 min |
| Step 3: Deep Dive | Technical Depth | 15 min |
| Step 4: Scale & Trade-offs | Trade-off Analysis | 10 min |

### Step 1: Clarify

問兩類問題：

| 類型 | 問什麼 | 範例（URL Shortener） |
|---|---|---|
| **Functional** | 系統做什麼（功能面） | 建立短網址、redirect、自訂短碼？過期？ |
| **Non-functional** | 系統做得多好（效能面） | 100M DAU、讀寫比 100:1、latency < 100ms |

**重點：限制 5 分鐘，問 5-8 個問題就收。不確定的先假設：**
> "I'll assume X for now. Let me know if you'd like me to adjust."

### Step 2: High-level Design

按順序做 3 件事（口訣：**API → Data → Diagram**）：

1. **API Design** — 定義主要 endpoints
2. **Data Model** — 定義主要資料結構
3. **Architecture Diagram** — 畫 high-level 架構圖

為什麼這個順序？API 決定系統要處理哪些請求，有了這個才知道架構圖需要哪些 component。先有需求，才有設計。

### Step 3: Deep Dive

**挑 1-2 個核心 component 深入，不是每個都講一遍。**

深入時講 4 點：

```
① What       — 選了什麼技術
② Why        — 為什麼選這個，不選其他的
③ How        — 具體怎麼運作
④ Limitation — 這個選擇的限制
```

### Step 4: Scale & Trade-offs

講 3 件事：

| 項目 | 問自己 |
|---|---|
| **Scale** | 流量成長 10 倍，哪裡先撐不住？怎麼解決？ |
| **Trade-offs** | 我選了 X，好處是...，代價是...，什麼條件下改選... |
| **Monitoring** | 監控什麼 metric？alert threshold？（DevOps 加分項）|

### 處理沒見過的題目

不需要「知道答案」，把任何系統拆成已知的 building blocks：

> **每個系統 = Storage + API + 獨特的 domain logic**

| 沒見過的題目 | 拆成 Building Blocks |
|---|---|
| Parking Lot System | DB（車子進出記錄）+ API（進出/結帳）+ Cache（車位狀態）|
| Library System | DB（書本/借閱記錄）+ API（借書/還書/上架）+ Cache（即時庫存）|

### Scope Negotiation

主動跟面試官協商範圍：

> **"I'll focus on [核心功能]. Should I also cover [延伸功能], or dive deeper into [核心功能]?"**

---

## 📋 Exercise: Notification System Step 1（✅ 完成）

題目：Design a Notification System（類似 AWS SNS）

**Functional Requirements:**
- 支援多管道（push / email / SMS / 電話 / Teams）
- 通知能否漏掉？需要 retry？
- 用戶可設定偏好（只要 email 不要 SMS）

**Non-functional Requirements:**
- 多少 user？一次通知多少人？
- 延遲要求？（1 秒內 vs 幾分鐘都行）

**Scope Negotiation:**
> "I'll focus on the core delivery pipeline. Should I also cover user preference management, or dive deeper into the delivery pipeline?"

---

## ⚖️ Trade-off

- Step 1 花太久（>5 min）→ 後面 3 個 Step 被壓縮，面試官看不到設計能力
- Deep Dive 每個 component 都講 → 每個都很淺，不如挑 1-2 個講深

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 不懂「API 決定邊界」是什麼意思 | API 定義系統要處理哪些請求，架構圖是為了處理這些請求而設計的。沒有 API 就不知道需要哪些 component | 以為架構圖是第一步，其實 API 才是起點 |
| 遇到沒見過的題目就不知道怎麼開始 | 用 4-Step Framework 都能開始，Step 1 問需求不需要預先知道答案 | 以為要「知道答案」才能開始，其實 Framework 就是你的起點 |
| Notification System 太廣泛不知道怎麼問 | 「太廣泛」本身就是信號，代表你需要問面試官「是什麼場景的通知？」 | 沒意識到模糊題目是故意的，就是考你會不會 clarify |
| 不知道怎麼做 Scope negotiation | 模板很簡單：「我先做 X，要不要也做 Y？」 | 以為需要很厲害才能談範圍，其實只是一句話的事 |
| 不知道 `:chatId` 的 `:` 是什麼 | REST API 的 path parameter 佔位符，`:chatId` 代表會被替換成實際值（如 abc123） | 之前 Go Day -2 寫過 `/keys/:key` 但沒注意到這個語法 |
