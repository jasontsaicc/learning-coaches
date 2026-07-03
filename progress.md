# Student Progress Tracking

> This file is the single source of truth for student progress.
> Updated by Claude at the end of every session (Step H) and when sessions are interrupted.
> Read by Claude at the start of every session to determine where to resume.
> **Coach 必讀：`docs/coaching-brief.md`**（S1-S36 蒸餾的作戰手冊：五個 chronic 弱點的對治協議、有效/無效手法、強項槓桿。開場讀完再教）。

---

## Student Info

| Field | Value |
|-------|-------|
| **Start date** | 2026-03-04 |
| **Current phase** | Phase 3 🏗️ |
| **Current day** | **S38 完成（跨機器接續）= Rate Limiting 複習 + Day 31 Distributed Rate Limiter 完整設計自推。** 下一步 = 續清 execution-heavy 逾期複習（Observability/DB/CH/LB）+ Drill Gauntlet（含 rate limiter bar-raiser） |
| **Language mode** | Bilingual — S27 切回繁中為主（學生英文閱讀疲勞），術語保留英文 |
| **Session count** | 38 |
| **Last weekly review** | 33 (S33 = WR4 完成) |

---

## 🎚️ Learning Mode (Active — set Session 23)

**Mode: 問題錨定 + 深度天花板 (Problem-anchored + Depth Ceiling)**

Reason: 學生在純理論主題(consistency models、consistent hashing 的 vnodes 數學)磨太久,
公式/形式化的深度對面試零回報,導致進度緩慢 + 學習痛苦。

Rules going forward:
1. **深度天花板三問** — 碰到一個主題往下鑽時問:(a) 面試官會問嗎? (b) 這層深度能讓我的回答更好嗎? (c) 我卡住是缺地基還是想完美? 任一題答「不會/不能/想完美」→ park 到 Curiosity Branches,繼續走。
2. **壓縮理論期** — Day 15-22 building block 改「概念 + 一句話 + 一個 trade-off」快速模式,PoC 降級為 Light/Discussion,不追完整 Full PoC。
3. **題目驅動 (pull)** — 用 **Design a Distributed Cache** 當錨,把 CAP(Day 17-18)、Consistency Models(Day 19-20)、Replication & Leader Election(Day 21-22)折進這個設計題,理論在設計需要時才 just-in-time 拉進來,capped 在面試深度。
4. 面試考的是 breadth of mental models + trade-off reasoning,**不是** CS 理論深度(linearizability 形式證明、consistency 數學模型 = PhD 範圍,不學)。

**Execution-Heavy overlay (2026-07-03, S37 meta review):** 在深度優先課表之上疊一層 — 暫停「每場一個新 archetype」的 acquisition 節奏,改 drill 為主（Drill Gauntlet）。理由:Phase 2 後已無知識缺口只有執行缺口。首攻 #1 結論不給論證。完整 protocol 見 `docs/coaching-brief.md` [Execution-Heavy Mode]。unprompted 三指標各 3 連達標後可回課表節奏。

**Scope decision (2026-07-02, S36 後 plan review):** 無明確面試日期 → 深度優先,全課表照走。從外部訓練營課表補進 3 個缺的 archetype(Day 54-59: Ticket Booking / Top-K / Ride Matching),Phase 4 順延為 Day 60-69(課表總長 69 units;含 skill 新版的 Brownfield Migration Day 62-63)。本機 sd-coach skill 原落後 remote 24 commits,2026-07-02 已同步至新版(Teach Yuki/RPG/Fast Path/Brownfield),3 個 archetype 是重放在新版上。其餘訓練營題目(Dropbox/YouTube/Twitter/A-B Testing 等)= 既有 pattern 組裝,不排課,對照表見 `docs/pattern-map.md`。照目前 ~2.2 session/週的節奏,預估 2026 年 12 月初完課。Parked PoC triage:留 distributed cache(Day 38-39)+ rate limiter(Day 31-32),放掉 Circuit Breaker 獨立 PoC(概念已 5/5,邊際回報低)。

---

## Current Session (Breakpoint)

✅ **Session 38 完成（跨機器接續，模型 Opus）。兩段跨機器：**
- **(工作 PC) execution-heavy Part 1 逾期複習 1/5：** ✅ **Rate Limiting failure-timeline PASS** — 本地計數陷阱「10 台 ×1000 = 10000/min」冷推出來（S28 的 N×limit 28 天後仍在），補「無聲失敗」點（每台全綠但合計 10 倍 = 監控盲點反例）。→ **Box 1→2**。但 one-liner 機制層（Token Bucket/Sliding Window/兩層/CB）掉了，下次再測。
- **(這台) Day 31 Distributed Rate Limiter 完整設計 —— 全鏈自推：** 從 Rate Limiting 暖身(同上,順接)→ 100 台各跑各的 = 孤島 → N×limit=10,000 → 共享 Redis counter(選對「共享計數器」非「一台限流機器」=SPOF)→ 搶票超賣比喻教 race condition → 學生**自己跳到** Redis 單執行緒 DECR 原子性 → TTL 過期(Fixed Window)取代排程手動補 → 抓到邊界 2 倍破綻 → sliding window「往回看 60s」補洞 → 多步 race 重演 → Lua 捆多步成原子收口。主軸就一個字 atomicity。筆記 `notes/day31-distributed-rate-limiter.md`+mindmap。
  - 🌟 **頭號弱點突破**：收尾 One-Liner 主動把「選 sliding window **因為**往回算 request」結論+論證綁一起,沒等追問(execution-heavy 首攻目標本場有一次達標)。
  - 🌟 自抽「**主動 vs 被動**」遷移心法(TTL 過期 > 排程主動清),連到 DevOps 半夜 job 掛。
  - ⚠️ **給我自己的教訓**:本場 3 次「有點亂/什麼意思」= 我一次塞太多 + 抽象 meta 問句;退小步+具象比喻(搶票、計數紙自燒)後全通。非概念不懂,是 pacing。

**execution-heavy 三條硬規則仍生效：** 第一句就評分 / 裸結論直接打回不接「為什麼」/ 追蹤 unprompted-argument·ops·no-freeze-capacity 三指標。監控收尾＝3AM page test 當第 5 步硬關卡。

**Next（接續點，優先序）：**
1. **execution-heavy 續清逾期複習（剩 4 筆）**：Observability(2/5,已出題:①三支柱各答什麼問題 ②30 微服務結帳轉 8 秒失敗 Metrics/Logs/Traces 查序) → Database B-tree/LSM(3) → Consistent Hashing(4) → Load Balancer(5)。清完才進 Gauntlet。
2. **Drill Gauntlet 第一場**（混合舊題 bar-raiser）—— **新增一題 Distributed Rate Limiter bar-raiser**（本場只教概念未 pressure-test,capacity 也沒做,一起補）。
3. Day 30 Snowflake Light PoC 排在 Gauntlet 之後（park）。

---

## 📦 S37 前的原 breakpoint（保留參考）

