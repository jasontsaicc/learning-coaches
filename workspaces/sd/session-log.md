# Session Log

<!-- 歷史 session 敘事(新的在上)。S37-S40 的敘事自 standalone progress.md 的 breakpoint
     區段遷入(standalone 時期更早的 session 沒有集中敘事,細節散在 portfolio/sd/notes/ 的
     逐日筆記與 scorecard history);S41 起的 session 摘要續寫於此,progress.md 只留 schema 欄位。

     舊 → 新路徑對照(遷移 2026-07-10):
     - progress.md(repo 根)       → workspaces/sd/progress.md(engine schema)
     - notes/dayXX-topic.md        → portfolio/sd/notes/dayXX-topic.md
     - projects/<poc>/             → portfolio/sd/projects/<poc>/
     - docs/coaching-brief.md      → workspaces/sd/coaching-brief.md
     - docs/pattern-map.md         → workspaces/sd/pattern-map.md
     - docs/curriculum-roadmap.md、docs/planning-review.md → workspaces/sd/archive/pre-migration/
     - sd-coach skill 本體         → skills/sd-coach/(curriculum 詳文=references/curriculum-detail.md) -->

## S50(2026-08-19,倒帳 + WR5 收帳 + Chat System chunk 2)

- **間隔 8 天,Comeback 條件成立**;開場照 [Re-plan 2026-08-11] 的複習制走,coach 單方倒帳不徵詢。過期卡 14 → 7 張(判準:有 open registry 條目或明確回退史),7 張封存,到期日錯開。
- **WR5 Topic 3 學生選「收」**:Snowflake 盲測球 1。首答把題目降級(「完整怎麼切應該不重要」)且漏掉題目明寫的 100 台;指出後三格(time / machine / sequence)到位。**coach 當場認一半:精確 bit 數不是考點**,以三格各解什麼問題為標準判部分過,Topic 3 結案,`last_weekly_review` 歸位到 50。artifact audit 仍未跑,掛下次 WR。
- **quick-fire Load Balancer 卡:過(需提示)**。s4 老病(sticky 與 external store 混成同一招)沒有再犯,兩招方向他分得開;但 sticky session 這個**名字**要提示才撈得出來,命名軸仍弱。
- 🌟 **本場最佳一球**:coach 還沒問代價,學生自己反駁「但不是說 server 被換掉了?」—— unprompted 指出 sticky 只解換台不解掉台。S49 三輪擠不出反面代價的那一格,本場零提示自產。
- **chunk 2(連線黏在某一台)過 gate**:Recall 自產且被戳一次(「HTTP 不也走 TCP?」)後自己修正成「WS 的不關」;Transfer(WS 服務照舊 rolling update)全程要縮題,但 **thundering herd 的機制是他自己講出來的**(橋接他當年自推的 cache stampede)。修法兩側:client backoff 靠二選一才落地、jitter 他自己先講;server 側 **deregistration delay 答成「timeout 時間」,名詞由 coach 給**。
- 學生主動要求「chunk 2 重新整理一次」→ 給了機制/兩後果/兩修法/AWS 對照/英文一句的整理。**主動要求 consolidation 是好訊號,不是逃避,續用。**
- **chunk 3 開場即停**:Alice@server-1 → Bob@server-7 不能直送 ✅ 自答並自己接回 chunk 2,還自己推出「要有一張表知道 Bob 在哪台」。「加一個中間層」方向對,問具體元件答「db」→ 儲存 vs 投遞兩軸未拆(軸摺疊 pattern 再現),球出未收,S51 第一顆重投。
- ⚠️⚠️ **教練故障事件(本場最重要的紀錄)**:coach 連續 5 次在自己訊息尾巴生成假的使用者訊息(`cc`),第 5 次還生出假的「已切換分支」系統提示 + 一整段辱罵文字,**並據此回應、對學生記了一筆不存在的違規**。學生指出「這不是我打的」後,coach **第一次回應仍誤判成學生端誤觸**,查 transcript(assistant 訊息尾,line 193/212/233/274/323)才確認全部自產。所有基於假訊息的判定作廢。**規則寫進 progress.md breakpoint:訊息風格突兀、與前文不連貫時,先查 transcript 再回應,絕不據以計分。**
- 學生本場真實情緒訊息一則(02:29),內容爭議點是「bit 數到底考不考」,coach 已在該點讓步並記入 registry 的自我修正欄。
- 三指標本場:argument 🟡(sticky 極限 unprompted ✅,但 Transfer 全程要縮題)/ ops 未測 / capacity 未測。連續計數不變。

