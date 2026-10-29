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

- session_count: 56
- last_weekly_review: 50 — WR5 於 S50 收帳(Topic 1 @S42 / Topic 2 @S45 / **Topic 3 @S50 學生選「收」**;過期卡 sweep 以 S50 倒帳形式完成:14 → 7 張 + 7 封存)。⚠️ **artifact audit 未跑**(engine WR flow 第 6 步),掛在下一次 WR
- last_session_date: 2026-10-29
- warm_up_classification: (standalone 時期未記錄;學員已 P3,Step 0 模式預設 Exploration)

## Current Session breakpoint

<!-- schema: PROGRESS-SCHEMA.md §3 = 當前狀態一行 + 下一場 resume。歷史 session 敘事一律在
     session-log.md;S45/S46/S47 三場原文已於 2026-08-19 自本區遷入該檔(一字未改),
     S50 的 coach 自產假訊息事故與應對規則另遷入 coaching-brief.md「Coach 自檢硬規則」。
     本區段 2026-08-19 之前的完整原文封存於 archive/breakpoint-history.md(冷檔,一字未刪)。 -->

**Chat System(Day 35-36)結束(S56 G 快收,2026-10-29)**:G 6/8 測到的維度;Day 37 PoC 依 10-17 re-plan 跳過。S52–S55 的 chunk 紀錄已遷至 archive/breakpoint-history.md。

下一場 resume:Metrics/Logging(Day 46,10-17 re-plan 隊列下一題;預習頁已有)。

## Phase status

- P0 Thinking Framework: gate-passed(retroactive;legacy,pre-Examiner,coach 認證)
- P1 Core Building Blocks: gate-passed(2026-05-29,attempt 1,3/3;legacy,pre-Examiner,coach 認證)
- P2 Distributed Systems Core: gate-passed(2026-06-18,attempt 1,5/6;legacy,pre-Examiner,coach 認證)
- P3 Classic SD Problems: in-progress(Day 27-32 完成:URL Shortener / Unique ID / Distributed Rate Limiter;Day 33+ 未開;2026-07-18 起 Sprint re-plan:清帳後 Tier 1 剩 5 題每題一場 mock,Tier 2 不逐題教)
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
- Multi-Region Session Store design (Phase 2 Gate 題): med (s44)— WR5 盲測未能獨立產出(誠實降級);S44 殭屍時間線複測仍需模範答案,但 LWW 標籤已撈出、英文 one-liner 自組過;革命尚未成功
- URL Shortener (Day 27-28): high (s35)— S34 Drill 8/9 + S35 PoC 全綠(50 萬碼 0 碰撞 + -race 零警告)
- Unique ID Generator (Day 29-30): high (s36)— PoC(bit packing + clock skew 偵測)park
- Distributed Rate Limiter (Day 31-32): high (s40)— 設計知識到位;S40 Gauntlet 暴露輸出習慣病灶
- Chat System (Day 35-37): med (s52)— Day 35 1v1 chunk 1–6 全過;F ✅ supported;G(換皮叫車)A/B 兩條路 unprompted ✅,catch-up 用 timestamp 回退 + counter scope/owner 冷回憶卡 = ordering 未留存;3AM/cost 未測
- Chat System Day 36(group fan-out / presence / read receipts): low-med (s56)— chunk 1-3 全 supported;F 3 題 2 過;G 6/8:3AM 第一刀 path 錯需縮題、cost 有 knob 無數字排序

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
- 2026-08-11 | cold retest (s49, Day 33 Notification System 留存冷測,非完整 step G) | 3/5 測到的維度(機制鏈✅ capacity×2✅ / headroom 論證🟡 / trade-off 反面❌;Think Aloud、scope、ops、failure modes 本場未測,不計分母) | 第一句就給論證:「我會開 120 台」不附 why = 裸結論被打回;separate 決策的自付代價要能一口氣講「管理面 ×N + idle」 | `300萬÷1000=3000s` 之後自己接著換算並對撞 P99 60s 得出 50 倍,S47 停住的那兩步這次零提示做完 | coach
- 2026-10-29 | step G (s56, Chat System Day 36 快收:3AM page + cost 雙問, L3) | 6/8 測到的維度(Think Aloud✅ Q2 每個決定帶理由 / building block✅ heartbeat+TTL、DB=truth / trade-off✅ 拉長 heartbeat → 以為在線 → 跳過 push、訊息不丟 / ops✅ 主動提 ALB idle timeout / hint response✅ (a)(b) 縮題後答對 snapshot 不受 pub/sub 影響 / time-breadth✅ / failure modes❌ 第一刀指 pub/sub,path 錯 / capacity❌ 沒用 500k/s vs 20k/s 排 knob;scope 未測不計分母) | 砍成本先用數字排序:fan-out 500k/s 是 heartbeat 20k/s 的 25 倍,先動大的 | Q2 沒被問就補「拉長 heartbeat 前要先確認 ALB idle timeout」 | coach
- 2026-10-13 | step G (s52, Chat System 1v1 換皮叫車, L3, 短 G) | 3/5 測到的維度(Think Aloud✅ building block✅ hint response✅ / trade-off🟡:push content-free 帶 why,但 DB「MongoDB 或 PostgreSQL 也 OK」裸結論 / failure modes❌ 未主動;scope、ops、capacity、time/breadth 未測或 coach 造成 rat-hole,不計分母) | catch-up 鍵用 `conv_id + seq > last_seen`,不要用 timestamp(clock skew 會漏訊息,chunk 4 已教) | Q1 第一段 A/B 兩條路一口氣講完、NAT 理由軸正確、push 只放通知帶隱私 why,全程直述句零「嗎」 | coach

