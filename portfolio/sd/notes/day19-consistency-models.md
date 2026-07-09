# Day 19 — Consistency Models（一致性模型）

> Phase 2 · Session 26 · 2026-06-03
> 延續 CAP：CAP 講「partition 時 C vs A」，Consistency Models 講「平時一致性是一道光譜」。

---

## One-Liner

> Consistency models 是一道**光譜**而非開關 — 從 Strong（所有人永遠看到最新、最貴）到 Eventual（最終才收斂、最便宜），本質是用**延遲預算**換**新鮮度**。

## Trade-off

> 選 Strong consistency 是用**延遲 + partition 時的可用性**換「所有人永遠看到最新」；選 Eventual 是用「暫時讀到舊值」換**低延遲 + 高可用**。沒有好壞，只有「這個業務能容忍多舊的資料」。

## Scale Trigger

> 當系統**跨地區**（台/日/美，RTT 50-150ms）且 **read-heavy**（100:1）時，全站 strong consistency 會讓寫入慢到不可用 → 改用 per-operation 的一致性等級（錢用 strong、按讚數用 eventual）。

## DevOps Angle

> Production 監控 **replication lag** 當作核心 SLI（直接量化「資料現在多舊」）+ stale read rate。SLO 例：P99 replication lag < 1s。Lag 持續超標就告警 — 代表 eventual 系統快要讀到很舊的資料。

---

## 核心光譜表（面試用）

| Model | 保證什麼 | 成本 | 例子 |
|---|---|---|---|
| **Strong** | 所有人、永遠看到最新 | 最高（同步等待 + CP 犧牲可用性） | 銀行餘額、庫存 |
| **Causal** | 有因果的事件不亂序（cause before effect） | 中 | 聊天問答、留言串 |
| **Read-your-writes** | **寫入者本人**看得到自己的寫入 | 低 | 改個人資料、發文後看自己 |
| **Eventual** | 最終會收斂（有終點保證） | 最低 | DNS、按讚數 |

**關鍵心法：** 同一功能不同部分可用不同等級。按讚數=eventual，但「我自己按的讚」=read-your-writes（CAP per-feature 決策延伸到 per-operation）。

---

## Quorum：一致性的旋鈕 🎛️

- **N** = 副本總數；**W** = 寫入要幾個副本確認；**R** = 讀取要問幾個副本（取最新）
- **公式：W + R > N → 保證讀到最新值**
- **為什麼？** 鴿籠原理：寫過的副本群 + 讀的副本群，數量加起來超過 N → 一定**重疊** → 重疊處有新值 → 讀得到
  - 比喻：3 個位子坐 4 個人（W+R）→ 一定有人共用位子（重疊）
- **旋鈕：** W 調大→寫慢但一致強；R 調大→讀慢但易讀到最新；W=1,R=1（≤N）→ 超快但不保證重疊 = eventual 的調法

---

## 🔗 Derivation Insight

- **Physical constraint:** 光速有限。台北→東京 RTT ~50ms。寫入要「傳到」東京才算同步，1ms 後資料還在太平洋上空。
- **My derivation:** 光速限制 → 跨節點同步要時間 → 要 Tokyo 馬上看到最新（strong）→ 寫入者必須**等** Tokyo 確認 → 等 = 延遲 → 所以一致性等級 = 不同的「願意等多久 / 容忍多舊」。
- **Surprise:** 「Eventual = 不一致」是錯的。Eventual 有「**最終會收斂**」的保證（像包裹運送中 📦，一定會到只是不知幾點），跟「no consistency（包裹寄丟 ❌，可能永遠不到）」差在那個保證。

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 平時（normal day）系統「拿到 CAP 三個」 | 平時拿到的是 **C 和 A**；P 不是選項，是「網路會不會斷」的物理事實 | 把 P 當成可選的好處，沒意識到 P 是前提不是選項 |
| 想不出「instant consistency 要付什麼代價」 | 代價是**延遲** — 寫入者必須等所有副本確認才算完成（同步） | 還沒把「同步 = 等待 = 慢」這條因果鏈內化 |
| Quorum W+R>N 不懂為什麼能保證讀到最新（卡兩次） | 鴿籠原理：寫的群 + 讀的群 > N → 必然**重疊** → 重疊副本有新值 | 抽象的集合重疊概念，需要杯子/位子的具體比喻才打通 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "Consistency isn't on/off — it's a spectrum, and the right level is really a latency budget. Strong consistency means everyone always sees the latest write, but you pay with latency and, during a partition, availability. Eventual consistency is the cheapest — reads can be stale, but it's guaranteed to converge. I pick per-operation based on how much staleness the business can tolerate."

**When asked to go deeper (Quorum):**
> Q: "How do you tune consistency in a replicated store?"
> A: "With quorums — W + R > N. If N is 3 and I set W=2, R=2, the read set and write set are forced to overlap, so I always hit a replica with the latest value. Crank W or R up for stronger consistency, drop them for speed. W=1, R=1 is effectively eventual."

**Showing production depth:**
> "For the eventual parts, I'd monitor replication lag as my key SLI and alert when P99 lag breaches the SLO — that's how I know staleness is staying within bounds."

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| 平時 C 和 A 都有，網路斷掉才被迫選 CP 或 AP | "On a normal day you get both consistency and availability; only when a partition happens are you forced to choose CP or AP." |
| eventual consistency 是最終一致，現在可能舊的但最終會同步，例如 DNS | "Eventual consistency means reads may be stale now, but the system is guaranteed to converge — DNS is a classic example." |
| read-your-writes 只保證自己看到自己的寫入，Tokyo 是不同 user 所以無效 | "Read-your-writes only guarantees you see your own writes; Tokyo is a different user, so that guarantee doesn't apply." |
| causal 只要有因果順序的就好，strong 要求所有事件 | "Causal consistency only orders causally-related events, while strong consistency requires a global total order across all events." |
| W+R>N 保證讀到最新是因為讀的和寫的一定會重疊 | "W + R > N guarantees a fresh read because the read set and write set are forced to overlap." |