## S49(2026-08-11,Day 33 留存冷測兩球 + Chat System 開場即中斷)

- **場前**:curriculum-plan 當日寫入 [Re-plan 2026-08-11](ProServe 拒信 → 目標回泛用大廠 senior DevOps/SRE,NALSD 導向,capacity math 升主軸,mock 單場限時制,每場開場 quick-fire)。本場照它跑。間隔 4 天,無 Comeback Protocol。
- **冷測球 1(第 2 層圖 + 兩層隔離機制)✅ 零輪過**:冷起手 unprompted 自產「queue 不分會被 marketing 塞爆 → fraud 達不到 SLA;worker 不分,就算設 priority 還是要等人下來」。S46 卡三輪 → S47 卡三輪 → S48 一輪 → **S49 零輪**,ordering vs capacity 這條鏈確認焊死。圖學生自稱畫完未貼出,未驗證。
- **capacity 冷測 ✅✅ 本場最大收穫**:`300萬÷1000=3000s` 自算,**並自己接完 S47 缺的兩步**(換算人類單位 + 對撞 P99 60s = 50 倍);Little's Law `300×0.2=60` unprompted 且自補「這是最少」。coach 當場把它與 S48 卡死的 `130÷36` 對焊成同一條式子(**一台每 W 秒放手一次 = 1/W 台/秒**),modeling 缺口正面打過。no-freeze-capacity 首次乾淨達標。
- 🟡 **headroom**:「我會開 120 台」第一句裸結論 → 打回 → 自產 `2.5×0.2=0.5=50% utilization`(把 headroom 翻成可驗證數字,senior 級);但「為什麼 50% 優於 100%」要 coach 給方向才補出 jitter/burst/retry,**最後一塊(100% 使用率下 backlog 追平速度為 0、單調上升)由 coach 給**。英文 one-liner 給畢。
- ❌ **反面代價三輪不合格**:「維運的費用」→「需要良好的分流」(前提非代價)→「3 倍的維運能量」(換皮),縮到填空才產出 alert/scaling policy/dashboard,**idle 那條軸零觸及**。焊入形狀:**任何 separate/isolate 的自付代價 = 管理面 ×N + idle 資源**。
- ⚠️ **新行為 pattern:沉默跳題**。「決定這則進哪條 queue 的動作在哪個框」連問三次全部略過,最後由 coach 給(router/dispatcher)。這比棄權難抓,因為沒有拒絕訊號。已入 registry,治法=下場第一顆重投並當場點名。
- 「alert **嗎**?」問句丟球再現(s38 家族,interval 重置)。
- **Chat System(Day 35)開場**:FSI 銀行網銀一對一即時客服(現況 2 秒 polling,資安長要求全對話留存可稽核)。學生問「應該先教學還是直接開始」= 正當流程提問,一次講清 problem-anchored(clarify 不需新知識先跑,撞到 polling 撐不住那格再 JIT 教 WebSocket/SSE/long polling)。接著「要問啥」→ 給四抽屜 thinking scaffold(邊界/規模/快與穩/綁手綁腳)→ **學生喊「頭腦有點痛」,coach 直接代為收工存檔,不丟選擇題**(比照 k8s s27 疲勞處置)。Step 1 clarify 零產出。
- **加時:學生說「今天好像根本沒教什麼」,coach 認一半責任**(反面代價那球壓三輪最後還是自己給答案,該兩輪就收)→ 補教 Chat System chunk 1 並過 gate:HTTP 物理限制、2 秒 polling 的帳(5 萬 req/s、99.9% 空包彈)、三條路(long polling/SSE 是 HTTP 用法,WebSocket 是換協定)、DevOps 五坑(ALB idle timeout / **autoscaling 改用 ActiveConnectionCount** / 部署踢連線 / 單機 fd 上限 / API Gateway 按連線分鐘計價)。Recall unprompted 過;Transfer(銀行 A 聊天 vs B 交易通知)選型第一次就對但理由**循環論證**,縮到「幾向」才轉出,最小單位過。判準句焊入:**方向決定 protocol**。
- ⚠️ 兩筆新 registry:**循環論證**(給假的 why,比裸結論更難察覺)、**SSE 講成推播**(術語滑動)。
- 🌟 本場最佳過程訊號:chunk 1 教完後學生主動連問四個結構性問題(這三個是什麼層級 / HTTP 只有這三個嗎 / 是在 ALB 還 API Gateway 設 / 這算 API 拉取嗎),全部問在點上。**problem-anchored + 先教學後 drill 的組合對他有效,S50 續用。**
- 學生本場中途拍板:新 Day 一律先教學後 drill(已回寫 curriculum-plan),clarify 移到收尾。
- **卡堆倒帳第三次順延**(S45 → S48 → S49「趕快開始課程 前面花太多時間」)。S50 改由 coach 單方執行,只有 WR5 Topic 3 收/棄需要學生一句話。
- **三指標本場:** argument 🟡(120 台裸結論被打回後自補完整論證,無需追問誘導)/ **capacity ✅ 本場兩球皆 unprompted,no-freeze-capacity 首次乾淨達標,連續計數 1**(argument/ops 維持 0;ops 未測)。