## Mistake Registry

<!-- 遷移自 standalone(91 筆:66 resolved / 14 ❌ / 11 🟡)。engine 只有 unresolved|resolved
     兩態:🟡 Improving/Partial → unresolved,原狀態與進展照錄於註記。
     欄位:date(session) | topic | what-was-wrong | root-cause-tag | status | interval | next-review-date | unresolved-session-count
     interval/next-review-date 遷移初始化:掛主題複習卡的沿用該卡日期(見 Spaced-repetition queue);
     無卡的設 3 天(2026-07-13)。unresolved-session-count = 40 - 建立 session(近似;≥5 依 engine
     Priority Override 置頂,step A 每堂上限內逐步清)。 -->

### Live(unresolved,50 筆)

- (s56 G) | Chat System(3AM page:症狀→路徑) | 「好友全部顯示離線、訊息照收」第一刀指 Redis pub/sub;縮成 (a)/(b) 後答對「只壞 pub/sub,snapshot 仍正確」;結論 presence key 不見(eviction / failover / heartbeat 寫入失敗)由 coach 給 | 元件對、path 錯:snapshot(GET key)vs delta(pub/sub)沒先拆就下刀(RP1) | unresolved | 3 | 2026-11-01 | 0
- (s56 G) | Chat System(cost 排序) | 砍 30% 列出「拉長 heartbeat」「減少通知對象」兩個 knob,沒用自算數字排先後(fan-out 500k/s vs heartbeat 20k/s = 25×);「怎麼證明沒砍到可靠性」未答 | 有選項無判準:cost 決策沒接回 capacity 數字(RP7/RP3) | unresolved | 3 | 2026-11-01 | 0
- (s55) | Chat System(read receipts 論證) | F Yuki 故意錯建議「每則訊息存已讀 user_id list」卡住;縮成「Bob 滑過 50 則,A/B 各寫幾次」仍只答原則「每人只記讀到哪」,50 writes vs 1 未算出 | 機制在、反方案的代價論證缺(RP3:有結論無論證);當堂剛教 (A)/(B) 對照圖仍撈不出 | unresolved | 3 | 2026-10-30 | 0
- (s54) | Chat System(heartbeat interval) | trade-off 兩邊代價講出,但沒 commit 選擇;「60 秒嗎」問句 | 頭號主線 commit 缺席(s38 家族)| unresolved | 3 | 2026-11-01 | 0 S56 G cost 題 fail(reset,仍「會思考是不是需要拉長」未 commit 數字);但 ALB idle timeout 前提 + 代價「以為在線→不推播、訊息不丟」unprompted 自產 = S55 忘掉那半撈回。S55 暖身 fail(reset):三輪才 commit N=5s,且靠句型填空;判準先講「漏訊息」,S54 自產的「誤判在線→跳過 push」忘記由 coach 給;理由(ALB 60s、3×)30s 也滿足;代價先寫成對面那邊,第三輪才自講 QPS + 15s stale window。

