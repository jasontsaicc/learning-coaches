# Weekly Review #2 — Part 2 (Mistake Review)

> Status: ✅ Session 18 complete
> Date: 2026-04-27
> Goal: 集中清掉 ❌ Unresolved 的 mistakes，讓 Mistake Registry 能勾選
> Result: **8 mistakes resolved in one session** 🔥（單次最高）
> See also: `weekly-review-02.md` for Part 1 (blind recall + interview templates)

---

## 📊 Gap Check Findings

| Topic | Recall Score | Gap Type | Action |
|-------|--------------|----------|--------|
| API Design | 2/4 | **Notes gap** — Scale Trigger / DevOps Angle 兩個 section 根本不在筆記裡 | ✅ 已補 (見 day12-api-design.md) |
| Caching | 4/4 | None | — |
| MQ | 2/4 | **Memory gap** — 筆記有寫但忘了 | 重念筆記 |

**Lesson learned：** 這次發現一種新的 gap — 「**筆記從一開始就漏寫**」。下次寫筆記後要對照 Weekly Review 的 4 個面向（One-liner / Trade-off / Scale Trigger / DevOps）自檢，不能漏 section。

---

## ✅ Mistakes Resolved (8 total)

### API Design (5 resolutions)

| # | Mistake | Key Insight |
|---|---------|-------------|
| 1 | 不知道 GET data 放 URL、POST data 放 body | **3 角度**：Security（URL 可見會 leak）/ Size（body 可放更大）/ Caching（GET URL 可被 CDN cache）|
| 2 | Price/user_id 放 request body | **Auth → Header（JWT）/ Business data → Body**。client 可竄改 body，但 JWT 是 signed 不能偽造 |
| 3 | Pagination 說成 "offline" | Offset（簡單但 deep pagination 慢）+ Cursor（O(log n)、stable，無法跳頁）|
| 4 | Idempotency 只想到 exists / not exists | 第三狀態 **`processing`** — 解決 race（同 key 100ms 內進來兩次的 mid-flight 重複）|
| 5 | SLI/SLO/Dashboard 當 metrics | **Metric → SLI → SLO → Dashboard** 階層：raw data → 度量類型 → 目標值 → 視覺化 |

### Message Queue (3 resolutions)

| # | Mistake | Key Insight |
|---|---------|-------------|
| 6 | Delivery semantics 名字不完整 | **At-most-once**（cheap, may lose）/ **At-least-once**（reliable, may duplicate）/ **Exactly-once**（perfect but expensive，幾乎沒人真的做到）|
| 7 | Why Async 只記得 "fast response" | **3 reasons**：Decoupling（Order→Notification）/ Buffering（Flash sale 10x traffic）/ Resilience（Payment service down 不掉資料）|
| 8 | 忘了 FR/NFR/Scope 定義 | FR = 做什麼（user follows + sees feed）/ NFR = 多好（feed P99 < 200ms）/ Scope = 做哪些不做哪些（only feed, exclude messaging）|

---

## 🎤 New Interview Templates (從 mistake review 提煉)

### GET vs POST data location

> "GET requests carry data in the URL as query strings because URLs are cacheable and bookmarkable, but they're visible in logs and history. POST requests use the request body for larger payloads and to keep sensitive data off the URL."

### Where user_id comes from

> "user_id should always come from the verified Authorization header, not the request body. The client could put any user_id in the body, but the JWT in the header is cryptographically signed and verified by the auth middleware. The pattern: **authentication data → header, business data → body**."

### Idempotency with crash recovery

> "An idempotency record needs three states, not two: `not_exists`, `processing`, and `done`. The `processing` state matters because duplicate requests can arrive while the original is still in flight — without this state, both requests see 'not exists' and execute concurrently, causing double-charge."

### Why MQ (3 reasons)

> "MQ serves three purposes: **decoupling** like Order handing off to Notification so email delays don't block checkout; **buffering** like flash sale 10x spikes flattening into steady consumer rate; and **resilience** — when Payment Service goes down, orders queue up and replay on recovery, no data loss."

