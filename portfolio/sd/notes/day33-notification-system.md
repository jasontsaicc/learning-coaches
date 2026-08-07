# Day 33 Notification System

> 整題重整版(收 S46 / S47 / S48 四次 sitting 的全部內容)。
> 四個問題:AWS 面試怎麼出這題、L6 怎麼做需求澄清、deep dive 挖多深、架構圖怎麼畫。

**One-liner:** A notification system takes an event from any internal service and reliably delivers it to a user through an external channel, decoupling the producer's latency from the provider's.

**Trade-off:** We chose three separate queues with dedicated worker pools over one priority queue, because priority solves ordering but not isolation, and the cost is triple the alarms plus idle capacity.

---

## 1. 這題在 AWS 面試房間裡長什麼樣

Interviewer 的開場句很短,而且故意模糊:

> "We need to notify our users. Design a notification system."

AWS 版本通常再包一層產業情境(你目標職缺會這樣出):

> "A retail banking client wants to send fraud alerts, transaction confirmations, and marketing campaigns to their customers. Walk me through how you'd design that."

**AWS 面試跟 Google 的差別(讀房間):**

| | AWS 會做的事 | 你要準備的 |
|---|---|---|
| Managed service | 鼓勵你用 SQS/SNS/Lambda,並追問營運與成本 | 用了要講得出坑,不能只講服務名 |
| 判別句 | "How would you operate this? Who gets paged?" | 3AM page test 當固定收尾 |
| 成本 | "What does this cost per month?" | 至少講得出最大那筆錢是哪一筆 |
| Ownership | 追問你上線後怎麼顧、怎麼 rollback | failure mode 主動講,不等問 |

Google 會逼你設計 SQS 的內部;AWS 讓你用 SQS,但要你證明你懂它會怎麼咬你。

---

## 2. Step 1 Clarify:L6 怎麼問(你最弱的一步)

### 判準句(先記這一句)

> **一個 clarify 問題,如果不管答案是什麼、你的架構都長一樣,那就不要問。**

L4 問「有哪些功能?要支援 email 嗎?」= 在收需求清單。
L6 問「這三類訊息的時效性差多少?」= 在找**哪個約束會改變架構**。

### 這題實際要問的四類(照順序)

| # | 問什麼(英文原句) | 為什麼問 | 這題的答案 | 這個答案改變了什麼 |
|---|---|---|---|---|
| 1 | "Is this one system for all three message types, or three separate ones?" | Scope negotiation。先圈範圍再設計 | 一套系統,三種流量 | 決定了「隔離」會是整題主軸 |
| 2 | "What's the latency requirement for each type? Are they the same?" | **這題的架構決定因素** | 詐騙 P99 60s / 交易 分鐘級 / 行銷 沒有 | 時效性差 3 個數量級 → 不可能共用一條路 |
| 3 | "What volume are we talking about, per type, and what's the peak?" | 沒有數字就不能算容量 | 詐騙 3-5 萬/日、尖峰 200-300/s;交易 500 萬/日;行銷 2-3 檔/週 × 100-300 萬則 | 讓你算得出 worker 數與 backlog |
| 4 | "What's the delivery guarantee? Is a duplicate SMS acceptable? Do stale messages expire?" | 失敗語意決定 dedupe 與 TTL 要不要做 | at-least-once + 行銷 24h TTL 作廢 + 可暫停 | 逼出 dedupe 與 consumer-side flag 兩個元件 |

### 收尾一定要做的 scope 宣告

問完不要就這樣進 Step 2,要**主動把範圍收窄並徵求同意**:

> "I'll scope this to SMS only for the MVP, with a message queue in between so adding email or push is just another worker pool. I'll cover system-side rate limiting, but I'll leave the user preference center out unless you want it. Does that work?"

這句話同時拿到 scorecard 的 Scope Negotiation 和 Time/Breadth Management 兩分。

⚠️ 你的紀錄:S46 這一步全程需要 coach 給填空。**這四行是可以背的**,背起來就不用臨場想。

---

## 3. Step 2 架構圖:怎麼畫(你問的第四題)

### 三條硬規則

1. **從 8-block skeleton 起手**,不要從這題的特殊元件起手
2. **分三層畫,邊畫邊講為什麼**。不要一次畫 11 個框,面試官看不懂,你自己也講不完
3. **每條箭頭標同步或非同步**。箭頭沒標 = 面試官不知道你懂不懂差別

### 畫圖順序(左到右,再往下掛)

```
先畫主鏈路(同步) → 再往下掛異步 → 最後才標數字與 SLO
```

### 第 0 層:現狀,也是問題本身

```
  Fraud Service ─────┐
  Order Service ─────┼──HTTP(sync)──→  SMS Provider A
  Campaign Service ──┘
```

