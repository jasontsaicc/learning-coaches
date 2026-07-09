# Day 29-30: Unique ID Generator (Snowflake)

> Session 36 · Phase 3 · 2026-06-28
> 接續 Day 28 KGS — 同一個「發唯一號」問題的另一條路線(去中心化)。

---

## One-Liner

> A unique ID generator produces globally unique IDs with **no per-ID coordination**. Snowflake does it by packing a **timestamp + machineID + sequence** into a 64-bit number — collision-free, roughly time-sortable, millions/sec/node.

---

## 核心:Snowflake bit layout

一個 64-bit 整數切成幾段,每段塞一個零件:

```
 0 | 41 bits timestamp | 5 bits datacenterID | 5 bits workerID | 12 bits sequence
 ↑        ↑                    ↑                     ↑                 ↑
sign   毫秒時間            哪個機房              機房內哪台         同毫秒流水號
(0)    (~69年)            (32 機房)            (32 台/機房)       (4096個/ms/台)
```

> 原版 Twitter 是 `10 bits machineID`,實務常拆成 `datacenterID + workerID`,讓多機房零協調保證唯一。

三段各自負責什麼(recall 時務必講功能,別只報菜名):
- **timestamp** → 給時間順序(可排序)
- **machineID(datacenter+worker)** → 跨機器 / 跨機房不撞
- **sequence** → 同一台、同一毫秒內不撞;每跨一毫秒歸零重數

---

## 為什麼是這個結構(自己推出來的因果鏈)

1. 每台機器有獨一無二的 **machineID** → 跨機器不撞。
2. 同一台一毫秒要發多個 → 加 **sequence** counter → 自己跟自己不撞。
3. 機器**重啟** → counter 歸零 → 會重發舊號撞號 → 加 **timestamp**(永遠往前)→ 重啟後時間不同 → 不撞。
4. timestamp 放**最高位** → 「照數字排序 ≈ 照時間排序」這個免費大禮。

### timestamp 為何放最高位(日期格式比喻)
`2026-06-28`(年-月-日)照字串排 = 時間順序,因為「年」在最前面。
若寫成 `28-06-2026`,排序就亂掉(所有 28 號擠一起)。
**多 bit 數字的排序由最高位主宰** → 要可排序就把 timestamp 頂上去。
放錯位(sequence 頂上去)→ 變成按 sequence 排 → 丟掉 time-ordering → DB index 退化成 UUID 的隨機亂插(B-tree page split)。

---

## ⚠️ 最大的雷:Clock Skew(時鐘倒退)

Snowflake 的唯一性**假設「時間只會往前」**。但 NTP 校時 / 閏秒 / VM 暫停恢復都會讓時鐘倒退。

倒退的具體災難:
```
1000ms 已發 (1000,5,0)(1000,5,1)(1000,5,2)
時鐘走到 1100ms → NTP 把它拉回 1000ms
機器以為是「新毫秒」→ sequence 歸零 → 又發 (1000,5,0)  ← 撞號!
```
**結果 = 生出重複 ID,整個唯一性保證崩掉。**(不是變慢這種小事,是直接違反存在理由)

### 解法:偵測 + 保守處理
每台機器記 `lastTimestamp`,發號前比 `now < lastTimestamp` → 偵測到倒退:
1. **報錯 / 拒發**(Twitter 原版)— 寧可罷工不發可疑號
2. **等(spin-wait)**直到時鐘追回 lastTimestamp
3. 借位(額外 bit 記 epoch,複雜少用)

心法:**拒發 > 冒險發重複號**。下游(DB PK、付款單號)拿到重複 ID 賠錢賠資料且難查,卡幾毫秒幾乎無感 = Day 27「丟得起 vs 丟不起」同款判斷。

---

## machineID 怎麼發?(協調又繞回來)

Snowflake 號稱 coordination-free,但有個小謊:machineID 是誰發的?兩台拿到同一個 = 跨機器撞號。

| 做法 | 怎麼運作 | 雷 |
|---|---|---|
| 手動 config 寫死 | 部署時人工指定 | 人為錯、容器多管不動 |
| ZooKeeper/etcd | 開機跟中央要唯一序號 | 多依賴,但只在**開機要一次** |
| K8s StatefulSet | pod 名 `worker-0/1/2` 天生唯一,取後綴 | 綁 K8s |
| IP/MAC 後幾位 | 用網卡位址 | 可能撞(IP 重用) |

關鍵:**「開機協調一次,運行時零協調」**。跟 KGS「領一個 block 用很久」是同一招成本攤平 — KGS 攤平號碼範圍,Snowflake 攤平機器身分。所以 ZooKeeper 不會變瓶頸(總共才被打 1024 次)。

---

## 四條路線光譜(主軸:協調越少越能 scale,代價是號越長/越難排序)

| 路線 | 怎麼生 | 唯一 | 排序 | 協調 | 雷 |
|---|---|---|---|---|---|
| UUID v4 | 隨機 128-bit | 機率 | ❌ | 零 | 又長又不可排序,DB index 差 |
| DB auto-increment | DB +1 | ✅ | ✅完美 | DB=中央 | **SPOF + 高並發 bottleneck** |
| KGS(領 block) | 中央發範圍本地用 | ✅ | ✅ | 開機/領block | 中央要 HA、丟號 |
| Snowflake | 本地算 time+machine+seq | ✅ | ✅粗略 | 開機發 machineID 一次 | **clock skew** |

`完全靠中央(DB) → 攤平(KGS) → 幾乎不靠(Snowflake) → 完全不靠(UUID)`

