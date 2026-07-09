# Weekly Review #2 — Blind Recall (Part 1)

> Status: ✅ Part 1 complete (Session 17 blind recall + interview templates)
> Topics reviewed: API Design, Caching & CDN, Message Queue
> Note: WR2 split across two sessions. Part 2 (Session 18 mistake review) is in `weekly-review-02-part2.md`.

---

## 📊 Recall Scores

| Topic | Score | Before → After |
|-------|-------|----------------|
| API Design | 2/4 | 🟡 → TBD (gap check pending) |
| Caching & CDN | 4/4 | 🔴 → TBD (gap check pending) |
| Message Queue | 2/4 | 🟡 → TBD (gap check pending) |

**Pattern:** One-liner + Trade-off 穩定通過，Scale trigger + DevOps angle 兩個 topic 都掛。代表「知道是什麼」但「不知道什麼時候用 + 怎麼維運」。

---

## 🔴 My Mistakes & Misconceptions

### Caching & CDN

| What I Said | Correct Answer | Why I Was Wrong |
|---|---|---|
| Cache-Aside write path 說反：「don't use delete because race condition, update is more easy」 | 正確是 **delete** cache key，不是 update。Delete 是 idempotent（刪兩次結果一樣），update 才有 race condition（兩個 thread 同時 update，慢的那個會蓋掉新值） | 把 delete 和 update 的風險搞反了。記住：**delete = safe（結果只有一種：沒資料），update = dangerous（結果不確定）** |
| Cache hit ratio alert 說 "drops below 80%" | 更精準的 alert 條件是 **hit ratio drop > 10% in 5 minutes**。重點是**突然下降的幅度**，不是絕對數字，因為突降代表有東西壞了（deploy 清空 key、key pattern 改變、Redis node 掛了） | 只想到絕對值，沒想到「變化率」才是 alert 的關鍵信號 |

### Message Queue

| What I Said | Correct Answer | Why I Was Wrong |
|---|---|---|
| MQ 3 key benefits 說成 "decoupling, buffering, **async**" | 第三個是 **resilience**（consumer 掛了 message 在 queue 等，不會丟）。Async 是機制/手段，不是好處本身 | 把「怎麼做」和「得到什麼」搞混了。Async 是 how，resilience 是 what you get |
| Scale trigger 完全答不出來 | 三個信號：① **Response too slow**（non-critical steps 如 notification 擋住 user response）② **Cascading failure**（一個 service 掛 = 整條 chain 掛）③ **Traffic spikes**（burst 流量壓垮 downstream） | 沒有從「sync chain 會出什麼問題」的角度去推導。要記住：queue 解決的是 sync 的三個痛點 |
| 被問「user 需要等 notification 寄完嗎」回答 "yes" | User 不需要等 notification。Amazon 下單後馬上看到 "Order confirmed!"，email 幾秒後才到。Non-critical steps（notification, analytics, logging）不該擋住 user response | 沒從 user experience 角度思考。要區分 critical path（payment, inventory）vs non-critical path（notification, analytics） |
| Cascading failure 的問題答不出來 | Sync chain 中任一 service down = 整條 chain fail。例：Payment OK → Inventory DOWN → user 看到 error，但錢已經扣了 | 沒想到 sync 的 coupling 問題。Queue 的 decoupling 就是在解這個 |
| Idempotency 知道名詞但說不出具體流程 | 完整流程：Consumer 收到 message with key "order-123-payment" → 查 DB/Redis 這個 key 處理過了嗎？ → YES = skip，回傳之前的結果 → NO = 處理 → 存 key → 回傳結果 | 只記了「概念」沒記「步驟」。面試要能講出 flow，不能只丟名詞 |

---

## ✅ What I Got Right

| Topic | Item | What I Said |
|---|---|---|
| API Design | One-liner | ✅ 能清楚描述 API Design 的核心概念 |
| API Design | Trade-off | ✅ REST vs GraphQL vs gRPC 的取捨 |
| Caching | One-liner | ✅ "把常用資料放更快的 store 擋住 DB" |
| Caching | Trade-off | ✅ 解釋清楚 delete vs update 的 race condition（被引導後） |
| Caching | Scale trigger | ✅ "DB read latency, P99 query latency" |
| Caching | DevOps | ✅ "cache hit ratio, Redis latency, memory usage, eviction rate" |
| MQ | One-liner | ✅ "async fast response, backend 慢慢消化, decoupling, buffering" |
| MQ | Trade-off | ✅ Kafka = distributed log，消費後 message 保留可 replay |

