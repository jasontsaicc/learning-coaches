# SD Curriculum Plan(戰略層,advisory)

<!-- Advisory 性質:runtime 真相永遠在 progress.md,衝突時現場贏、回寫這份。
     整併自 standalone progress.md 的 Learning Mode 區段(S23/S36/S37 三次拍板);
     更早的 curriculum-roadmap.md 與 planning-review.md 已 superseded,verbatim 存
     archive/pre-migration/。教法層(怎麼教這個學生)在 coaching-brief.md,本檔是課什麼、
     什麼順序、多深。 -->

## North Star 對齊

~~無明確面試日期 → 深度優先,全課表照走,預估 2026 年 12 月初完課~~
**(2026-07-18 改向:目標鎖定 AWS 職缺面試,深度優先讓位給面試就緒。見 Sprint re-plan。)**
Readiness 領先 curriculum position 的原則不變(見 scorecard-dims 的 Readiness Report 規則)。

## Learning Mode(S23 拍板,仍生效)

**問題錨定 + 深度天花板(Problem-anchored + Depth Ceiling)**

背景:學生在純理論主題(consistency models、consistent hashing 的 vnodes 數學)磨太久,
公式/形式化深度對面試零回報,導致進度緩慢 + 學習痛苦。

1. **深度天花板三問**(現為 engine Depth Ceiling,教練主動執行):(a) 面試官會問嗎?(b) 這層深度能讓回答更好嗎?(c) 卡住是缺地基還是想完美?任一「不會/不能/想完美」→ park 到 curiosity branch。
2. **理論期壓縮**:理論型 building block 用「概念 + 一句話 + 一個 trade-off」快速模式,PoC 降級 Light/Discussion。
3. **題目驅動(pull)**:理論密集段用一個設計題當錨(P2 用 Design a Distributed Cache),理論 just-in-time 拉進來(現為 curriculum hook 的 Problem-Anchored Mode)。
4. 面試考 breadth of mental models + trade-off reasoning,不是 CS 理論深度(形式證明 = PhD 範圍,不學)。

## Execution-Heavy overlay(S37 拍板;2026-07-18 起被 Sprint re-plan 修改)

Phase 2 後已無知識缺口只有執行缺口 → 暫停「每場一個新 archetype」的 acquisition 節奏,
改 drill 為主(**Drill Gauntlet**)。首攻 #1「結論不給論證」。完整 protocol 與評分錨
(tier-1 strong-hire bar、L3 預設)見 `coaching-brief.md` [Execution-Heavy Mode]。
~~退出條件:三指標各 3 連達標後回課表節奏~~ **3 連退出條件廢除(S40-S43 四場零進展,
擋住所有新內容 = 進度緩慢的根源)。三指標保留為每場 mock 的評分維度,不再擋進度。**

## Scope decision(2026-07-02,S36 後 plan review)

- 從外部訓練營課表補進 3 個缺的 archetype(Day 54-59:Ticket Booking / Top-K / Ride Matching),Phase 4 順延為 Day 60-69。課表總長 69 units(含 Brownfield Migration Day 62-63)。
- 其餘訓練營題目(Dropbox/YouTube/Twitter/A-B Testing 等)= 既有 pattern 組裝,不排課;對照表見 `pattern-map.md`(面試前確認每個 pattern 都能講,碰到沒練過的題拆 pattern 再組裝)。
- Parked PoC triage:留 distributed cache(Day 38-39)+ rate limiter(Day 31-32 的 capacity 補測);放掉 Circuit Breaker 獨立 PoC(概念已 5/5,邊際回報低)。Snowflake Light PoC(Day 30)park 中,排 Gauntlet 之後。

## Conditional Sprint overlay(2026-07-17;背景修正 2026-07-18)

背景修正(2026-07-18 現場確認):**尚未投遞**,原記載「已投遞」不符,以本行為準。目標職缺
仍是雲端原廠 consultant(delivery 導向)。該 loop 型態:behavioral 佔比 ~50%、architecture
case 用客戶情境包裝、coding 輕量。兩層外皮照常生效於所有 mock/drill:

1. **AWS 服務映射層**:每個元件收尾追問「在 AWS 上這是什麼」(LB→ALB/NLB、cache→ElastiCache、
   MQ→SQS/Kinesis、KV→DynamoDB、blob→S3)。同時綁 Well-Architected 六支柱詞彙:failure
   timeline=reliability、3AM page test=operational excellence、cost 格=cost optimization。
   學員 AWS 底子在,這層是便宜的詞彙映射,不是新知識。
2. **產業情境包裝**:drill 題目改用「[半導體/製造/FSI/公部門] 客戶要上雲/遷移 X」開場。
   各產業主導約束:半導體=IP 保護+HPC burst;製造=OT/edge+產線不能停;FSI=法遵+data
   residency;公部門=資料分級+主權。考點是 discovery 流程(先 clarify 約束再開藥方)=
   Step 1 頭號主線的變體,正中現有病灶,不是新增負擔。
3. **一次性插課(約半場)**:migration 詞彙 — Assess/Mobilize/Migrate 三階段、7 Rs、
   landing zone/Control Tower。之後靠 drill 外皮重複,不獨立成 chunk。

收到具體面試日期 → 走下方 Re-plan triggers 第一條(壓縮 Tier 2、mock 連發)。
求職材料(履歷、STAR 故事庫)不進本 repo,只在學員私人機器;本 overlay 僅含教學面。

## Sprint re-plan(2026-07-18 拍板,生效中)

學員明確轉向:目標 AWS 職缺面試,快速過完、不糾結。深度優先前提失效,改面試就緒優先。

**砍掉(不再排課):**
- Gauntlet 三指標 3 連退出條件(見上;三指標降級為 mock 評分維度)。
- 所有 parked PoC:Snowflake(Day 30)、distributed cache(Day 38-39)、rate limiter capacity 補測。面試前不做。
- Tier 2 七題逐題教學。改 pattern-map 驗證:碰到沒練過的題能拆 pattern 再組裝即可。

**衝刺排程(~2.2 場/週,估 3-4 週):**
1. 清帳(1-2 場):WR5 剩餘(Topic 2 Security & Auth、Topic 3 Unique ID)+ 8 張過期卡
   壓成 quick-fire sweep;One-Liner 複測(Session Revocation)+ 3AM page test 換題複測照跑。
   Migration 詞彙半場插課(7 Rs、Assess/Mobilize/Migrate、landing zone)併入。
2. 主衝刺(5 場):Tier 1 剩 5 題(Day 33+ Notification System 起)每題壓成一場 mock:
   產業情境開場 → 4-step → AWS 映射收尾 → 三指標計分。理論 just-in-time,面試深度封頂,無 PoC。
3. 之後全 mock 連發(P4 模式提前),混 pattern-map 抽題。

**維持不變:** engine 各 gate 的嚴格度(壓縮的是範圍與順序,不是 rigor)、AWS 映射+產業
外皮、L3 評分錨、registry/複習卡機制(排程壓縮進清帳場與 mock 開場)。

**One-liner 抽考停用(2026-07-18 學生拍板):** 開場抽考段與英文一句輸出練習全面移除。
Coach 立場記錄:反對完全移除(S19/S43 兩筆壓力下英文 retrieval 斷線證據;建議改嵌入
mock),學生決策完全拿掉,照辦。庫檔保留作自修素材。拿到具體面試日期時本決策重新檢視一次。

**Repo 外提醒:** 尚未投遞 → 照 career plan,履歷+內推投遞先於學習衝刺;behavioral/LP
故事庫與口說(fsi-devops-english)是這個 loop 的另一半,不在本 repo 排程。

## Re-plan triggers

- 拿到具體面試日期 → 再壓縮:清帳收斂成 1 場,主衝刺只挑 2-3 題最可能考的,直接 mock 連發。
- ~~三指標達標退出 execution-heavy~~(2026-07-18 廢除,見 Sprint re-plan)。
- Weekly Review 連兩次同主題衰退 → 該主題進 Gauntlet 換情境重測(S40 的 Bloom 模式)。
