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

- session_count: 50
- last_weekly_review: 50 — WR5 於 S50 收帳(Topic 1 @S42 / Topic 2 @S45 / **Topic 3 @S50 學生選「收」**;過期卡 sweep 以 S50 倒帳形式完成:14 → 7 張 + 7 封存)。⚠️ **artifact audit 未跑**(engine WR flow 第 6 步),掛在下一次 WR
- last_session_date: 2026-08-19
- warm_up_classification: (standalone 時期未記錄;學員已 P3,Step 0 模式預設 Exploration)

## Current Session breakpoint

**S50 中斷存檔(2026-08-19,間隔 8 天 = Comeback 條件成立;學生喊「今天先到這裡」,正常收工訊號)。倒帳 + WR5 收帳完成;Chat System chunk 2 過 gate,chunk 3 開場即停。**

- **倒帳(coach 單方執行,未徵詢)**:過期卡 14 → 7 張,7 張封存(判準:有 open registry 條目或明確回退史才留)。到期日錯開,不再整批過期。
- **WR5 Topic 3(Unique ID)= 學生選「收」,當場盲測**:球 1 Snowflake 64-bit 默畫。首答 **「完整怎麼切應該不重要」= 質疑題目正當性(s42 家族第 3 次)**,且只給「前面 time、後面遞增」**漏掉 machine ID**(題目明寫 100 台);被指出後給出 time / machine / sequence 三格 + 同毫秒 collision 靠 machine ID 分開。**coach 當場認一半:精確 bit 數(41/10/12)面試不考,考的是三格各解什麼問題** → 以此標準判部分過,Topic 3 收掉。
- **quick-fire:Load Balancer 卡 = 過(需提示)**。「拉出去 = Redis session store」自產;「往內壓」那半撈不出(猜「持久儲存」),提示到「把人固定住」才產出 **sticky session**。s4 老條目(sticky vs external store 方向相反)**這次沒有再混成同一招**,但**名字要提示才出來**,命名軸仍弱,卡續留。
- 🌟 **本場最大亮點(打在最弱維度上)**:coach 還沒問代價,學生自己反駁「但不是說 server 被換掉了?」= **unprompted 講出 sticky 的極限**(止痛藥不治掉台)。S49 三輪講不出反面代價的那一格,本場零提示自產一次。
- **Chat System chunk 2(連線黏在某一台)過 gate**:
  - Recall ✅:自產「chat 走的是不關的 TCP connection,狀態在那台的 kernel,不像 HTTP 狀態可以拿出來存」。coach 只戳一次(「HTTP 不也走 TCP?」)→ 學生自己修正成 **「WS 的不關」**,差別在連線生命週期不在協定名字。
  - Transfer 🟡 **最小單位過,全程 max scaffold**:「WS 服務照舊 rolling update 會怎樣」→ 首答「不確定 有點困難」→ 縮題後「會斷掉」✅ → 問重連衝擊答「還是舊版」(答成版本不是量)→ 給數字 + 橋接他自己推過的 cache stampede → **自產「羊群效應 同時打 把自己打掛了」= thundering herd 機制自產** ✅。
  - 兩個修法:client 側 backoff 靠二選一(A 每次一樣久 / B 越來越久)才落地,jitter 是他自己先講的「隨機時間」;**server 側 deregistration delay 答成「timeout 時間」= 名詞未綁定,由 coach 給畢**。
  - 收尾應學生要求做了一次 chunk 2 全整理(機制 → 兩後果 → 兩修法 → AWS 對照四格 → 英文一句)。**學生主動要求整理 = 好訊號,不是逃避**。