**你要講的一句:** 每個 service 自己打 provider,provider 慢一秒,三個 service 一起慢一秒。**producer 的延遲被 provider 綁架了。**

### 第 1 層:加 queue,解耦

```
  Fraud Service ─────┐
  Order Service ─────┼──→ [Notification API] ──→ [ queue ] ──→ [ workers ] ──→ SMS Provider A
  Campaign Service ──┘         (sync, 回 202)      (async)
```

**你要講的兩句:**
- API 收下就回 202 Accepted,呼叫端不必等 provider(**解耦**)
- queue 當緩衝,provider 掛掉訊息不會掉(**削峰 + 持久化**)

### 第 2 層:一條變三條(這是本題的答案)

```
                          ┌─→ [fraud-queue] ──→ [fraud workers  ×60] ─┐
  services ──→ [API] ─────┼─→ [txn-queue]   ──→ [txn workers    ×15] ─┼──→ [Provider A]
                (202)     └─→ [mktg-queue]  ──→ [mktg workers   ×50] ─┘      ↓ CB 跳開
                                                                            [Provider B]
                                    每條 queue 一個獨立的 scaling policy
```

**你要講的一句(這是整題的核心論證):**

> 行銷單檔 200 萬則,以 1000/s 消化要 2000 秒也就是 33 分鐘。詐騙警示的 SLO 是 60 秒。**共用一條路等於用 33 分鐘去撞 60 秒。**

### 常見死法

| 死法 | 為什麼死 |
|---|---|
| 一開始就畫最終圖 | 面試官看到 11 個框,不知道你是推出來的還是背出來的 |
| 箭頭不標 sync/async | 這題的全部價值就在那一個 async |
| 畫完不講演進理由 | 圖是證據,論證才是分數 |
| 沒有 data model | 只有框框沒有表,Step 2 只做一半 |

---

## 4. Step 2 的另一半:API 與 Data Model(常被跳過)

**API(4 支就夠):**

```
POST   /v1/notifications          # 送一則,body 帶 type / user_id / template_id / payload
POST   /v1/notifications:batch    # 行銷批次投遞
GET    /v1/notifications/{id}     # 查單則狀態(queued/sent/failed/expired)
POST   /v1/campaigns/{id}:pause   # 暫停一檔行銷
```

`POST /v1/notifications` 要帶 **Idempotency-Key** header,呼叫端重試不會重複發。

**Data model(4 張表):**

| 表 | 關鍵欄位 | 存取模式 |
|---|---|---|
| `notifications` | id, user_id, type, status, provider, expire_at, created_at | 依 id 查狀態;依 status 掃 stuck |
| `templates` | template_id, channel, body, locale | 讀多寫極少,直接 cache |
| `user_prefs` | user_id, channel, opted_out, quiet_hours | 發送前查一次,cache 住 |
| `send_counters` | user_id + date (PK), count | 頻率上限,原子 increment |

`expire_at` 就是行銷 24h TTL 的落地位置:worker 拿到訊息第一件事是比對 `expire_at`,過期直接丟掉不發。

---

## 5. Step 3 Deep Dive:AWS 面試挖哪裡、挖多深

Deep dive 不是「講到你會的極限」,是**面試官挑 1 到 2 個點往下壓**。你要準備的是 6 個挖點各一個完整論證,而不是一個挖點的博士論文。

**深度天花板:機制 + 數字 + 反面代價。** 到這裡就停,再深是扣分(rat-hole)。

### 挖點 1:為什麼要三條 queue(bulkhead)

> Interviewer: "Why not one queue with a priority tag? That's a lot less to operate."

**你的答案骨架:**
1. 先承認他對的地方:priority 確實解決 ordering,fraud 排第一,等的只是一台 worker 放手
2. 再講他沒解決的:priority 決定「你排第幾」,不決定「有沒有人有空」
3. 給五個死因(下表),挑最強的兩個講
4. 主動講自己的代價:三套 alarm、三套 scaling policy、idle worker

| Max 的方案死在哪 | 機制 |
|---|---|
| Failure isolation | 一則 marketing poison message 觸發 retry storm,shared pool 全被吃光,fraud 陪葬 |
| Independent scaling | autoscaling 看 queue depth,200 萬則把訊號淹掉,fraud 永遠 scale 不出來 |
| Pause / TTL 語意 | 暫停 marketing 只能把訊息 pull 出來再丟掉,照樣燒 worker |
| Provider quota | 對外 TPS 是帳號級共享,marketing 燒光額度,fraud 收 429 |
| **工程現實** | **SQS 沒有 priority,Kafka 也沒有。** 這選項在 AWS 技術棧不存在,要換 RabbitMQ |