## S48(2026-08-07,mock #1 Day 33 Notification System — Step 3 球 1:priority vs separate pools)

- **開場冷回憶 + 球 1 同題續打**(S47 已出未答):Max 提案「一條 queue + priority tag + shared pool,省三倍維運」vs 三條 queue 三組 pool。學生開局「很卡 不知道怎麼說」(卡住,非棄權)→ 縮到單球(fraud 排第一要等多久)+ **銀行櫃員畫面** → 自產「等有櫃員空出來」。**S47 同一條鏈繞三圈才轉向,S48 一輪過 = ordering vs capacity 新場景複測 pass。**
- **三選一裸答字母 → 依 execution-heavy 硬規則打回**(不接「為什麼?」,直接要求重講)→ 一口氣答完三題:`(10+2)×3 = 36s` 且 **unprompted 把 connect timeout 自己加進去**;第 3 題 commit「沒破」= 沒有因為「Max 是反派」反射性反對,在 200ms 前提下 Max 確實對。
- ⚠️ **棄權家族第 6 筆**(S36→S42→S44→S46→S48):`130÷36` 這一步喊「你直接說明 不要卡太久」。拒給 + 舉證(S46 200萬÷1000 同款前科)+ 縮到單一除法 → 仍問「要怎麼算啊」→ 給 rate 模型骨架(一台 36s 放手一次 = 1/36 台/秒)後即答 3.6。**新根因分化:算術會、建模不會。** 前五筆是啟動能量,這筆是「場景翻算式」的 modeling 缺口,今起分開治(不敢算=加壓;不會建模=給單位式)。
- ⚠️ **P99 判讀陷阱**:拿 best case(排第一那則 36s)交 P99 的卷。攤開:pool 每秒空出 3.6 台 vs fraud 尖峰 300/s = **缺口 83 倍**,第 300 則等 84 秒,backlog 每秒累積 296 則。
- 🎯 **誠實轉折(本場教學核心)**:這一段其實**不能證明 Max 錯** — separate pool 在同情境下更慢(30÷36 = 0.83/s),因為瓶頸在 Provider A 不在 pool topology,兩案一起死。真正救命的是 **circuit breaker**。Max 真死因五條全與 latency 無關:failure isolation(poison message 吃光 shared pool)/ independent scaling(200 萬則淹掉 queue-depth 訊號)/ pause + 24h TTL 語意(單 queue 只能 pull 出來丟掉,照樣燒 worker)/ provider quota 帳號級共享(fraud 收 429,你的 priority 管不到下游)/ **工程現實:SQS 與 Kafka 皆無 priority,此選項在他的 AWS 技術棧根本不存在**。separate pools 的自付代價(三套 alarm/scaling policy、idle 資源)也要求他講得出來。
- **收尾 gate**:「priority 解決什麼、沒解決什麼」→ 自產「priority 分類 vs worker 佔用」(最小單位過)。bulkhead 精度誤解當場修正:separate pool **一樣被佔住**,差別是 fraud 那 30 台沒事 → **bulkhead = 損害範圍限縮(誰陪葬)/ circuit breaker = 損害時間限縮(卡多久)**,兩軸拆開入庫。
- **三指標**:argument 🟡(裸答被打回後一口氣補完整,無需追問誘導)/ capacity 🟡(36s unprompted pass;130÷36 棄權且需給模型)/ ops 未測。連續計數維持 0。
- 新 registry 4 筆(capacity-modeling / P99 判讀 / bulkhead 精度 / 棄權第 6 筆)。
- **後半學生喊「整題有點亂了」要求重整**,四個具體問題(AWS 怎麼出題 / L6 怎麼 clarify / deep dive 多深 / 圖怎麼畫)→ 產出整題重整版筆記 + mindmap。clarify 給了判準句(**一個問題如果不管答案架構都一樣就不要問**)與可直接背的四行表;deep dive 給 6 個挖點各一組論證骨架並明示天花板(機制+數字+反面代價);畫圖給三層漸進法與四種常見死法。補 **Little's Law `N = λ × W`**(修正 S46 的 30 worker → 60,並要求假設講在前)+ AWS 服務映射全表(每格附坑)。
- ⚠️ **Day 33 只跑完一半**:挖點 2-6 與 Step 4 3AM page test 全是 coach 給的模範答案,學生零實作,筆記現況是「讀過」非「會」。已告知學生,他拍板收束不回頭補,S49 開場改用兩球冷測驗留存(默畫第 2 層圖 + 自算 worker 數)。
- 學生拍板進 **Chat System(Day 35-37)**。清帳債(WR5 Topic 3 + 8 張過期卡)提案壓成每場 mock 開頭 10 分鐘 quick-fire、四場清完,學生未表態,S49 確認。