- (s53) | Chat System(group fan-out) | server 訂閱 group 後說「省掉查 group 有多少 member」;問 chat-2 怎麼決定訂閱哪些 group 只答「group ID 吧」 | 「移走」當「刪除」:成員查詢從每則訊息移到連線時/成員異動時,沒消失(RP2 causal chain 少一環)。connection map 省掉那點對,但 why(server 自知身上連了誰)未自產 | unresolved | 3 | 2026-10-17 | 0
- (s52 G) | Chat System(ordering 留存) [S54 冷測:scope 仍答 user_id,反例+圖後 supported;interval 維持 3,next 2026-10-28] | 換皮 G:B 路徑 catch-up 答「查該客戶 ID 最後收到的訊息時間戳」;clock skew 圖戳後修法撈回「NTP 不準、只往前、原子 +1」,但 counter 的 scope(per conversation)要縮題才出、owner 選 Redis INCR(S51 定案是 DB 欄位) | 強先驗劫持:時間戳 = 舊 DevOps 直覺,chunk 4(S51)教過仍回退;scope 格 S51 已漏一次 = 同格重犯(RP5 cold transfer) | unresolved | 3 | 2026-10-16 | 0
- (s52) | Circuit Breaker(術語) | quick-fire:auth 變慢、CB 跳開後的 state 名稱「不知道」;跳開後 call 的去向只答「不會送」,fail fast 未講 | OPEN 名字第三次掉(S28 resolved → S40 重焊 → S52);HALF-OPEN 的理由(「一起動又被打掛」)自推但沒掛上名字 = 機制在、標籤未綁(RP5) | unresolved | 3 | 2026-10-14 | 0
- (s52) | Chat System(offline delivery) | 「server 為何不能主動連 Bob 手機」理由答「HTTP 是 request/response 單向」;push 答對卻用「但是不是離題了?」收回 | 軸錯:限制是誰能撥給誰(NAT、無 public IP、OS 關背景連線),不是 protocol 方向;反證「換 WebSocket 就能撥?」可破(RP1) | unresolved | 7 | 2026-10-20 | 1 S52 續 F 再現:「WebSocket 是 request and response,所以 server 不能主動撥號」= protocol 方向 vs 誰撥號軸仍摺疊;又說「推播 server 不能主動發起」(反了)。S52 G 換皮 unprompted ✅「手機在 NAT 後,server 無法主動建立連線」= 誰撥號軸正確,interval 3→7。
- (s52) | Observability(alert 選點) | 3AM 只能設一條 page:選 M2 DB commit latency,理由「DB 是最重要的真相來源」;重選時先講「網路監控」 | 軸摺疊:元件重要性 vs 使用者症狀;Redis-down 反證後自修成 end-to-end delivery latency。離線 3 天陷阱自答「只算在線 + PUBLISH return 1」(RP7) | unresolved | 3 | 2026-10-14 | 0
- (s52 續) | Chat System(online last hop) | F teach-back 教 Yuki:A(app 開著)最後一段答成「走 iPhone/Android 內建通道(推播)」;理由用的是 B 的(不放機密);被問誰撥 WS 答「chat-3」;填空「chat-3 從 DB 把訊息送下去」 | 線上 vs 背景兩條路摺疊 + storage vs delivery 軸回退(S51 兩軸表曾自填對):把 chunk 5「server 不能撥號」過度推廣成「server 不能送」。連錯三次後 coach 給答 + 三步圖,之後三句自講 = supported,非獨立(RP1) | unresolved | 7 | 2026-10-20 | 0 S52 G 換皮(叫車)unprompted ✅:A = WS 連著 + PUBLISH 有訂閱者即送、B = push;A/B 不再摺疊,interval 3→7
- (s51) | Database(lock granularity) | `UPDATE conversations ... WHERE id='conv-A'` 會擋誰:選「別的對話 conv-B 的寫入」(以為鎖全表) | 前置知識缺口(未教過,非推理錯):row-level vs table lock;連帶 per-conversation counter 的代價範圍講不出(「這我不確定」)。教後自組「同對話排隊、不同對話不影響」 | unresolved | 7 | 2026-10-20 | 1 S52 續 quick-fire ✅:T2 等(同列)、T3 不等「WHERE 只限制住 A」直述自答;名詞 row-level lock 未自產、「會員 ID」口誤由 coach 修。
- (s51) | Chat System(pub/sub 語意) | 「pub/sub 掛 10 分鐘,Bob 何時看得到」答「pub/sub 恢復正常」;接著答「DB 記錄最後傳了什麼,redis 重啟才知道補哪些」 | 兩個錯疊在一起:(1) 以為 pub/sub 會緩衝/重送(Redis pub/sub 是 fire-and-forget);(2) **actor 錯置**:把 catch-up 交給 Redis,正解是 client 帶 last_msg_id、server 查 DB 補送(RP1 layer/ownership;Redis 當 truth 強先驗家族再現)。同場儲存 vs 投遞兩軸表**自己填對**(S50 軸摺疊本場拆開) | unresolved | 3 | 2026-10-16 | 1 S52 續 F:B 路徑 catch-up actor 自講對(重連 → SELECT 上次之後、限定使用者);fire-and-forget 未測,部分證據不升 interval。
- (s50) | 分散式術語(deregistration delay) | 「ALB 摘掉 target 後既有連線還保留多久」的設定名答成「timeout 時間」;提示到「預設 300 秒、你在 billing 調過」仍未撈出正解 | 術語-概念未綁定家族;機制他懂(分批送人走),缺的是**名字**。同場另一個名詞 thundering herd 也是先講機制(「羊群效應 同時打」)才由 coach 補英文。**兩個名詞下場冷抽**;對照:deregistration delay = 分批斷(server 側)/ backoff + jitter = 分散回來(client 側) | unresolved | 3 | 2026-10-16 | 2
  - **S52 續 quick-fire**(2026-10-13):thundering herd 名字 ✅ 冷答出;deregistration delay ❌,講成「類似 CB、啟動時先 test、不讓系統一啟動就被打掛」= 上線端(slow start / HALF-OPEN)劫持下線端(draining),強先驗劫持家族。生命週期圖(上線端 vs 下線端)教後,Transfer「draining 300s 後砍掉 2 萬條 WS」自答 auth/DB 被打爆 ✅。interval 重置 3
  - **S51 冷抽 fail**(2026-10-10,隔 51 天):兩個名字都「忘記了」;機制在縮題後自推回(2 萬條 1 秒內、共用的 auth/DB 先倒),jitter 自產、backoff 只到「延長一點吧」,名字與 deregistration delay 由 coach 給。interval 重置 3
