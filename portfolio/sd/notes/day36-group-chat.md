# Day 36 — Group Chat（S53，chunk 1 fan-out）

情境：500 人群組 `all-co`，成員散在 50 台 chat server。之後放大到 10 萬人、每秒 5 則。
圖解版：https://claude.ai/artifact/7VgFbt6PENEfZSCJejQy7F 、[day36-group-fanout.html](day36-group-fanout.html)

## Basic Elements

| Element | 內容 |
|---|---|
| One-liner | Group chat stores each message once per group and fans it out through pub/sub, with chat servers subscribing to the groups their connected users belong to. |
| Trade-off | We chose server-subscribes-to-group over per-member publish because the sender publishes once and never looks up where members are. The cost is a membership lookup at connect time, cached and updated on join/leave. |
| Scale trigger | At 100k members × 5 msg/s, per-member lookups hit 500k/s on both the member table and the connection map. That is when we flip to group subscriptions. |
| DevOps angle | Watch Redis pub/sub output buffer per subscriber and delivery latency per group size. A huge group is a hot channel. |

## 核心機制

1. 一人一個 channel（Day 35）→ 500 人群組 = 500 次 PUBLISH。一台一個 channel → 50 次。
2. 做法 B 要兩張表：`group_members`（DB，建群/加人/退群時寫）、connection map（Redis，WS 連上寫、斷線刪）。
3. 離線成員走 push，之後 catch-up：`group_id + seq > last_seen`，訊息每群只存一份。
4. 10 萬人：瓶頸是每則訊息都掃全部成員（500k/s），不是 PUBLISH（250/s）。
5. 翻過來：chat server 在使用者連上時查他的 group，SUBSCRIBE `group:<id>`。sender PUBLISH 1 次。成員查詢從「每則訊息」移到「連線時 / 成員異動時」。

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| server 訂閱 group 後，成員表就省掉了 | 還是要查，移到連線時查一次（+ join/leave 時更新） | 把「移走」當成「刪除」 |
| 10 萬 × 5 = 50 萬「個訊息」；PUBLISH 50 次 | 50 萬是讀取次數，訊息只有 5 則；PUBLISH 50 × 5 = 250 | 沒寫單位；漏乘 5 |
| 題目是每秒 5 千、直接猜「DB 先爆」 | 每秒 5 則；先填數字再判斷 | 跳過算數直接猜結論 |

## 🎤 How to Say It in Interview

**Opening:** "For group chat I store each message once per group. Delivery goes through pub/sub, and each chat server subscribes to the groups of the users connected to it."

**Deeper:** Q: "What breaks at 100k members?" A: "Per-member fan-out. 100k members × 5 msg/s is 500k lookups per second. So servers subscribe to the group, and the sender publishes once. The cost is a membership lookup at connect time, which we cache."

**Production:** "I'd watch delivery latency by group size and Redis output buffers, since one big group is a hot channel."
