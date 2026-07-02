# SD Pattern Map — 題目是 pattern 的組裝

> 2026-07-02 建立。來源：外部訓練營 22 題 vs 本課綱的缺口分析。
> 用法：面試前不背題，先確認每個 pattern 都能講；碰到沒練過的題目，拆成 pattern 再組裝。

---

## Pattern 總表

| # | Pattern | 核心零件 | 課綱位置 | 狀態 |
|---|---------|---------|---------|------|
| 1 | Read-heavy KV + Cache | cache-aside, immutable mapping 免 invalidation, Bloom 擋穿透 | Day 6-7, 26, 27-28 | 🟢 |
| 2 | Unique ID / 免協調發號 | Snowflake, clock skew, KGS | Day 29-30 | 🟢 (PoC 待做) |
| 3 | Fan-out / Feed | push vs pull, hybrid, celebrity problem, ranking | Day 40-42 | ⬜ |
| 4 | Real-time messaging | WebSocket, delivery guarantee, presence, read receipts | Day 35-37 | ⬜ |
| 5 | 高並發庫存一致性 | hot-row contention, distributed lock, 超賣防線, reservation TTL | Day 54-55 (新增) | ⬜ |
| 6 | Geo-spatial + Matching | Geohash/QuadTree 查詢 → matching, dispatch, 狀態機 | Day 52-53 + 58-59 (新增) | ⬜ |
| 7 | 機率型資料結構 | Bloom (membership), Count-Min Sketch (counting), Top-K | Day 26 + 56-57 (新增) | 🟡 (Bloom 🟢, CMS ⬜) |
| 8 | Async pipeline | queue 解耦, DLQ, retry, priority, 多 channel | Day 10-11, 33-34, 50-51 | 🟡 (MQ 🟢, 題目 ⬜) |
| 9 | Ledger / Exactly-once | idempotency key, SAGA, 對帳, double-entry | Day 43-45 | ⬜ |
| 10 | Observability / Time-series | 三支柱, TSDB, aggregation, downsampling | Day 25, 46-47 | 🟡 (概念 🟢, 題目 ⬜) |
| 11 | Rate limiting / 防護 | token bucket, sliding window, circuit breaker, 分層限流 | Day 23-24, 31-32 | 🟡 (單機 🟢, 分散式 ⬜) |
| 12 | Storage / Sync | chunking, delta sync, metadata DB, version conflict | 不排課 (Tier 3) | ⬜ |

---

## 訓練營 22 題 → Pattern 對照

| 訓練營題目 | 拆成哪些 pattern | 課綱對應 |
|-----------|----------------|---------|
| URL Shortener | 1 + 2 | Day 27-28 ✅ 已完成 |
| 核心 Components | (= Phase 1 全部) | Day 4-16 ✅，本課綱花 13 天，訓練營壓 1 節 |
| Dropbox / Google Drive | 12 + consistency (Day 19-20) | Tier 3，需要時組裝 |
| FB News Feed | 3 + 1 | Day 40-42 |
| Local Delivery | 6 (matching 規則不同) | Day 58-59 的變體 |
| Ticket Booking | 5 + 9 + 11 | Day 54-55 (新增) |
| Chat System | 4 + 3 (group fan-out) | Day 35-37 |
| Online Auction | 5 (hot-row 併發寫) + eventual consistency | Day 54-55 的變體 |
| Uber / Ride Sharing | 6 全套 | Day 58-59 (新增) |
| Proximity Service | 6 (只有查詢半套) | Day 52-53 |
| Instagram | 3 + 8 (media pipeline) + CDN | Day 40-42 組裝 + Tier 3 |
| YouTube | 8 (transcode pipeline) + CDN + 1 | Tier 3 |
| Payment (Stripe) | 9 全套 | Day 43-45 |
| Job Scheduler | 8 + DAG 依賴 + 9 (exactly-once firing) | Tier 3 |
| Notification System | 8 + 11 | Day 33-34 |
| IP Denylist | 7 (Bloom 直接應用) + 高 QPS 讀 | Day 26 已覆蓋 |
| Leaderboard / Top-K | 7 (CMS) + hot key | Day 56-57 (新增) |
| A/B Testing Platform | 流量分流 + feature flag + 10 (指標收集) | Tier 3 |
| Tinder | 6 (雙向 matching) + 3 (推薦 feed) | Day 58-59 變體 |
| Monitoring System | 10 全套 | Day 46-47 |
| Twitter | 3 (更大 scale) + hot content + 1 | Day 40-42 組裝 |
| SD 面試框架 | (= 4-step framework) | Day 1-3 ✅ |

---

## 怎麼用這張表

1. Phase 3 每完成一題，回來把對應 pattern 打勾，看覆蓋率。
2. 面試前一週：不重刷題，改成每個 pattern 練「一句話 + 一個 trade-off + 一個 failure mode」。
3. Mock 碰到沒練過的題（如 Dropbox）：先拆 pattern 再組裝，這比背過答案更接近真實面試的評分點（Problem Navigation）。