### KGS vs Snowflake(面試常問)
- **KGS 集中產生「號的值」** → 能做到**短**(URL 短碼 `aZ3k9`),但無時間資訊。
- **Snowflake 每台自己「算」ID** → 零運行時協調 + 可排序,代價 64-bit 較長(base62≈11字)。
- 要短(給人看)→ KGS;要可排序+高吞吐(內部用)→ Snowflake。

---

## Capacity(別被 2 的次方嚇到)

- sequence 12 bits → `2^12 = 1024×4 ≈ 4000` 個/毫秒
- 1 秒 = 1000 毫秒 → 一台 ≈ **400 萬/秒**
- 需求 10 萬/秒 → 一台就是 **40 倍**。throughput 完全不是問題。
- 那為何還要多台多機房?**高可用(避 SPOF)+ 地理延遲(就近發號)**,不是為了吞吐量。

招式:看到 `2^n` 先拆成 `1024 × 2^(n-10)`,再移小數點。

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| Q2「不准中央配號」→ 想「每台有自己的區間範圍」 | 區間是誰分的?又需要中央 + 會用完 + 新增機器會重疊。正解 = 把機器身分(machineID)揉進 ID,每台自己算 | 還停在 KGS「切號碼空間」思路,沒跳到「切身分」 |
| 防撞想用 hash(machine 名字) | hash 會碰撞 = 只「大概不撞」。直接給門牌號(machineID)塞進 ID = 保證不撞。與 Day27 counter≠hash 同理 | 反射性想到 hash,忘了上週「counter 消滅碰撞」的教訓 |
| timestamp 放哪位無所謂(Transfer 卡住) | 排序由最高位主宰;timestamp 不在最高位 → 變按 sequence 排 → 丟掉 time-ordering | 沒有「多位數排序看最高位」的直覺(日期格式比喻補上) |
| clock skew 只覺得「很危險」講不出為什麼 | 倒退 → 重入舊毫秒 → seq 歸零 → 重發已發過的 ID = **撞號** | 沒把「危險」翻成精確機制,停在感覺 |
| Interview Drill 給結論不給論證(「Snowflake 最適合」) | 要主動講「為何 DB auto-increment 不行 / Snowflake 為何剛好全中」 | 頭號主線弱點:答太精簡,被追問才展開 |
| Drill 全程沒提 operational 監控(第4次) | ID 服務要監控 clock skew alert + 發號 QPS + sequence 打滿率 | S29/30/34 重複盲點,監控未變收尾反射 |
| capacity「直接放棄」 | 全是 `1024×4` + 移小數點,沒有難算的東西 | 被 `2^12` 寫法嚇到,不是真的不會 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "A unique ID generator needs globally unique IDs without coordinating on every single ID. I'd reach for Snowflake: a 64-bit number split into a timestamp, a machine ID, and a per-millisecond sequence. The timestamp sits in the high bits so IDs are roughly time-sortable — great for a DB primary key — while the machine ID and sequence guarantee no collisions across nodes and within a node."

**When asked "why not DB auto-increment / UUID?":**
> "DB auto-increment is a single-point bottleneck and a SPOF under high concurrency — if that DB is down, nobody can place an order. UUID is coordination-free but it's 128-bit, unsortable, and hurts B-tree index locality. Snowflake gives me both: collision-free AND time-sortable, coordinating only once at boot to assign machine IDs."

**When asked "isn't a sortable ID a security leak?":**
> "Good catch — Snowflake leaks creation time and within one machine the sequence is consecutive, so it's sortable-but-not-secret. Fine for internal IDs; if it's exposed to clients I'd randomize or encrypt it. Sequential DB auto-increment is worse — it leaks total order volume (German tank problem) and lets people enumerate others' records."

**Showing production depth (FIX the blind spot — say this every time):**
> "In production I'd monitor **clock skew per node** with an alert (the #1 Snowflake failure), plus issue QPS and how often the sequence saturates — saturation means I should add nodes. On detected clock-rewind, the node refuses to issue rather than risk a duplicate."

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| 組合 timestamp + machineID + sequence 來達到排序優勢以及 HA,不會碰撞,不像 UUID 會是亂碼,or KGS 單點 or DB auto 可遞增但單點 + 要解決高併發 | "Snowflake packs a timestamp, machine ID, and sequence into a 64-bit ID — collision-free and roughly time-sortable at millions/sec per node. Unlike UUID (long and unsortable), a central DB (single-point bottleneck under high concurrency), or KGS (also centralized), it only coordinates once at boot." |
| 因為每次詢問 DB 會產生瓶頸以及要解決 DB cluster 分配的問題 | "A central DB auto-increment becomes a throughput bottleneck and a single point of failure; sharding it just pushes the problem into offset/step coordination across the cluster." |
| Snowflake 可排序是因為前面幾碼依照 timestamp,後面機器和流水號不同 | "It's sortable because the high bits are the timestamp; the lower machine-ID and sequence bits make consecutive IDs jump around, so it's ordered by time but not consecutively guessable." |

---

## Parked (Curiosity Branches)
- ULID / KSUID(Snowflake 的字串表親,lexicographically sortable)— 面試提到名字即可
- Snowflake PoC(Go 實作 bit packing + clock skew 偵測)→ Day 30 可做 Light PoC
- Clock skew 變體:借位 epoch bit 的細節 — 深度天花板,面試不問

## Cross-Verification (下次帶)
雙查 Snowflake bit layout 對照 Alex Xu Vol.1 Ch.7 「Design a Unique ID Generator」 — 確認 epoch 起點、41 bits=~69 年的算法、以及 datacenter/worker 各 5 bits 的拆法。有出入下次提出。
