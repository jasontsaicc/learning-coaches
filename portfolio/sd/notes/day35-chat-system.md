# Day 35 — Chat System: 1v1 Messaging（S49–S51，進行中）

情境：FSI 銀行網銀一對一客服。現況 client 每 2 秒 polling；資安長要求全對話留存、可稽核。
圖解版複習頁：https://claude.ai/artifact/HYWyCXM8NH1z8WafM9Yf3k

## Basic Elements

| Element | 內容 |
|---|---|
| One-liner | A 1v1 chat system keeps every message durable in a DB and pushes it in real time over WebSocket, with pub/sub routing across servers. |
| Trade-off | We chose WebSocket over polling because chat is bidirectional and 2s polling costs 25k req/s, 99.9% empty. The cost is long-lived connections: idle timeouts, drains, reconnect storms. |
| Trade-off | We chose Redis pub/sub over direct RPC because servers don't need to know where a user is. The cost is fire-and-forget delivery, covered by DB + client catch-up. |
| Trade-off | We order by a per-conversation sequence (atomic increment in DB) over timestamps because clocks drift even with NTP. The cost is row-level lock contention within one conversation. |
| Scale trigger | A 10k-member group makes the per-conversation counter a hot row (Day 36). A big online fleet splits the connection tier from the business tier so deploys don't kick connections. |
| DevOps angle | ALB idle timeout 60s → ping every ~30s. Deregistration delay (default 300s) on drain. Autoscale on ActiveConnectionCount, not CPU. |

## 核心機制（chunk 1–4）

1. **方向決定 protocol**：long polling / SSE 是 HTTP 用法（SSE 只能 server→client）；WebSocket 先發 HTTP Upgrade，server 回 101，同一條 TCP 換成雙向 frame。
2. **連線黏單台**：drain 一台 → 2 萬 client 同秒重連 → 打爆共用的 auth / DB（400x 突波，autoscaling 分鐘級救不到）= **thundering herd**。修法：client `jitter` + `exponential backoff + cap`；ALB `deregistration delay`。
3. **儲存 vs 投遞兩軸**：DB 管 durability（commit 才 ack Alice），Redis pub/sub 管 latency（`PUBLISH user:Bob`）。DB 掛 = 掉訊息；pub/sub 掛 = 只掉即時性。
4. **catch-up**：pub/sub 是 fire-and-forget，恢復後不補送。client 重連帶 `last_msg_id`，server 查 `WHERE conversation_id=:cid AND msg_id > :last`，並先驗證 Bob 是該 cid 的參與者。少了 conversation_id = 個資外洩。
5. **ordering**：不用時間戳（clock skew 會讓稽核紀錄出現假劇情）。per-conversation `next_seq` 在寫訊息的同一 transaction 裡 atomic increment（SQL `UPDATE ... RETURNING` / DynamoDB `ADD`）。row-level lock，只有同一對話要排隊。
6. **gap detection**：seq 連續 → client 收到 1045 但 last=1043 → buffer 1045、等 ~500ms、逾時就 catch-up、msg_id 去重。語意 at-least-once。

## Full Elements（目前覆蓋到的）

- Failure modes：WS node drain（thundering herd）、Redis down（延遲不掉資料）、DB down（send 失敗要明確回錯，不能假 ack）、pub/sub 亂序（gap detection）。
- Security：catch-up 查詢必須 scope 到 conversation 並驗證參與者，否則改 cid 即可讀別人的對話。
- 未覆蓋：chunk 5 offline delivery（mobile push）、chunk 6 observability、capacity 段、cost。

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| SSE 是「推播」(S49) | SSE 是一條不結束的 HTTP response，不是 mobile push | 術語聽起來像，沒綁到機制 |
| 訊息寫進 DB 就送到了 (S50) | DB 是被動的，不會通知 server-7；沒 pub/sub 就變 server→DB polling | 存和送摺成一軸 |
| ALB 那個設定叫「timeout 時間」(S50)，S51 直接忘記 | `deregistration delay`：除名後給既有連線的寬限期，預設 300s | 機制懂、名字沒綁 |
| pub/sub 恢復後 Bob 就會收到 (S51) | Redis pub/sub fire-and-forget，那段訊息只在 DB | 以為 pub/sub 有緩衝 |
| Redis 重啟後查 DB 補送 (S51) | client 帶 last_msg_id，server 查 DB 補；Redis 不參與 | actor 放錯（Redis 當 truth 舊直覺） |
| `WHERE msg_id > 1042` 就夠 (S51) | 要 `conversation_id = :cid`，不然全行訊息外洩 | 沒想範圍 |
| 用「只會往前」的時間戳排序 (S51) | 各台各自單調仍會互相衝突；要單一權威發號 | 問題是兩個時鐘，不是倒退 |
| 順序範圍看「訊息重不重要」(S51) | 範圍看「誰需要彼此有序」= 同一 conversation | 軸搞錯 |
| `UPDATE ... WHERE id='conv-A'` 鎖全表 (S51) | row-level lock，只擋同一列 | lock granularity 沒學過 |

## 🎤 How to Say It in Interview

> "I split it into two axes. Storage goes to the DB: the message is committed before I ack the sender, so anything acked is auditable. Delivery goes through Redis pub/sub on a per-user channel, so servers don't need to know where the recipient is connected. Pub/sub is fire-and-forget, so the client tracks the last sequence it saw. On reconnect, or when it sees a gap, it backfills from the DB. Ordering uses a per-conversation sequence assigned by an atomic increment, not wall-clock time, because clocks drift. The lock is per row, so only the same conversation serializes."
