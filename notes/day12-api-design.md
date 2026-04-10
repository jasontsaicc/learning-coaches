# Day 12 — API Design

> Session 14-17 | 2026-04-07 ~ 04-10 | Phase 1
> Chunks 1-7 全部通過 | Interview Drill 3/3 ✅

---

## One-liner

API Design 是根據「誰在呼叫、頻率多高、資料多複雜」來選擇 REST / GraphQL / gRPC，核心矛盾是「通用性 vs 效率」。

## 🔗 Derivation Insight

- **Physical constraint:** 手機頻寬有限（每個 request 都是成本）、網頁期望 <100ms 回應、API 發布後改動成本極高（breaking change）
- **My derivation:** 50 fields 只用 2 個 → over-fetching 浪費頻寬 → 兩條路：固定菜單 (REST) vs 自助餐 (GraphQL) → 不同場景適合不同方案 → 大公司三個都用
- **Surprise:** GraphQL 解決 over-fetching 但犧牲 caching（所有 query 走 POST，CDN 沒法 cache）

## 核心概念整理

### REST vs GraphQL vs gRPC 選擇框架

| 場景 | 選擇 | 理由 |
|------|------|------|
| 外部 API（簡單 CRUD） | REST | 簡單、URL-based caching、CDN 友善 |
| 多種 client 不同資料需求 | GraphQL | client 自己選欄位，解決 over-fetching |
| 內部 service-to-service | gRPC | binary format，速度快，type-safe |

### Chunk 1: REST Fundamentals

- **核心原則：** Resource-based — URL 是名詞（resource 地址），HTTP method 是動詞
- **好處：** Predictable — 不用看文件就能猜到怎麼用

| HTTP Method | 用途 | Idempotent? |
|-------------|------|-------------|
| GET | 讀取 | ✅ |
| POST | 新增 | ❌ |
| PUT | 完整更新 | ✅ |
| PATCH | 部分更新 | ✅ |
| DELETE | 刪除 | ✅ |

**好的設計：** `POST /products/{productId}/likes`（按讚 = 新增一個 like resource）
**壞的設計：** `POST /likeProduct?id=456`（動詞塞在 URL）

### ⚠️ 小杰的錯誤方案

幫每個 client 做不同 API（`/mobile/user/123`, `/web/user/123`）→ 不 scale，N 個 client = N 份 API 要維護

### Chunk 2: GraphQL Fundamentals

- **核心概念：** Client 自己寫 query 指定要哪些 fields，server 只回傳那些 → 解決 over-fetching
- **單一 POST endpoint：** 所有 query 走 POST → URL-based caching（CDN）失效
- **跟 REST 的差別：** REST 由 server 決定回什麼（固定菜單），GraphQL 由 client 決定要什麼（自助餐）
- **小杰的方案 vs GraphQL：** 小杰幫每個 client 開不同 endpoint（burden on backend），GraphQL 同一個 endpoint 讓 client 自己寫 query（burden on client）

### Chunk 3: gRPC Fundamentals

- **定位：** Machine-to-machine 的 API style，不給人類看的
- **為什麼快：** Protobuf binary format → 序列化速度 ~10x faster than JSON，payload 更小
- **Strict contract：** `.proto` file 是 enforced schema，改了 field name → code generation 直接報錯（不像 REST 的 OpenAPI 是 optional 的）
- **HTTP/2：** 原生支援 streaming（client/server/bidirectional）
- **適用場景：** 內部 microservice 高頻呼叫 + latency-sensitive；不適合 public-facing API（browser 不原生支援）

### Chunk 4: Pagination (Offset vs Cursor)

- **Offset：** `?offset=20&limit=10` — 簡單、支援跳頁，但大 offset 慢（掃 N rows 再丟掉）+ 資料變動時會 duplicate/miss
- **Cursor：** `?cursor=xxx&limit=10` — `WHERE id > cursor LIMIT 10` 用 index seek（快）+ 穩定不跳位，但不能跳頁
- **選擇框架：** Admin 後台小資料集 → offset（要頁碼）；Feed/即時資料 → cursor（資料一直在變）

### Chunk 5: API Versioning