✅ **Session 36 完成（Day 29 Unique ID Generator 設計+理論,Snowflake)。** 筆記 `notes/day29-unique-id-generator.md`。
- **問題錨定教法奏效**:從 KGS(上場)橋接 — 「不准中央配號,100 台各自發唯一 ID」→ 學生**自己推出** Snowflake 三段骨架(machineID 不撞跨機器 → 加 counter 同台不撞 → 重啟撞號 → 加 timestamp)。timestamp 放最高位用「日期格式 `2026-06-28` vs `28-06-2026`」比喻打通(「排序由最高位主宰」)。
- **Clock skew(最大雷)**:學生卡在「只覺得很危險」講不出機制 → 用具體數字走「倒退→重入舊毫秒→seq 歸零→重發已發號=撞號」釘死。解法拒發>等>借位,連回 Day27「丟得起 vs 丟不起」。
- **兩條 coaching 設定本場建立(已存 memory)**:[[coaching-no-mechanical-gate-labels]](學生點名「Recall/Transfer」標籤太機械 → 收回,自然問) + [[coaching-aggressive-interviewer-drills]](學生主動要求 Drill 當 bar-raiser 用力追問,他真面試常被追問考倒)。
- **Interview Drill ~4/7(未達 Phase3 線 5/7,練習非 Gate)**:✅ think aloud/scope(主動想到 enumeration 洩漏營業額=architect 級,加分)/用 Snowflake;🟡 trade-off WHY(給結論不給論證,被追問才展開=老毛病)/failure modes(SPOF 有 clock skew 沒主動帶);❌ operational(第4次監控掛蛋)+ capacity(「直接放棄」,我拆 1024×4 才跟上)。

**Next session = 先清逾期複習(5 筆: Consistent Hashing / Load Balancer / Rate Limiting / Observability / Database B-tree-LSM,其中 Rate Limiting + Observability 是 Box 1 從未確認過,優先),再進 Day 30 Snowflake Light PoC**(Go 實作 bit packing + clock skew 偵測;學生堅持手打,參 [[poc-student-types-everything]]+[[poc-go-drill-style]])。複習清不完就佔滿整場,PoC 順延,不趕。

**Pending PoC(park):** 分散式 Redis rate limiter → Day 31-32。Consistent hashing 獨立 PoC + distributed cache 完整實作 → Day 38-39。~~Circuit Breaker PoC~~ + ~~Replication lag PoC~~ → 2026-07-02 triage 放掉(概念皆已 drill 至 5/5,邊際回報低;Day 38-39 replication 設計時若自然需要再拉回)。

**Pending review(下次 Step A 帶):**
- **Security 廣度(OAuth/JWT/session)** 只測了 crypto-primitives 一塊,full recall 仍欠 → Box 維持 2,下次補。
- **Review Schedule 多筆逾期**：Consistent Hashing(6/05)/Load Balancer(6/05)/Rate Limiting(6/10)/Observability(6/16)/Database B-tree-LSM(6/17)。
- **🔴 頭號習慣弱點（S8→S36 主線）**:「答太精簡,被追問才展開」+「主動要提示而非先嘗試」。**S36**:Drill 給結論不給論證再現(DB auto-increment 一句帶過、Snowflake「最適合」沒論證)。已啟動 bar-raiser 模式加壓。
- **🔴 operational 監控盲點(S29/30/34/36 第4次)**:Drill 從不主動提監控。固定要求:設計收尾必加一句監控(對 ID 服務=clock skew alert + 發號 QPS + sequence 打滿率)。
- **capacity 心理障礙**:被 `2^n` 寫法嚇到就放棄,非真不會。固定提醒「拆 1024×2^(n-10)」。

---

## Topic Mastery