**Caching 從 WR1 的 0/4 進步到 4/4，是這次最大的成長！**

---

## 📝 Recall Cheatsheet（下次 session 前複習）

| Topic | 記住這些 |
|---|---|
| **MQ 3 Benefits** | Decoupling / Buffering / **Resilience**（不是 async） |
| **MQ Scale trigger** | Sync 三痛點：Response too slow / Cascading failure / Traffic spikes |
| **MQ Critical vs Non-critical** | Critical = payment, inventory（user 要等）。Non-critical = notification, analytics（丟 queue） |
| **MQ Idempotency flow** | 收 message → 查 key → 有 = skip → 沒有 = 處理 → 存 key |
| **Cache delete vs update** | Delete = idempotent（safe）。Update = race condition（dangerous） |
| **Cache alert** | 看「變化率」不是「絕對值」。Hit ratio drop > 10% in 5min = 有東西壞了 |
| **Queue vs Kafka 比喻** | Queue = 工作清單（做完就消失）。Kafka = 事件歷史紀錄（永久保留可回放） |

---

## 🎤 How to Say It in Interview — 改進版

### Message Queue — Scale Trigger

**When asked "When would you add a queue?":**
> "I'd introduce a message queue when I see three signals: first, user response time is slow because non-critical steps like notifications are blocking the critical path. Second, cascading failures — one downstream service going down takes out the entire chain. Third, traffic spikes overwhelming downstream services. The queue decouples the chain, so the user gets a fast response while non-critical work happens asynchronously."

### Message Queue — Idempotency

**When asked "How do you handle duplicate messages?":**
> "With at-least-once delivery, duplicates are expected. Each message carries an idempotency key like 'order-123-payment'. When the consumer receives a message, it checks Redis or DB — if the key exists, skip and return the previous result. If not, process the message, save the key, then return. This way, processing the same message twice produces the same outcome."

### Caching — Why Delete Not Update

**When asked "Why delete cache instead of update?":**
> "Delete is idempotent — no matter how many threads delete the same key or in what order, the result is always the same: cache is empty. Update has race conditions — if Thread A and Thread B both update, the slower thread's stale value can overwrite the correct one. With delete, the next read simply goes to DB and gets the truth."

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| In Cache-Aside pattern if request can't hit data from cache, cache will hit db and write cache, we don't use delete because get rate condition so update is more easy and save | In Cache-Aside, when a cache miss occurs, the app reads from DB and writes to cache. On the write path, we delete the cache key instead of updating it, because update can cause race conditions — delete is simpler and safer. |
| message queue solve async fast response, backend 慢慢消化, 3 Key Benefits decoupling, buffering, async | A Message Queue enables asynchronous communication between services. The producer sends a message and gets a fast response, while consumers process at their own pace. The three key benefits are decoupling, buffering, and resilience. |
| kafka is save log? | Kafka retains messages as a log, so consumers can replay past messages even after reading them. |
| 1 will disappear | SQS and RabbitMQ delete messages after consumption, so once a consumer reads and acknowledges it, the message is gone. |
| at-least-once 最少會傳一次 但是可能 duilicate 所以要做好重複收到的準備 | At-least-once delivery guarantees the message is delivered at least once, but it may be duplicated. So we need to handle duplicate processing with idempotency. |
| 但DB 的讀寫成爲瓶頸的時候 以及讀大於寫的時候 | When DB read/write latency becomes a bottleneck, and when the workload is read-heavy — that's when adding a cache layer makes sense. |
| I monitor cache hit ratio, Redis latency, and memory usage with eviction rate | I'd monitor cache hit ratio, Redis latency, memory usage, and eviction rate. |
| alert when cache hit ratio drops below 80% because it means most requests are missing the cache and hitting the database, which can quickly overload the DB and spike latency | Alert when cache hit ratio drops more than 10% in 5 minutes, because a sudden drop means something broke — a deploy wiped keys, key patterns changed, or a Redis node died — and DB is getting hammered. |

---

## 📌 Curiosity Branches

| Question | Status |
|----------|--------|
| Message Queue 的 long polling（長輪詢）怎麼運作？ | ⏸ Parked — likely Day 33-34 Notification System |
