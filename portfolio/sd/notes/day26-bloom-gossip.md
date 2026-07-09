# Day 26: Bloom Filter & Gossip Protocol

> Phase 2 最後一站。兩個「用近似/最終換效率」的經典招式。學完 → Phase 2 Gate。

## One-Liners

- **Bloom Filter**：用 hash 把「資料的存在性」壓成 bit array 的成員查詢結構，能斬釘截鐵說「一定不在」、只能說「可能在」，用一點誤判率換巨大空間節省，DB 永遠是最終裁判。
- **Gossip Protocol**：去中心化的狀態同步，每個節點每回合隨機告訴幾個 peer，訊息指數擴散、O(log N) 回合收斂，沒有 master 當 SPOF，代價是 eventual（最終）一致而非即時。

---

## 1. Bloom Filter 核心機制

- **不存原始 ID，只存「被 hash 打過的痕跡」**。一排燈泡（bit array，全 0）+ k 個 hash function。
- **Insert**：算 k 個位置 → 把那幾盞燈打開（set bit = 1）。一個元素永遠只佔 k 個 bit，與長度無關。
- **Query**：算同樣 k 個位置 → 看是否「全亮」。
  - 有任一格是 0 → **一定不在**（它若進過一定會點亮，不可能留空）
  - 全亮 → **可能在**（probably in）

### 關鍵不對稱 (asymmetry)
> **No false negative, but yes false positive.**
- 誤報來源 = 不同元素的章**重疊**（hash 碰撞）。
- 「全亮」≠「一定在」，因為可能是別人的章剛好把這幾格填滿。

### 為什麼 false positive 可接受
Bloom = 便宜的第一道篩子，後面站著 DB（權威）：
```
request → [Bloom] ──「一定不在」──→ 直接放行（擋掉絕大多數流量，0 次查 DB）
                └──「可能在」────→ 查 DB 確認（誤報只是偶爾多查一次）
```
最終結果永不出錯，1% 誤報 = 只有 1% 清白流量多查一次 → 划算。

---

## 2. 空間 Trade-off (面試 punchline)

| 方案 | 空間 (10 億筆) |
|---|---|
| 精確存 HashSet | ~8 GB（每台 server 一份 → 爆炸）|
| Bloom Filter | ~1.2 GB（公式 `m = -n·ln(p)/(ln2)²`，p=1%）|

> **不用背公式**，記結論：**約省 85%，代價是 1% 誤報 + 偶爾多查 DB。**

---

## 3. Bloom 真實落地 (DevOps 角度)

| 放法 | 實現 | 優點 | 代價 |
|---|---|---|---|
| Local in-memory | Guava / Go `bits-and-blooms` | 0 網路延遲，奈秒級 | 每台一份 copy，更新要同步 |
| 集中式 Redis | RedisBloom `BF.ADD`/`BF.EXISTS` 或 bitmap `SETBIT` | 全 server 共用，更新一次全看到 | 每次查多一個網路 hop |
| DB 內建 | Cassandra/HBase/RocksDB 每個 **SSTable 一個 Bloom** | 跳過「一定沒有」的 SSTable，省 disk I/O | （LSM 讀放大的解藥）|

**常見戰場**：黑名單/防詐、**快取穿透防護**（cache penetration，擋查不存在 key 的攻擊）、爬蟲 URL 去重。

---

## 4. Gossip Protocol 核心機制

- **問題**：N 個節點要互相知道死活（membership）。全量廣播 = O(N²)。N=10,000 → 1 億條訊息，不 scale。
- **解法（學八卦/病毒傳播）**：每個節點每回合**隨機挑**幾個 peer 說悄悄話 → 收到的人下回合也變傳播者 → 知道的人**每回合翻倍**。
- **數量級**：收斂回合數 **O(log N)**（N=10,000 約 13~14 回合），總訊息量 **O(N log N)**，都遠小於 O(N²)。
- **為什麼隨機而非固定鄰居**：固定鄰居消息會卡在角落傳不出去；隨機才保證不被困住、抗分區。
- **去中心化**：沒有 master → 沒有 SPOF、沒有瓶頸，掛幾台不影響其他人繼續八卦 → 高可用。Cassandra/Consul/DynamoDB 都用它管 membership。

### 優雅性質
> **Union of Bloom filters = bitwise OR of bit arrays.**
> Crawler 之間 gossip 同步 Bloom 時，不傳 URL 清單，只交換並 OR 各自的 bit array 就完成合併。