| Day | Topic | Mastery | Phase Gate | Notes |
|-----|-------|---------|------------|-------|
| -5 to -1 | Go Refresher | 🟢 | — | 5 days complete |
| 1 | SD Interview Rubric | 🟢 | — | |
| 2 | Back-of-Envelope Estimation | 🟢 | — | |
| 3 | 4-Step Framework | 🟢 | Phase 0 Gate | |
| 4-5 | Load Balancer | 🟢 | — | WR3 (S25) recall 4/5 大回血。Weighted RR 老錯 resolved，補回 RR + Least Connections 基礎，L4/L7 最強。Upgraded 🟡→🟢. |
| 6-7 | Caching & CDN | 🟢 | — | **WR4 (S33) 六維度全收 → 升 🟢**(WR1 曾 0/4)。scale trigger/trade-off/invalidation(寫時刪 zero退化)/DevOps(hit rate)/failure modes(stampede+penetration+avalanche 三件套)/capacity(補 80/20 盲區,自算 1TB→256GB)全穩。最弱主題救成最穩之一。 |
| 8-9 | Database Selection | 🟡 | — | WR4 (S33): 避開「資料量大→NoSQL」陷阱,訂單→SQL 完整三理由(關聯/join/ACID)一口氣講足,主線弱點本場練成功。但 NoSQL 何時選的完整光譜仍未全 drill,維持 🟡。B-tree/LSM resolved。 |
| 10-11 | Message Queue | 🟢 | — | WR2 Part 2: 3 mistakes resolved (delivery semantics, why-async 3 reasons, FR/NFR/Scope definitions). Now confident on core concepts. Recall 2/4 → notes patched gap. Upgraded from 🟡. |
| 12-13 | API Design | 🟢 | — | WR2 Part 2: 5 mistakes resolved (GET/POST data location, JWT in header, pagination, idempotency 3rd state, SLI/SLO hierarchy). Notes patched with Scale Trigger + DevOps Angle sections. Upgraded from 🟡. |
| 14 | Security & Auth | 🟢 | — | Sessions 19-21. All 8 chunks ✅. OAuth Q2/Q3 resolved, Auth Code Flow, Observability Mini, Scale Trigger, JWT PoC, Simon Drill passed. |
| 15-16 | Consistent Hashing | 🟢 | — | S22-23. 所有 chunk ✅ at interview depth。Strong self-recall。S24 在 distributed cache 設計中當 sharding 機制實際應用。vnode 統計證明 + 獨立 PoC parked → Day 38-39。|
| 17-18 | CAP Theorem | 🟢 | — | S24 problem-anchored。自己推出 cache stampede → replication → C vs A 矛盾。AP 選擇給出教科書級三理由(DB=truth, TTL 自癒, cache 天職是答得出)。partition 定義一開始不清→當場補。業界 CAP 對照表 + 「給錯=賠錢→CP」心法。PACELC 未深入(park)。|
| — | Distributed Cache (design) | 🟢 | **Phase 1 Gate ✅** | S24. 問題錨定設計，3/3 PASS = Phase 1→2 Gate。涵蓋 clarify→sharding→cache-aside→client vs proxy routing→replication→CAP→thundering herd/request coalescing。完整 PoC park 到 Day 38-39。|
| 19-20 | Consistency Models | 🟢 | — | S26 Day 19。7 chunk 全過 at interview depth。自推 strong=同步=等待=慢。光譜表(Strong/Causal/RYW/Eventual)+ Quorum W+R>N(鴿籠重疊)。Eventual≠不一致(收斂保證)misconception 打通。Vector clock(Day 20)park。Drill 4/5。|
| 21-22 | Replication & Leader Election | 🟢 | — | S27。7 chunk 全過 at interview depth。核心因果鏈打通(硬體壞→多份→ordering→election→split-brain→lag→監控)。Single-leader=唯一 ordering 免衝突、過半票防腦裂(鴿籠)、read replica≠strong(lag) 三大點都能在設計題情境自然調用。Interview Drill 5/5 滿分。Raft 細節/Service Discovery/PoC park。|
| 23-24 | Rate Limiting & Circuit Breaker | 🟢 | — | S28。7 chunk 全過 at interview depth (一次過沒卡)。Token Bucket(+自連 AWS T-series credits)、lazy refill(成本跟流量走不跟桶數)、Sliding Window 嚴格封頂、分散式 local counter 失效(N×limit→Redis 3代價)、Circuit Breaker Closed/Open/Half-Open(fail fast 防雪崩)。Light PoC 手打 lazy refill 驗證 rate=refillRate×time。Interview Drill「惡意爬蟲攻擊 API」5/5 滿分,自推 per-user+global 兩層+SW 護 DB+CB 防雪崩。lazy 概念當場補。CB PoC park。|
| 25 | Observability | 🟢 | — | S29。3 chunk 全過 at interview depth。自推三支柱(Metrics→想到 CPU/mem、Logs→想到查原因、Traces→用 traceroute 點到方向對工具錯)。盲區互補表+debug 動線「Metrics 報警→Traces 指路→Logs 挖根因」。Correlation ID 機制(入口生成→header 傳遞→斷鏈風險)手寫 Go snippet。SLI/SLO/SLA 弱點鞏固(考試比喻:實際分/目標分/合約罰則,SLO 比 SLA 嚴格留 buffer)。Drill 5/6。理論日 Discussion tier 無 Full PoC。S30 cross-verify 補上 Saturation(第四 Golden Signal,leading indicator)。|
| 26 | Bloom Filter & Gossip | 🟢 | — | S30。5 chunk 全過 at interview depth。Bloom:燈泡/蓋章比喻打通機制,親手踩 false positive 陷阱(全亮≠一定在,hash 碰撞重疊),DB 當最終裁判。空間 8GB→1.2GB 省85%。落地 local/RedisBloom/SSTable 內建三放法+快取穿透應用。Gossip:八卦接力擴散 O(N²)→O(log N)回合,隨機挑 peer 抗分區,去中心化無 SPOF。共同哲學「近似/最終換效率」自己抽不出但兩實例講全。Interview Drill「爬蟲 100億 URL 去重」5/6,自己把 local Bloom 同步問題連到 Gossip(零提示)。理論日 Discussion tier。**S34**: Bloom+Cache 組合(S33 點名模糊)重講打通 — Bloom 位置/cache 為何擋不住/no false negative 為何敢擋/bit 機制全自己講出,Feynman PASS。|
| — | Multi-Region Session Store (design) | 🟢 | **Phase 2 Gate ✅** | S31. Transfer 題(沒設計過)。自組 home-region + Redis(TTL self-heal) + geo-routing + fetch-on-miss；中途改需求(US region 掛)→ 自戳設計洞(無 source of truth=被登出)→ async 複製到 backup(replication lag=資料遺失窗口)+ AP 選擇。Operational: P99 + replication lag。5/6 PASS。弱點: 答太精簡靠追問 + 兩次主動要提示。|
| 27-28 | URL Shortener | 🟢 | — | S32 設計 + S33 地基 + **S34 Interview Drill 8/9 PASS** + **S35 Full PoC 全綠**。capacity 反推學會 62≈2⁶、counter+base62 主動講足 trade-off、NoSQL access-pattern 理由、讀路徑擺對 Bloom、三次被質疑自修正、KGS range allocation。**S35 PoC**:`projects/day28-url-shortener/main.go` 跑 50 萬碼 0 碰撞 + `-race` 零警告 + 失敗注入丟空洞號仍 0 碰撞,把設計從「我相信」變「程式證明」。盲點:operational 監控仍是真實 Drill 中要證明的習慣。|
| 29-30 | Unique ID Generator | 🟢 | — | S36 設計+理論。從 KGS 橋接,**自己推出** Snowflake 三段(machineID/seq/timestamp)+ timestamp 放最高位(日期格式比喻)+ clock skew 機制(倒退→重入毫秒→seq 歸零→撞號,拒發>等)+ machineID 開機協調一次(ZooKeeper 不變瓶頸)+ 四路線光譜(協調越少越 scale)+ KGS vs Snowflake(集中產值=短 vs 本地算=可排序)。理論一次過幾乎沒卡。PoC(bit packing + clock skew 偵測)park 到 Day 30。Drill ~4/7:operational/capacity 仍弱。|
| 31-32 | Distributed Rate Limiter | 🟢 | — | S38 設計/理論。全鏈自推:100 台孤島→N×limit=10k→共享 Redis counter→race condition(搶票比喻)→單執行緒 DECR 原子性→TTL 過期(Fixed Window)→邊界 2 倍破綻→sliding window→多步 race→Lua 收口。主軸 atomicity(單一命令 vs Lua 捆多步)。🌟 收尾 One-Liner 主動綁結論+論證(頭號弱點突破)+自抽「主動 vs 被動」心法。**Interview Drill + PoC 未做(概念日,放慢略過)→ Gauntlet 補 rate limiter bar-raiser + capacity。** |
| 33-34 | Notification System | ⬜ | — | |
| 35-37 | Chat System | ⬜ | — | |
| 38-39 | Distributed Cache | ⬜ | — | |
| 40-42 | News Feed | ⬜ | — | |
| 43-45 | Payment System | ⬜ | — | |
| 46-47 | Metrics & Logging | ⬜ | — | |
| 48-49 | Search Autocomplete | ⬜ | — | |
| 50-51 | Web Crawler | ⬜ | — | |
| 52-53 | Proximity Service | ⬜ | — | |
| 54-55 | Ticket Booking / Flash Sale | ⬜ | — | 訓練營補強：高並發庫存一致性 + distributed lock，含 Auction 變體 |
| 56-57 | Top-K / Leaderboard | ⬜ | — | 訓練營補強：Count-Min Sketch（Bloom 的兄弟結構）|
| 58-59 | Ride Matching (Uber) | ⬜ | Phase 3 Gate | Geo capstone：matching + dispatch + 狀態機，含 Delivery/Tinder 變體 |
| 60-61 | Trade-off Deep Dive | ⬜ | — | |
| 62-63 | Brownfield / Legacy Migration | ⬜ | — | skill 新版新增：Strangler Fig、dual-write、cutover/rollback |
| 64-65 | Mock Interview Round 1 | ⬜ | — | |
| 66-67 | Weak Spot Reinforcement | ⬜ | — | |
| 68-69 | Final Mock (Brutal) | ⬜ | Phase 4 Gate | |

---

## Interview Drill Scorecard History

