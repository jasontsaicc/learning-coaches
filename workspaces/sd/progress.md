# progress

<!-- Engine-owned schema: engine/PROGRESS-SCHEMA.md. Converted 2026-07-10 from the
     standalone system-design-notes progress.md (original verbatim in
     archive/pre-migration/progress.md; entry reconciliation in archive/pre-migration/README.md).
     Session narratives live in session-log.md; coaching playbook in coaching-brief.md;
     strategic plan in curriculum-plan.md; pattern map in pattern-map.md;
     one-liners in one-liner-library.md; RPG state in rpg-state.md.
     Standalone 時期 scorecard/registry 以 session 編號為鍵、多數未記日期;已知日期照填,
     其餘標 (未記日期),不回填猜測。 -->

## Meta

- session_count: 41
- last_weekly_review: 33 — ⚠️ WR5 於 S41 開跑未完成(Topic 1/3),trigger 持續成立,下場續跑;完成時才把本欄更新為當時 session_count
- last_session_date: 2026-07-10
- warm_up_classification: (standalone 時期未記錄;學員已 P3,Step 0 模式預設 Exploration)

## Current Session breakpoint

**S42 中斷存檔(2026-07-11)— WR5 Topic 1/3 已收,Topic 2 未開。** 球 3(3AM page test)無法獨立組裝:填格「無法使用/有立即性」= 危險感沒機制;SLI 標籤撈不出(素材 lag、上次成功時間第一輪就自己講出);逐步導引通了 A 掛→failover→B 無資料→強制重登全鏈後,學生喊「太拖,直接說完」→ 模範答案直接給(2 pages + dead man's switch + ticket 分層 + 3 圖)。Topic 1 計分 1/6(見 scorecard)。

下一場開場順序:
1. One-Liner Challenge 口頭抽考:S41 新句 Session Revocation + 抽 2 條舊句。
2. **3AM page test 複測(直接給的留沒留住)**:換題(URL Shortener 或 Rate Limiter),學生自己跑 page 句型 "Page me when [SLI] > [threshold] for [duration], because [harm]" + page/ticket/dashboard 分層。
3. 續 WR5:Topic 2 Security & Auth(OAuth/JWT/session 廣度盲測,完整題目敘述開場)→ Topic 3 Unique ID Generator → registry sweep(到期條目)→ quick drill → artifact audit → 收帳(last_weekly_review 更新)。

WR5 收完後恢復原佇列:Drill Gauntlet 續跑(多區域全球限流專門 drill + 換題 bar-raiser:URL Shortener / Session Store / Snowflake / Distributed Cache,三指標各求 3 連)→ Day 30 Snowflake Light PoC(park)。execution-heavy 三條硬規則生效中(見 coaching-brief.md [Execution-Heavy Mode]):第一句就評分 / 裸結論直接打回 / 盯 unprompted-argument・unprompted-ops・no-freeze-capacity。S41 指標:argument 🟡(前裸後全)/ ops 未測 / capacity ❌ — argument、capacity 連續計數歸零。S42 指標:argument 🟡(導引段句子多半完整,但四格填空兩度交白/半句)/ ops ❌(第 6 記:即測都跑不動,遑論 unprompted)/ capacity 🟡(球 1:29+N=10 自解,cost 代打)— 三項連續計數全部為 0。

## Phase status

- P0 Thinking Framework: gate-passed(retroactive;legacy,pre-Examiner,coach 認證)
- P1 Core Building Blocks: gate-passed(2026-05-29,attempt 1,3/3;legacy,pre-Examiner,coach 認證)
- P2 Distributed Systems Core: gate-passed(2026-06-18,attempt 1,5/6;legacy,pre-Examiner,coach 認證)
- P3 Classic SD Problems: in-progress(Day 27-32 完成:URL Shortener / Unique ID / Distributed Rate Limiter;Day 33+ 未開;execution-heavy overlay 生效中,暫停新 archetype 改 Drill Gauntlet)
- P4 Advanced & Mocks: not-started

Weak-topic flags: 無(至今沒有帶 flag 過 gate 的紀錄)。

## Mastery

<!-- 原表 🟢→high、🟡→med;⬜ 未開課主題不列(見 curriculum hook 的 Phase Map)。
     last-updated 用 session 編號。原表完整版含逐格 notes 在 archive。 -->

- Go Refresher (Day -5~-1): high (s5)
- SD Interview Rubric (Day 1): high (s1)
- Back-of-Envelope Estimation (Day 2): high (s2)
- 4-Step Framework (Day 3): high (s3)
- Load Balancer (Day 4-5): high (s40)— S40 結掉三筆 S4 老錯;Least Connections 命名 33 天又掉,續盯
- Caching & CDN (Day 6-7): high (s33)— WR1 曾 0/4,WR4 六維全收,最弱救成最穩
- Database Selection (Day 8-9): med (s39)— 訂單→SQL 三理由穩;NoSQL 何時選的完整光譜未全 drill
- Message Queue (Day 10-11): high (s18)
- API Design (Day 12-13): high (s18)
- Security & Auth (Day 14): high (s21)— WR4 只重測 crypto-primitives 一塊,OAuth/JWT/session 廣度待補測
- Consistent Hashing (Day 15-16): high (s40)— 失敗時間線+ring/vnode 兩軸;vnode 數學 depth-ceiling park
- CAP Theorem (Day 17-18): high (s31)
- Distributed Cache design (Phase 1 Gate 題): high (s24)— 完整 PoC park 到 Day 38-39
- Consistency Models (Day 19-20): high (s31)— Vector clock (Day 20) park
- Replication & Leader Election (Day 21-22): high (s27)— Raft 細節/Service Discovery park
- Rate Limiting & Circuit Breaker (Day 23-24): high (s40)— CB 三狀態 S28 resolved 後又掉,S40 配電箱重焊,續盯
- Observability (Day 25): high (s39)— 知識到位、drill 輸出習慣待練
- Bloom Filter & Gossip (Day 26): high (s40)— FP/FN 嚴重性換情境重測過=真修好
- Multi-Region Session Store design (Phase 2 Gate 題): med (s42)— WR5 盲測未能獨立產出(誠實降級);clarify 強、核心軸 commit 對,機制層需逐格導引;S42 收尾:殭屍免疫✅、capacity 🟡、3AM page test 直接給,ops 組裝待複測
- URL Shortener (Day 27-28): high (s35)— S34 Drill 8/9 + S35 PoC 全綠(50 萬碼 0 碰撞 + -race 零警告)
- Unique ID Generator (Day 29-30): high (s36)— PoC(bit packing + clock skew 偵測)park
- Distributed Rate Limiter (Day 31-32): high (s40)— 設計知識到位;S40 Gauntlet 暴露輸出習慣病灶

## Scorecard history

<!-- 轉換規則:原符號照錄於註記;分數採原表數字,唯 s36 原記 ~4/7,依 ✅=1、🟡/❌=0 正規化為 3/7。
     legacy = pre-Examiner 時期由教學 coach 認證。standalone 未記日期的列標 (未記日期)。 -->

- (未記日期) | step G (s8, tier 1, Database Selection) | 2/3 | Scope Negotiation 忘了跑 | 資料量陷阱當場被抓後修正 | coach
- (未記日期) | weekly review (s10, WR1: DB/LB/Cache) | DB 3/4・LB 1/4・Cache 0/4 | LB 🟢→🟡、Cache 🟢→🔴 誠實降級 | 2 mistakes resolved(DNS limits、LSM-tree) | coach
- (未記日期) | step G (s13, tier 1, Message Queue) | 3/3 | requirements framework 與 idempotency 擺位需引導 | Think Aloud/Scope/用 MQ 全過 | coach
- (未記日期) | step G (s17, tier 1, API Design) | 3/3 | — | drill 中途自己修正 endpoint 錯誤 + idempotency deep-dive 強 | coach
- (未記日期) | weekly review (s18, WR2: API/Cache/MQ) | 8 mistakes resolved(單場紀錄) | 發現 notes-gap pattern(API 筆記缺 Scale Trigger/DevOps Angle) | API 5 + MQ 3 筆一場清掉 | coach
- 2026-05-29 | phase gate (P1, legacy, attempt 1) | 3/3 | clarify 時更早明確圈定 scope | 自己推出 stampede + cascading failure(Phase 2 級反應) | coach
- (未記日期) | weekly review (s25, WR3: Caching/LB/CAP) | Caching 3.5/5・LB 4/5・CAP 3/5 | CAP 剛學已衰退(術語掉,核心判斷在) | Weighted RR 老錯 resolved,LB 🟡→🟢 | coach
- 2026-06-03 | step G (s26, Consistency Models) | 4/5 | 漏 replication lag 監控收尾(operational) | 主動 clarify 開場;社群三功能各選對等級 | coach
- (未記日期) | step G (s27, Replication & Leader Election) | 5/5 | 選 C 時主動講反面代價 | read-after-write 一口氣三解法無提示;Day 19 監控弱點收斂 | coach
- (未記日期) | step G (s28, Rate Limiting & CB) | 5/5 | 第一次答太精簡,被追問才展開(主線) | 被 challenge 後自修正 global→per-user+global 兩層 | coach
- (未記日期) | step G (s29, Observability) | 5/6 | 答案精簡 + 中途要提示(原符號:Trade-off WHY 🟡) | 沒等講完就抓到 tail latency 並調用 P99 | coach
- 2026-06-16 | step G (s30, Bloom & Gossip) | 5/6 | 漏監控(重複爬率/實際 FP rate)(原符號:Operational ❌) | local Bloom 同步問題零提示連到 Gossip | coach
- 2026-06-18 | phase gate (P2, legacy, attempt 1) | 5/6 | 答太精簡 + 兩次主動要提示(原符號:Trade-off WHY 🟡) | 自己戳破單一 home-region 在 region 掛掉時的洞 | coach
- 2026-06-24 | weekly review (s33, WR4: URL Shortener/Caching/Database) | Caching 6/6・Bloom 回血・DB 陷阱避開 | 意外複習掉 Security 一塊(crypto primitives) | Caching WR1 0/4→六維滿分;主線弱點(一口氣講足)本場練成 | coach
- 2026-06-26 | step G (s34, URL Shortener, P3 bar-raiser) | 8/9 | operational 監控當固定收尾(S29/30 重複盲點,原符號:Operational ❌) | 被質疑「Redis 當 DB」自己想起重啟掉資料;Bloom 自己擺對讀路徑 | coach
- (未記日期) | step G (s36, Unique ID Generator, bar-raiser) | 3/7(原記 ~4/7;✅=1 正規化,原符號:TWY🟡 FM🟡 Ops❌ Cap❌) | 結論要附論證;收尾固定提監控(第 4 次);capacity 別被 2^n 嚇退 | enumeration 洩漏營業額觀點零提示(architect 級) | coach
- 2026-07-08 | step G (s40, Distributed Rate Limiter, Gauntlet #1, L3) | 3/9(原記 ~3/9;原符號:Scope❌ TWY❌ Ops❌ FM🟡 Cap🟡✅ Hint🟡 TB❌) | 三指標:unprompted-argument ❌ / unprompted-ops ❌(第 5 次) / no-freeze-capacity 🟡✅ | 「謝謝你拒絕我,逃避心態又來了」頂回去自推 5000/min=反脆弱本身 | coach
- 2026-07-11 | weekly review (s42, WR5 Topic 1: Multi-Region Session Store, S41-S42 跨場) | 1/6(✅=1 正規化:security/殭屍免疫✅;trade-off🟡 capacity🟡 failure-timeline🟡 one-liner🟡未抽;ops❌;scale trigger 未測) | 3AM page test 句型組裝獨立跑不動;SLI 標籤掉 | 「上一筆成功時間」零提示 = dead man's switch 直覺,素材在缺組裝 | coach

## Mistake Registry

<!-- 遷移自 standalone(91 筆:66 resolved / 14 ❌ / 11 🟡)。engine 只有 unresolved|resolved
     兩態:🟡 Improving/Partial → unresolved,原狀態與進展照錄於註記。
     欄位:date(session) | topic | what-was-wrong | root-cause-tag | status | interval | next-review-date | unresolved-session-count
     interval/next-review-date 遷移初始化:掛主題複習卡的沿用該卡日期(見 Spaced-repetition queue);
     無卡的設 3 天(2026-07-13)。unresolved-session-count = 40 - 建立 session(近似;≥5 依 engine
     Priority Override 置頂,step A 每堂上限內逐步清)。 -->

### Live(unresolved,30 筆)

- (s4) | Load Balancer | "least robin":RR 與 Least Connections 名字揉成一個 | 演算法「行為」與「名字」沒綁定 | unresolved | 3 | 2026-07-11 | 36
- (s4) | Load Balancer | 以為 8.8.8.8 是 ISP DNS(是 Google Public DNS) | trivia 型;冷知識未錨定 | unresolved | 3 | 2026-07-11 | 36
- (s4) | Load Balancer | sticky session 與 Redis external store 當同一招(方向相反的兩策略) | 狀態「留在 server」vs「搬出 server」軸沒拆開 | unresolved | 3 | 2026-07-11 | 36
  - S40 進展:已焊「sticky=往內壓 vs Redis=往外拉,都解換台登出」→ 待複測確認留得住
- (s4) | Load Balancer | 漏 sticky session 風險:負載不均 | 只記 happy path,反面代價沒收 | unresolved | 3 | 2026-07-11 | 36
  - S40 進展:sticky 不均風險已結掉一次,待複測
- (s9) | Database Selection | Interview Drill 忘了 Scope Negotiation | Step 1 流程未成肌肉(後演化為頭號主線) | unresolved | 3 | 2026-07-10 | 31
- (s12) | Message Queue | 設計練習不知道怎麼起手 | 缺「拆成小問題逐步推」的起手式 | unresolved | 3 | 2026-07-13 | 28
- (s13) | Message Queue | Idempotency 當獨立 service(是 Order Service 內的邏輯) | 邏輯歸屬 vs 部署單元混淆 | unresolved | 3 | 2026-07-13 | 27
- (s13) | Message Queue | Redis DECR(庫存 pre-check)與 idempotency check(防重複)搞混 | 兩個 Redis 用途各解什麼問題沒拆 | unresolved | 3 | 2026-07-13 | 27
- (s15) | API Design | GraphQL 只說「可以用」講不出 HOW(client 選 fields,burden 移到 client) | 機制層沒建立 | unresolved | 3 | 2026-07-13 | 25
- (s16) | API Design | 「修改不需要新版本」— rename field 是 breaking change | breaking vs non-breaking 判準缺 | unresolved | 3 | 2026-07-13 | 24
- (s24) | Distributed Cache | client-side vs proxy routing 答「不確定」 | 缺「開放題=trade-off 取捨、沒有對錯」反射 | unresolved | 3 | 2026-07-13 | 16
- (s24) | Distributed Cache | clarify 偏「問 AI 要答案」而非主動斷言圈 scope | S8 Scope Negotiation 老問題變體 | unresolved(原 🟡 Improving:S26 主動 clarify 開場,但問的是容量題非一致性核心) | 3 | 2026-07-13 | 16
- (s29) | Interview habit | 答太精簡被追問才展開 + 中途要提示 | 頭號主線:壓力下只出結論吞推導(見 coaching-brief 診斷) | unresolved(原 🟡 Improving:S31 回升、S33 WR4 scaffold 後講足、S38 一度突破) | 3 | 每場 drill 即測(execution-heavy 指標) | 11
- (s32) | Interview habit | 卡住直接喊「提示我」 | 同頭號主線(獨立 drive 不足) | unresolved(原 🟡 Improving:S32 給 thinking scaffold 後自己 commit NoSQL) | 3 | 2026-07-11(每場 drill 即測) | 8
- (s34) | Interview habit (operational) | drill 全程沒主動提監控(S29/30 重複) | 監控收尾未成反射 | unresolved(原 🟡 Improving:S35 PoC 收尾主動建監控表,真實 drill 待證明) | 3 | 2026-07-11(每場 drill 即測) | 6
- (s35) | KGS (operational) | 丟掉 1 萬空洞號當 bug 要修 | batching 代價(不領 block→KGS 瓶頸+每碼多一 round-trip)沒收全 | unresolved(原 🟡 Partial:「命名空間大丟得起」答對) | 3 | 2026-07-13 | 5
- (s36) | Interview habit (trade-off) | 給結論不給論證(「Snowflake 最適合」一句帶過) | 頭號主線 | unresolved(原 🟡 Improving:被追問後補得出,首句仍裸) | 3 | 2026-07-11(每場 drill 即測) | 4
- (s36) | Interview habit (operational) | drill 沒主動提監控(第 4 次) | 監控收尾未成反射 | unresolved | 3 | 2026-07-11(每場 drill 即測) | 4
- (s36) | Capacity estimation | 算 2^12/秒「直接放棄」 | 被 2^n 寫法嚇退,非真不會(拆 1024×2^(n-10)) | unresolved(原 🟡 Improving:S36 拆次方後跟上;S40 半扶沒凍結) | 3 | 2026-07-11(每場 drill 即測) | 4
- (s38) | Interview habit (commit) | 「用統一的限流器**嗎**?」問句丟球不敢 commit | 頭號主線(commit 缺席) | unresolved(原 🟡 Improving:S38 收尾 One-Liner 主動綁結論+論證=當場突破) | 3 | 2026-07-11(每場 drill 即測) | 2
- (s39) | Interview habit (argument) | 連 3 次「問兩件事只答一件」 | 頭號主線在複習題再現 | unresolved(原 🟡 Improving:逼問後每次補得出) | 3 | 2026-07-11(每場 drill 即測) | 1
- (s40) | Load Balancer | 該用 Least Connections 選了 latency + 英文名想不起(33 天又掉) | 語音近似+當場🟢≠留得住;命名軸摺疊 | unresolved(原 🟡 Improving:S40 對照表重錨) | 3 | 2026-07-11 | 0
- (s40) | Interview habit (Step 1) | 跳過 clarify 直接報解法 + LB 亂套進 rate limiter(recency bias) | Step 1 未成硬關卡 | unresolved — 下次 drill 開場自己跑完 clarify 才准進 Step 2 | 3 | 2026-07-11(每場 drill 即測) | 0
- (s40) | Interview habit (cost 格) | trade-off 的 cost 格填「low」(初階 tell) | 沒想過營運代價;cost 格禁用低/高,換具體會咬人的東西 | unresolved(原 🟡 Improving:L4 vs L6 對照演示過) | 3 | 2026-07-11(每場 drill 即測) | 0
- (s40) | Interview habit (unprompted-ops) | 沒主動收尾監控(第 5 次:S26/30/34/36/40) | 監控收尾未成反射;3AM page test 已焊進框架當第 5 步硬關卡 | unresolved | 3 | 2026-07-11(每場 drill 即測) | 14
- (s41) | Multi-Region Session Store | 「兩區互抄會有同步的問題」講到這就卡,一致性妥協無法量化 | 危險感沒機制(S31/S36 同款);公式「傷害=窗口×人口×症狀」已教,換場景複測 | unresolved | 3 | 2026-07-13 | 0
- (s41) | 分散式術語 | last-writer-wins 不認識(殭屍機制推得動,純標籤缺) | 術語-概念未綁定;LWW/tombstone 對照表待建 | unresolved | 3 | 2026-07-13 | 0
- (s41) | Interview habit | 裸結論×2:「多一種 block 黑名單嗎?」問句丟球 +「bloom filter」兩字答案 | 頭號主線;同場後半自修正(in-memory、pull 兩句完整) | unresolved | 3 | 2026-07-11(每場 drill 即測) | 0
- (s41) | 工具選擇反射 | 量級沒估先丟 Bloom filter(幾百筆名單 set 就夠) | 「先估量級再選工具」反射缺;S24 開放題反射變體;S40 才練的 FP/FN 判斷沒先跑 | unresolved | 3 | 2026-07-13 | 0
- (s42) | Interview habit | 卡住瞬間質疑題目正當性(「面試不會考吧」+「什麼面試會帶到這裡」,同場兩次) | 逃避家族新面具:攻擊題目而非跑機制;S36 放棄→S41 不確定→S42 質疑題目 | unresolved | 3 | 2026-07-14(每場 drill 即測) | 0
- (s41) | Capacity | 1+2N≤30 解 N 喊「不太確定要怎麼算」 | capacity-freeze 家族:被式子外觀嚇退非不會算;拆解式已給,中斷未完成 | unresolved | 3 | 2026-07-14(S42 複測 🟡:自己算出 29 並 commit N=10+why;cost 量化喊「直接說明」由 coach 代打,未全過) | 0
- (s43) | One-Liner: Session Revocation | 首次口頭抽考滑掉:LWW 覆蓋機制講得出(中文),英文一句組裝不出,喊「跳過」;fix 半句(blacklist 獨立 data class + in-memory + ~10s full pull)未產出 | 壓力下英文 retrieval + 「零件在、組裝不出貨」同款(S42) | unresolved | 3 | 2026-07-15 | 0
- (s42) | Observability | SLI 標籤現場撈不出(「SLI 是我最不熟悉的」;lag、上次成功時間素材第一輪就自己講出) | 術語-概念未綁定;s39 標 high 複驗打臉 = 當場🟢≠留得住再一例;考試分數比喻重錨過 | unresolved | 3 | 2026-07-14 | 0
- (s42) | Operational | 3AM page test 無法獨立組裝:「無法使用」「有立即性」交卷 = 症狀/事件/機制拆不開;pager/alarm/ticket 分層概念本身陌生 | 危險感沒機制家族 + 監控知識掛「救火」腳本不掛「設計收尾」腳本;句型模板+模範答案直接給,留沒留住下次換題複測 | unresolved | 3 | 2026-07-14(下次 drill 換題複測) | 0

### Resolved history(66 筆,遷移照錄)

原表 66 筆 ✅ Resolved 條目(含解法註記與 resolved 場次)verbatim 保存於
`archive/pre-migration/progress.md` 的 Mistake Registry 表。engine 的精度複測不逐筆排程,
改由 Spaced-repetition queue 的主題卡帶(複測滑掉 → 開新 registry 條目,原筆不改)。

## Spaced-repetition queue

<!-- 遷移自 standalone Review Schedule(14 張主題卡,Leitner Box 1-4)。
     Box→interval 對映:Box1→3、Box2→3、Box3→7、Box4→14(Box1 的「隔天」檔位 engine 無,
     取最近的 3;到期日照原檔 verbatim,過期就是過期,S41 WR5 收)。type=chunk(主題級 recall)。 -->

- chunk:Multi-Region-Session-Store(design) | chunk | 3 | 2026-07-13(S41 WR5 重打:盲測不過、導引後全鏈通;interval 重置 3) | active
- chunk:Consistency-Models | chunk | 3 | 2026-06-21(過期;原 Box 2) | active
- chunk:Distributed-Cache+CAP | chunk | 7 | 2026-06-25(過期;原 Box 3) | active
- chunk:Security-&-Auth | chunk | 3 | 2026-06-27(過期;原 Box 2;WR4 只測了 crypto-primitives,OAuth/JWT/session 廣度未測) | active
- chunk:Replication-&-Leader-Election | chunk | 3 | 2026-06-19(過期;原 Box 2) | active
- chunk:Caching-&-CDN | chunk | 7 | 2026-07-01(過期;原 Box 3) | active
- chunk:URL-Shortener(design) | chunk | 7 | 2026-07-03(過期;原 Box 3) | active
- chunk:Database(B-tree/LSM) | chunk | 3 | 2026-07-10(原 Box 2;S39 過,逼問才補全論證) | active
- chunk:Observability | chunk | 3 | 2026-07-10(原 Box 2;S39 過,知識到位輸出待練) | active
- chunk:Load-Balancer | chunk | 3 | 2026-07-11(原 Box 2;下次重測演算法命名) | active
- chunk:Rate-Limiting-&-CB | chunk | 3 | 2026-07-11(原 Box 2;下次重測 CB 三狀態) | active
- chunk:Bloom-Filter-&-Gossip | chunk | 3 | 2026-07-11(原 Box 2;S40 換情境重測過) | active
- chunk:Distributed-Rate-Limiter(design) | chunk | 3 | 2026-07-11(原 Box 2;S40 Gauntlet 實戰過) | active
- chunk:Consistent-Hashing | chunk | 7 | 2026-07-15(原 Box 3;S40 過,Box 2→3) | active

## Curiosity branch

- MQ long polling | (s13 前後) | Q1 no(Day 33-34 Notification System 大概率會用到,先 park) | 長輪詢怎麼運作
- Trace/log sampling(head vs tail-based)+ metrics high-cardinality | (s29) | Q1 no(面試不問細節) | follow-up preview 已預告,Day 31-32/46-47 可拉
- Sidecar 自身可靠性(掛了/拖慢主服務) | (s29) | Q2 no(observability 自身的資源隔離) | drill follow-up 預告過,下次可帶

## Domain registries

- `one-liner-library.md`(同目錄):面試一句話庫,21 條。抽考跟 Weekly Review quick-fire 走(headline first),滑掉 → 開 registry 條目。
- `rpg-state.md`(同目錄):RPG 狀態(title/streak/achievements 16/25/last story summary)。非間隔複習型,規則見 narrative hook。
- 其他 coach 讀取檔:`session-log.md`(session 敘事,S37-S40 自 standalone 遷入)、`coaching-brief.md`(作戰手冊,開場必讀)、`curriculum-plan.md`(戰略層,advisory)、`pattern-map.md`(題目=pattern 組裝對照)。

## Examiner ledger

(空 — P0/P1/P2 為 pre-Examiner 時期由教學 coach 認證,見 Scorecard history 的 legacy 列。
第一筆 Examiner 紀錄將是 P3 gate。)
