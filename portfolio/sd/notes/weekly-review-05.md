# Weekly Review #5 (S41, 2026-07-10) — Part 1: Multi-Region Session Store 重打

> WR5 進行到 Topic 1/3 中斷存檔。盲測未能獨立產出 → 轉導引重打,全鏈走到 pull 間隔計算。
> 未完:1+2N≤30 解 N、殭屍免疫格、監控收尾、Topic 2 (Security & Auth)、Topic 3 (Unique ID)、registry sweep、artifact audit。

## 題目

ScaleUp 美日雙區,任一區登入後請求可能落到任一區,session 都要有效。10M DAU 各半、峰值每區 50K req/s、session ~1KB、本地 lookup p99 < 5ms、TTL 30 天 sliding、撤銷 30 秒全球生效、failover 時 500 萬人重登不可接受(旅行者 ~1% 重登可忍)。

## Basic Elements

| Element | 內容 |
|---------|------|
| **One-liner** | (revocation 這塊的新句在 one-liner-library「Session Revocation (multi-region)」;原 Session Store 句已在庫) |
| **Trade-off** | Async over sync replication: sync puts a 150ms trans-Pacific hop on EVERY request-path write (sliding TTL ⇒ 寫入頻率=請求頻率) and couples both regions' availability; async costs a ~1s inconsistency window that almost nobody hits in steady state. |
| **Scale trigger** | Sliding TTL 讓「每個請求都是寫入」:50K req/s × 150ms sync 等待 = 預算 5ms 直接爆 30 倍 → sync 出局的主因。 |
| **DevOps angle** | 黑名單傳播選 pull(每輪撈全量 → 自愈、server 重啟自動補課),同構物:Prometheus scrape、k8s reconcile loop。監控點:pull 管道本身壞掉誰發現(下次收尾補)。 |

## 核心推導鏈(這次的主菜)

1. **Failover 需求反推複製策略**:一區掛不能群體重登 → 兩區互抄(active-active)。
2. **sync vs async,兩邊標價再選**:
   - 傷害公式:**傷害 = 不一致窗口 × 落窗人口 × 症狀嚴重度**
   - async:1s 窗口 × 路由恰好翻面的人(每天個位數)× 重登一次 ≈ 0
   - sync:每寫入 +150ms × 全體 × 每請求 + 可用性跨區傳染 = 毀題
3. **LWW 殭屍**:刪除在 last-writer-wins 眼裡只是普通寫入;攻擊者 sliding-TTL 狂寫 → 刪除被複製管道自己推翻 → session 死不掉。**撤銷 ≠ 刪資料。**
4. **撤銷開小灶**:量級先估(客服一天踢幾筆到幾百筆)→ Bloom filter 出局(大砲打蚊子還附送 FP 誤殺)→ 普通 set,每台 API server in-memory 副本(~100ns,零網路依賴)。
5. **傳播選 pull**:30s 預算寬 + 名單小到全量撈 → pull 簡單且自愈。N=20 被戳破:一次 timeout 就 39s > 30s。最壞 = 複製 1s + 錯過一輪 N + 失敗一輪 N = **1 + 2N ≤ 30**(解 N = 下次第一球)。

## 通用原則落袋

- 一致性妥協一律標價:窗口 × 人口 × 症狀,三個數字走出來才算「機制」,只說「有同步問題」是標籤。
- sync/async 不是全域開關,**per-write-type 各選**:量大症狀輕 → async;量小症狀重(撤銷)→ 單獨更強機制。
- **先估量級,再選工具**(Bloom 是名單大到放不下才用的壓縮,代價 FP)。
- Pull 的超能力 = 全量自愈;push 快但漏訊息 + 管道死得無聲。

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 「兩區互抄會有同步的問題」講到這就卡 | 傷害 = 窗口 × 人口 × 症狀,算出來 async 代價趨近零 | 危險感沒機制(S31/S36 同款):聞到風險但沒走數字 timeline |
| last-writer-wins 這個詞陌生 | LWW = 衝突時只看時間戳,晚到蓋早到;著名死穴是刪除打不贏狂寫 | 機制推得動(殭屍結論自己抓到),純標籤沒綁定 |
| 撤銷 → 「bloom filter」兩字丟出 | 幾百筆名單用 in-memory set;Bloom 是空間換 FP 的壓縮技巧,這裡不需要 | 量級沒估先抓工具;S40 才練過的 FP/FN 嚴重性判斷沒先跑 |
| 1+2N≤30 「不太確定要怎麼算」 | 三段加法 + 一條國中不等式 | capacity-freeze 家族:被式子外觀嚇住,非不會算(中斷,下次收) |

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "For a multi-region session store I'd go active-active with async replication: sync would add a 150ms trans-Pacific round trip to every request-path write and couple both regions' availability, while async costs a one-second inconsistency window that almost nobody hits in steady state."

**When asked to go deeper (revocation):**
> Q: "You have async replication. How do you force-logout a stolen account globally in 30 seconds?"
> A: "Revocation can't be a plain delete: with last-writer-wins, the attacker's sliding-TTL refreshes keep resurrecting the session. I'd make 'revoked' its own data class: a tiny blacklist (hundreds of IDs), held in memory by every API server, re-pulled in full every ~10s. Full pulls are self-healing, and the check is a ~100ns set lookup, so the 5ms budget doesn't notice."

**Showing production depth:**
> "In production I'd monitor the blacklist pull loop itself: last-successful-pull age per server, alert if it exceeds the revocation SLA, because a silently dead pull loop means revoked sessions stay alive."

## 🌍 Real World

| My design block | Real-world tool | Its trap |
|---|---|---|
| GeoDNS 就近路由 + failover | Route 53 latency-based routing + health checks | failover 沒演練過 = 沒有 failover |
| 兩區互抄 async (~1s) | DynamoDB Global Tables (0.5~2s) | 衝突解決就是 LWW:delete/write race 官方要你自己繞 |
| 本地熱層 <5ms | ElastiCache Redis | Global Datastore 是 active-passive,不是 active-active |
| Redis 真 active-active | Redis Enterprise Active-Active | 用 CRDT 不是 LWW(未來雷點:CRDT vs merge) |
| 撤銷黑名單 in-memory + pull | JWT denylist(Auth0/Okta)、TLS CRL、LaunchDarkly flag polling | pull loop 無聲死掉 = 撤銷失效,要 alert staleness |

**Industry reality:** 大多數公司走 stateless 短命 JWT(5~15 分)+ refresh token,接受分鐘級撤銷窗口因為便宜;要 30 秒級才加 denylist。落地幾乎都是混合體:JWT 走 90% 流量 + denylist 兜底 + server 端真相(購物車、nonce)放 Global Tables。

## 下次複測點

- 解 1+2N≤30,講出挑 N=10 之類的工程餘裕理由
- 殭屍為何咬不動黑名單(黑名單 append-only,session 寫入路徑碰不到它)
- 3AM page test 自己收尾(unprompted-ops 即測)