---

## 5. 共同哲學 (Phase 2 收官金句)

| | 放棄什麼 | 換到什麼 |
|---|---|---|
| Bloom Filter | 100% 精確（接受誤報）| 巨大**空間**節省 |
| Gossip | 瞬間一致（接受 eventual）| 巨大**訊息量**節省 |

> 🏆 **精確（exact）和即時（instant）是昂貴的。當業務能容忍「近似」或「最終」，就能換到數量級的效率提升。**
> 這是分散式系統的母題：Eventual consistency、virtual nodes、Quorum 全是同一個 pattern。面試遇 scale 題反射問：「這裡能容忍多少不精確/多少延遲？」

---

## 🔗 Derivation Insight

- **Physical constraint:** 精確成員查詢 O(N) 空間（10 億筆 ~8GB）；全量廣播 O(N²) 訊息（N=10⁴ → 1 億條）。精確與即時都隨規模爆炸。
- **My derivation:** 接受「寧可錯殺不可放過」→ 只存 hash 痕跡 → 空間暴減（Bloom）；不要人人廣播 → 隨機接力擴散 → 訊息暴減（Gossip）。
- **Surprise:** 「全亮」竟然不能推「一定在」（親手踩到 false positive 陷阱）；以及 Bloom 合併居然只是 bitwise OR。

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| Bloom 查詢「三格全吻合 = 一定在」 | 只能推「**可能在**」，全亮可能是別人的章重疊 | 沒意識到 hash 碰撞讓不同元素共用 bit |
| 爬蟲 100 億 URL 存不下是因為「訊息量 O(N²)」 | 儲存是 **O(N) 空間**（100億×100B≈1TB），只是 N 太大；O(N²) 是 gossip 的**廣播訊息**問題 | 把「儲存空間」和「節點間訊息量」兩個軸搞混 |
| LSM-tree 細節（一度忘記） | B-tree 讀優化、LSM 寫優化（memtable→批次刷 SSTable，讀要合併多層，配 Bloom 跳層）| Phase 1 舊知識衰退，需重排複習 |

**Interview habit（持續改善中）**：drill 答案第一次太精簡，被追問才展開（S8/S24 老主線）。本次只追一次就講全，有進步。目標：**一次講足「選什麼 + 為什麼 + 反面代價」**。

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "Bloom filter is a space-efficient, hash-based membership test — it answers 'definitely not in' or 'probably in', trading a small false-positive rate for huge space savings, with the DB as source of truth. Gossip is its sibling on the network side: decentralized state sync where each node tells a few random peers, converging in O(log N) rounds with no central master."

**When asked to go deeper (distributed crawler dedup):**
> Q: "50 台 crawler 各有 local Bloom，怎麼不重複爬？"
> A: "Centralized Redis Bloom 每次查都多一個網路 hop，10K/s 全卡在它身上且是 SPOF（加 replica 也增複雜度）。我選 gossip 同步 local Bloom：收斂前會短暫重複爬，但對爬蟲來說重複爬只是小浪費、完全可接受 → eventual 划算。Bloom 合併直接 bitwise OR，gossip 成本很低。"

**Showing production depth:**
> "In production, I'd monitor the **重複爬率**（gossip 收斂效果）、Bloom 的**實際 false-positive rate**（vs 設計值）、bit array 飽和度（填太滿 FP 會飆）。Saturation 當早期預警。"

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| Bloom 用 hash 判斷在不在名單，省 space，trade off 會誤判，但真相始終在 db | "A Bloom filter is a hash-based membership test that trades a small false-positive rate for huge space savings — and the database stays the source of truth for any 'probably in' hit." |
| Gossip 多節點傳遞信息，每節點隨機分享 2~5 台，等待同步但最終一致，O(N²)→O(log N) | "Gossip is decentralized state sync — each node tells a few random peers, so info spreads exponentially and converges in O(log N) rounds with no master SPOF; the trade-off is eventual rather than instant consistency." |
| 共用 Redis Bloom 經過慢網路又是 10K/s，建議 gossip 同步 local bloom，量體大短暫重複爬可接受 | "A central Redis Bloom adds a network hop on every check at 10K/s and is a bottleneck, so I'd gossip-sync local Bloom filters — brief duplicate crawling during convergence is a tolerable waste at this scale." |
| 中心化 Redis Bloom 會有 SPOF | "A centralized Redis Bloom introduces a single point of failure and becomes a throughput bottleneck on the hot path." |
