# Day 28 — URL Shortener Full PoC (base62 + KGS 發號器)

> Session 35。把 S32–S34 嘴上講通的設計用 Go 跑出來,證明「counter + base62 = 零碰撞」。
> 程式碼:`projects/day28-url-shortener/main.go`

---

## One-liner

短碼生成 = base62 編碼一個**全域唯一的 counter**;碰撞是被「消滅」的(不是減少),所以根本不需要 hash。KGS 中央發號器靠「一次領一整塊號 (block)」攤平協調成本。

## Trade-off

- **counter + base62 vs hash(URL)**:選 counter,因為 counter 天生唯一 → 零碰撞;hash 是大空間壓到小空間(鴿籠原理)必然碰撞,還要額外處理。
- **KGS 領 block vs 每次要一個號**:選領 block。代價 = 機器當機時手上剩號變「空洞」浪費掉;換來 = KGS 流量降到 1/block,不變單點瓶頸,每碼省一次網路 round-trip。命名空間 `62⁷≈3.5兆`,丟幾千個號無感。
  - 哲學家族:跟 rate limiter 的 lazy refill、gossip 一樣 = **犧牲一點精確/連續,換大幅降低協調成本 (batching)**。

## Scale trigger

- 每生一碼跑一趟 KGS → 幾萬 QPS 時 KGS 先倒 → 改「領 block」批次化。
- counter 逼近 `62⁷` 用量 80% → 要擴碼位(7→8)。

## DevOps angle(operational 收尾,治 S29/S30/S34 老盲點)

| SLI | 為什麼 | 告警 |
|---|---|---|
| collision rate | 核心正確性,恆 0 | `>0` 立刻 page(KGS 發了重號=災難) |
| KGS counter 剩餘空間 | counter 是有限資源 | 用量 >80% |
| block 領取 P99 | KGS 健康度,變慢=瓶頸前兆 | P99 超閾值 |
| 空洞率 dropped/total | 太高=block 開太大或頻繁當機 | 異常飆高 |

---

## PoC 實驗結果(全綠)

| 實驗 | 指令 | 證明 |
|---|---|---|
| 正常 50 萬碼 | 預設 | `COLLISIONS: 0`,50 萬全 unique |
| 並發安全 | `go run -race` | race detector 零警告 → `sync.Mutex` 真的擋住重號 |
| 失敗注入 | `-drop -block 1500` | 丟 1 萬個空洞號,**仍 0 碰撞** → 「機器掛掉剩號丟掉=OK」成立 |

**長度自然分布**(印證「碼自然長大不補 0」):1碼 62 個 → 2碼 3782 → 3碼/4碼 數十萬。早期 URL `short.ly/7`,後期 `short.ly/aZ3k`。

### Go 學到的點(教 Yuki)
- string 底層是 **byte 序列**;`s[i]` 拿到的是 **byte(數字編號)** 不是字串,要看字得 `string(s[i])`。實測 `alphabet[1]=49`、`string(alphabet[1])="1"`。
- `len(string)` 數的是 **byte 數**(ASCII 才等於字元數;中文每字 3 bytes)。
- base62Encode 核心三行:`r := n%62` / `append(buf, alphabet[r])` / `n = n/62`,除法從低位吐 → 最後 `reverse`。
- KGS 用 `sync.Mutex` 保護 counter;Worker 用 pointer receiver `func (w *Worker) Next()` 才能改自己的 `next`。

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| base62 把「長網址」encoding 成固定長度 | base62 編的是 **counter 那個數字**,長網址原封不動存進 DB 當 value,base62 碰不到它 | S32 踩過、S34 修好的點,隔 2 天又滑回去 — counter 負責唯一,base62 只是換進制讓數字變短 |
| 短碼要「固定 7 位數」 | 碼是**自然長大**的(counter 小→碼短);「7」是容量天花板 `62⁷`,不是每碼補滿 7 位 | 把「命名空間上限」誤當「固定長度」;補 0 反而浪費+洩漏發號量 |
| (operational) 丟 1 萬個號是 bug 要修 | 是設計選擇:命名空間 3.5 兆,空洞無感;真正要避免的是每碼問 KGS 一次 → KGS 變瓶頸 | 只想到「浪費」沒想到「協調成本」這一面 = operational 視角缺口 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "短碼生成我會用 counter + base62,不用 hash。counter 全域唯一保證零碰撞,base62 只是把那個數字換進制變短 —— 6 碼就有 640 億個,夠用。hash 是把大空間壓小空間,必然碰撞還要額外處理,不划算。"

**When asked to go deeper（生號怎麼 scale?）:**
> Q: "每秒幾萬個短碼,counter 怎麼發不變瓶頸?"
> A: "中央 KGS 發號,但不是每碼問一次 —— 那 KGS 會被打爆。改成每台機器一次領一整塊號 (block),自己慢慢用,KGS 流量降到 1/block。代價是機器當機時手上剩號變空洞浪費掉,但命名空間 3.5 兆,丟幾千個無所謂,短碼也不需要連續。"

**Showing production depth:**
> "上線我會盯 collision rate(理論恆 0,一旦 >0 立刻 page,代表 KGS 發了重號)、KGS counter 剩餘空間(逼近 80% 要擴位)、還有 block 領取的 P99 當 KGS 健康度的 leading indicator。"

---

## Cross-Verification(下次帶回)

- Alex Xu Ch.8 URL Shortener:確認他對「unique ID generator / KGS」跟 base62 的拆法,跟我這版是否一致(他可能把發號獨立成 Day 29-30 的 Unique ID Generator 主題)。
- 查:Twitter Snowflake ID 跟「KGS 領 block」差在哪 —— Snowflake 用 timestamp+machineID 不需中央協調,是另一條路線。