| Session | Day | Topic | Score | Details |
|---------|-----|-------|-------|---------|
| 8 | 8-9 | Database Selection | 2/3 | ❌ Scope Negotiation, initially chose NoSQL based on data volume (wrong reasoning) |
| 10 | WR1 | Weekly Review (DB/LB/Cache) | DB 3/4, LB 1/4, Cache 0/4 | First weekly review. LB 🟢→🟡, Cache 🟢→🔴. 2 mistakes resolved (DNS limits, LSM-tree). |
| 13 | 10 | Message Queue (Interview Drill) | 3/3 | ✅ Think Aloud, ✅ Scope Negotiation, ✅ Used MQ. Needed guidance on requirements framework and idempotency placement. |
| 17 | 12 | API Design (Interview Drill) | 3/3 | ✅ Think Aloud, ✅ Scope Negotiation, ✅ Used API Design. Fixed endpoint mistakes mid-drill. Strong idempotency deep dive. |
| 18 | WR2 | Weekly Review (API/Cache/MQ) — Mistake Review | 8 resolved | Single-session record. API Design 5 + MQ 3 mistakes fixed. Found notes-gap pattern (Scale Trigger / DevOps Angle missing from API Design notes). |
| 24 | Gate | **Phase 1 Gate** — Distributed Cache design (problem-anchored) | **3/3 ✅ PASS** | ✅ Think Aloud, ✅ Scope Negotiation, ✅ Used building block. 自己推出 stampede + cascading failure (Phase 2 級反應)。Improvement: clarify 時更早明確圈定範圍。Gate crashed on attempt 1. |
| 25 | WR3 | Weekly Review (Caching/LB/CAP) | Caching 3.5/5, LB 4/5, CAP 3/5 | Caching 🔴→🟡 (補 invalidation), LB 🟡→🟢 (Weighted RR 老錯 resolved). CAP 本週剛學已衰退 (英文字母+stampede 術語掉,核心判斷在). |
| 26 | 19 | Consistency Models (Interview Drill) | 4/5 | ✅ Think Aloud, ✅ Scope Negotiation (主動 clarify 開場), ✅ Used spectrum, ✅ Trade-off WHY (老問題改善). ❌ Operational concerns (漏 replication lag 監控收尾). 社群三功能各選對等級。|
| 27 | 21-22 | Replication & Leader Election (Interview Drill) | **5/5 滿分** | 「設計訂單資料層,機器掛掉不掉訂單」。全 5 項過: ✅ Think Aloud, ✅ Scope(收斂 create/read order), ✅ 用 replication+election, ✅ Trade-off WHY(C→sync), ✅ Operational(補回 lag/election 監控,Day 19 弱點收斂). read-after-write 一口氣列三解法無提示。改善點: 選 C 時主動講反面代價(partition 下不了單也賠錢)。|
| 28 | 23-24 | Rate Limiting & Circuit Breaker (Interview Drill) | **5/5 滿分** | 「惡意爬蟲攻擊 API,DB 1000 QPS 上限 vs 50K 攻擊」。全 5 項過: ✅ Think Aloud, ✅ Scope(開場三問+主動提 WAF), ✅ 用 Rate Limiter+Circuit Breaker 雙主角, ✅ Trade-off WHY(global→per-user 被 challenge 後自修正+SW 護硬上限), ✅ Operational(reject數/CB狀態/P99). 改善點: 第一次答常太精簡(「global 一個桶」),被追問才展開,可主動把 why+反面代價一次講完。|
| 29 | 25 | Observability (Interview Drill) | **5/6** | 「單體拆 30 微服務,結帳慢+失敗查不到」。✅ Think Aloud, ✅ Scope(定位≠修復圈得好+問 scale/團隊配合), ✅ 用三支柱+trace-id+P99, 🟡 Trade-off WHY(多半被追問才講), ✅ Operational(sidecar→ELK,整題即 ops), ✅ Hint response(metrics-first + P99 兩個 redirect 都接住自修正). 改善點: 答案太精簡 + drill 中途問面試官「提供不同思路/提示」(S8/S24 握不住球老根:問需求 OK、問答案 NG)。Best: 沒等講完就抓到 tail latency 並調用今天的 P99。|
| 30 | 26 | Bloom Filter & Gossip (Interview Drill) | **5/6** | 「Web Crawler 100億 URL 去重」L2 probing+中途改需求(分散式 50 台 crawler)。✅ Think Aloud, ✅ Scope(問 scale/throughput/write pattern), ✅ 用 Bloom+Gossip 雙主角, ✅ Trade-off WHY(被追兩次但最終講全:Redis 網路 hop+SPOF vs gossip eventual 短暫重複爬,判斷爬蟲可容忍), ❌ Operational(漏監控:重複爬率/實際 FP rate), ✅ Hint response(改需求+SPOF 反將都接住). Best: local Bloom 同步問題零提示連到 Gossip。改善點(老主線在進步): 一次講足「選什麼+為什麼+反面代價」,別等追問,本次只追一次就完整。|
| 31 | Gate | **Phase 2 Gate** — Multi-Region Session Store (transfer) | **5/6 ✅ PASS** | ✅ Think Aloud, ✅ Scope, ✅ 用 Phase 2 零件(consistency/CAP/replication/TTL/AP), 🟡 Trade-off WHY(對但靠追問才展開), ✅ Operational(P99+replication lag,連到資料遺失窗口), ✅ Hint response(US-down 設計洞被 challenge 後自戳自修正). 弱點(頭號主線): 答太精簡 + 兩次主動要提示(本來都會,暖身講過). Best: 自己戳破單一 home-region 在 region 掛掉時的洞。|
| 33 | WR4 | Weekly Review (URL Shortener / Caching / Database + Bloom bonus) | Caching 6/6, Bloom recall restored, DB trap避開 | **Caching** WR1 0/4 → WR4 六維滿分(capacity 盲區當場補)→ 升 🟢。**URL Shortener** base62≠hash 回退再修 + encoding/hashing/encryption 三件套地基。**Bloom** recall 模糊→Feynman PASS。**Database** 避陷阱+一口氣講足選 SQL → 頭號主線弱點本場練成功。意外複習掉 Security 一塊(crypto primitives)。|
| 34 | 27 | URL Shortener (Interview Drill, Phase 3 Bar Raiser) | **8/9 ✅ PASS** | ✅ Think Aloud, ✅ Scope, ✅ 用 Bloom+cache(自己擺對讀路徑), ✅ Trade-off WHY(counter 取捨+NoSQL access-pattern 主動講足=R3), ❌ Operational(全程沒主動提監控,S29/S30 重複盲點), ✅ Failure modes(Redis durability+counter SPOF), ✅ Capacity(學會 62≈2⁶,6碼=640億), ✅ Hint response(Redis→cache/LB歸位/6vs7 三次自修正), ✅ Time/breadth(4步走完). Best: 被質疑「Redis當DB」自己想起重啟掉資料改 cache + 今天打通的 Bloom 自己擺進讀路徑。改善: operational 監控當固定收尾;讀路徑/LB/DB 仍被追問才展開。|
| 36 | 29 | Unique ID Generator (Interview Drill, bar-raiser 首場) | **~4/7（練習,未達 Phase3 線）** | ✅ Think Aloud, ✅ Scope(**主動想到 enumeration 洩漏營業額**=architect 級加分), ✅ 用 Snowflake, 🟡 Trade-off WHY(給結論不給論證:DB auto-increment 一句帶過、「Snowflake 最適合」沒論證,被追問才展開), 🟡 Failure modes(SPOF 有提,clock skew 沒主動帶進設計), ❌ Operational(第4次監控掛蛋), ❌ Capacity(「直接放棄」,拆 1024×4 後才跟上). Best: enumeration 洩漏觀點零提示自己冒出。改善: 結論要附論證、收尾固定提監控、capacity 別被 2^n 嚇退。本場啟動 bar-raiser 加壓模式。|

---

## 🔴 Mistake Registry

