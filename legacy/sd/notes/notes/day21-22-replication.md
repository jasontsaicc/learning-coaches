# Day 21-22: Replication & Leader Election

> Phase 2 ｜ Sessions 27 ｜ 問題錨定 + 深度天花板模式

---

## 🎯 核心因果鏈（一條線記住全部）

> 硬體會壞 → 要複製多份 → 多份就有「誰對」的問題 → 單 leader 用 **ordering** 解決
> → 但 leader 會死 → 要**選新的 (election)** → 選的時候怕**腦裂 (split-brain)**（過半解決）
> → 而複製本身有**延遲 (lag)** → 所以要**監控 lag**

面試時順著這條鏈講，聽起來像在推理，不是背書。

---

## One-liner

> Replication 把資料存多份來扛硬體故障；關鍵是「誰能收寫入」決定了一致性複雜度 — single-leader 用唯一 ordering 免解衝突，multi-leader/leaderless 換來寫入可用性但要付 conflict resolution 的代價。

## Trade-off

- **選 sync replication（而非 async）** because 訂單=錢，要強一致、不能掉資料。代價：寫入變慢、replica 掛掉會卡寫入 → 實務用 **semi-sync**（至少 1 台確認就好）。
- **三種 topology 是一個滑桿**：Single → Multi → Leaderless，往右走「寫入可用性↑」但「conflict 複雜度↑」。

## Scale trigger

- 讀取壓力大 → 加 **read replica** 水平擴展讀取（但只解讀，不解寫）。
- 寫入卡單點 → 垂直擴展 leader 或 sharding。

## DevOps angle

> In production, I'd monitor **replication lag (P99)**, replica sync status, 和 **leader election 頻率**（一直重選 = flapping = 腦裂前兆）。

---

## 📚 7 個 Chunk 重點

| # | Chunk | 一句話 key point |
|---|-------|-----------------|
| 1 | Why replication | 硬體年故障率 2-10%，單點 = 單點故障 |
| 2 | Single-Leader | 唯一節點 → 唯一寫入 **ordering** → conflict 不可能；讀可擴展，寫卡單點 |
| 3 | Sync vs Async | 判斷標準=「丟這筆的代價」；async crash = data loss；折衷 = semi-sync |
| 4 | Multi-Leader & Leaderless | 沒單一 ordering → 兩個並發寫同 key 會 conflict → 需 vector clock/LWW/merge；Leaderless = Quorum W+R>N |
| 5 | Leader Election | leader 死了要選新的，**過半票** (majority) 才能當選 → 防 split-brain |
| 6 | Read replica ≠ strong | replication lag → 剛寫完讀 replica 讀到舊值（破壞 read-your-writes）|
| 7 | Observability Mini | 盯 replication lag / sync status / election 頻率 |

### 🧠 關鍵術語

- **Split-brain（腦裂）**：叢集裂兩半，每半都以為自己該當家 → 同時兩個 leader 收寫入。通常肇因是 **network partition**（不是真的死）。
- **Raft 核心一招**：選 leader 要過半同意。兩個過半群組**不可能同時存在**（鴿籠原理，跟 Quorum W+R>N 同源）→ split-brain 數學上不可能。

### read-after-write lag 三解法

| 解法 | 做法 | 代價 |
|------|------|------|
| Read from leader | 剛寫完的讀直接打 leader | leader 負擔↑ |
| Sync replication | 等 replica 確認才回 OK | 寫入變慢 (CAP 選 C) |
| Sticky session | 同 user 讀寫綁同台/寫後一段時間讀 leader | 實作較複雜 |

---

## 🔗 Derivation Insight

- **Physical constraint:** 硬體年故障率 2-10%，單機 = 單點故障；光速有限，跨節點同步要時間 → lag。
- **My derivation:** 硬體會壞 → 要多份 server 做 HA → 多份就有網路/同步問題 → replication 必然帶來 consistency 問題（閉環接回 Day 19）。
- **Surprise:** 原本以為「加 read replica = 系統變強一致」，其實 replica 只解讀取擴展，replication lag 反而讓「讀自己剛寫的」會失敗。

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 被問「為什麼 single-leader 不用解衝突」，我答「只有一個節點但 leader 是 bottleneck」 | 問的是「為什麼免解衝突」，答案是「單節點提供唯一 ordering」。bottleneck 是 single-leader 的**缺點**，是另一個問題 | 把「缺點」和「為什麼免衝突」混在一起答，沒抓到問題真正問的點 |
| （潛在）read replica 加了就有強一致 | replica 有 replication lag，讀到的可能是舊資料，不是 strong consistency | replica 的價值是讀取**擴展**，不是一致性 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "Replication stores data on multiple nodes to survive hardware failure. The key design question is *who accepts writes* — a single leader gives you one total ordering so conflicts are impossible, while multi-leader or leaderless buys write availability at the cost of conflict resolution. For something like orders, I'd lean single-leader with synchronous (or semi-sync) replication, prioritizing consistency."

**When asked to go deeper (failover):**
> Q: "Leader dies at 3am — what happens?"
> A: "The surviving replicas run a leader election requiring a *majority* of votes. Majority quorum is what prevents split-brain — two majority groups can't coexist, so you can never accidentally get two leaders. During the few seconds of election, writes are briefly unavailable; that's the failover window."

**When asked the read-your-writes trap:**
> Q: "User places an order, refreshes, can't see it. Why?"
> A: "Replication lag — the read hit a replica before the write propagated. Fix by routing read-after-write to the leader, using sticky sessions, or sync replication for that path."

**Showing production depth:**
> "I'd monitor replication lag P99 and leader election frequency — frequent re-elections (flapping) signal instability or a brewing split-brain."

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| single-leader just need one node but leader is a bottleneck | Single-leader has one node imposing a total ordering on all writes, so conflicts are impossible — though that one node can become a write bottleneck. |
| 會有 2 個 leader 寫入 順序會亂 如果同時寫入會有衝突 | With two leaders there's no single write ordering, so concurrent writes to the same key will conflict. |
| 4台那群能選leader 因為4>3.5過半 3台那群湊不到過半所以不行 | The 4-node side can elect a leader because 4 is a majority (4 > 3.5); the 3-node side can't reach a majority, so it can't. |
| replica 有 replication lag，讀到的可能是舊資料 | Replicas have replication lag, so reads can return stale data — that's not strong consistency. |
| 因爲是訂單系統 我認爲是 C consistency 比較重要 | Since this is an order system dealing with money, I'd prioritize consistency over availability. |
| 看是要增加 leader 負擔去讀，or 等 consistency 完成，或者使用 sticky session | Either route the read to the leader at some extra load cost, wait for replication to complete, or use sticky sessions. |

---

## 📌 Park（之後再深入）

- Raft 細節：log replication、term 號、heartbeat（面試只需過半投票直覺）
- Service Discovery（Consul / K8s DNS / Cloud Map）— Day 22 原訂內容，壓縮模式 park
- Replication Light/Full PoC（模擬 lag）→ park 到 Phase 3 Day 38-39
- Vector clock 數學 → park（概念版已會）