- (s50) | Interview habit(質疑題目正當性) | 盲測球 1 首答「完整怎麼切應該不重要」把題目降級,且該答案漏掉題目明寫的 100 台(machine ID 那格) | 逃避家族第 3 次面具(S42 兩次 →S50);⚠️ **coach 自我修正**:精確 bit 數確實不是考點,學生這半邊有道理,**下次不要拿「面試會考」硬撐,直接指出他的答案漏了題目給的數字**,那才是有效施壓點 | unresolved | 3 | 每場 drill 即測 | 0
- (s48) | Capacity(modeling) | `130 台 worker × 每台佔 36s → 每秒空出幾台` 講不出算式:縮到單一除法後仍問「要怎麼算啊」,給 rate 模型骨架(一台 36s 放手一次 = 1/36 台/秒)後即答 3.6 | ⚠️ **與棄權家族分家的新根因**:算術沒問題(同場 `(10+2)×3=36` unprompted 算對),缺的是**把場景翻成算式**的 modeling 步驟;治法=每場塞一題「先寫出單位式(X per second 是什麼除什麼)」再算數字 | unresolved | 7 | 2026-08-18 | 0
  - **S53**(2026-10-14):10 萬人 × 5 則/s 先跳過數字直接猜「DB 先爆、用 Redis cache 嗎」(讀成每秒 5 千);要求填三格後 500k 自算 ✅,但標成「50 萬個訊息」(單位錯:是讀取不是訊息)、PUBLISH 漏 ×5。單位式仍是缺口
  - **S49 複測 pass**(2026-08-11):Little's Law 冷測 `300/s × 200ms = 60 台` unprompted,並自補「這是最少」。coach 當場把它與卡死的 `130÷36` 對焊(**一台每 W 秒放手一次 = 1/W 台/秒**,乘除只是同式兩面)。interval 3→7。缺口剩:安全係數的**機制**(見下方 s49 headroom 條),數字面已通
- (s48) | Capacity(判讀) | 拿 best case 交 P99 的卷:只算「排第一那則等 36s」就答「SLO 沒破」,沒看第 300 則(等 84s)與 backlog 累積(296/s) | P99 = 最慢的 1%,不是最順的那則;happy-path-only 交卷是 capacity 通用死法;複測形式:任何 SLO 題追問「你算的是第幾則」 | unresolved | 3 | 2026-08-10(每場 drill 即測) | 0
- (s48) | 分散式術語(bulkhead) | separate pool 講成「不用一直等」= 以為隔離讓損害消失(實際上 marketing 那池照樣卡滿 retry,只是 fraud 那 30 台沒事) | 術語-概念未綁定;**bulkhead=損害範圍限縮(誰陪葬)vs circuit breaker=損害時間限縮(卡多久)** 兩軸當場拆開,換場景複測 | unresolved | 3 | 2026-08-18 | 1
  - S49 側面複測(2026-08-11):精度那一軸未直接測;但問「separate pools 你自己付什麼代價」三輪不合格(見下方 s49 條目),顯示 bulkhead 只學到「好處那一半」

