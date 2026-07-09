# Day 15 — Consistent Hashing (Theory, Part 1)

> Session 22 (2026-05-15) + Session 23 (2026-05-28)
> Status: 🟢 Complete — 概念全收（depth-ceiling 模式收尾，公式/統計證明已 park）
> PoC 不單獨做,折進 Day 17+ 的 "Design a Distributed Cache" 設計題

---

## One-liner

> Consistent Hashing 把 server 和 key 都 hash 到同一個環狀座標系上，每個 key 由「順時針第一個 server」負責 — 讓「新增/移除一台機器」只影響相鄰的一小段資料，而不是整個資料集重新洗牌。

**面試 one-liner(先講這句,headline first):**
> "Consistent hashing maps both keys and nodes onto a ring, so adding or removing a node only remaps about **1/N** of the keys instead of nearly all — and virtual nodes keep the load evenly spread."

---

## Step 0 — First Principles 推導

**物理限制（physical constraint）：**
分散式系統的伺服器數量 N 不是常數。會擴容、縮容、節點故障。任何依賴 N 當作除數的設計都會在 N 變動時崩潰。

**簡單推導 `hash(key) % N` 的問題：**

| 狀況 | N | 公式 | 結果 |
|---|---|---|---|
| Day 1 | 3 | `hash(k) % 3` | key 落在 server 0/1/2 |
| Day 2 加一台 | 4 | `hash(k) % 4` | key 落在 server 0/1/2/3 |

**關鍵問題：** N 從 3 變 4，幾乎所有 key 的歸屬都改變。

- 只有當 `hash(k) % 3 == hash(k) % 4` 才不動 → 大約 1/4 的 key
- **約 75% 的 key 需要搬家**
- 100 萬筆資料 = 75 萬筆同時搬移 → 網路爆炸 / 寫入失敗 / 讀打錯節點 → **只能停機**

**結論：** `% N` 設計把「key 的位置」綁在「N 的當前值」上，N 一變所有 key 重算。我們需要一個「key 位置與 N 無關」的設計。

---

## Chunk 2 — Ring Model（環狀模型）

**核心轉換：**
- 把 hash space 折成一個環：`0 ──── 2^32-1 ──── 0`
- **Server 也被 hash 到環上**（不只是 key）
- 每個 key 由「順時針方向第一台 server」負責

```
              [Server A @ 12]
             /
[Key @ 10] ───clockwise──▶ Server A 負責這個 key
             \
              [Server B @ 50]
```

**為什麼這樣 reshard-safe？**

| 比較 | hash % N | Ring |
|---|---|---|
| Key 的位置 | **動態**（隨 N 浮動）| **固定座標**（一次算好就不變）|
| 加 1 台 server | 所有 key 重算（~75% 搬家）| 只有「新 server 擠進那段弧」的 key 受影響 |
| 平均搬遷量 | O(K) | **O(K/N)** |

---

## Chunk 3+4 — Node Operations + Virtual Nodes

### 純 Ring 的隱藏問題

**Scenario：** 3 台 server 隨機 hash 到環上，位置可能很不均勻：

```
A @  100,000,000
B @  150,000,000   ← A 和 B 很近
C @ 3,000,000,000  ← C 離很遠
```

Server C 要負責「從 B 到 A」這段巨大的弧（~92% 的 keyspace）。
→ **負載嚴重失衡。** C 死掉，92% 流量瞬間轉到 A → cascade failure。

**根本原因：** 樣本太少。3 個點分佈在 2^32 空間，統計學救不了你。

### Virtual Nodes（vnodes）

**做法：** 每台實體 server 在環上放 **很多個點**（150 個常見）：

```
A → hash("A-0"), hash("A-1"), ..., hash("A-149")
B → hash("B-0"), hash("B-1"), ..., hash("B-149")
C → hash("C-0"), hash("C-1"), ..., hash("C-149")
```

環上總共 450 個點隨機分佈。
每台 server 擁有 ~150 個散落的小弧。
**樣本數 3 → 450，variance 大幅降低。**

### Core Lookup Code

```go
type Ring struct {
    nodes   []uint32           // sorted positions on ring
    nodeMap map[uint32]string  // position → physical server name
}

func (r *Ring) GetServer(key string) string {
    pos := hash(key)
    // Binary search for first node position >= pos
    idx := sort.Search(len(r.nodes), func(i int) bool {
        return r.nodes[i] >= pos
    })
    // Wrap-around at end of ring
    if idx == len(r.nodes) {
        idx = 0
    }
    return r.nodeMap[r.nodes[idx]]
}
```

關鍵點：
1. **Sorted slice + binary search** → O(log N) lookup
2. **Wrap-around** = 環的順時針性質
3. **nodeMap** 把虛擬位置和實體 server 解耦 → 加減 server = 插入/刪除 150 entries

### vnodes trade-off（150 vs 10,000）✅ Resolved S23

| 更多 vnodes | 賺到 | 付出 |
|---|---|---|
| 150 → 10,000 | distribution 更均勻(load 更平) | routing table 更大 + node 間 gossip 同步更重 |

- 超過某個點 = **diminishing returns**(邊際效益遞減):均勻度幾乎不再進步,memory 照付。
- 實務錨點:**Cassandra 預設 256 tokens/node**。記這數字就夠面試用。
- ⏸ Parked(depth ceiling):背後「為何更多點 → variance 下降」的統計學證明(Law of Large Numbers 的數學) — 面試不考,不深究。

