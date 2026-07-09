# Day 10 — Message Queue & Async Processing（Part 2）

> Session 12-13: Chunk 5-6 ✅ + Design Exercise ✅ + Simon Drill ✅ + Interview Drill ✅
> 所有步驟已完成

---

## Chunk 5 Feynman Gate: Idempotency ✅

**小杰的錯誤做法 vs 正確做法：**

| 小杰：separate flag | 正確：atomic transaction |
|---|---|
| 先處理，再設 `processed = true` | idempotency key 和 business logic 在**同一個 transaction** |
| Crash between process & flag → 重複處理 | Atomic：兩者一起成功或一起 rollback |
| Race condition with multiple consumers | Unique constraint on key → 第二次 write 自動失敗 |

```sql
-- atomic idempotency（正確做法）
BEGIN TRANSACTION;
  INSERT INTO processed_messages (idempotency_key) VALUES ('order-123-abc');
  -- duplicate key → transaction fails → skip
  UPDATE account SET balance = balance - 100 WHERE user_id = 42;
COMMIT;
```

**面試金句：** "The dedup check and the business operation must be atomic — one transaction, not two separate steps."

---

## Chunk 6: Observability Mini ✅

| Element | Message Queue |
|---------|--------------|
| **SLIs** | Queue depth, consumer lag, processing latency (P50/P99), error rate (DLQ count) |
| **SLO target** | Consumer lag < 30s at P99, error rate < 0.1%, queue depth 不能無限增長 |
| **Alerts** | 🔴 Consumer lag > 60s, 🔴 DLQ count spike, 🟡 Queue depth 持續增長 5+ min |
| **Dashboards** | 1. Throughput (messages in vs out/sec) 2. Latency distribution 3. DLQ trend + queue depth |

**Consumer lag** = queue 最重要的 metric。代表 consumer 跟不上 producer 的程度。
- Kafka: latest produced offset - latest consumed offset (per partition)
- SQS: `ApproximateNumberOfMessagesVisible`

**3 AM Queue Depth Alert — Debug Decision Tree：**
```
Queue depth growing 📈
  ├─ Producer throughput spiked? → traffic surge → scale consumers
  ├─ Consumer throughput dropped?
  │   ├─ Consumer errors up? → check DLQ → fix bug / rollback
  │   ├─ Consumer latency up? → downstream slow (DB? API?)
  │   └─ Consumers crashed? → check pod count → restart
  └─ Both normal? → partition imbalance (Kafka) / visibility timeout (SQS)
```

---

## Design Exercise: Order Processing with MQ ✅

**架構圖：**
```
Client ─→ DNS ─→ LB ─→ API Server ─→ Cache (order status)
                            │                    ↑
                      (async)│              (update status)
                            ▼                    │
                         Queue ──→ Worker ──→ Database
                            │         │
                            │    [idempotency check]
                            ▼
                           DLQ (failed messages)
```

**設計決策：**
1. **API Server** sync 回覆 "order received"（快），heavy work 丟 queue（async）
2. **Idempotency check 在 Worker**（因為 Worker 才是收到重複 message 的人）
3. **DLQ** 接 failed messages → alert → 人工調查

**核心 pattern：fast sync ack + async heavy processing** — 適用於 order processing, email, video transcoding, notifications。

---

## Simon Drill Recall Gaps

| Chunk | Recalled | Gap |
|---|---|---|
| 1. Why Async | fast response | 漏了 **decoupling** 和 **buffering** |
| 2. Core Components | ✅ | — |
| 3. SQS/Kafka/RabbitMQ | 方向對但模糊 | 要用 **event streaming + replay** 定位 Kafka，**complex routing** 定位 RabbitMQ |
| 4. Delivery Semantics | "most, least, excely" | 講完整名稱：at-most-once, at-least-once, exactly-once |
| 5. Idempotency | ✅ concept | 補充 **how**：atomic transaction with idempotency key |
| 6. Observability | ✅ triage 對 | 記住關鍵字 **consumer lag** |

---

## Interview Drill: Flash Sale Order Processing ✅ (3/3)

**題目：** Design an order processing system for flash sale spikes without duplicate charges

**架構 flow：**
```
User clicks Buy
       │
       ▼
   API Server ─── Redis DECR inventory (atomic)
       │
   inventory ≥ 0?
   ├── NO  → "Sold out"（快速回應）
   └── YES → 丟進 Queue，回 "Order received, processing..."
                    │
                    ▼
              Order Service
              ├─ 1. Idempotency check (查 DB: order_id 處理過沒)
              │     → 處理過 → skip
              │     → 沒處理過 ↓
              ├─ 2. paymentService.charge()
              ├─ 3. 寫 DB（訂單 + 標記已處理）
              └─ 4. 通知 user
```

**每一層解決什麼問題：**

| Component | 解決的問題 |
|-----------|-----------|
| Redis DECR | Race condition — atomic 操作避免賣超 |
| Queue | 削峰（peak shaving）— buffer 住突然湧入的流量 |
| Idempotency check | At-least-once 可能重複送 → 用 order_id 擋重複處理 |
| Async 回應 | User 不用等完整流程 → 先回 "received" |

