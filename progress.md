# Student Progress Tracking

> This file is the single source of truth for student progress.
> Updated by Claude at the end of every session (Step H) and when sessions are interrupted.
> Read by Claude at the start of every session to determine where to resume.

---

## Student Info

| Field | Value |
|-------|-------|
| **Start date** | 2026-03-04 |
| **Current phase** | Phase 3 🏗️ |
| **Current day** | **WR4 完成 (S33)** → 下一步 = Day 27 Interview Drill + Day 28 Full PoC（仍 pending）|
| **Language mode** | Bilingual — S27 切回繁中為主（學生英文閱讀疲勞），術語保留英文 |
| **Session count** | 33 |
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

---

## Current Session (Breakpoint)

✅ **Session 33 = Weekly Review #4 完成（gap-mode 工作空擋，內容很滿）。** 3 主題 + 1 bonus：
- **URL Shortener**：暖身時 base62 又黏回「hash」(S32 resolved 後 2 天回退)→ 用進制轉換(hex/`#FF0000`)比喻 + encoding/hashing/encryption 三件套表打通。意外挖出深層誤解「base64 是加密被破解所以可回推」→ 校準 encoding≠encryption(摩斯密碼:可逆是設計非漏洞)。延伸到密碼存法：學生答 encryption→自推「只需驗證不需還原→不可逆才安全」→ 正解 salted slow hash(bcrypt/argon2)。
- **Caching**：六維度全收。scale trigger/trade-off/invalidation(寫時刪口訣 zero-退化)/DevOps(hit rate)/failure modes(補成 stampede+penetration+avalanche 三件套)全穩；**capacity 是真盲區→補 80/20 法則**(只存熱20%,自算 1TB→200GB→256GB Feynman PASS)。**最弱主題(WR1 0/4)打成滿分 → 升 🟢。**
- **Bloom Filter**(bonus,學生主動要求複習,逾期)：recall 一開始模糊(只記用途+insert 蓋 bit)→ 8格牆走查詢+假陽性→ Feynman PASS「靠 no-false-negative 才敢安全擋掉『一定不在』」。connect 到 cache penetration。
- **Database**(狙擊老毛病)：避開「資料量大→NoSQL」陷阱,抓到 relationship/join;最後一答**一口氣講足**選 SQL+三理由(關聯/join/ACID)→**頭號主線弱點本場練成功**。

**Next session 兩個選項（工作空擋學，挑短的先做）：**
1. Day 27 Interview Drill（當面試官完整講一遍，練口條 + 頭號弱點：第一次開口講足方案+why+代價）
2. Day 28 Full PoC（Go：base62 編碼 + KGS 發號）

**Pending PoC(park):** Circuit Breaker PoC + 分散式 Redis rate limiter → Day 31-32。Replication lag + Consistent hashing 獨立 PoC + distributed cache 完整實作 → Day 38-39。