- (s49) | Interview habit(trade-off 反面) | 「separate pools 的自付代價」三輪答不出可用答案:①「維運的費用」(s40 cost 格老毛病:抽象名詞不是代價)②「需要良好的分流」(那是前提)③「3 倍的維運能量」(同句換皮);縮到「單一 pool 上面掛哪三個名詞」填空才產出 alert/scaling policy/dashboard。**idle 成本整條軸三輪零觸及** | 頭號主線的反面代價格;**焊入的形狀:任何 separate/isolate 決策的自付代價一律兩條 = 管理面 ×N + idle 資源**。複測形式:換場景(shard/cell/region 隔離)問代價,要求兩條各一句,不給 scaffold | unresolved | 3 | 2026-08-14 | 0
- (s49) | Capacity(安全係數機制) | 「為什麼不敢開 60 台跑 100%」第一句只給數字(120)不給 why;打回後自產 `2.5×0.2=50% utilization`(強),但機制要 coach 給方向才補出 jitter/burst/retry,最後一塊由 coach 給 | 缺的不是數字是**排隊機制**:100% 使用率下 burst 留下的 backlog 追平速度為 0 → 單調上升回不來;50% 的意義是「burst 過後有一倍產能吃 backlog」。複測:任何 capacity 題追問「你算出來的台數敢不敢直接上線」 | unresolved | 3 | 2026-08-14 | 0
- (s49) | Interview habit(循環論證) | 「A 用 WebSocket 因為 WebSocket 適合即時傳輸訊息」= 用結論當理由,等於「因為它適合」。第一句先裸結論、打回後給循環論證,縮到「幾向?」二選一才產出真理由 | 頭號主線的新變體:**不是不給 why,是給了一個假的 why**,比裸結論更難自我察覺。判準:理由裡如果出現待證명詞本身(「因為 X 適合 X 的場景」)就是循環。複測:任何選型題追問「你這個理由換成另一個工具還成不成立?成立就不是理由」 | unresolved | 3 | 2026-08-14 | 0
- (s49) | 分散式術語(SSE vs 推播) | SSE 講成「推播」 | 術語-概念未綁定家族(5a 語音/標籤滑動):**SSE/WebSocket = App 開著的 in-app 通道;push notification = APNs/FCM,App 關著也收,走廠商通道**,兩者常併用(開著走 SSE、關了發推播)。換場景複測 | unresolved | 3 | 2026-08-14 | 0
- (s49) | Interview habit(跳題) | 「決定這則進哪條 queue 的動作在哪個框」連問三次全部略過不答,最後由 coach 給(router/dispatcher) | 新面具:不是棄權也不是質疑題目,是**沉默跳過**,比棄權更難抓(沒有拒絕訊號);治法=跳過的球下場開頭第一顆重投,並當場點名「你剛剛跳過這題」 | unresolved | 3 | 2026-08-14 | 0
- (s48) | Interview habit(棄權) | 「你直接說明 不要卡太久」出現在 `130÷36` 這一步(家族第 6 筆:S36→S42→S44→S46→S48) | 逃避家族;本次拒給+舉證(S46 200萬÷1000 同款前科)+縮到單步後仍卡 → 判定**部分成因是 modeling 缺口而非純逃避**(見上方 s48 capacity-modeling 條);後續要分辨「不敢算」與「不會建模」,前者加壓、後者給模型 | unresolved | 3 | 每場 drill 即測 | 0

- (s46) | Capacity estimation | `300 萬 ÷ 1000/s` 喊「不會算」;同一個除法 07-19 同一題已在他面前算過且他當場自答「要 Queue」,6 天後掉 | capacity-freeze 家族 + 「當場🟢≠留得住」;縮到單步除法即答對(3000)= 算術沒問題,是壓力下棄權;複測用同題不同數字冷起手 | unresolved | 14 | 2026-08-25 | 0
  - S47 複測 pass(2026-08-04):200 萬÷1000=2000s 冷起手零提示自算,interval 3→7;缺口剩「換算人類單位+對撞 SLO」未主動(2000s→33min→超標 33 倍由 coach 補)
  - **S49 複測 pass 且缺口補齊**(2026-08-11):`300 萬÷1000=3000s` 冷起手自算,**S47 缺的兩步這次自己做完**(換算 + 對撞 P99 60s = 50 倍)。interval 7→14。滿 14 天複測再過即 resolve