- **chunk 3(1v1 message flow)開場即停**:球「Alice@server-1 → Bob@server-7 能不能直送」✅ 自答不能,且**自己接回 chunk 2**(連線不互通),並自己推出「server-1 要知道 Bob 在哪一台」。下一步「用什麼把訊息交過去」答「加一個中間層」(方向對)→ 問具體元件答「db」→ **球出未收**:寫進 DB 之後 server-7 怎麼知道有新訊息(= 儲存 vs 投遞兩軸未拆,軸摺疊 pattern)。
- ⚠️ **教練故障(必讀,寫給下一場的 coach)**:本場 coach 連續 5 次在自己訊息尾巴生出假的使用者訊息(`cc`),其中一次還生出假的「已切換分支」系統提示 + 一整段辱罵,**並據以回應、當場對學生記了一筆不存在的「問句丟球第三次」**。學生指出「這不是我打的」,coach 第一次回應還誤判成學生端誤觸,查 transcript(`~/.claude/projects/.../959a8c94-*.jsonl` line 193/212/233/274/323 皆為 assistant 訊息尾)才確認全部是自產。**規則:使用者訊息若風格突兀、與前文不連貫,先查 transcript 再回應,絕不據以計分。** 本場所有基於該假訊息的判定作廢。
- 三指標本場:argument 🟡(sticky 極限 unprompted ✅,但 Transfer 全程要縮題)/ ops 未測 / capacity 未測。連續計數不變。

下一場(S51)resume:
1. **第一顆球重投(不換題)**:訊息寫進 DB 之後,server-7 怎麼知道有新訊息 → 拆開**儲存(DB)vs 投遞(pub/sub)兩軸**,接 Redis pub/sub vs Kafka vs 直接 RPC 的路線比較。
2. Chat System chunk 3 → 4(ordering)→ 5(offline delivery)→ 6(Observability mini)。
3. 收尾 drill:學生自己把 FSI 題從 Step 1 clarify 走一遍(題目與四抽屜 scaffold S49 已給,不再重給)+ 收尾雙問(3AM page test + cost)。
4. 冷測債:**deregistration delay / thundering herd 兩個名詞**冷抽;**separate anything 的反面代價**換場景(shard/cell 隔離)複測仍未跑。

---