---

## Trade-off

| 決策 | 選了什麼 | 為什麼不選另一個 |
|------|---------|-----------------|
| Inventory check 放哪 | Queue 之前（Redis DECR） | 放 Queue 之後 → 99,500 個 user 排隊等半天才知道沒貨，體驗差 |
| Delivery semantic | At-least-once + idempotency | At-most-once 會丟訊息 → 用戶付了錢但訂單不見 |
| 回應方式 | Async（先回 ack） | Sync 等完整流程 → 100K request 打爆 Order Service |

---

## Scale Trigger

- **100K concurrent** → 單一 Order Service 扛不住，需要 Queue 做 buffering
- **Queue consumer 不夠快** → 水平擴展 consumer 數量
- **Redis 單點故障** → Redis Cluster + 庫存預熱

---

## DevOps Angle

- **Monitor:** Queue depth（是否持續增長）、consumer lag（是否跟不上）、DLQ count（失敗率）
- **Alert:** Consumer lag > 60s、DLQ spike、Redis 連線失敗
- **SLO:** Order confirmation < 2s（async ack）、end-to-end processing < 30s

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| Simon Drill: Why Async 只記得 "fast response" | 三個好處：decoupling, buffering, resilience | 從 user 角度想得到 fast，但 system architecture 角度的 decoupling 和 buffering 沒內化 |
| Simon Drill: delivery semantics 說成 "most, least, excely" | 完整名稱：at-most-once, at-least-once, exactly-once | 術語要講完整，面試印象差很多 |
| 設計練習不知道怎麼開始 | 拆成小問題一步步推：先決定 sync vs async → 再決定 idempotency 放哪 | 面試也是一樣，不需要一次畫完，一步一步 reason through |
| 忘了 Functional / Non-Functional / Scope 的定義 | Functional = 系統做什麼、Non-Functional = 表現多好、Scope = 今天只做哪塊 | Step 1 是面試第一步，每次都要做，不能跳過 |
| Inventory check 放 Queue 之後 | 應該在 Queue 之前用 Redis DECR 快速擋掉 | 放之後 → 99,500 人排隊等半天才知道沒貨，user 體驗差 |
| Idempotency 是一個獨立 service | Idempotency check 是 Order Service 裡面的邏輯 | 它是一個「步驟」不是一個「元件」— 就像洗米是在廚房裡做的步驟 |
| 把 Redis DECR 跟 Idempotency check 搞混 | Redis DECR = 庫存（Queue 之前）、Idempotency = 防重複（Queue 之後，Order Service 裡） | 兩個在不同時間點、解決不同問題 |
| 說 at-least-once 是解決重複扣款的方法 | At-least-once 是問題的來源（可能重複送），idempotency 才是解法 | At-least-once 保證不丟訊息，但代價是可能重複 → 要靠 idempotency 擋 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "For a flash sale order system, the key challenge is handling 100K concurrent requests without duplicate charges. I'd use a message queue to buffer the traffic spike, Redis for atomic inventory control, and idempotency keys to prevent duplicate processing."

**When asked to go deeper:**
> Q: "How do you prevent overselling?"
> A: "I use Redis atomic DECR before the queue. Redis is single-threaded so DECR is naturally atomic — no race conditions. If inventory drops below zero, we immediately return 'Sold out' and INCR it back."

> Q: "How do you prevent duplicate charges?"
> A: "The queue uses at-least-once delivery, which means duplicates are possible. The Order Service checks the order_id against the database before processing. The idempotency check and the payment must be in the same transaction — if the order_id already exists, we skip."

**Showing production depth:**
> "In production, I'd monitor consumer lag and queue depth as primary SLIs. A growing queue depth with stable producer throughput means consumers are falling behind — I'd auto-scale consumers based on this metric."

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| idempotency is use queue maybe send more time message but consumer will just prosses one time | Idempotency means that even if the queue delivers the same message multiple times, the consumer will only process it once — preventing duplicate charges. |
| worker will get dulicate message | The Worker is the one receiving duplicate messages from the queue, so it should be responsible for the idempotency check. |
| payment processing is not good idea, because at-most-once only send massage once maybe will losing massage | At-most-once is terrible for payment processing because if a message is lost, the user paid but their order never gets processed. Duplicates are fixable with idempotency, but lost payments are unrecoverable. |
| use SQS or Kafka can thinks about trade-off like the cost, infra | The choice between SQS and Kafka depends on whether you need message replay. SQS for simple job queues, Kafka when you need event replay or streaming analytics. |
| does the user can order and edit profile like address? and can check order status and edit order? | Can users place orders and edit their profile, like their address? Can they also check order status and modify orders? |
| i not sure how many user, i forget functional and non functional + scope | I'm not sure about the user count. I forgot what functional requirements, non-functional requirements, and scope negotiation mean. |
| check idempotency_id, DECR? | The Order Service checks the idempotency ID... does it also do a DECR? |
| client > redis > queue > Idempotency > order service | The request goes from the client to Redis for inventory check, then to the queue, and the Order Service handles idempotency internally. |

---

## ✅ 所有步驟完成