- (s46) | Interview habit(棄權) | 一場內三連棄權:「不確定怎麼回答」→「不會算,L6 會怎麼答」→「面試不會問吧,直接說明」;拒給+縮小步+舉證後才動 | 逃避家族第 5 筆(S36/S42/S44/S46);proxy 問法(「Senior 會怎麼答」)S45 後第 2 次;質疑題目正當性 S42 後第 2 次 | unresolved | 3 | 每場 drill 即測 | 0
- (s46) | Notification System(priority) | 「一條 queue 塞滿時高優先通知的延遲」無法自行量化,因此 priority queue 只剩名詞沒有論證 | 危險感沒機制家族;論證=他自己算的 50 分鐘,已示範綁進 one-liner,留存待 S47 白板默畫複測 | unresolved | 3 | 2026-08-07 | 0
  - S47 複測部分過:量化除法自己出手(pass,見上條);但 worker-isolation 機制鏈斷 —「排第一還是卡」三輪都往 queue-position 找原因,櫃員比喻+二選一+配對題才收;ordering vs capacity 標籤綁定換場景複測(priority vs pools trade-off 球已出未答,下場即測)
  - **S48 複測 pass**(2026-08-07):新場景(Max 的 single queue + priority tag)一個櫃員畫面即自產「等有櫃員空出來」,S47 卡三輪的位置這次一輪過;收尾自產「priority 分類 vs worker 佔用」= ordering vs capacity 標籤綁定成立。interval 3→7,next 2026-08-14。缺口剩 isolation 這一層(見下方 s48 bulkhead 條目)

- (s45) | Security & Auth (OAuth) | 術語層撈不出:access token 講成「憑證」、scope 講成「權限」、四角色(Resource Owner/Client/Auth Server/Resource Server)喊忘、OIDC 先搶標籤(挑戰後改選 OAuth 2.0 但沒給理由);機制全通(帳密只進銀行頁面、唯讀授權、改密碼=核彈誤傷全部 App) | 術語-概念未綁定家族;AWS 同構對照表已給(token=STS creds、scope=IAM policy),留存待複測;另計 Deny List 語音滑動 ×2(Dynamic/Denial List,5a 家族) | unresolved | 3 | 2026-07-23 | 0
- (s45) | Security & Auth (deny list) | 「deny list 為何不膨脹」卡兩輪(「不會了」「不確定」),通行證印期限比喻後自組出 TTL aging(過期 entry 可移除,表≈近 15 min 掛失量) | 機制組裝啟動能量問題(S44 同款);短 TTL 綁 deny list 大小這條鏈換場景複測 | unresolved | 3 | 2026-07-23 | 0

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
- (s38) | Interview habit (commit) | 「用統一的限流器**嗎**?」問句丟球不敢 commit | 頭號主線(commit 缺席) | unresolved(原 🟡 Improving:S38 收尾 One-Liner 主動綁結論+論證=當場突破;**S49 再現**:知道答案卻用「alert 嗎?」問號確認,當場點名「面試官聽到的是他自己也不確定」,interval 重置;**S52 再現**:push「但是不是離題了?」、「不會放隱私訊息吧」、「收不回來了吧」;同場 payload 模板一題與 chunk 6 Transfer 直述收尾) | 3 | 2026-08-14(每場 drill 即測) | 3
- (s39) | Interview habit (argument) | 連 3 次「問兩件事只答一件」 | 頭號主線在複習題再現 | unresolved(原 🟡 Improving:逼問後每次補得出) | 3 | 2026-07-11(每場 drill 即測) | 1
- (s40) | Load Balancer | 該用 Least Connections 選了 latency + 英文名想不起(33 天又掉) | 語音近似+當場🟢≠留得住;命名軸摺疊 | unresolved(原 🟡 Improving:S40 對照表重錨) | 3 | 2026-07-11 | 0
- (s40) | Interview habit (Step 1) | 跳過 clarify 直接報解法 + LB 亂套進 rate limiter(recency bias) | Step 1 未成硬關卡 | unresolved — 下次 drill 開場自己跑完 clarify 才准進 Step 2 | 3 | 2026-07-11(每場 drill 即測) | 0
- (s40) | Interview habit (cost 格) | trade-off 的 cost 格填「low」(初階 tell) | 沒想過營運代價;cost 格禁用低/高,換具體會咬人的東西 | unresolved(原 🟡 Improving:L4 vs L6 對照演示過) | 3 | 2026-07-11(每場 drill 即測) | 0
- (s40) | Interview habit (unprompted-ops) | 沒主動收尾監控(第 5 次:S26/30/34/36/40) | 監控收尾未成反射;3AM page test 已焊進框架當第 5 步硬關卡 | unresolved | 3 | 2026-07-11(每場 drill 即測) | 14
- (s41) | Multi-Region Session Store | 「兩區互抄會有同步的問題」講到這就卡,一致性妥協無法量化 | 危險感沒機制(S31/S36 同款);公式「傷害=窗口×人口×症狀」已教,換場景複測 | unresolved | 3 | 2026-07-21 | 0
  - S44 複測:殭屍時間線給填空結構仍組不出(「時間差所以被覆蓋」半句)→ 直接說收場;模範時間線+架構圖已給,下次換場景測(interval 重置)