| Session | Day | Topic | Mistake | Status |
|---------|-----|-------|---------|--------|
| 4 | 4-5 | Load Balancer | Said "least robin" — confused RR and Least Connections names | ❌ Unresolved |
| 4 | 4-5 | Load Balancer | Thought Weighted RR is for different request processing times (it's for different server specs) | ✅ Resolved (WR3-S25, 答對「新舊機混用→Weighted」) |
| 4 | 4-5 | Load Balancer | Couldn't recall LB algorithm names during Simon Drill | ✅ Resolved (WR3-S25, 補回 RR+Least Connections 5 演算法表) |
| 4 | 4-5 | Load Balancer | Forgot DNS-based LB limitations (TTL stale IP, no real-time health check) | ✅ Resolved (WR1) |
| 4 | 4-5 | Load Balancer | Thought 8.8.8.8 is ISP DNS (it's Google Public DNS) | ❌ Unresolved |
| 4 | 4-5 | Load Balancer | Confused sticky sessions and Redis external store as same approach (opposite strategies) | ❌ Unresolved |
| 4 | 4-5 | Load Balancer | Missed sticky session risk: uneven load distribution | ❌ Unresolved |
| 9 | 8-9 | Database Selection | LSM-tree 讀寫搞反（以為是 read-optimized） | ✅ Resolved (WR1) |
| 9 | 8-9 | Database Selection | Denormalization 跟 Normalization 搞混 | ✅ Resolved (S11) |
| 9 | 8-9 | Database Selection | Consistency Trade-offs 空白（不知道三種 model） | ✅ Resolved (S26 Day 19, Strong/Causal/RYW/Eventual 光譜全建立) |
| 9 | 8-9 | Database Selection | 看到「大量資料」就選 NoSQL（data volume ≠ DB 選擇關鍵） | ✅ Resolved (S11) |
| 9 | 8-9 | Database Selection | Interview Drill 忘了 Scope Negotiation | ❌ Unresolved |
| 12 | 10 | Message Queue | Simon Drill: Why Async 只記得 fast response，漏 decoupling/buffering | ✅ Resolved (WR2-S18) |
| 12 | 10 | Message Queue | Simon Drill: delivery semantics 名稱講不完整 (most/least/excely) | ✅ Resolved (WR2-S18) |
| 12 | 10 | Message Queue | 設計練習不知道怎麼起手（需要拆成小問題逐步推） | ❌ Unresolved |
| 13 | 10 | Message Queue | 忘了 Functional / Non-Functional / Scope 的定義（Step 1 基礎） | ✅ Resolved (WR2-S18) |
| 13 | 10 | Message Queue | Inventory check 放 Queue 之後（沒考慮 user 等半天才知道沒貨的體驗） | ✅ Resolved (S14) |
| 13 | 10 | Message Queue | 把 Idempotency 當獨立 service（其實是 Order Service 裡的邏輯） | ❌ Unresolved |
| 13 | 10 | Message Queue | 把 Redis DECR（庫存 pre-check）跟 Idempotency check（防重複）搞混 | ❌ Unresolved |
| 13 | 10 | Message Queue | 說 at-least-once 是解決重複扣款的方法（at-least-once 是問題來源，idempotency 才是解法） | ✅ Resolved (S14) |
| 15 | 12 | API Design | gRPC recall 只說 "for service to service"，說不出 WHY（binary fast + strict contract） | ✅ Resolved (WR2) |
| 15 | 12 | API Design | GraphQL transfer 只說「可以用」沒解釋 HOW（client 寫 query 選 fields，burden 從 backend 移到 client） | ❌ Unresolved |
| 16 | 12 | API Design | Simon Drill: Pagination 完全忘記（Offset vs Cursor） | ✅ Resolved (WR2-S18) |
| 16 | 12 | API Design | Versioning 說「修改不需要新版本」，但 rename field 是 breaking change | ❌ Unresolved |
| 16 | 12 | API Design | Observability: 又把 SLI/SLO/Dashboard 當成 metrics（正確是 Latency, Error rate, Throughput） | ✅ Resolved (WR2-S18) |
| 16 | 12 | API Design | Interview Drill: REST endpoint 寫 `/v1/get/restaurants`，verb 塞進 URL（正確：`GET /v1/restaurants`） | ✅ Resolved (S17) |
| 17 | 12 | API Design | 不知道 GET data 放 URL (query string)、POST data 放 request body | ✅ Resolved (WR2-S18) |
| 17 | 12 | API Design | REST path 用 singular noun + path param 寫成字面文字 | ✅ Resolved (S17, 當場修正) |
| 17 | 12 | API Design | Price/user_id 放 request body（沒想過 client 可以竄改） | ✅ Resolved (WR2-S18) |
| 17 | 12 | API Design | Pagination 說成 "offline"（正確: offset），cursor 也靠提示才想起 | ✅ Resolved (WR2-S18) |
| 17 | 12 | API Design | Idempotency record 只想到 exists/not exists，沒想到需要 processing 中間狀態 | ✅ Resolved (WR2-S18) |
| 20 | 14 | Security (JWT vs Session) | Scenario A trade-off 用「more mantion more infra」這種抽象詞，沒拆成 HA/failover/monitoring/backup | ✅ Resolved (S20, English Polish 補強) |
| 20 | 14 | Security (JWT vs Session) | Scenario B 直接跳到答案 (Hybrid)，沒先論證為什麼 base 是 JWT 不是 Session — WR2 老問題 (WHAT 知道 WHY 跳過) 重現 | ✅ Resolved (S20, 補上 centralized state 的 WHY) |
| 20 | 14 | Security (OAuth) | Q2「為什麼 Auth Server 跟 Resource Server 要分開」答「不同 api」— 描述現象沒講 blast radius separation | ✅ Resolved (S21) |
| 20 | 14 | Security (OAuth) | Q3「三個 disaster 對應 OAuth 解法」跳過沒答 — 還沒建立「設計每元件對應一個痛點」的對照感 | ✅ Resolved (S21) |
| 24 | 17-18 | Distributed Cache / CAP | 不清楚 network partition 是什麼（把「node 死」和「node 失聯但都活著」混為一談） | ✅ Resolved (S24, 當場補：partition = 都活著但網路斷、各自收 request) |
| 24 | 17-18 | Distributed Cache | client-side vs proxy routing 答「不確定」— 缺「開放題=trade-off 取捨、沒有對錯」的反射 | ❌ Unresolved |
| 24 | 17-18 | Distributed Cache | Clarify 時偏向「問 AI 要答案」而非主動斷言並圈定 scope（S8 Scope Negotiation 老問題變體） | 🟡 Improving (S26 Day 19 drill 主動 clarify 開場,但問的是容量題非一致性核心) |
| 26 | 19 | Consistency | CAP recall 說平時「拿到 CAP 三個」— P 不是選項,是「網路會不會斷」的物理事實,平時拿到的是 C+A | ✅ Resolved (S31 暖身,明確答出「平常 C+A,只有 partition 才選 AP/CP」) |
| 26 | 19 | Consistency | 一開始推不出「instant/strong consistency 要付什麼代價」— 缺「同步=等待=慢」因果鏈 | ✅ Resolved (S26, 白板比喻當場通,後續自己推出) |
| 26 | 19 | Consistency | Quorum W+R>N 不懂為何保證讀到最新(卡兩次) | ✅ Resolved (S26, 杯子/位子鴿籠比喻+填空打通「重疊」) |
| 27 | 21-22 | Replication | Gate「為何 single-leader 免解衝突」答成「leader 是 bottleneck」— 把缺點誤當成原因,沒抓到「唯一 ordering」才是答案 | ✅ Resolved (S27, 用 Tokyo/London 同時寫比喻打通,後續自己遷移到設計題) |
| 28 | 23-24 | Rate Limiting | 不清楚 lazy 是什麼 — 沒有 lazy/eager(敲門才算 vs 背景一直算)這組 CS 概念 | ✅ Resolved (S28, 集點卡比喻+「成本跟流量走不跟桶數走」打通,後續 drill 自己答出 N×limit) |
| 28 | 23-24 | Rate Limiting | Interview Drill 選 global 一個桶 — 只想「保護 DB」漏「公平性」,沒想到爬蟲會吸乾全局桶餓死正常 user | ✅ Resolved (S28, 被 challenge 後自己推到 per-user+global 兩層) |
| 28 | 23-24 | Circuit Breaker | 概念懂但講不出三狀態術語名 (Closed/Open/Half-Open) | ✅ Resolved (S28, 補上術語對照表,白話對應正式名稱) |
| 29 | 25 | Observability | 追蹤請求路徑想用 traceroute (那是 L3 追路由器;追請求跨服務要 distributed tracing 應用層) | ✅ Resolved (S29, 「tracing = 應用層的 traceroute」校準,方向本來就對) |
| 29 | 25 | Observability | Debug 動線先看 trace (應先看 metrics 當雷達指方向→trace 定位→log 挖根因) | ✅ Resolved (S29, 補「Metrics 報警→Traces 指路→Logs 挖根因」口訣) |
| 29 | 19 | Consistency (review) | 複習時 recall「consistency = 三個選項(strong/RYW/eventual)」沒抓到是光譜+軸 | ✅ Resolved (S29, 台北/倫敦同步比喻重建「軸=新鮮度 vs 等待成本」,自推出 Strong 慢在等同步) |
| 29 | 25 | Interview habit | Drill 答案太精簡(被追問才展開)+中途問面試官「提供不同思路/提示」要參考答案 | 🟡 Improving (S31 Gate 回升;**S33 WR4 進展(好)**: Database 最後一答無需追問、一口氣 commit SQL+三理由(關聯/join/ACID)。給「四格填空 scaffold」後成功講足 → 主線弱點本場有練到且成功。續逼:第一次開口就講足方案+why+反面代價) |
| 31 | Gate | Session Store (DR) | US region 掛掉時答「EU Redis 可服務」— 忽略 home-region 設計下 EU 根本沒這些 session,且 fetch-from-US 前提是 US 活著 | ✅ Resolved (S31, 被 challenge 一次後自戳:US 死=無 source of truth=被登出,續推 async 複製到 backup) |
| 30 | 26 | Bloom Filter | 查詢「三格全吻合 = 一定在」— 沒抓到 hash 碰撞讓不同元素 bit 重疊,全亮只能推「可能在」 | ✅ Resolved (S30, 親手踩陷阱:牆上只蓋過 evil_user,B 撞到同三格被誤判,當場通) |
| 30 | 26 | Bloom/Gossip | 爬蟲 100億 URL 存不下歸因「訊息量 O(N²)」— 把儲存空間(O(N),~1TB)和節點間廣播訊息(O(N²))兩軸搞混 | ✅ Resolved (S30, 當場校準:這題是 O(N) 空間太大,O(N²) 是 gossip 廣播問題) |
| 30 | 8-9 | Database (review) | LSM-tree 一度忘記 | ✅ Resolved (S30, 1 分鐘喚回 B-tree 讀優化/LSM 寫優化+SSTable 配 Bloom,加回複習排程) |
| 32 | 27 | URL Shortener | 讀寫比從「每天產量」推 | ✅ Resolved (S32, 校準成「一條 URL 一生被讀幾次」= 用戶行為,跟產量無關) |
| 32 | 27 | URL Shortener | hash+salt 再加 counter 來「減少」碰撞（A/B 兩路線混在一起）| ✅ Resolved (S32, counter=「消滅」碰撞非減少;salt 只是 A 撞了之後的重試手段,銀行號碼牌比喻打通) |
| 32 | 27 | URL Shortener | 架構真相來源(②)誤填 redis cache | ✅ Resolved (S32, redis 重啟清空→全站短碼永久 404;真相來源要 durable DB,cache 只是前面擋的) |
| 32 | 27 | Interview habit | 卡住直接喊「提示我」（頭號主線弱點再現）| 🟡 Improving (S32, 給 thinking scaffold 非答案後成功自己 commit「NoSQL」且用對 access-pattern 理由) |
| 33 | 27 | URL Shortener | 暖身 recall 又把 base62 講成「做 hash」(S32 resolved 後 2 天回退) | ✅ Resolved (S33 WR4, 進制轉換 hex/`#FF0000` 比喻 + encoding/hashing/encryption 三件套對照表;碰撞判斷本身答對只是名詞滑掉) |
| 33 | 14 | Security (encoding vs encryption) | 以為 base64 是「加密但被破解」所以人人能回推 | ✅ Resolved (S33 WR4, 摩斯密碼比喻:encoding 可逆是「設計」非「漏洞」,從不是拿來保密;三件套表釐清 encoding/hashing/encryption) |
| 33 | 14 | Security (password storage) | 存密碼答 encryption (業界正解 = salted slow hash) | ✅ Resolved (S33 WR4, 自推「只需驗證、永遠不需還原原始密碼 → 不可逆才是安全特性」;補 salt 防 rainbow table + bcrypt/argon2 慢 hash) |
| 33 | 6-7 | Caching (capacity) | cache 容量完全不會估(盲區) | ✅ Resolved (S33 WR4, 80/20 法則:不存全部只存熱20%;自己算對 1TB→200GB→256GB headroom,Feynman PASS) |
| 34 | 27 | URL Shortener (read path) | LB 放在 redis 跟 db 中間 | ✅ Resolved (S34, 餐廳帶位員比喻:LB 站最前面 DNS後/API前,邊緣分流) |
| 34 | 27 | URL Shortener (HTTP code) | 短碼不存在回 401 | ✅ Resolved (S34, 401=沒登入/403=沒權限/404=不存在;查無短碼=404) |
| 34 | 27 | URL Shortener (storage) | Redis 當 source of truth(S32 老錯回退) | ✅ Resolved (S34, 被質疑「半夜 Redis 重啟」自己想起掉資料→改 cache + durable DB 當真相來源) |
| 34 | 27 | Capacity estimation | 算不出 62ⁿ(預設背「7 碼」) | ✅ Resolved (S34, 學會 62≈2⁶ + 2³⁰≈10億 估算錨;算出 6 碼=640億已是需求10倍) |
| 34 | 27 | URL Shortener (KGS) | 配號器去哪領範圍/機器掛掉剩號碼怎辦(知識邊界,沒想過) | ✅ Resolved (S34, 中央配號器每 block 領一次非 per-request;掛掉剩號丟掉=空洞=OK,短碼不需連續) |
| 34 | 27 | Interview habit (operational) | Drill 全程沒主動提監控(S29/S30 重複盲點) | 🟡 Improving (S35 PoC 收尾主動建監控表+講 batching trade-off,但漏「不領block→KGS瓶頸」由我補;真實 Drill 主動提監控仍待證明,維持固定要求) |
| 35 | 28 | URL Shortener (base62) | base62 把「長網址」encoding 成固定長度(S34 resolved 後 2 天回退) | ✅ Resolved (S35, 拆 POST 四步流程:base62 輸入是 counter 數字,長網址原封不動存 DB 當 value;counter 負責唯一,base62 只換進制) |
| 35 | 28 | URL Shortener (code length) | 以為短碼要「固定 7 位數」 | ✅ Resolved (S35, 碼自然長大不補0;「7」是命名空間天花板 62⁷ 非固定長度;補0 浪費+洩漏發號量。PoC 長度分布實證:1碼62個→4碼數十萬) |
| 35 | 28 | Go (string/byte) | 以為 `s[i]` 拿到字串(Python 思維) | ✅ Resolved (S35, 親手跑 alphabet[1]=49 vs string(alphabet[1])="1";Go string=byte 序列,抓一格=byte 編號) |
| 35 | 28 | KGS (operational) | 以為丟掉 1 萬個空洞號是 bug 要修 | 🟡 Partial (S35, 答對「命名空間大丟得起」但漏「不領block→KGS 變瓶頸+每碼多一次 round-trip」的 batching 代價,由我補) |
| 36 | 29 | Unique ID | 「不准中央配號」→ 想「每台有自己的區間範圍」(區間誰分?又需中央+會用完+重疊) | ✅ Resolved (S36, 跳到「切身分非切號碼空間」:把 machineID 揉進 ID,每台自己算) |
| 36 | 29 | Unique ID | 防撞反射想用 hash(machine 名) | ✅ Resolved (S36, hash 只「大概不撞」;直接給門牌號 machineID=保證不撞,同 Day27 counter≠hash) |
| 36 | 29 | Unique ID (bit order) | Transfer 卡:timestamp 放哪位無所謂 | ✅ Resolved (S36, 日期格式 `2026-06-28` vs `28-06-2026` 比喻打通「排序由最高位主宰」,放錯→丟 time-ordering→DB index 退化) |
| 36 | 29 | Unique ID (clock skew) | 時鐘倒退「只覺得很危險」講不出機制 | ✅ Resolved (S36, 具體數字走「倒退→重入毫秒→seq 歸零→重發已發號=撞號」;解法拒發>等) |
| 36 | 29 | Interview habit (trade-off) | Drill 給結論不給論證(「Snowflake 最適合」/ DB auto-increment 一句帶過) | 🟡 Improving (S36, 啟動 bar-raiser 加壓;被追問後能補足 DB SPOF + Snowflake 機制,但仍未做到第一次開口就附論證) |
| 36 | 29 | Interview habit (operational) | Drill 全程沒主動提監控(第4次重複) | ❌ Unresolved (S29/30/34/36;固定要求:設計收尾必加監控句=clock skew alert+發號QPS+sequence打滿率) |
| 36 | 29 | Capacity estimation | 算 2^12/秒「直接放棄」 | 🟡 Improving (S36, 拆 `1024×4×1000≈400萬/秒` 後跟上;非真不會,是被 2^n 寫法嚇退,固定提醒拆次方) |
| 38 | 31 | Rate Limiter (counter reset) | counter 扣到 0 後想用 INCR「手動補回去」 | ✅ Resolved (S38, 改用 TTL 被動過期:key 塞當前分鐘+EXPIRE 60s,每分鐘天生新 key,舊的自燒;學生自抽「主動 vs 被動」心法) |
| 38 | 31 | Interview habit (commit) | 中段「使用一個統一的限流器**嗎**?」用問句把球丟回 AI(不敢 commit + 沒說哪一層) | 🟡 Improving (S38 頭號主線**當場突破**:收尾 One-Liner 主動把「選 sliding window + 因為往回算」結論+論證綁一起講,沒等追問;續逼第一次開口就講足) |

---

## 🎯 One-Liner Library (Interview Quick-Answer Bank)

| Topic | One-Liner |
|-------|-----------|
| Load Balancer | A Load Balancer distributes traffic across multiple backend servers to achieve high availability, horizontal scalability, and zero-downtime deployments. |
| Caching & CDN | Cache puts frequently-used data in a faster store like Redis in front of the DB, reducing latency and DB load by serving most requests without hitting the database. |
| Database Selection | Database selection is choosing the right storage engine — SQL, NoSQL, or NewSQL — based on access patterns, relationship complexity, and consistency requirements, so the database fits the workload rather than forcing the workload to fit the database. |
| Message Queue | A Message Queue decouples producers from consumers, enabling async processing, peak traffic buffering, and failure resilience through retry and dead letter queues — the key is pairing at-least-once delivery with idempotency to prevent duplicate processing. |
| API Design | API Design is about choosing the right style (REST, GraphQL, gRPC) based on who's calling, call frequency, and data complexity — the key trade-off is flexibility versus simplicity and cacheability. |
| Security & Auth | Security in distributed systems means separating what can issue credentials from what can consume them — OAuth solves password-sharing disasters by introducing scoped, revocable access tokens exchanged through a trusted server-to-server flow. |
| Consistent Hashing | Consistent hashing maps both keys and nodes onto a ring, so adding or removing a node only remaps about 1/N of the keys instead of nearly all — and virtual nodes keep the load evenly spread. |
| Distributed Cache | A distributed cache spreads data across multiple nodes using consistent hashing to route keys, with replicas for availability — the key trade-off is favoring AP over CP, because the DB is the source of truth and TTL makes staleness self-healing. |
| CAP Theorem | CAP isn't "pick 2 of 3" — without a partition you get both C and A; CAP only forces a choice during a partition: stay consistent (refuse stale answers) or stay available (serve possibly-stale), and the choice can be made per-feature. |
| Replication & Leader Election | Replication stores data on multiple nodes to survive hardware failure; the key design question is who accepts writes — a single leader gives one total ordering so conflicts are impossible, while multi-leader/leaderless buys write availability at the cost of conflict resolution, and leader election uses majority quorum to prevent split-brain. |
| Consistency Models | Consistency is a spectrum, not on/off — a latency budget from Strong (everyone always sees the latest, most expensive) to Eventual (stale now but guaranteed to converge, cheapest); you tune it with quorums (W+R>N forces read/write overlap) and pick per-operation by how much staleness the business tolerates. |
| Rate Limiting & Circuit Breaker | Rate limiting protects the backend and ensures fairness — Token Bucket allows bursts while Sliding Window strictly caps, and you layer per-user limits for fairness plus a global cap to protect downstream; a Circuit Breaker complements it on outbound calls by failing fast when a dependency is down (Closed→Open→Half-Open) to prevent cascading failure. |
| Observability | Observability answers three different questions with three pillars — Metrics (how much / which service is unhealthy), Logs (what happened / why), and Traces (where / which hop in the request is slow) — stitched together by a correlation ID so a single request's journey across services forms one timeline, letting you localize problems across thousands of nodes without ssh-ing into any of them. |
| Bloom Filter | A Bloom filter is a space-efficient, hash-based membership test that answers "definitely not in" or "probably in" — it trades a small false-positive rate (from hash collisions) for huge space savings (≈85% vs exact storage), with the database as the source of truth for any "probably" hit. |
| Gossip Protocol | Gossip is a decentralized way for nodes to share state — each node periodically tells a few random peers, so information spreads exponentially and converges in O(log N) rounds with no central master to become a single point of failure; the trade-off is eventual rather than instant consistency. |
| Multi-Region Session Store | A multi-region session store keeps each user's small KV session in their home region (Redis + TTL for self-healing staleness) and routes via geo-DNS, fetching on miss; for region-failure DR it async-replicates sessions to a backup region — an AP choice that accepts a few seconds of replication lag because a stale session is fine but logging out 100M users is not. |
| URL Shortener | A URL shortener is an extremely read-heavy key-value system; short codes are generated collision-free by base62-encoding a globally unique counter (not by hashing), stored in a NoSQL KV store for simple point lookups, and served through a cache that needs no invalidation because the mapping is immutable. |
| Cache vs Queue | Cache solves a read problem (same data read many times, serve it fast, losing it is fine because the DB is source of truth); Queue solves a work-handoff problem (decouple producer from consumer, each message consumed once, losing it is bad because the work may have no backup). Both often run on Redis but use different structures and have opposite durability needs. |
| Cache Penetration (Bloom + Cache) | Cache penetration is a flood of queries for keys that don't exist — the cache only stores real keys, so every such request misses and crushes the DB; a Bloom filter in front rejects definitely-absent keys safely, because it has no false negatives (a real key is never wrongly blocked) and the worst case is a rare false positive that just wastes one lookup. |
| Unique ID Generator (Snowflake) | A unique ID generator produces globally unique IDs with no per-ID coordination; Snowflake packs a timestamp + machineID + sequence into a 64-bit number — collision-free and roughly time-sortable at millions/sec per node, coordinating only once at boot to assign machine IDs. It beats UUID (long, unsortable), DB auto-increment (single-point bottleneck + SPOF), and KGS (centralized) — the catch is clock skew: if the clock rewinds, a node can re-issue an ID, so on detected rewind it must refuse rather than risk a duplicate. |
| Distributed Rate Limiter | A distributed rate limiter keeps each user's counter in a shared store like Redis (local per-node counters would let a user get N×limit across N servers). The hard part is concurrency, not counting: multiple servers racing on read-modify-write cause over-admission, so check-and-update must be atomic — a single atomic command (DECR/INCR) for a simple counter, or a Lua script when the logic is multi-step. Counters reset by passive TTL expiry (not an active refill job), and the algorithm is a sliding window over a fixed window to close the 2× boundary-burst hole. |

---

## RPG Profile

| Field | Value |
|-------|-------|
| **Title** | 🏗️ Staff Architect |
| **Current streak** | 3 週 🔥 (連續活躍週：S31 / S32-S36 / 本週 S37-S38,同週不加碼) |
| **Longest streak** | 4 (days, pre-weekly) |
| **Last session date** | 2026-07-03 (S38, Day 31 Distributed Rate Limiter) |
| **Last story summary** | Session 38（跨機器接續）。Day 31 Distributed Rate Limiter。Karen 要開放第三方 API,Max 想「加個 rate limiter 就收工」。學生從 Rate Limiting 暖身一路**自己推完整條鏈**:100 台各跑各的 = 100 座孤島 → 惡意 user 實際打 N×limit=10,000 → 共享 counter 放 Redis(選對「共享計數器」非「一台限流機器」=SPOF)→ 搶票超賣比喻打通 race condition → 學生自己跳到 Redis 單執行緒 DECR 原子性 → 「讓 key 自己 TTL 過期」取代「派 job 手動補」(自抽主動 vs 被動心法)→ 抓到 Fixed Window 邊界 2 倍破綻 → sliding window「往回看 60 秒」補洞 → 多步 race 重演 → Lua 把多步捆成原子收口。全天主軸就一個字:atomicity。🌟 收尾 One-Liner 主動把「選 sliding window + 因為往回算」結論與論證綁一起講,頭號主線弱點(結論不給論證,execution-heavy 首攻目標)當場突破一次。教訓在我這邊:中段塞太多害學生 3 次卡住,退小步+具象比喻後全通。|

---

## Achievements

| ID | Name | Status | Date |
|----|------|--------|------|
| M1 | First Steps | 🏆 | retroactive |
| M2 | Framework Forged | 🏆 | retroactive |
| C1 | First Blood | 🏆 | retroactive |
| C4 | Comeback Kid | 🏆 | retroactive |
| S2 | Weekly Warrior | 🏆 | retroactive |
| E1 | Perfect Drill | 🏆 | 2026-04-02 |
| S1 | Three-peat | 🏆 | 2026-04-02 |
| K4 | Bug Squasher ×5 | 🏆 | 2026-04-10 |
| M3 | Builder's Foundation | 🏆 | 2026-05-29 (Pass Phase 1 Gate) |
| C3 | Gate Crasher | 🏆 | 2026-05-29 (Phase 1 Gate, attempt 1) |
| K1 | One-Liner ×10 | 🏆 | 2026-06-03 (S26, Consistency Models 補上第 10 條) |
| C5 | Myth Buster | 🏆 | 2026-06-16 (S30, cross-verify 找出 Observability 漏掉 Saturation) |
| R1 | Max's Nightmare | 🏆 | 2026-06-16 (S30, 解釋 Max「全量廣播」為何 O(N²) 不 scale) |
| M4 | Distributed Mind | 🏆 | 2026-06-18 (S31, Pass Phase 2 Gate — 分散式思維覺醒) |
| R2 | Karen's Hero | 🏆 | 2026-06-24 (S33 記功 — Day 27 URL Shortener Phase 3 設計完成 = 達成 Karen 可追蹤短網址需求) |
| R3 | 小球's Pride | 🏆 | 2026-06-26 (S34 Drill — 被問生碼方式時主動補上 counter+base62 的 trade-off,未經 prompt 的 architect 思維) |

**Total: 16/25**

---

## Review Schedule (Spaced Repetition)

> Box 1 → next day | Box 2 → 3 days | Box 3 → 7 days | Box 4 → 14 days → retired

| Topic | Box | Next Review |
|-------|-----|-------------|
| Security & Auth | 2 | 2026-06-27 (S33 WR4 測了 crypto-primitives slice: encoding/hashing/encryption + 密碼存法 PASS;但 OAuth/JWT/session 廣度未測 → Box 維持 2,下次補 full recall) |
| Consistent Hashing | 2 | 2026-06-05 |
| Distributed Cache + CAP | 3 | 2026-06-25 (S31 暖身 recall PASS「平常 C+A,只有 partition 才選 AP/CP」,CAP misconception 收掉,Box 2→3) |
| Multi-Region Session Store (design) | 1 | 2026-06-19 (S31 Gate,新 design pattern,Box 1) |
| Caching & CDN | 3 | 2026-07-01 (S33 WR4 六維度全收 zero退化 + 補 capacity 盲區,Box 2→3) |
| Load Balancer | 2 | 2026-06-05 (WR3 recall 4/5 pass, Box 1→2) |
| Consistency Models | 2 | 2026-06-21 (S31 暖身 recall PASS「光譜+等同步 trade-off」無需 scaffolding,Box 1→2) |
| Replication & Leader Election | 2 | 2026-06-19 (S30 recall PASS「read replica≠strong 因 replication lag」,Box 1→2) |
| Rate Limiting & Circuit Breaker | 2 | 2026-07-06 (S38 failure-timeline PASS: 本地計數 N×limit 冷推出,Box 1→2;但 one-liner 機制層掉,下次補測) |
| Observability | 1 | 2026-06-16 (S29 新學,Box 1, overdue) |
| Bloom Filter & Gossip | 3 | 2026-07-03 (S34 Bloom+Cache 組合重講 Feynman PASS,no false negative/bit 機制自講,Box 2→3) |
| Database (B-tree/LSM) | 1 | 2026-06-17 (S30 LSM 一度遺忘→喚回,backfill Box 1;S33 測的是 selection 軸非 LSM 內部,此項仍欠) |
| URL Shortener (design) | 3 | 2026-07-03 (S34 Day 27 Drill 8/9,整套設計實戰過一遍,Box 2→3) |
| Distributed Rate Limiter (design) | 1 | 2026-07-04 (S38 新學,Box 1) |

---

## Curiosity Branches

| Topic | Question | Status |
|-------|----------|--------|
| Message Queue | Long polling in MQ (長輪詢) | ⏸ Parked (likely relevant at Day 33-34 Notification System) |
| Observability | Trace/log sampling (head-based vs tail-based) + metrics high-cardinality 解法 | ⏸ Parked (深度天花板,面試不問細節。Follow-up preview 已預告,Day 31-32/46-47 可拉) |
| Observability | Sidecar 本身掛了/拖慢主服務 → observability 自身可靠性與資源隔離 | ⏸ Parked (Drill follow-up 預告,下次可帶) |

---

## Phase Gate Results

| Phase | Date | Score | Result | Weak spots |
|-------|------|-------|--------|------------|
| Phase 0 | — | — | ✅ Pass (retroactive — completed Day 1-3) | |
| Phase 1 | 2026-05-29 | 3/3 | ✅ Pass (attempt 1) — Distributed Cache design (problem-anchored mini-mock) | clarify 時更早明確圈定 scope |
| Phase 2 | 2026-06-18 | 5/6 | ✅ Pass (attempt 1) — Multi-Region Session Store (transfer mock, 中途改需求 US region 掛) | 答太精簡靠追問才展開 + 兩次主動要提示(獨立 drive 不足) |