**兩個名詞分開記:**
- **Bulkhead** = 損害**範圍**限縮(誰陪葬)。船破洞照樣進水,只是不沉船
- **Circuit breaker** = 損害**時間**限縮(卡多久)

### 挖點 2:Provider 掛了怎麼辦(circuit breaker)

> Interviewer: "Provider A starts timing out. Walk me through what happens."

**失敗時間線(要用數字走):**

```
t=0     Provider A 開始退化,每個 request 拖到 timeout 才失敗
        read timeout 10s + connect 2s,retry 3 次 = 一則佔住 worker 36 秒
t=36s   一台 worker 才放手一次
        shared pool 130 台 → 130 ÷ 36 = 每秒只空出 3.6 台
        fraud 尖峰 300/s,缺口 83 倍,backlog 每秒累積 296 則
t=84s   第 300 則 fraud 才輪到 worker → P99 60s 早就破了
```

**關鍵誠實點(這句講出來會加分):**

> 這裡分不分 pool 都會死,因為瓶頸在 provider 不在 pool topology。專屬 30 台反而更慢(30 ÷ 36 = 0.83/s)。**救命的是 circuit breaker,不是 bulkhead。**

CB 連續 N 次失敗就跳開,不再打 A,直接走 B。timeout 從「每則 36 秒」變成 fail fast,吞吐立刻回來。

### 挖點 3:重複發送(idempotency)

> Interviewer: "The worker sends the SMS, then crashes before it can ack. What happens?"

SQS 是 at-least-once,訊息會被重投。**去重要在 provider call 之前做一次 conditional write:**

```
PutItem(pk = idempotency_key, ConditionExpression = "attribute_not_exists(pk)")
  成功 → 我是第一個,發
  失敗 → 別人發過了,直接 ack 不發
```

**反面代價要主動講:** 這是每則多一次 DynamoDB 寫入,500 萬則/日就是 500 萬次寫。用 `expire_at` 讓它自動過期,不然表無限長大。

### 挖點 4:頻率上限(per-user rate limit)

`send_counters` 表 `user_id + date` 當 PK,原子 increment 後比對上限。超過就丟掉並記 metric。
**注意:** 這跟系統側的 rate limit 是兩回事,前者保護用戶不被轟炸,後者保護 provider 額度。兩層都要有。

### 挖點 5:暫停與過期

- **暫停** = consumer 端旗標,不是刪 queue。worker 讀到 flag 就停止 poll,訊息留在 queue 裡
- **過期** = payload 帶 `expire_at`,worker 拿到先比對,過期直接丟。不要靠 queue 的 retention

### 挖點 6:容量(你的弱點,照這個模板做)

**先寫單位式,再填數字。** 你 S48 卡的就是這一步。