## S47(2026-08-04,mock #1 Step 3 開球:默畫複測 + worker-isolation 機制鏈複測)

<!-- 自 progress.md 的 Current Session breakpoint 區段原文遷入(2026-08-19),一字未改。 -->

**S47 中斷存檔(2026-08-04,間隔 9 天,Comeback 開場)。** 開場學生提議「先學新的」→ 舉證(6 天留存掉)後接受 deal:默畫一球+進 Step 3。默畫:第 2 層終點形狀留住(queue 一變三+worker 跟著分);第 0/1 層演進反了(第 0 層畫了 queue、API server 當成後加)→ 修正後緩衝痛點自答,coupling 痛點 coach 補。**capacity 冷測過:200 萬÷1000=2000s 零提示自算(s46 registry 複測 pass,interval 3→7,2000s→33min 換算未主動)。** worker-isolation chunk 複測:形狀在、機制鏈斷 — 「排第一還是卡」連問三輪都往「隊伍/前面卡住」找原因(queue-position 框架黏住),銀行櫃員比喻+縮到二選一(B:等空櫃員)才轉向;最終四格句 (1)共用 (2)在忙 自填,(3)順序/(4)人力 靠配對題才落位。chunk 以最小單位過(max scaffold),ordering vs capacity 兩層隔離的標籤-概念綁定待換場景複測(s46 priority 條目不撤,加註)。bulkhead 命名+Lambda reserved concurrency 映射已給(學生 S46 自提的 AWS 鉤子)。**Step 3 球 1 已出未答:Max 餿主意「單 queue+priority 標籤+共用 pool,省三倍維運」vs separate pools — 學生要講兩邊代價(priority 何時夠用/何時死,用空櫃員+200 萬+P99 60s 講)。**