### Functional / Non-functional / Scope (Instagram example)

> "Functional describes what the system does — like users can follow others and see their posts. Non-functional describes how well — like feed P99 latency under 200ms. Scope defines in/out — for Instagram, I'd focus on feed and explicitly exclude messaging."

---

## 🗣️ English Practice — Session 18

| My Answer | English Polish |
|-----------|----------------|
| ok REST GET method use URL POST use request body | For REST APIs, GET requests carry data in the URL as query parameters, while POST requests carry data in the request body. |
| 1. client can see URLs, 2. size in body can carry more data, 3. URL can use cache | Three reasons: GET data in URL leaks to logs and history (security), URL has length limits while body can carry more (size), and GET URLs are cacheable by browsers and CDNs (caching). |
| always not trust client, so price to db search | Never trust the client — the price should come from a database lookup by item_id, never from the request body, because the client can forge any value. |
| body client can fake, so in header use jwt | The body can be forged by the client, so authentication data like user_id should live in the Authorization header as a signed JWT, which can't be tampered with. |
| offset pagination 類似 limit 抓前 50 筆... cursor 是記錄上一筆 id | Offset pagination is simple like LIMIT 50 OFFSET N, but deep pagination is slow because the database has to scan and skip N rows. Cursor pagination uses the last seen ID as a bookmark — it's O(log n) and stable under concurrent writes. |
| third state is processing... duplicate request can arrive while original still in progress | The third state is `processing`. It matters because a duplicate request can arrive while the original is still in flight — without this state, both requests would execute and cause double-charge. |
| metric are raw data, SLIs define how we measure user experience, SLOs define acceptable targets, dashboard visualize them | Metrics are raw data points. An SLI is the kind of measurement we care about, derived from metrics. An SLO is the target threshold for the SLI. Dashboards visualize SLIs against SLO thresholds. |
| at-most-once cheap but unreliable, at-least-once reliable but duplicated, exactly-once perfect but expensive | At-most-once is cheap but may lose messages. At-least-once is reliable but may duplicate, requiring idempotent consumers. Exactly-once is the perfect guarantee but expensive — most systems pick at-least-once + idempotency instead. |
| 1. Decoupling Notification Service 2. buffering Flash sale 10x traffic 3. resilience payment service | MQ enables three things: decoupling (Order hands off to Notification so email delays don't block checkout), buffering (flash sales spike 10x and the queue absorbs the peak), and resilience (Payment Service goes down, orders queue up and replay on recovery). |
| Functional 系統要做什麼功能 / Non-functional 系統做得多好 / Scope 這次設計做哪些不做哪些 | Functional requirements describe what the system does, non-functional describe how well, and scope defines what's in or out of this design. |

---

## 🧠 Patterns Across Mistakes

1. **WHAT 知道，WHY 講不出** — Day 12 GraphQL/gRPC、Pagination 都是這個型態。下次學新概念，**強迫自己問 WHY**。
2. **客戶端不可信** — Body / URL / 任何 client 給的東西都不能信。auth 資訊一律走 signed channel（JWT in header）。
3. **狀態不是二元** — Idempotency 不是 yes/no、API 版本不是只有 v1/v2、SLI 不是只有 pass/fail。**先想「中間狀態」存不存在**。
4. **單詞精準度** — `offline` vs `offset`、`SLI` vs `metric`、`at-most/least/exactly-once`。**面試聽錯一個詞就 -1 分**。

---

## 🎯 Next Session Plan

- [ ] WR2 結束，繼續 Day 14 Security & Auth
- [ ] Day 14 第一個 chunk 接續今天 JWT 的討論（Auth deep dive）
- [ ] **Interviewer Follow-Up Preview**：下次面試官可能會問
  - "JWT 怎麼防 replay attack？"
  - "Refresh token 跟 access token 差別？"
  - "如果 JWT secret 外洩了怎麼處理？"