- (s41) | 分散式術語 | last-writer-wins 不認識(殭屍機制推得動,純標籤缺) | 術語-概念未綁定;LWW/tombstone 對照表待建 | unresolved | 3 | 2026-07-13 | 0
- (s41) | Interview habit | 裸結論×2:「多一種 block 黑名單嗎?」問句丟球 +「bloom filter」兩字答案 | 頭號主線;同場後半自修正(in-memory、pull 兩句完整) | unresolved | 3 | 2026-07-11(每場 drill 即測) | 0
- (s41) | 工具選擇反射 | 量級沒估先丟 Bloom filter(幾百筆名單 set 就夠) | 「先估量級再選工具」反射缺;S24 開放題反射變體;S40 才練的 FP/FN 判斷沒先跑 | unresolved | 3 | 2026-07-13 | 0
- (s42) | Interview habit | 卡住瞬間質疑題目正當性(「面試不會考吧」+「什麼面試會帶到這裡」,同場兩次) | 逃避家族新面具:攻擊題目而非跑機制;S36 放棄→S41 不確定→S42 質疑題目 | unresolved | 3 | 2026-07-14(每場 drill 即測) | 0
- (s41) | Capacity | 1+2N≤30 解 N 喊「不太確定要怎麼算」 | capacity-freeze 家族:被式子外觀嚇退非不會算;拆解式已給,中斷未完成 | unresolved | 3 | 2026-07-14(S42 複測 🟡:自己算出 29 並 commit N=10+why;cost 量化喊「直接說明」由 coach 代打,未全過) | 0
- (s43) | One-Liner: Session Revocation | 首次口頭抽考滑掉:LWW 覆蓋機制講得出(中文),英文一句組裝不出,喊「跳過」;fix 半句(blacklist 獨立 data class + in-memory + ~10s full pull)未產出 | 壓力下英文 retrieval + 「零件在、組裝不出貨」同款(S42) | unresolved | 3 | 2026-07-21 | 0
  - S44 複測過:自組新句(absence can't propagate → positive record)納庫;原排 07-21 再抽,**抽考機制 2026-07-18 學生拍板停用 → 條目凍結**(復測通道移除,不再排程)
- (s42) | Observability | SLI 標籤現場撈不出(「SLI 是我最不熟悉的」;lag、上次成功時間素材第一輪就自己講出) | 術語-概念未綁定;s39 標 high 複驗打臉 = 當場🟢≠留得住再一例;考試分數比喻重錨過 | unresolved | 3 | 2026-07-14 | 0
- (s44) | Interview habit(棄權) | 「直接說」×2:球 1 時間線填空後棄權、球 2 零嘗試就喊(家族第 3 筆:S36 放棄→S42 太拖→S44) | 逃避家族:壓力下棄推導;球 2 拒給後縮三空白即過 = 能力在,是啟動能量問題,不是知識 | unresolved | 3 | 每場 drill 即測 | 0
  - S44 收尾根因修正(學生自報+證據支持):兩次棄權都發生在「腦中沒畫面就被逼文字組裝」的機制題;圖先行後同場即產出理解問題+最佳英文句。條目不撤(S36/S42 前科在),但複測改「圖先行+白板默畫」形式,見 coaching-brief 有效手法快取
- (s42) | Operational | 3AM page test 無法獨立組裝:「無法使用」「有立即性」交卷 = 症狀/事件/機制拆不開;pager/alarm/ticket 分層概念本身陌生 | 危險感沒機制家族 + 監控知識掛「救火」腳本不掛「設計收尾」腳本;句型模板+模範答案直接給,留沒留住下次換題複測 | unresolved | 3 | mock #1 內建考 | 0
  - S44 換題複測(URL Shortener):零嘗試喊直接說→拒給→縮三空白後 page 句最小單位過;dead man's switch/ticket/dashboard 三格仍 coach 給,mock #1 驗留存

### Resolved history(66 筆,遷移照錄)

原表 66 筆 ✅ Resolved 條目(含解法註記與 resolved 場次)verbatim 保存於
`archive/pre-migration/progress.md` 的 Mistake Registry 表。engine 的精度複測不逐筆排程,
改由 Spaced-repetition queue 的主題卡帶(複測滑掉 → 開新 registry 條目,原筆不改)。

## Spaced-repetition queue

<!-- 遷移自 standalone Review Schedule(14 張主題卡,Leitner Box 1-4)。
     Box→interval 對映:Box1→3、Box2→3、Box3→7、Box4→14(Box1 的「隔天」檔位 engine 無,
     取最近的 3;到期日照原檔 verbatim,過期就是過期,S41 WR5 收)。type=chunk(主題級 recall)。

     ⚠️ 2026-08-11(S49):14 張全部過期,倒帳第三次順延(S45 押後 → S48 提案 → S49 學生喊
     「趕快開始課程」)。依 curriculum-plan [Re-plan 2026-08-11] 複習制,S50 開場由 coach
     單方執行:砍到 ≤10(只留弱項相關,其餘封存),不再徵詢學生同意。
     ✅ 2026-08-19(S50)執行完畢:14 → 7 張。留下的判準 = 有 open registry 條目、或有明確
     回退史;其餘封存(複測改由 mock 順帶抽,不再排程)。到期日重新錯開,避免再次整批過期。 -->

### Active(9 張)

- chunk:Load-Balancer | chunk | 3 | 2026-08-19(S50 quick-fire:sticky vs external store 兩策略 + Least Connections 命名;s4 四筆條目未結) | active
- chunk:Rate-Limiting-&-CB | chunk | 3 | 2026-10-14(S52 quick-fire fail:OPEN 名字掉,見 s52 條目) | active
- chunk:Observability | chunk | 3 | 2026-10-15(S52 併入 chunk 6:首選 DB 被反證才改 end-to-end,判 fail) | active
- chunk:Multi-Region-Session-Store(design) | chunk | 3 | 2026-08-26(WR5 盲測不過、S44 殭屍時間線仍需模範答案 = 現存最弱卡) | active
- chunk:Security-&-Auth | chunk | 3 | 2026-08-26(OAuth/JWT/session 廣度未測;s45 兩筆條目 unresolved) | active
- chunk:Consistency-Models | chunk | 3 | 2026-08-26(session store / LWW 的地基) | active
- chunk:Database(B-tree/LSM) | chunk | 3 | 2026-08-29(S39 過但逼問才補全論證) | active
- chunk:Chat-System-1v1 | chunk | 3 | 2026-10-16(S52 G:A/B 過,ordering catch-up 鍵回退) | active
- chunk:Chat-System-Group(Day 36) | chunk | 3 | 2026-11-01(S56 G 6/8:3AM path 錯、cost 無數字排序) | active

### Archived(7 張,2026-08-19 S50 封存)

Caching-&-CDN(WR4 六維滿分)/ URL-Shortener(design)(S34 8/9 + S35 PoC 全綠)/
Distributed-Cache+CAP(P1 gate 題,high)/ Replication-&-Leader-Election(S27 5/5,無 open 條目)/
Bloom-Filter-&-Gossip(S40 換情境重測過 = 真修好)/ Distributed-Rate-Limiter(design)(S40 Gauntlet 實戰過)/
Consistent-Hashing(S40 過,vnode 數學已 park)

## Curiosity branch

- Redis INCR 當 per-conversation counter 遇 failover(async replication 掉號 → seq 重複)| (s52 G) | 學生喊太深,coach 挖過 depth ceiling;Q2 no(G 範圍外) | 一句結論已給:seq 跟訊息同存 DB
- MQ long polling | (s13 前後) | Q1 no(Day 33-34 Notification System 大概率會用到,先 park) | 長輪詢怎麼運作
- Trace/log sampling(head vs tail-based)+ metrics high-cardinality | (s29) | Q1 no(面試不問細節) | follow-up preview 已預告,Day 31-32/46-47 可拉
- Sidecar 自身可靠性(掛了/拖慢主服務) | (s29) | Q2 no(observability 自身的資源隔離) | drill follow-up 預告過,下次可帶

## Domain registries

- `one-liner-library.md`(同目錄):面試一句話庫,23 條。**抽考機制停用(2026-07-18 學生拍板)**,庫保留作自修素材,不再排程、不再產 registry 條目。
- `rpg-state.md`(同目錄):RPG 狀態(title/streak/achievements 16/25/last story summary)。非間隔複習型,規則見 narrative hook。
- 其他 coach 讀取檔:`session-log.md`(session 敘事,S37-S40 自 standalone 遷入)、`coaching-brief.md`(作戰手冊,開場必讀)、`curriculum-plan.md`(戰略層,advisory)、`pattern-map.md`(題目=pattern 組裝對照)。

## Examiner ledger

(空 — P0/P1/P2 為 pre-Examiner 時期由教學 coach 認證,見 Scorecard history 的 legacy 列。
第一筆 Examiner 紀錄將是 P3 gate。)