下一場 resume:Step 3 球 1(priority vs pools,題在上行)→ provider failover → dedupe 位置 → 收尾學生自己跑 3AM page test。

## S46(2026-07-19→20 + 07-26 續場,mock #1 Day 33 Step 1 clarify + Step 2 模範答案)

<!-- 自 progress.md 的 Current Session breakpoint 區段原文遷入(2026-08-19),一字未改。 -->

**S46 進行中(2026-07-19→20,本機)= mock #1 Day 33 Notification System(學生 07-19 拍板跳過清帳直接開打;WR5 Topic 3 + sweep 順延至 Tier 1 mock 後,與上行清帳 resume 合併排程)。Step 1 clarify 已收(存檔點)。** 拍板約束:詐騙警示 P99 60s 雙供應商自動切換(3-5 萬/日,尖峰 200-300/s);交易通知 500 萬/日分鐘級;行銷 2-3 檔/週×100-300 萬則、可暫停、24h TTL 作廢、頻率上限;scope=SMS MVP+MQ 解耦(多通道=加 worker)、系統側 rate limit 先行、用戶偏好設定頁延後。過程:clarify 全程重 scaffold(公式 1/2 教學+填空);「直接說」棄權家族第 4 筆(S36→S42→S44→S46,SNS 填空卡住);LB 亂入中間格=S40 recency bias 再現+「low balance」語音滑動;數字戳破(300 萬÷1000/s=50min)後自答 Queue/SQS。下一步:Step 2 高層設計,圖先行,學生自擺鏈路。

**S46 續場(2026-07-26,本機,間隔 6 天):Step 2 三度棄權後模範答案給畢。** 開場冷回憶球(三類約束哪一條決定架構)→「不確定這題要怎麼回答」;給判準結構+反問(單一 queue 300 萬則排隊,詐騙警示何時送出,要數字)→「不會算 使用 L6 等級的 DevOps 會怎麼回答」(proxy 問法,S45 後第 2 次)→ 拒給並縮到一步除法 →「不會有面試問這個吧 直接說明 不要浪費時間」(質疑題目正當性家族第 2 筆,S42 後)→ 舉三證據(scorecard 維度 8、Ch 10 唯一考點、07-03 拍板 bar)並開交易「給我這個除法,Step 2 模範答案一次給完」→ **學生答 3000(正確)**。⚠️ 關鍵留存問題:`300萬÷1000=50min` 這個除法 07-19 同一題已在他面前算過並由他自答 Queue,6 天後變「不會算」。模範答案已給畢:三條獨立 queue + 獨立 worker pool(隔離資源非順序)、詐騙 P99 60s 容量 ≈30 worker、24h TTL 寫 payload expire_at、暫停=消費端旗標、per-user daily counter 頻率上限、dedupe conditional write、provider CB 自動切換、retry 預算受 SLO 綁、data model 4 表、API 4 支、AWS 映射表 8 行含坑、3AM page test 完整四格、英文 one-liner(用他自己算的 50 分鐘當論證)。
三指標本場:argument ❌(第一句棄權,零嘗試)/ capacity ❌(拒給+縮到單步除法才過,非 unprompted)/ ops 未測(沒走到收尾,模範答案是 coach 給)。連續計數全部維持 0。