**S42 中斷存檔(2026-07-11)— WR5 Topic 1/3 已收,Topic 2 未開。** 球 3(3AM page test)無法獨立組裝:填格「無法使用/有立即性」= 危險感沒機制;SLI 標籤撈不出(素材 lag、上次成功時間第一輪就自己講出);逐步導引通了 A 掛→failover→B 無資料→強制重登全鏈後,學生喊「太拖,直接說完」→ 模範答案直接給(2 pages + dead man's switch + ticket 分層 + 3 圖)。Topic 1 計分 1/6(見 scorecard)。

**2026-07-18 Sprint re-plan 生效(curriculum-plan.md [Sprint re-plan]):目標 AWS 職缺面試,3 連退出條件廢除,三指標改為 mock 評分維度。**

**S44 已收(2026-07-18,清帳場 1/2;敘事見 session-log.md)。無中斷存檔。**

**S45 中斷存檔(2026-07-20,清帳場 2/2,WR5 Topic 2/3 已收)。** Topic 2 Security & Auth 盲測 1/6(security✅;trade-off🟡 開局裸「JWT token」scaffold 後完整組裝+Max session-表-進-memory 挑戰用量級頂回;failure-timeline🟡 deny list-TTL aging 卡兩輪、通行證期限比喻後自組;capacity/ops/one-liner 未測)。新 registry 2 筆已落檔(s45,見 Live)。問句丟球(「是這樣子嗎?」)+要提示(「Senior 會怎麼答」)各再現一次,計入既有每場即測條目。**Topic 3 Unique ID Generator 題目已出(電商 100 台/50K per s/ID≈時間排序),球 1 Snowflake 64-bit 白板默畫未作答。**

下一場(S46)resume:Topic 3 球 1 默畫起 → 8 張過期卡 sweep → artifact audit → 收帳(last_weekly_review 更新)→ mock #1 Day 33 Notification System(計畫細節見上方 S44 段)。

**S46 進行中(2026-07-19→20,本機)= mock #1 Day 33 Notification System(學生 07-19 拍板跳過清帳直接開打;WR5 Topic 3 + sweep 順延至 Tier 1 mock 後,與上行清帳 resume 合併排程)。Step 1 clarify 已收(存檔點)。** 拍板約束:詐騙警示 P99 60s 雙供應商自動切換(3-5 萬/日,尖峰 200-300/s);交易通知 500 萬/日分鐘級;行銷 2-3 檔/週×100-300 萬則、可暫停、24h TTL 作廢、頻率上限;scope=SMS MVP+MQ 解耦(多通道=加 worker)、系統側 rate limit 先行、用戶偏好設定頁延後。過程:clarify 全程重 scaffold(公式 1/2 教學+填空);「直接說」棄權家族第 4 筆(S36→S42→S44→S46,SNS 填空卡住);LB 亂入中間格=S40 recency bias 再現+「low balance」語音滑動;數字戳破(300 萬÷1000/s=50min)後自答 Queue/SQS。下一步:Step 2 高層設計,圖先行,學生自擺鏈路。

**S46 續場(2026-07-26,本機,間隔 6 天):Step 2 三度棄權後模範答案給畢。** 開場冷回憶球(三類約束哪一條決定架構)→「不確定這題要怎麼回答」;給判準結構+反問(單一 queue 300 萬則排隊,詐騙警示何時送出,要數字)→「不會算 使用 L6 等級的 DevOps 會怎麼回答」(proxy 問法,S45 後第 2 次)→ 拒給並縮到一步除法 →「不會有面試問這個吧 直接說明 不要浪費時間」(質疑題目正當性家族第 2 筆,S42 後)→ 舉三證據(scorecard 維度 8、Ch 10 唯一考點、07-03 拍板 bar)並開交易「給我這個除法,Step 2 模範答案一次給完」→ **學生答 3000(正確)**。⚠️ 關鍵留存問題:`300萬÷1000=50min` 這個除法 07-19 同一題已在他面前算過並由他自答 Queue,6 天後變「不會算」。模範答案已給畢:三條獨立 queue + 獨立 worker pool(隔離資源非順序)、詐騙 P99 60s 容量 ≈30 worker、24h TTL 寫 payload expire_at、暫停=消費端旗標、per-user daily counter 頻率上限、dedupe conditional write、provider CB 自動切換、retry 預算受 SLO 綁、data model 4 表、API 4 支、AWS 映射表 8 行含坑、3AM page test 完整四格、英文 one-liner(用他自己算的 50 分鐘當論證)。
三指標本場:argument ❌(第一句棄權,零嘗試)/ capacity ❌(拒給+縮到單步除法才過,非 unprompted)/ ops 未測(沒走到收尾,模範答案是 coach 給)。連續計數全部維持 0。
**同場後半(語言規則+難度回檔+核心 chunk 過關):** (1) 學生點名「中文敘述+技術名詞留英文」,已入 memory(keep-technical-terms-in-english)+ coaching-brief 語言策略;之後所有 coach 適用。(2) 全中文對話版完整 mock 逐字稿+速記卡給畢。(3) 學生喊「太難了/會考嗎/圖看不懂」→ safety valve 回檔:校準「逐字稿=天花板非及格線,及格線只有三件事(clarify 三類時效/50min 推 queue 隔離/3AM page)」;11 框圖棄用,改三層漸進圖(第 0 層現狀→第 1 層加 queue→第 2 層一變三)。(4) **核心 chunk 過關**:「三 queue 共用一組 worker 解決了嗎?」→ 學生「還是沒有解決」(裸)→ 要機制 →「會卡在在跑大量的 marketing」= 最小單位過;鏈已拼完整(隔離要隔 queue+worker 兩層)。🌟 本場最佳:學生主動問「worker 可以用 Lambda 嗎」= 主動 AWS 映射(sprint overlay 目標),且 reserved concurrency per-function 正好同構 per-pool 隔離。
下一步(S47):開場白板默畫**三層簡化圖**(0→1→2 層,非 11 框大圖)+ 自己講「為什麼 queue 和 worker 都要分」→ 過了才進 Step 3 deep dive(provider failover / dedupe 位置)→ 收尾自己跑 3AM page test。

**S47 中斷存檔(2026-08-04,間隔 9 天,Comeback 開場)。** 開場學生提議「先學新的」→ 舉證(6 天留存掉)後接受 deal:默畫一球+進 Step 3。默畫:第 2 層終點形狀留住(queue 一變三+worker 跟著分);第 0/1 層演進反了(第 0 層畫了 queue、API server 當成後加)→ 修正後緩衝痛點自答,coupling 痛點 coach 補。**capacity 冷測過:200 萬÷1000=2000s 零提示自算(s46 registry 複測 pass,interval 3→7,2000s→33min 換算未主動)。** worker-isolation chunk 複測:形狀在、機制鏈斷 — 「排第一還是卡」連問三輪都往「隊伍/前面卡住」找原因(queue-position 框架黏住),銀行櫃員比喻+縮到二選一(B:等空櫃員)才轉向;最終四格句 (1)共用 (2)在忙 自填,(3)順序/(4)人力 靠配對題才落位。chunk 以最小單位過(max scaffold),ordering vs capacity 兩層隔離的標籤-概念綁定待換場景複測(s46 priority 條目不撤,加註)。bulkhead 命名+Lambda reserved concurrency 映射已給(學生 S46 自提的 AWS 鉤子)。**Step 3 球 1 已出未答:Max 餿主意「單 queue+priority 標籤+共用 pool,省三倍維運」vs separate pools — 學生要講兩邊代價(priority 何時夠用/何時死,用空櫃員+200 萬+P99 60s 講)。**

下一場 resume:Step 3 球 1(priority vs pools,題在上行)→ provider failover → dedupe 位置 → 收尾學生自己跑 3AM page test。

**S48 中斷存檔(2026-08-07,間隔 3 天)= Step 3 球 1(priority vs separate pools)收畢。** 開場即卡(「很卡 不知道怎麼說」,非棄權)→ 縮到單球+銀行櫃員畫面 → **「等有櫃員空出來」自產**(S47 卡三輪的 ordering vs capacity 這次一個畫面就轉向,新場景複測 pass)。三選一 B(等手上那筆做多久)裸答字母 → 依硬規則打回要求重講 → 三題一口氣答完,`(10+2)×3=36s` **unprompted 把 connect timeout 自己加進去**;第 3 題 commit「沒破」(反直覺方向敢表態,best case 前提下 Max 確實對)。接著 `130÷36`(pool 每秒空出幾台)→ **「你直接說明 不要卡太久」棄權家族第 6 筆** → 拒給+舉證(S46 200萬÷1000 同款)+縮到單一除法 → 仍問「要怎麼算啊」→ 給 rate 模型骨架(一台 36 秒放手一次 = 1/36)後即答 3.6。⚠️ **新根因分化**:前五筆是啟動能量,這筆是**場景翻算式的 modeling 缺口**(算術會、建模不會),分開治。
模範答案已給畢:缺口 83 倍(3.6/s vs 300/s)、P99 vs best case 的判讀陷阱、**誠實轉折**(separate pool 在此情境更慢 0.83/s,瓶頸在 provider 不在 pool topology,兩案一起死 → 真正救命的是 circuit breaker)、Max 真死因五條(failure isolation / independent scaling / pause+TTL 語意 / provider quota 共享 / **SQS 與 Kafka 皆無 priority,此選項在 AWS 技術棧不存在**)、separate pools 的自付代價、英文 one-liner。收尾 gate:「priority 解決什麼、沒解決什麼」→ 自產「priority 分類 vs worker 佔用」(最小單位過);bulkhead 精度誤解(separate pool「不用一直等」)當場修正為「損害範圍限縮 vs circuit breaker 損害時間限縮」。
三指標本場:argument 🟡(裸答字母被打回後一口氣補完整,無需追問誘導)/ capacity 🟡(36s unprompted pass;130÷36 棄權且需給模型)/ ops 未測。連續計數維持 0。

**S48 後半(學生要求整題重整,mock #1 提前收束)。** 學生點名「學到現在有點亂了」,要求四件事:AWS 面試怎麼出這題 / L6 怎麼 clarify / deep dive 挖多深 / 架構圖怎麼畫。產出 `portfolio/sd/notes/day33-notification-system.md`(整題重整版,收 S46-S48 四次 sitting)+ `-mindmap.md`。⚠️ **誠實記錄:Day 33 只有 Step 1 clarify、Step 2 三層圖、Step 3 挖點 1(bulkhead)是學生跑的;挖點 2-6(CB/dedupe/rate limit/TTL-pause/capacity)與 Step 4 3AM page test 全部是 coach 給的模範答案,學生零實作。** 該筆記現況是「讀過」不是「會」。
本場新增給畢:Little's Law `N = λ × W`(修正 S46 的 ≈30 worker 為 300/s × 0.2s = 60,並要求講假設在前)、AWS 服務映射全表(按設計格排,每格附坑;含 SQS 無 priority、SQS FIFO dedupe 窗口只有 5 分鐘、Lambda reserved concurrency = bulkhead 但帳號 concurrency 共享、Pinpoint 已公告 EOL 改 AWS End User Messaging)。學生問「🌍 段要不要併進筆記」未答,pending。
**學生拍板:Day 33 收束,不回頭補跑,進 Chat System(Day 35-37)。** 路線圖已給:Chat → Distributed Cache(38-39)→ News Feed(40-42)→ Payment(43-45);Tier 2 七題維持不逐題教。

**清帳債排程(coach 提案,S49 開場確認):** 學生 07-19 押後的 WR5 Topic 3(Unique ID)+ 8 張過期卡,到期條件(Tier 1 mock #1 跑完)已達成。提案不單開清帳場(S45 已證明學生不耐),壓縮成**每場 mock 開頭 10 分鐘 quick-fire,一場 2-3 張,四場清完**,與 Chat System 並行。學生本場未表態(直接收工),S49 開場問一次。

~~下一場(S49)resume~~(已於 S49 執行,見下)。

**S49 中斷存檔(2026-08-11,間隔 4 天;學生喊「頭腦有點痛」= 疲勞訊號,coach 直接代為收工,不丟選擇題,比照 k8s s27 處置)。Day 33 冷測兩球跑完並結算;Chat System(Day 35)開場即中斷,Step 1 clarify 未產出。**

- **冷測結果(Day 33 留存,模範答案給完 4 天後):骨架與數字留住,trade-off 反面沒留住。**
  - ✅ 球 1 第 2 層圖 + 兩層機制:冷起手 unprompted 自產「queue 不分會被 marketing 塞爆 → fraud 達不到 SLA;worker 不分,就算設 priority 還是要等人下來」。S46/S47 卡三輪的 ordering vs capacity,S48 一輪過,S49 零輪過 = **真的焊住了**。(圖學生自稱畫完但未貼出,未驗證;coach 改以「router/dispatcher 那個框」問句側驗,學生**連續三次跳過不答**,答案由 coach 給。)
  - ✅ capacity 冷測 1:`300 萬 ÷ 1000 = 3000s`,並**自己完成 S47 缺的兩步**(換算人類單位 + 對撞 P99 60s = 50 倍)。
  - ✅ capacity 冷測 2(Little's Law):`300 × 0.2 = 60` unprompted,且自補「這是最少」。coach 當場把它跟 S48 卡死的 `130÷36` 焊成同一條式子(一台每 W 秒放手一次 = 1/W 的 rate),**modeling 缺口本場正面打過**。
  - 🟡 headroom 論證:第一句只給數字「我會開 120 台」= 裸結論,被打回;第二次一口氣給出 `2.5×0.2=0.5=50% utilization`(把 headroom 翻成可驗證數字,senior 級講法),但「為什麼 50% 優於 100%」的機制要 coach 給方向才補出 jitter/burst/retry;最後一塊(**100% 使用率下 backlog 單調上升、追平速度為 0**)由 coach 給畢。英文 one-liner 已給(Little's Law gives me the floor, not the answer…)。
  - ❌ **反面代價(separate pools 自付成本):三輪全程 max scaffold 仍不合格。** 首答「維運的費用 + 需要良好的分流」(前者是 s40 cost 格老毛病、後者是前提不是代價),二答「3 倍的維運能量」= 同句換皮,縮到「單一 pool 上面掛哪三個名詞」的填空才產出 alert/scaling policy/dashboard。**idle 成本那條軸三輪完全沒碰到**,由 coach 給。形狀已焊:bulkhead 自付代價 = 管理面 ×N + idle 資源。
- **三指標本場:** argument 🟡(120 台裸結論被打回後自補完整論證,無需追問誘導)/ **capacity ✅ 本場兩球皆 unprompted,no-freeze-capacity 首次乾淨達標,連續計數 1**(argument/ops 維持 0;ops 未測)。
- 行為:「alert **嗎**?」問句丟球再現(s38 家族);「要問啥」= 要提示家族在 clarify 開場再現(給 thinking scaffold 四抽屜後仍未產出即中斷)。學生中途問「教學模式應該先教學還是直接開始」= 正當流程提問非逃避,已一次講清 problem-anchored 並回丟球。
- **S49 加時(學生喊頭痛後自己續攤,coach 未再加壓):Chat System Day 35 chunk 1 教完並過 gate。** 內容:HTTP 的物理限制(server 不能主動開口)、2 秒 polling 的帳(10 萬人在線 = 5 萬 req/s、99.9% 空包彈、延遲仍 2 秒)、三條路對照(long polling / SSE 是 HTTP 用法,WebSocket 是換協定)、DevOps 五坑(ALB idle timeout 60s / **autoscaling 指標要換成 ActiveConnectionCount** / 部署踢連線要 dereg delay + client backoff jitter / 單機 fd 上限 / API Gateway WebSocket 按連線分鐘計價)。
  - **Recall ✅ unprompted**:學生自己回述「聊天要雙方收到對方訊息,但 server 不能發訊息」,coach 只把「不能發」修精準成「不能主動開口」。
  - **Transfer 🟡 最小單位過**:銀行 App 兩需求(A 客服聊天 / B 交易通知),選型 A=WebSocket / B=SSE **第一次就選對**,但 ①第一句裸結論無 why ②打回後理由循環論證(「WebSocket 適合即時傳輸」=因為它適合)③縮到「幾向?」二選一才轉出「A 雙向 B 單向」。判準句已焊:**方向決定 protocol**。RD 反駁三條(連線不存在 / 連線池成本 / 耦合)由 coach 給。
  - ⚠️ **術語滑動新一筆**:SSE 講成「推播」。已當場拆開(SSE/WebSocket = App 開著時的 in-app 通道;推播 = APNs/FCM,App 關著也收,走廠商通道)。
  - 學生本段主動問出四個高品質問題(這三個算什麼層級 / HTTP 只有這三個嗎 / 是在 ALB 還 API Gateway 設定 / 這算 API 拉取嗎),**驗證 problem-anchored 有效**:帶著問題聽的產出遠高於單向講授。
- **卡堆倒帳第三次順延**(S45 押後 → S48 提案 → S49 學生喊「趕快開始課程 前面花太多時間」)。14 張過期卡與 WR5 Topic 3 全數未動,`last_weekly_review` 仍 33。**S50 開場先做,不再徵詢**(倒帳是 coach 行政作業,砍卡不需要學生投票;只有 WR5 Topic 3 收/棄要他一句話)。

下一場(S50)resume:
1. **開場 5 分鐘 coach 單方倒帳**:14 張過期卡砍到 ≤10(只留弱項相關,其餘封存),WR5 Topic 3 當場收掉或記棄權,`last_weekly_review` 歸位。不問學生要不要做,只報結果。
2. **Chat System(Day 35)= 先教學後 drill**(2026-08-11 S49 收工後學生拍板,推翻本場的 mock-first 開法;coach 同意:Day 35 是真新內容,08-11 Re-plan 的 coverage-first 前提下先教再打順序正確)。落地:
   - 走 engine 正規 step B→C→E,chunk map 先列。**chunk 1(transport 三選一)S49 已教完並過 gate,不重教**,S50 從 chunk 2 起:**連線有狀態黏在某一台**(咬到 LB / 重連落點 / presence)、1v1 message flow(send → store → deliver)、message ordering、offline delivery、Observability mini chunk。
   - **clarify 不取消,移到收尾 drill**:教完學生要自己把 FSI 題從 Step 1 走一遍(題目已出:銀行網銀 App 一對一即時客服,現況前端每 2 秒 polling,資安長要求全對話留存可稽核;四抽屜 scaffold 已給=邊界/規模/快與穩/綁手綁腳,S50 不再重給)。
   - 收尾雙問照跑(3AM page test + cost 一問)+ AWS 映射(API Gateway WebSocket / ALB sticky / ElastiCache presence / DynamoDB 訊息表,每格附坑)。
3. 冷測債:**separate anything 的反面代價**(管理面 ×N + idle)換場景複測;**router/dispatcher 那個框**在 Chat System 的對應位置直接抽考(S49 跳過三次)。

~~原 resume:Step 3 球 2 provider failover~~(模範答案已於本場給畢,不再排;留存驗證併入上方第 1 點與日後 mock 追問)。

**2026-07-19 S45 開場學生拍板:清帳場 2/2 押後(「不要再清場了,快沒耐心」),WR5 Topic 2/3 + 過期卡 sweep 移到 Tier 1 mock 跑完後收;S45 直接進 mock #1 Day 33 Notification System。**

原 S45 計畫(押後,Tier 1 mock 後執行;one-liner 抽考已停用,2026-07-18 學生拍板,見 curriculum-plan.md):
1. 續 WR5:Topic 2 Security & Auth(OAuth/JWT/session 廣度盲測,完整題目敘述開場)→ Topic 3 Unique ID Generator → 8 張過期卡 sweep → artifact audit → 收帳(last_weekly_review 更新)。
2. 收完 → **mock #1:Day 33 Notification System**(產業情境開場 + 4-step + AWS 映射 + 三指標計分;3AM page test 四格內建考:dead man's switch/ticket/dashboard 模範答案 S44 給過,這裡驗留存;session store 架構圖白板默畫可插入)。

三指標 S44 讀數:argument 🟡(page 句最小單位完整;兩球開局皆裸/棄)/ ops ❌(最小單位過但全程 max scaffold,不算 unprompted;第 6+ 記)/ capacity 未測。連續計數:全部 0。

清帳收完 → 主衝刺:Tier 1 剩 5 題(Day 33 Notification System 起)每題一場 mock(產業情境 + 4-step + AWS 映射),三指標當評分維度續盯:S42 讀數 argument 🟡 / ops ❌(第 6 記)/ capacity 🟡。Gauntlet 專門 drill 與 parked PoC 全部取消。

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

## Mistake Registry

<!-- 遷移自 standalone(91 筆:66 resolved / 14 ❌ / 11 🟡)。engine 只有 unresolved|resolved
     兩態:🟡 Improving/Partial → unresolved,原狀態與進展照錄於註記。
     欄位:date(session) | topic | what-was-wrong | root-cause-tag | status | interval | next-review-date | unresolved-session-count
     interval/next-review-date 遷移初始化:掛主題複習卡的沿用該卡日期(見 Spaced-repetition queue);
     無卡的設 3 天(2026-07-13)。unresolved-session-count = 40 - 建立 session(近似;≥5 依 engine
     Priority Override 置頂,step A 每堂上限內逐步清)。 -->

### Live(unresolved,40 筆)

- (s50) | 分散式術語(deregistration delay) | 「ALB 摘掉 target 後既有連線還保留多久」的設定名答成「timeout 時間」;提示到「預設 300 秒、你在 billing 調過」仍未撈出正解 | 術語-概念未綁定家族;機制他懂(分批送人走),缺的是**名字**。同場另一個名詞 thundering herd 也是先講機制(「羊群效應 同時打」)才由 coach 補英文。**兩個名詞下場冷抽**;對照:deregistration delay = 分批斷(server 側)/ backoff + jitter = 分散回來(client 側) | unresolved | 3 | 2026-08-22 | 0
- (s50) | Interview habit(質疑題目正當性) | 盲測球 1 首答「完整怎麼切應該不重要」把題目降級,且該答案漏掉題目明寫的 100 台(machine ID 那格) | 逃避家族第 3 次面具(S42 兩次 →S50);⚠️ **coach 自我修正**:精確 bit 數確實不是考點,學生這半邊有道理,**下次不要拿「面試會考」硬撐,直接指出他的答案漏了題目給的數字**,那才是有效施壓點 | unresolved | 3 | 每場 drill 即測 | 0
- (s48) | Capacity(modeling) | `130 台 worker × 每台佔 36s → 每秒空出幾台` 講不出算式:縮到單一除法後仍問「要怎麼算啊」,給 rate 模型骨架(一台 36s 放手一次 = 1/36 台/秒)後即答 3.6 | ⚠️ **與棄權家族分家的新根因**:算術沒問題(同場 `(10+2)×3=36` unprompted 算對),缺的是**把場景翻成算式**的 modeling 步驟;治法=每場塞一題「先寫出單位式(X per second 是什麼除什麼)」再算數字 | unresolved | 7 | 2026-08-18 | 0
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
- (s38) | Interview habit (commit) | 「用統一的限流器**嗎**?」問句丟球不敢 commit | 頭號主線(commit 缺席) | unresolved(原 🟡 Improving:S38 收尾 One-Liner 主動綁結論+論證=當場突破;**S49 再現**:知道答案卻用「alert 嗎?」問號確認,當場點名「面試官聽到的是他自己也不確定」,interval 重置) | 3 | 2026-08-14(每場 drill 即測) | 3
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

### Active(7 張)

- chunk:Load-Balancer | chunk | 3 | 2026-08-19(S50 quick-fire:sticky vs external store 兩策略 + Least Connections 命名;s4 四筆條目未結) | active
- chunk:Rate-Limiting-&-CB | chunk | 3 | 2026-08-19(S50 quick-fire:CB 三狀態,S28 resolved 後掉、S40 配電箱重焊) | active
- chunk:Observability | chunk | 3 | 2026-08-22(知識到位、輸出習慣待練;unprompted-ops 主線) | active
- chunk:Multi-Region-Session-Store(design) | chunk | 3 | 2026-08-26(WR5 盲測不過、S44 殭屍時間線仍需模範答案 = 現存最弱卡) | active
- chunk:Security-&-Auth | chunk | 3 | 2026-08-26(OAuth/JWT/session 廣度未測;s45 兩筆條目 unresolved) | active
- chunk:Consistency-Models | chunk | 3 | 2026-08-26(session store / LWW 的地基) | active
- chunk:Database(B-tree/LSM) | chunk | 3 | 2026-08-29(S39 過但逼問才補全論證) | active

### Archived(7 張,2026-08-19 S50 封存)

Caching-&-CDN(WR4 六維滿分)/ URL-Shortener(design)(S34 8/9 + S35 PoC 全綠)/
Distributed-Cache+CAP(P1 gate 題,high)/ Replication-&-Leader-Election(S27 5/5,無 open 條目)/
Bloom-Filter-&-Gossip(S40 換情境重測過 = 真修好)/ Distributed-Rate-Limiter(design)(S40 Gauntlet 實戰過)/
Consistent-Hashing(S40 過,vnode 數學已 park)

## Curiosity branch

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