**Pending review(下次帶到):**
- **⭐ 學生主動點名(S33 結束時)：Bloom + Cache 組合仍模糊 → 下次優先重講。** 切入點建議：畫完整 request flow（User → Bloom filter → Cache → DB），走兩條路徑 — (1) happy path：key 存在；(2) cache penetration：查不存在的 key。重點釐清 Bloom 在流程哪個「位置」、它擋的是「不存在的 key 打穿 cache 直接砸 DB」、為什麼 cache 自己擋不住（cache miss 也會放行到 DB，Bloom 在 cache 之前先攔）。
- **Review Schedule 仍有多筆逾期**：Consistent Hashing(6/05)/Load Balancer(6/05)/Rate Limiting(6/10)/Observability(6/16)/Database B-tree-LSM(6/17)。WR4 清了 Caching(Box2→3)+Bloom(1→2)+URL Shortener(1→2)+Security 一個 slice。**Security 廣度(OAuth/JWT/session)只測了 crypto-primitives 一塊,full recall 仍欠 → 下次 Step A 帶。**
- **🔴 頭號習慣弱點（S8→S33 主線）**：「答太精簡，被追問才展開」+「主動要提示而非先嘗試」。**S33 進展(好)**：Database 最後一答無需追問、一口氣 commit SQL+三理由 → 主線弱點本場有練到且成功。繼續在 Drill 場景逼「第一次開口就講足方案+why+反面代價」。

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
| 26 | Bloom Filter & Gossip | 🟢 | — | S30。5 chunk 全過 at interview depth。Bloom:燈泡/蓋章比喻打通機制,親手踩 false positive 陷阱(全亮≠一定在,hash 碰撞重疊),DB 當最終裁判。空間 8GB→1.2GB 省85%。落地 local/RedisBloom/SSTable 內建三放法+快取穿透應用。Gossip:八卦接力擴散 O(N²)→O(log N)回合,隨機挑 peer 抗分區,去中心化無 SPOF。共同哲學「近似/最終換效率」自己抽不出但兩實例講全。Interview Drill「爬蟲 100億 URL 去重」5/6,自己把 local Bloom 同步問題連到 Gossip(零提示)。理論日 Discussion tier。|
| — | Multi-Region Session Store (design) | 🟢 | **Phase 2 Gate ✅** | S31. Transfer 題(沒設計過)。自組 home-region + Redis(TTL self-heal) + geo-routing + fetch-on-miss；中途改需求(US region 掛)→ 自戳設計洞(無 source of truth=被登出)→ async 複製到 backup(replication lag=資料遺失窗口)+ AP 選擇。Operational: P99 + replication lag。5/6 PASS。弱點: 答太精簡靠追問 + 兩次主動要提示。|
| 27-28 | URL Shortener | 🟡 | — | S32 Day 27 設計完成。生碼 counter/KGS+base62(設計掉碰撞)、7位、NoSQL KV(access pattern 非 volume)、cache immutable 無 invalidation、async analytics、SPOF+bottleneck→分散式發號。架構圖三路全拼出。**S33 WR4**: base62≠hash 回退已再修(進制轉換比喻)+ 補 encoding/hashing/encryption 三件套地基。Interview Drill + Full PoC(base62+KGS) 仍待 Day 28。|
| 29-30 | Unique ID Generator | ⬜ | — | |
| 31-32 | Distributed Rate Limiter | ⬜ | — | |
| 33-34 | Notification System | ⬜ | — | |
| 35-37 | Chat System | ⬜ | — | |
| 38-39 | Distributed Cache | ⬜ | — | |
| 40-42 | News Feed | ⬜ | — | |
| 43-45 | Payment System | ⬜ | Phase 3 Gate | |
| 46-47 | Metrics & Logging | ⬜ | — | |
| 48-49 | Search Autocomplete | ⬜ | — | |
| 50-51 | Web Crawler | ⬜ | — | |
| 52-53 | Proximity Service | ⬜ | — | |
| 54-55 | Trade-off Deep Dive | ⬜ | — | |
| 56-57 | Mock Interview Round 1 | ⬜ | — | |
| 58-59 | Weak Spot Reinforcement | ⬜ | — | |
| 60-61 | Final Mock (Brutal) | ⬜ | Phase 4 Gate | |

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

---

## RPG Profile

| Field | Value |
|-------|-------|
| **Title** | 🏗️ Staff Architect |
| **Current streak** | 2 週 🔥 (連續活躍週：上週 S31 + 本週 S32-S33,同週不加碼) |
| **Longest streak** | 4 (days, pre-weekly) |
| **Last session date** | 2026-06-24 |
| **Last story summary** | Session 33 = Weekly Review #4。小球帶學生回顧 URL Shortener / Caching / Database。一條「base62 是不是 hash」的小疑問滾出整串底層地基：進制轉換(hex `#FF0000`) → encoding/hashing/encryption 三件套 → 「base64 不是被破解、本來就設計成可逆」→ 密碼該用 salted slow hash 不是 encryption(學生自己推出「只需驗證不需還原 → 不可逆才安全」)。Caching 從歷史最弱(WR1 0/4)打成六維滿分,當場補掉 capacity 80/20 估算盲區。Bloom filter 從模糊 recall 救回,答出「靠 no-false-negative 才敢擋掉一定不在」。最後 Database 老毛病狙擊:學生避開「資料量大→NoSQL」陷阱、一口氣講足選 SQL+三理由 → 頭號主線弱點本場練成功。Karen 的短網址設計正式記功(R2)。|

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

**Total: 15/25**

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
| Rate Limiting & Circuit Breaker | 1 | 2026-06-10 (S28 新學,Box 1, overdue) |
| Observability | 1 | 2026-06-16 (S29 新學,Box 1, overdue) |
| Bloom Filter & Gossip | 2 | 2026-06-27 (S33 WR4 recall 模糊起步→8格牆走查詢+假陽性→Feynman PASS,Box 1→2) |
| Database (B-tree/LSM) | 1 | 2026-06-17 (S30 LSM 一度遺忘→喚回,backfill Box 1;S33 測的是 selection 軸非 LSM 內部,此項仍欠) |
| URL Shortener (design) | 2 | 2026-06-27 (S33 WR4 re-test,base62≠hash 回退已修,Box 1→2) |

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