| 要算什麼 | 單位式 | 這題的數字 |
|---|---|---|
| 平均 QPS | 每日總量 ÷ 86400 | 500 萬 ÷ 86400 ≈ 58/s |
| 消化時間 | 總則數 ÷ 消費速率 | 200 萬 ÷ 1000/s = 2000s ≈ 33 min |
| **需要幾台 worker** | **到達率 × 單則耗時**(Little's Law) | 300/s × 0.2s = **60 台** |
| pool 每秒放出幾台 | 台數 ÷ 單則佔用時間 | 130 ÷ 36s = 3.6 台/s |

⚠️ **Little's Law 是這題唯一要記的公式:`N = λ × W`(worker 數 = 到達率 × 服務時間)。**
講出來的時候要**先講假設**:"I'm assuming 200ms per send, so 300 per second times 0.2 seconds gives me 60 workers." 假設講在前面,面試官就算不同意也是調數字,不是判你錯。

---

## 6. Step 4 收尾:3AM page test(硬關卡,不等問)

| 格 | 這題的答案 |
|---|---|
| **什麼會 page 我** | (1) fraud queue 的 oldest message age > 30s(SLO 60s 的一半就叫)(2) dead man's switch:fraud 通道 5 分鐘內送出量歸零 |
| **SLI** | 端到端投遞延遲 P99(事件進 API 到 provider 回 200)、投遞成功率、queue oldest message age |
| **SLO** | fraud P99 < 60s、成功率 > 99.9% |
| **Dashboard 三張圖** | (1) 三條 queue 各自的 depth 與 oldest message age (2) 投遞延遲 P50/P99 分通道 (3) provider A/B 的錯誤率與 CB 狀態 |
| **只開 ticket 不 page** | 行銷 backlog 偏高、單一 template 錯誤率上升、DynamoDB 寫入量逼近預算 |

**dead man's switch 是這題的關鍵:** 只監控錯誤率抓不到「什麼都沒發生」。fraud 流量本來就低(3-5 萬/日),整條通道靜默死掉時錯誤率是 0,漂亮得像沒事。

---

## 🌍 Real World

| My design block | Real-world tool | Its trap |
|---|---|---|
| 三條 queue | Amazon SQS ×3 | **沒有 priority 功能**,想做優先權只能開多條 queue;standard queue 是 at-least-once 且不保證順序 |
| worker pool | Lambda(reserved concurrency)或 ECS service | Lambda 的 reserved concurrency 就是 per-pool bulkhead;但同帳號的 concurrency 是共享池,一個 function 吃光會餓死別人 |
| dedupe 表 | DynamoDB conditional write | 每則多一次寫入成本;一定要配 TTL,否則表無限長大 |
| CB 與 failover | 應用層自己實作,或 AWS AppConfig 放 feature flag | AWS 沒有現成的 provider-level circuit breaker,別以為 SDK retry 等於 CB(SDK retry 只會讓事情更慢) |
| 扇出到多通道 | Amazon SNS 或 EventBridge | SNS 扇出無法 per-subscriber 重試控制;失敗只能丟 DLQ |
| SMS 送出 | Amazon SNS SMS / Pinpoint 或第三方(Twilio) | 帳號級 TPS 有上限且需要申請調高;監管簡訊(fraud alert)要另外走 short code |

**Industry reality:** 多數公司停在「一條 queue + 一組 worker」,直到第一次行銷檔次壓垮交易通知才拆。拆的成本是三套 alarm 與 idle 資源,大部分團隊要被燒過一次才願意付。

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| fraud 訊息排第一還是會被前面的 200 萬則卡住 | priority 決定「你排第幾」,不決定「有沒有 worker 有空」。等的是一台 worker 放手,不是等前面的人走完 | 用 queue-position 框架解釋所有延遲(S47 連問三輪都往「隊伍」找原因),銀行櫃員畫面才轉向 |
| 第一則 fraud 等 36 秒,所以 P99 60s 沒破 | P99 是最慢的 1%。第 300 則等 84 秒,backlog 每秒累積 296 則,破得很難看 | 拿 best case 交 P99 的卷,只算 happy path 就收工 |
| separate pool 讓 worker「不用一直等」 | separate pool 一樣被佔住,marketing 那池照樣卡滿 retry。差別是 fraud 那 60 台沒事 | bulkhead 講成「損害消失」,實際上是「損害關在一個艙裡」;損害時間要靠 circuit breaker 才會短 |
| `130 台 worker 佔 36 秒 → 每秒空出幾台` 不知道怎麼算 | 一台 36 秒放手一次 = 速率 1/36,130 台就乘 130 | 算術沒問題(同場 (10+2)×3 自己算對),缺的是「把場景翻成算式」這一步。**修法:先寫單位式再填數字** |
| 分不分 pool 是這題的生死關鍵 | provider 退化時分不分 pool 都會死,瓶頸在下游。bulkhead 管的是 poison message 與獨立 scaling,不是 provider 故障 | 把兩種故障(內部污染 vs 下游退化)混成一種,對應的解法也就混了 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "A notification system decouples whoever produces an event from whoever delivers it, so a slow SMS provider can't slow down the checkout path. The key trade-off here is isolation versus operational cost: these three message types have latency requirements three orders of magnitude apart, so I'll give each one its own queue and its own worker pool, and pay for triple the alarms."

**When asked to go deeper:**
> Q: "Why not one queue with a priority tag? That's a lot less to operate."
> A: "Priority solves ordering, not isolation. A tag decides who goes first; it doesn't stop marketing's retry storm from eating every worker, and it doesn't let me scale or pause fraud independently. There's also a practical problem: SQS has no priority support at all, so on AWS that design isn't buildable without switching brokers. I pay for three pools with idle capacity, and what I buy is a blast radius that stops at one queue."

> Q: "Provider A starts timing out. Walk me through it."
> A: "With a 10-second read timeout and three retries, one message pins a worker for 36 seconds. A 130-worker pool then frees only 3.6 workers per second, against a fraud peak of 300 per second, so the backlog grows by nearly 300 a second and P99 blows past 60 seconds. Splitting the pools doesn't save me here, because the bottleneck is the provider, not the topology. What saves me is a circuit breaker that trips after N failures and sends traffic straight to provider B."

**Showing production depth:**
> "In production I'd page on two things: fraud queue oldest-message-age above 30 seconds, which is half my SLO, and a dead man's switch on fraud throughput. Fraud volume is low enough that a silently dead channel shows a zero error rate, which looks perfectly healthy on a dashboard. Marketing backlog only opens a ticket."
