# Phase 2 Gate — Multi-Region Session Store (S31)

> Transfer mock：用 Phase 2 學過的零件，組裝一個**沒設計過**的題目。
> Result: **5/6 ✅ PASS** → 晉升 🏗️ Staff Architect，進入 Phase 3。

---

## One-Liner

> A multi-region session store keeps each user's small KV session in their **home region** (Redis + TTL for self-healing staleness), routes requests via **geo-DNS**, and **asynchronously replicates** sessions to a backup region — so a whole-region outage doesn't force a mass re-login. It accepts a few seconds of **replication lag** (an **AP** choice: a slightly stale session is fine, logging out 100M users is not).

## Trade-offs（這題的核心都是取捨）

| 決策 | 選了什麼 | 為什麼 | 反面代價 |
|------|---------|--------|---------|
| 旅客跨區 | **不全量同步**，home region 存 + miss 才回源抓 | 多數人待同區，全量即時同步太貴 | 旅客第一個 request 慢一個跨區 round trip (~100ms+) |
| EU 暫存副本 | 存，但給**短 TTL** | TTL 到期回 home 重抓 → staleness 自癒 | 登出在 TTL 內仍有效 = 安全風險，需主動 invalidate |
| Region 掛掉 (DR) | **async 複製**到 backup 區 | 撐得住整區故障，又比 sync 便宜 | home 那一瞬間掛 → 還沒複製出去的幾秒 session 丟掉 |
| 一致性等級 | **AP**（可用優先） | session 稍微舊可接受，全員被登出不可接受 | partition 期間可能讀到舊 session |

> **成熟點**：同樣是「複製」，**需求變答案就變** — 為旅客 → 不複製；為 DR → async 複製。

## Scale Trigger

- 100M DAU、每個 request 都讀 session → **read-heavy**，每區放本地 Redis 扛讀。
- 整區故障的可用性需求 → 觸發**跨區 async replication**（不是為了旅客，是為了 DR）。

## DevOps Angle（上線後監控什麼）

- **P99 read latency**：每個 request 都讀 session，慢了全站慢。
- **Replication lag** ⭐：這個指標 = 「region 掛掉會丟幾秒 session」的資料遺失窗口，lag 爆掉要被 page。
- **Session store availability / Redis 連線健康**（per region）。

## Capacity（粗估）

- Session ~1KB，100M 活躍 session ≈ **~100GB** → 空間不是瓶頸（記憶體分區放得下）。
- 所以「多存一份副本」的成本**不是空間**，是**一致性**。

---

## 🔗 Design Reasoning（我自己推出來的路徑）

- **物理限制**：session 寫在哪台，那台才有資料；跨區傳輸有延遲、會斷。
- **我的推理**：美國登入 → session 在 US。人到 EU → geo-DNS 把他導到 EU server → EU 本地沒這份 session。要嘛回 US 抓（US 活著才行），要嘛事先複製。多數人不跨區 → 不值得全量同步。但「整區掛掉」是另一個需求 → 用 async 複製到 backup 換可用性。
- **意外點**：一開始以為「留副本的代價是浪費空間」，其實 session 只有 1KB，**真正代價是兩份不一致 (stale)**；也一開始誤以為 US 掛掉 EU 還能服務，忘了 EU 根本沒資料 + 回源前提是 US 活著。

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| US region 掛掉時，request 跑到 EU Redis 就能登入 | EU 在 home-region 設計下**根本沒**這些 session；而且「miss → 回 US 抓」的前提是 **US 活著**，US 死了無源可抓 → 使用者被登出 | 把「旅客跨區回源」機制套到「源頭整個掛掉」，沒注意那個隱藏前提 |
| 留一份副本在 EU 的代價是「浪費空間」 | session 才 1KB，空間是假議題；真正代價是 **US/EU 兩份 stale 不一致** | 反射性想到資源成本，沒連到剛暖身的 consistency |
| （習慣）第一次開口只講最短答案（"waste space" / "redis can set TTL" / "async"），靠面試官追問才展開；兩次主動「提示我一下」 | 真實面試官不會幫你挖，求助前要先嘗試 | S8→S31 主線弱點，獨立 drive 不足，**Phase 3 頭號訓練目標** |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "A session is a small KV blob read on every request, so latency matters and I'll keep it in-region. The key tension in *multi-region* is: a traveling user might hit a region that doesn't have their session. Most users stay in one region, so I won't replicate everything everywhere — I'll store in the home region and fetch-on-miss, with a short TTL on cached copies so staleness self-heals."

**When asked "what if a whole region goes down?":**
> "Fetch-on-miss assumes the home region is alive — that breaks on a region outage. So for DR I'd async-replicate sessions to a backup region. I pick async over sync because sessions tolerate a little staleness — the cost is losing the last few seconds of unreplicated sessions, which at worst means those few users re-login. That's the AP choice, and it's the right one here: a stale session is fine, logging out 100M users is not."

**Production depth:**
> "I'd monitor replication lag specifically — it *is* my data-loss window. If lag spikes, my blast radius on a region failure grows, so that's a page-worthy alert. Plus P99 read latency since every request reads a session."

**One security note:**
> "Short TTL is good for reads but dangerous for logout — a logged-out session stays valid until TTL expires. So logout needs active invalidation, not just TTL."

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| 會失敗 因為歐洲的 store 沒有這個 session 除非要同步 但是感覺成本高 不確定效益 | "It would fail — the European store doesn't have that session. We'd need to replicate it, but that feels expensive and I'm not sure the benefit justifies the cost." |
| 抓不到，US 死了沒 source of truth，使用者等於被登出 | "We can't fetch it — US is down, there's no reachable source of truth, so those users are effectively logged out." |
| async 的方式 不用每次都要等同步，代價是如果一瞬間掛掉 會少掉還沒同步的 session | "Async replication — the home region doesn't wait for the copy to propagate. The cost is that if it dies at that exact moment, we lose the sessions that hadn't replicated yet." |
| 我會監控 P99 的 latency 以及 replication 的同步情況 | "I'd monitor P99 read latency and replication lag — the lag is literally my data-loss window on a region failure." |

---

## Follow-ups to anticipate（下次可能被問）

- 一個 request 怎麼知道使用者的 home region 是哪？（session_id 編碼 home region / 全域路由表）
- 登出 / 權限變更如何跨區即時生效？（主動 invalidation、pub/sub、token 版本號）
- 對照 **AWS DynamoDB Global Tables**：它的多區複製是 async + last-writer-wins，和你推的設計一致嗎？（cross-verify 作業）