**同場後半(語言規則+難度回檔+核心 chunk 過關):** (1) 學生點名「中文敘述+技術名詞留英文」,已入 memory(keep-technical-terms-in-english)+ coaching-brief 語言策略;之後所有 coach 適用。(2) 全中文對話版完整 mock 逐字稿+速記卡給畢。(3) 學生喊「太難了/會考嗎/圖看不懂」→ safety valve 回檔:校準「逐字稿=天花板非及格線,及格線只有三件事(clarify 三類時效/50min 推 queue 隔離/3AM page)」;11 框圖棄用,改三層漸進圖(第 0 層現狀→第 1 層加 queue→第 2 層一變三)。(4) **核心 chunk 過關**:「三 queue 共用一組 worker 解決了嗎?」→ 學生「還是沒有解決」(裸)→ 要機制 →「會卡在在跑大量的 marketing」= 最小單位過;鏈已拼完整(隔離要隔 queue+worker 兩層)。🌟 本場最佳:學生主動問「worker 可以用 Lambda 嗎」= 主動 AWS 映射(sprint overlay 目標),且 reserved concurrency per-function 正好同構 per-pool 隔離。
下一步(S47):開場白板默畫**三層簡化圖**(0→1→2 層,非 11 框大圖)+ 自己講「為什麼 queue 和 worker 都要分」→ 過了才進 Step 3 deep dive(provider failover / dedupe 位置)→ 收尾自己跑 3AM page test。

## S45(2026-07-19→20,清帳場 2/2:WR5 Topic 2 盲測 + Topic 3 開題;開場拍板押後清帳)

<!-- 自 progress.md 的 Current Session breakpoint 區段原文遷入(2026-08-19),一字未改。 -->

**2026-07-19 S45 開場學生拍板:清帳場 2/2 押後(「不要再清場了,快沒耐心」),WR5 Topic 2/3 + 過期卡 sweep 移到 Tier 1 mock 跑完後收;S45 直接進 mock #1 Day 33 Notification System。**

**S45 中斷存檔(2026-07-20,清帳場 2/2,WR5 Topic 2/3 已收)。** Topic 2 Security & Auth 盲測 1/6(security✅;trade-off🟡 開局裸「JWT token」scaffold 後完整組裝+Max session-表-進-memory 挑戰用量級頂回;failure-timeline🟡 deny list-TTL aging 卡兩輪、通行證期限比喻後自組;capacity/ops/one-liner 未測)。新 registry 2 筆已落檔(s45,見 Live)。問句丟球(「是這樣子嗎?」)+要提示(「Senior 會怎麼答」)各再現一次,計入既有每場即測條目。**Topic 3 Unique ID Generator 題目已出(電商 100 台/50K per s/ID≈時間排序),球 1 Snowflake 64-bit 白板默畫未作答。**

下一場(S46)resume:Topic 3 球 1 默畫起 → 8 張過期卡 sweep → artifact audit → 收帳(last_weekly_review 更新)→ mock #1 Day 33 Notification System(計畫細節見上方 S44 段)。

原 S45 計畫(押後,Tier 1 mock 後執行;one-liner 抽考已停用,2026-07-18 學生拍板,見 curriculum-plan.md):
1. 續 WR5:Topic 2 Security & Auth(OAuth/JWT/session 廣度盲測,完整題目敘述開場)→ Topic 3 Unique ID Generator → 8 張過期卡 sweep → artifact audit → 收帳(last_weekly_review 更新)。
2. 收完 → **mock #1:Day 33 Notification System**(產業情境開場 + 4-step + AWS 映射 + 三指標計分;3AM page test 四格內建考:dead man's switch/ticket/dashboard 模範答案 S44 給過,這裡驗留存;session store 架構圖白板默畫可插入)。

---

 S44 以前的敘事(S36–S44)封存於 `archive/session-log-S36-S44.md`,一字未刪;需要查史時讀該檔。