- **三種策略：** URL path `/v1/`（最常用）、Header versioning、Query param `?version=2`
- **核心原則：** Don't break existing clients — 保持舊版運行，deprecated 後才下架
- **Breaking vs Non-breaking：** 新增 field/optional param = non-breaking；移除/改名 field = breaking，需要新版本
- ⚠️ Versioning 初次測驗失敗（說「修改不需要新版本」），reteach 後通過

### Chunk 6: Idempotency in APIs

- **問題：** User 按兩次 "Place Order" → 兩張訂單、扣兩次款
- **解法：** Client 產生 Idempotency-Key（UUID），Server 用 `(user_id, idempotency_key)` 當唯一識別
- **流程：** 收到 request → 查 key → 不存在就處理 + 綁結果到 key → 第二次同 key 進來直接回原結果
- **中間狀態：** idempotency record 需要 `pending → processing → completed`，不只是 exists/not exists
- **Crash recovery：** Server crash 在 order 建好但 payment 未完成時 → 第二次 request 看到 status=processing → 檢查已完成步驟 → 從未完成的步驟繼續（resume, not restart）

### Chunk 7: Observability Mini

| Element | API Design |
|---------|-----------|
| **SLIs** | Latency (P50/P99), Error rate (4xx/5xx), Throughput (req/sec) |
| **SLO target** | P99 < 200ms, 99.9% availability |
| **Alerts** | Error rate spike, latency 突然上升 |
| **Dashboards** | Throughput, latency distribution, error rate by endpoint |

⚠️ 之前混淆：把 SLI/SLO/Dashboard 當成 metrics 本身（SLI 是 **measurement**，metrics 如 latency/error rate 是具體數值）

---

## Interview Drill: Food Delivery API Design

**Score: 3/3 ✅** (Think Aloud ✅ | Scope Negotiation ✅ | Used API Design ✅)

### Step 1: Clarify Requirements
- Functional: 找餐廳、看菜單、下單、追蹤
- Non-functional: low latency for search, order reliability
- Scope: focus on customer-facing API, not driver/restaurant side

### Step 2: High-Level Design
- REST for client-facing, gRPC for internal services
- Core endpoints:
  ```
  GET  /v1/restaurants                      -- 搜尋餐廳
  GET  /v1/restaurants/{restaurant_id}/menu  -- 某餐廳的菜單
  POST /v1/orders                           -- 下單
  GET  /v1/orders/{order_id}                -- 查/追蹤訂單
  GET  /v1/users/{user_id}/orders           -- 歷史訂單
  ```
- Pagination: cursor-based（資料持續新增 + 大量資料 offset 效能差）
- Order body: restaurant_id, items[{item_id, quantity}], delivery_address, payment_method_id
- Security: price 由 server 算（防竄改），user_id 從 auth token 取（不放 body）

### Step 3: Deep Dive — Idempotency
- Idempotency key 防止 duplicate order/payment
- 中間狀態處理 crash recovery（見 Chunk 6）

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| REST 核心就是用 HTTP method 做 CRUD | REST 核心是 **resource-based**：URL 用名詞表達資源，method 當動詞，讓 API predictable | 只記住了 method 的部分，沒想到 URL 設計原則也是核心 |
| Over-fetching 的問題只有「比較慢」 | 兩個問題：(1) over-fetching 浪費頻寬 (2) tight coupling — 每次前端需求變動都要改後端 | 只想到效能面，沒想到維護面的 coupling 問題 |
| gRPC 知道是 service-to-service 用，但說不出 WHY | 要講出具體原因：(1) binary format ~10x faster (2) `.proto` strict contract 避免跨團隊 field 改名爆炸 | 只記住 WHAT（用途），沒記住 WHY（為什麼比 REST 更適合）— 面試要答的是 WHY |
| GraphQL transfer 只說「可以用 GraphQL」沒解釋 HOW | 要說出機制：同一 endpoint，client 自己寫 query 選 fields → burden 從 backend 移到 client | 知道 GraphQL 能解決問題，但沒辦法解釋它怎麼解決的 — 理解停在表面 |
| 不知道 GET data 放 URL、POST data 放 body | GET 參數放 query string（URL 上），POST 放 request body（大小限制小） | HTTP 基礎沒碰過，只用過 curl 或 UI 工具 |
| REST path 用 singular noun (`/restaurant`) | Collection 用 plural（`/restaurants`），single item 用 `/{id}`（`/restaurants/123`） | 沒想過 URL 是在描述 collection |
| Path parameter 寫成字面文字 (`restaurant_id`) | Path parameter 用 placeholder: `/restaurants/{restaurant_id}`，實際呼叫是 `/restaurants/123` | API 文件讀太少，不知道 `{id}` 慣例 |
| Price 和 user_id 放 request body 讓 client 傳 | Price 由 server 從 DB 算（防竄改），user_id 從 auth token 取（防偽造） | **沒想過 client 可以竄改 request body** — API security 盲點 |
| Pagination 說成 "offline"，cursor 想不起來名字 | Offset（偏移量）和 Cursor（游標）是兩種分頁法 | 學過但沒記住名詞，說明理解不夠深 |
| Idempotency record 只有 "有/沒有" 兩種狀態 | 需要中間狀態 `pending → processing → completed`，才能在 crash 後 resume 未完成的操作 | 只想到 "擋重複"，沒想到 crash recovery 場景 |
| Versioning 說「修改不需要新版本」 | Rename/remove field = breaking change，必須新版本 | 把「修改」跟 non-breaking change 搞混了 |
| Observability 把 SLI/SLO 當成 metrics | SLI 是 measurement type（如 latency），metrics 是具體數值（如 P99=150ms） | 概念層次沒分清楚，framework vs 具體指標 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "API Design is about choosing the right API style — REST, GraphQL, or gRPC — based on who's calling, how often, and how complex the data is. The key trade-off is flexibility versus simplicity and cacheability."