---

## Chunk 5 — Range vs Hash partitioning(天花板版,一句對比)

- **Range-based**:按 key 範圍切(A-M / N-Z)。利於**範圍查詢**,但易**熱點**(某段 key 特別熱)。
- **Hash-based / consistent hashing**:按 hash 切。分佈**均勻**,但**範圍查詢**要掃所有節點。
- 細節(re-balancing 策略、secondary index)→ ⏸ parked,設計題需要時再拉。

---

## Chunk 6 — When to use（面試最值錢)

**觸發條件一句話:** 要把 stateful 資料/負載分散到一組「**會變動**」的節點上,且希望加減節點時只搬 ~1/N 的 key。

| 看到這個場景 | 想到 consistent hashing |
|---|---|
| Distributed cache(Redis/Memcached cluster) | cache node 擴縮,不想加一台就 invalidate 全部 |
| NoSQL 分片(Cassandra/DynamoDB) | 資料按 key 分散到動態節點 |
| Sticky load balancing | 同一個 user/key 永遠打到同一台 backend |

**反向(何時 NOT 用):** 節點數**固定不變** → 直接 `hash % N` 更簡單。CH 的全部價值在 **elasticity**。

> Chunk 7 Observability Mini:SLI = key distribution skew(最熱 node / 最冷 node 的比值)、lookup P99;Alert = 某 node 負載 > 平均 ×1.5(分佈失衡);Dashboard = per-node key count。(天花板版,點到為止)

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| Security One-liner 只記得 token 屬性（scoped/short/revocable）和 JWT 簽章 | 這些屬性是「衍生」的，不是核心 — 核心是 OAuth 把三邊關係（user-client-Resource Server）獨立出 Authorization Server | 把實作機制當成本質。屬性是結果，不是原因 |

---

## 🔗 Derivation Insight

**物理限制：** 分散式系統中 N（server 數）會變動，任何依賴 N 為常數的設計都會崩潰。

**我的推導路徑：**
1. 看到 `hash % N` → 發現 N 變 key 的歸屬就變
2. 量化問題：~75% 的 key 要搬 → 不可能 online 做
3. 看到 Ring 模型 → 立刻抓到「key 位置從動態變固定座標」的差別
4. 看 3 個 server 的 ring → 馬上想到「樣本太少 → 統計學失效 → 負載失衡」

**最讓我驚訝的：** 我自己把「sample size → variance」這個統計學概念脫口而出 — 原來分散式系統的均勻分佈本質上是個 Law of Large Numbers 問題。這個視角在 Bloom Filter / HyperLogLog / Sharding 都會重現。

---

## 🗣️ English Practice

| My Answer (中文/混合) | English Polish |
|---|---|
| 「把一把密碼拆成多張窄、短、可獨立撤銷的票券 — 用簽章廉價驗證」 | "Split one master credential into multiple narrow, short-lived, independently revocable tokens — verified cheaply via signature." |
| 「OAuth 把三邊關係獨立成 Authorization Server，讓 user 變成 credential 的源頭和撤銷權的擁有者。Scoped/revocable/short-lived 是衍生屬性，不是本身」 | "OAuth takes the three-party relationship — user authorizing a client to access a Resource Server on their behalf — and architecturally isolates it as a dedicated Authorization Server. This makes the user the origin of credentials and the owner of revocation. Scoped, revocable, and short-lived are properties derived from that architectural decision, not the decision itself." |
| 「hash % N 的 key 位置會隨 N 浮動，所以全部重算。Ring 的 key 位置是固定座標，只有新 server 擠進去那一小段的鄰居關係變了，其他人完全沒感覺」 | "With `hash % N`, key positions drift as N changes — so the entire dataset has to be remapped. On the ring, key positions are fixed coordinates; adding a server only affects the small arc where it's inserted. Everyone else is untouched." |
| 「一台 server = ring 上 1 個點 → 樣本太少 → 統計學讓你失望 → 負載嚴重失衡」 | "One server equals one point on the ring — that's too few samples. Statistics fails you at small N, and you end up with severely uneven load distribution." |

---

## 🎤 How to Say It in Interview (草稿，下半場再 polish)

**Opening (30 sec):**
> Consistent Hashing solves a specific problem: when you use `hash(key) % N` to distribute data across servers, changing N forces roughly 75% of keys to move. That makes scaling impossible without downtime. Consistent hashing fixes this by giving every key a *fixed coordinate* on a ring, independent of how many servers exist. Adding or removing a server only moves the K/N keys in the affected arc.

**When asked: "why virtual nodes?"**
> With few physical servers on a ring, random hash placement creates uneven arcs — one server can end up owning 90% of the keyspace. Virtual nodes increase the sample size: each physical server gets 150 positions on the ring, so the variance of arc sizes collapses. It's a statistics fix, not a hashing fix.

---

## ⏸ Parked (depth ceiling — 面試不考,未來真需要再回來)

- vnodes 數量 → variance 下降的統計學證明(Law of Large Numbers 數學)
- Range vs hash 的 re-balancing 策略、secondary index 細節
- 獨立的 consistent hashing Go PoC → 折進下一場 Distributed Cache 設計題一起做

---

## ▶ Next Session — Design a Distributed Cache(問題驅動)

用一個設計題當錨,把 CAP / Consistency Models / Replication 在「設計需要時」just-in-time 拉進來,
consistent hashing 在這裡實際派上用場(分片 cache key)。深度全程 capped 在面試級。