**When asked to go deeper:**
> Q: "Why not just use GraphQL for everything?"
> A: "GraphQL solves over-fetching, but all queries go through POST, making CDN caching much harder. For simple CRUD with predictable data, REST is simpler and more cache-friendly. For internal high-throughput service-to-service calls, gRPC's binary format is faster."

> Q: "How do you prevent duplicate orders?"
> A: "The client generates an idempotency key before sending the request. The server checks if this key exists. If not, it processes the order and binds the result to the key. If the same key comes in again, it returns the cached response. The key also needs intermediate states like processing, so if the server crashes mid-flow, it can resume from where it left off."

**Showing production depth:**
> "In production, I'd monitor P99 latency per endpoint, 4xx/5xx error rates, and set alerts on error budget burn rate. For order APIs, I'd track idempotency key hit rate to detect retry storms."

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| REST is easily use but will get all data maybe will late | REST is easy to use but returns all data, which may cause latency |
| GraphQL 要什麽取就取什麽 但是 trade off 是後端會稍微複雜 且學習成本高 | GraphQL lets you fetch exactly what you need, but the trade-off is higher backend complexity and learning cost |
| gRPC 是 binary 機器内部使用的 速度快 人類沒法閲讀 | gRPC uses binary format for internal machine-to-machine communication — it's fast but not human-readable |
| 統一 人類好懂 | It provides a uniform interface that's easy for humans to understand |
| graphQl solves the REST get to much data ploblem... but the trade-off is the backend will more complex and all POST single endpoint | GraphQL solves REST's over-fetching problem. Different devices need different fields — mobile might only need 2 fields, so we don't want to fetch all 50 and waste bandwidth. But the trade-off is higher backend complexity and a single POST endpoint, which breaks URL-based caching. |
| gPRC is for service to service use | gRPC is designed for internal service-to-service communication. |
| gRPC use binary format fast than REST usually json and more small | gRPC uses binary format, which is faster than REST's JSON and produces smaller payloads. |
| when use REST two teams use API docs... gRPC is different strict schema | With REST, two teams rely on API docs or OpenAPI specs. If one team changes a field name, the other service will break. gRPC enforces a strict schema via the `.proto` file, reducing cross-team integration errors. |
| i'd push for gRPC if the inventory call is on a high volume latency-sensitive | I'd push for gRPC if the inventory call is high-volume and latency-sensitive. |
| 因爲GraphQL是自己寫query 決定要拿什麽 | GraphQL uses POST because the client writes its own query to specify which fields to fetch. The query can be complex with nested fields and variables, so it goes in the request body, which means POST. |
| cursor 因爲一直有新的, 而且數量太多了 | I'd use cursor-based pagination because new restaurants are constantly being added, and with a large dataset, offset pagination degrades in performance as you go deeper. |
| 因爲擔心duplicate order or payment | I'd deep dive into the Order service because duplicate orders and duplicate payments are the most critical failure mode in a food delivery system. |
